from lxml import html

from odoo.tests import HttpCase
from odoo.tools import html2plaintext


def _normalize(text):
    return ' '.join(text.split())


class TestKawiilPages(HttpCase):

    def _open_page(self, url):
        response = self.url_open(url)
        self.assertEqual(response.status_code, 200, f"{url} should be reachable")
        return response.text, html.fromstring(response.text)

    def _assert_h1(self, tree, expected):
        headings = [_normalize(h1.text_content()) for h1 in tree.xpath("//div[@id='wrap']//h1")]
        self.assertIn(expected, headings)

    def _get_lead_form(self, tree):
        forms = tree.xpath("//div[@id='wrap']//form[@data-model_name='crm.lead']")
        self.assertEqual(len(forms), 1, "The page should hold one form creating a CRM lead")
        form = forms[0]
        self.assertEqual(form.get('action'), '/website/form/')
        return form

    def _post_lead_form(self, form, values):
        """Post the values the way the form snippet does, with the lead title
        taken from the form itself."""
        lead_title = form.xpath(".//input[@name='name']/@value")[0]
        self.authenticate(None, None)
        response = self.url_open('/website/form/crm.lead', data={
            'name': lead_title,
            **values,
            'csrf_token': self.csrf_token(),
        })
        self.assertEqual(response.status_code, 200)
        lead_id = response.json().get('id')
        self.assertTrue(lead_id, response.text)
        return self.env['crm.lead'].browse(lead_id)

    def test_financing_page(self):
        page, tree = self._open_page('/financing')
        self._assert_h1(tree, 'Ride now. Pay monthly.')

        # Each monthly figure comes with its term, APR and down payment.
        plans = tree.xpath("//section[contains(@class, 's_comparisons')]//div[@data-name='Plan']")
        self.assertEqual(len(plans), 3)
        expected_plans = [
            ('36 months', '$667', '6.99%'),
            ('48 months', '$527', '7.99%'),
            ('60 months', '$448', '8.99%'),
        ]
        for plan, (term, monthly, apr) in zip(plans, expected_plans):
            plan_text = _normalize(plan.text_content())
            for expected in (term, monthly, apr, '$2,400'):
                self.assertIn(expected, plan_text)
        self.assertIn('Lowest monthly', _normalize(plans[2].text_content()))
        self.assertIn('8.99% APR, 60 months, 10% down', page)

        apply_links = tree.xpath("//div[@id='wrap']//a[@href='/financing/apply']")
        self.assertIn('Apply for financing', [_normalize(link.text_content()) for link in apply_links])

    def test_financing_apply_form(self):
        _page, tree = self._open_page('/financing/apply')
        self._assert_h1(tree, 'Apply for financing')
        form = self._get_lead_form(tree)
        self.assertEqual(
            set(form.xpath(".//*[@required]/@name")),
            {'contact_name', 'email_from', 'phone', 'Model', 'name'},
        )

        lead = self._post_lead_form(form, {
            'contact_name': 'Robin Example',
            'email_from': 'robin.example@example.com',
            'phone': '+1 415-555-0100',
            'Model': 'Ukko',
            'Battery': 'Extended',
            'Preferred term': '48 months',
            'description': 'Trading in my old bike.',
        })
        self.assertEqual(lead.name, 'Financing enquiry')
        self.assertEqual(lead.type, 'lead')
        self.assertEqual(lead.team_id, self.env.ref('sales_team.team_sales_department'))
        self.assertEqual(lead.contact_name, 'Robin Example')
        self.assertEqual(lead.email_from, 'robin.example@example.com')
        self.assertTrue(lead.phone.endswith('0100'))
        notes = html2plaintext(lead.description)
        for expected in (
            'Trading in my old bike.',
            'Model : Ukko',
            'Battery : Extended',
            'Preferred term : 48 months',
        ):
            self.assertIn(expected, notes)

    def test_test_ride_form(self):
        page, tree = self._open_page('/test-ride')
        self._assert_h1(tree, 'Book a test ride.')
        self.assertIn('Bring your motorcycle licence or endorsement.', page)
        self.assertIn('4100 Thunderbird Road', page)
        self.assertIn('info@kawiil.example.com', page)
        form = self._get_lead_form(tree)
        self.assertEqual(
            set(form.xpath(".//*[@required]/@name")),
            {'contact_name', 'email_from', 'phone', 'Model', 'Preferred date', 'name'},
        )
        self.assertEqual(
            form.xpath(".//select[@name='Model']/option/@value"),
            ['Raijin', 'Ukko', 'Indra'],
        )
        self.assertIn('Book my test ride', _normalize(form.text_content()))

        lead = self._post_lead_form(form, {
            'contact_name': 'Sam Example',
            'email_from': 'sam.example@example.com',
            'phone': '+1 415-555-0101',
            'Model': 'Indra',
            'Preferred date': '10/15/2026',
            'description': 'Saturday morning if possible.',
        })
        self.assertEqual(lead.name, 'Test ride request')
        self.assertEqual(lead.type, 'lead')
        self.assertEqual(lead.team_id, self.env.ref('sales_team.team_sales_department'))
        self.assertEqual(lead.contact_name, 'Sam Example')
        self.assertEqual(lead.email_from, 'sam.example@example.com')
        self.assertTrue(lead.phone.endswith('0101'))
        notes = html2plaintext(lead.description)
        for expected in ('Saturday morning if possible.', 'Model : Indra', 'Preferred date : 10/15/2026'):
            self.assertIn(expected, notes)

    def test_about_page(self):
        _page, tree = self._open_page('/about')
        self._assert_h1(tree, 'Lightning is the one force every culture has a god for.')
        team_names = [
            _normalize(h3.text_content())
            for h3 in tree.xpath("//section[contains(@class, 's_company_team')]//h3")
        ]
        self.assertEqual(team_names, ['Itzel', 'Tomás Herrera', 'Diego Ramírez', 'Arjun Mehta'])
        milestones = [
            _normalize(h3.text_content())
            for h3 in tree.xpath("//section[contains(@class, 's_timeline')]//h3")
        ]
        self.assertEqual(milestones, ['2018', '2020', '2022', '2023', '2024', '2025', '2026'])

    def test_no_fourth_model(self):
        for url in ('/financing', '/financing/apply', '/about', '/test-ride'):
            page, _tree = self._open_page(url)
            self.assertNotIn('xolotl', page.lower(), f"{url} must not mention the fourth model")
