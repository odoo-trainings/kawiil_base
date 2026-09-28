from urllib.parse import urlparse

from lxml import html

from odoo.tests import HttpCase


class TestBikePages(HttpCase):

    def _open_page(self, url):
        response = self.url_open(url)
        self.assertEqual(response.status_code, 200)
        return response, html.fromstring(response.content)

    def _text(self, node):
        return ' '.join(node.text_content().split())

    def _section(self, root, snippet):
        sections = root.xpath(f"//div[@id='wrap']//section[@data-snippet='{snippet}']")
        self.assertEqual(len(sections), 1, f"expected one {snippet} section")
        return sections[0]

    def _assert_bike_page(self, url, name, tagline, monthly, disclosure, product_xmlid):
        response, root = self._open_page(url)
        self.assertNotIn('xolotl', response.text.lower())

        # Hero: model name and "from" price
        self.assertEqual([self._text(h1) for h1 in root.xpath("//div[@id='wrap']//h1")], [name])
        self.assertIn(tagline, self._text(self._section(root, 's_cover')))

        # The monthly amount is shown with its financing terms
        finance_text = self._text(self._section(root, 's_cta_box'))
        self.assertIn(f"Finance this bike from {monthly}", finance_text)
        self.assertIn(disclosure, finance_text)
        self.assertIn('8.99% APR', finance_text)

        colours_text = self._text(self._section(root, 's_three_columns'))
        for colour in ('Jade Arc', 'Night Strike', 'Storm White'):
            self.assertIn(colour, colours_text)

        # Every "Buy" button leads to the bike's product page
        product = self.env.ref(product_xmlid)
        for label in (f"Buy {name}", 'Buy Standard', 'Buy Extended'):
            hrefs = root.xpath(f"//div[@id='wrap']//a[normalize-space()='{label}']/@href")
            self.assertEqual(hrefs, [product.website_url], f"wrong link on '{label}'")
            self.assertEqual(self.env['ir.http']._unslug(urlparse(hrefs[0]).path.rsplit('/', 1)[-1])[1], product.id)

        product_response, product_root = self._open_page(product.website_url)
        # No redirect: the link is the product's canonical URL
        self.assertEqual(urlparse(product_response.url).path, product.website_url)
        self.assertIn(product.name, self._text(product_root))

    def test_raijin_page(self):
        self._assert_bike_page(
            '/raijin', 'Raijin',
            'Thunder, without the noise. From $24,000.',
            '$448/month',
            'Raijin Standard, $24,000. 8.99% APR, 60 months, 10% down. Example only, subject to credit approval.',
            'kawiil_base.product_template_raijin',
        )

    def test_ukko_page(self):
        self._assert_bike_page(
            '/ukko', 'Ukko',
            'Sky and thunder, on any road. From $21,000.',
            '$392/month',
            'Ukko Standard, $21,000. 8.99% APR, 60 months, 10% down. Example only, subject to credit approval.',
            'kawiil_base.product_template_ukko',
        )

    def test_indra_page(self):
        self._assert_bike_page(
            '/indra', 'Indra',
            'Lightning for the city. From $11,500.',
            '$215/month',
            'Indra Standard, $11,500. 8.99% APR, 60 months, 10% down. Example only, subject to credit approval.',
            'kawiil_base.product_template_indra',
        )

    def test_bike_pages_published(self):
        pages = self.env['website.page'].search([('url', 'in', ['/raijin', '/ukko', '/indra'])])
        self.assertEqual(sorted(pages.mapped('url')), ['/indra', '/raijin', '/ukko'])
        self.assertTrue(all(pages.mapped('is_published')))
        self.assertTrue(all(pages.mapped('website_indexed')))
