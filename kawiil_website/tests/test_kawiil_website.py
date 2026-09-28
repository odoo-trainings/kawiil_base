from lxml import html

from odoo.tests import HttpCase
from odoo.tools import file_open


class TestKawiilWebsite(HttpCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.website = cls.env.ref('base.default_website')

    def test_homepage(self):
        response = self.url_open('/')
        self.assertEqual(response.status_code, 200)
        page = response.text
        self.assertIn('Silent. Sudden. Electric.', page)
        self.assertIn('Ride from $215/month', page)
        # A monthly amount is never shown without its financing terms.
        self.assertIn('8.99% APR, 60 months, 10% down', page)
        self.assertNotIn('xolotl', page.lower())
        # The same links also appear in the page body: check them in the header only.
        header = html.fromstring(page).xpath('//header')[0]
        cta = header.xpath(".//a[contains(concat(' ', normalize-space(@class), ' '), ' btn_cta ')]")
        self.assertEqual({a.get('href') for a in cta}, {'/test-ride'})
        self.assertIn('Book a test ride', cta[0].text_content())
        for url in ('/raijin', '/ukko', '/indra', '/financing', '/shop', '/about'):
            self.assertTrue(header.xpath(f".//a[@href='{url}']"), url)

    def test_crm_settings(self):
        self.assertIn(self.env.ref('crm.group_use_lead'), self.env.ref('base.group_user').all_implied_ids)
        team = self.env.ref('sales_team.team_sales_department')
        self.assertTrue(team.use_leads)
        self.assertEqual(self.website.crm_default_team_id, team)

    def test_product_publishing(self):
        for key in ('raijin', 'ukko', 'indra', 'home_charger', 'helmet', 'extended_warranty'):
            self.assertTrue(self.env.ref(f'kawiil_base.product_template_{key}').is_published, key)
        self.assertFalse(self.env.ref('kawiil_base.product_template_xolotl').is_published)
        shop = self.url_open('/shop')
        self.assertEqual(shop.status_code, 200)
        self.assertIn('Raijin', shop.text)
        self.assertNotIn('xolotl', shop.text.lower())

    def test_logo_and_favicon(self):
        with file_open('kawiil_website/static/img/logo/kawiil_logo_on_dark.svg', 'rb') as logo_file:
            self.assertEqual(bytes(self.website.logo), logo_file.read())
        self.assertTrue(self.website.favicon)
        self.assertNotEqual(self.website.favicon.checksum, self.website._default_favicon().checksum)

    def test_menu(self):
        menus = self.env['website.menu'].search([('parent_id', '=', self.website.menu_id.id)])
        expected_names = ['Models', 'Financing', 'Shop', 'About']
        self.assertEqual(
            [name for name in menus.mapped('name') if name in expected_names],
            expected_names,
        )
        self.assertEqual(len(menus.filtered(lambda menu: menu.url == '/shop')), 1)

        models_menu = menus.filtered(lambda menu: menu.name == 'Models')
        self.assertEqual(
            [(menu.name, menu.url) for menu in models_menu.child_id],
            [('Raijin', '/raijin'), ('Ukko', '/ukko'), ('Indra', '/indra')],
        )

        # Home and Contact us are gone from the menu, their pages are not.
        self.assertFalse(menus.filtered(lambda menu: menu.url in ('/', '/contactus')))
        self.assertTrue(self.env['website.page'].search_count([
            ('url', '=', '/'),
            ('website_id', 'in', [False, self.website.id]),
        ]))
        self.assertEqual(self.url_open('/contactus').status_code, 200)
