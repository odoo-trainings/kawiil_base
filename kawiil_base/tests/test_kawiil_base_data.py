import re

from odoo import fields
from odoo.tests import TransactionCase
from odoo.tools import file_open

BIKES = {
    # template xml id: (model code, price extra of the extended battery)
    'product_template_raijin': ('RAI', 4500.0),
    'product_template_ukko': ('UKK', 4000.0),
    'product_template_indra': ('IND', 2000.0),
}
BOUGHT_IN_GOODS = [
    'home_charger', 'portable_charger', 'charging_cable', 'helmet', 'jacket',
    'gloves', 'boots', 'tyre_set', 'brake_pads', 'key_fob',
]


class TestKawiilBaseData(TransactionCase):

    def _module_records(self, model):
        data = self.env['ir.model.data'].search([('module', '=', 'kawiil_base'), ('model', '=', model)])
        return self.env[model].browse(data.mapped('res_id'))

    def test_company(self):
        company = self.env.ref('base.main_company')
        self.assertEqual(company.name, "K'awiil Motors")
        self.assertEqual(company.country_id, self.env.ref('base.us'))
        self.assertEqual(company.currency_id, self.env.ref('base.USD'))
        self.assertEqual(company.city, "San Francisco")
        self.assertTrue(company.logo)

    def test_settings(self):
        self.assertIn(self.env.ref('product.group_product_variant'), self.env.ref('base.group_user').all_implied_ids)

    def test_admin_renamed(self):
        admin = self.env.ref('base.user_admin')
        self.assertEqual(admin.name, "Itzel Admin")
        self.assertEqual(admin.partner_id.function, "CEO")
        self.assertTrue(admin.email.endswith('@kawiil.example.com'))

    def test_users_and_groups(self):
        manager = self.env.ref('kawiil_base.user_sales_manager')
        rep = self.env.ref('kawiil_base.user_sales_rep')
        finance = self.env.ref('kawiil_base.user_finance')
        self.assertEqual(manager.login, 'sales.manager')
        self.assertEqual(rep.login, 'sales.rep')
        self.assertEqual(finance.login, 'finance')

        self.assertTrue(manager.has_group('sales_team.group_sale_manager'))
        self.assertTrue(rep.has_group('sales_team.group_sale_salesman'))
        self.assertFalse(rep.has_group('sales_team.group_sale_salesman_all_leads'))
        self.assertTrue(finance.has_group('account.group_account_manager'))
        self.assertFalse(finance.has_group('sales_team.group_sale_salesman'))

    def test_employee_hierarchy(self):
        employees = self._module_records('hr.employee')
        ceo = self.env.ref('kawiil_base.hr_employee_itzel')
        self.assertGreaterEqual(len(employees), 12)
        self.assertEqual(ceo.user_id, self.env.ref('base.user_admin'))
        self.assertFalse(ceo.parent_id)
        for employee in employees - ceo:
            self.assertTrue(employee.parent_id, f"{employee.name} has no manager")
            # every chain of managers ends at the CEO
            top = employee
            while top.parent_id:
                top = top.parent_id
            self.assertEqual(top, ceo)

        users = (
            self.env.ref('base.user_admin')
            | self.env.ref('kawiil_base.user_sales_manager')
            | self.env.ref('kawiil_base.user_sales_rep')
            | self.env.ref('kawiil_base.user_finance')
        )
        self.assertEqual(employees.user_id, users)

        departments = self._module_records('hr.department')
        self.assertEqual(len(departments), 5)
        self.assertTrue(all(departments.mapped('manager_id')))

    def test_employee_photos(self):
        for key in ('itzel', 'tomas', 'diego', 'arjun'):
            employee = self.env.ref(f'kawiil_base.hr_employee_{key}')
            with file_open(f'kawiil_base/static/img/employees/{key}.jpg', 'rb') as photo:
                self.assertEqual(bytes(employee.image_1920), photo.read(), employee.name)
            # the photo is the avatar too, also for employees linked to a user
            self.assertEqual(employee.avatar_1920, employee.image_1920, employee.name)

    def test_bike_variants(self):
        code_pattern = re.compile(r'^KWL-(RAI|UKK|IND)-\d{1,2}-[A-Z]{3}$')
        for xmlid, (code, extra) in BIKES.items():
            template = self.env.ref(f'kawiil_base.{xmlid}')
            variants = template.product_variant_ids
            self.assertEqual(len(variants), 6, template.name)
            self.assertEqual(len(set(variants.mapped('default_code'))), 6)
            for variant in variants:
                self.assertRegex(variant.default_code, code_pattern)
                self.assertTrue(variant.default_code.startswith(f'KWL-{code}-'))
                battery = variant.product_template_attribute_value_ids.filtered(
                    lambda ptav: ptav.attribute_id == self.env.ref('kawiil_base.product_attribute_battery')
                )
                expected_extra = extra if battery.name.startswith('Extended') else 0.0
                self.assertEqual(variant.price_extra, expected_extra, variant.display_name)
                self.assertEqual(variant.lst_price, template.list_price + expected_extra)

        self.assertEqual(self.env.ref('kawiil_base.product_raijin_20_nst').default_code, 'KWL-RAI-20-NST')

    def test_bike_images(self):
        colours = self.env['product.attribute.value'].browse([
            self.env.ref('kawiil_base.product_attribute_value_color_jade_arc').id,
            self.env.ref('kawiil_base.product_attribute_value_color_night_strike').id,
            self.env.ref('kawiil_base.product_attribute_value_color_storm_white').id,
        ])
        self.assertEqual(colours.mapped('html_color'), ['#0B7A64', '#0A0F1F', '#E8ECEA'])
        jade_arc = colours[0]
        for xmlid in BIKES:
            template = self.env.ref(f'kawiil_base.{xmlid}')
            self.assertTrue(template.image_1920, template.name)
            for variant in template.product_variant_ids:
                colour = variant.product_template_attribute_value_ids.product_attribute_value_id & colours
                if colour == jade_arc:
                    # the default colour shows the template image
                    self.assertFalse(variant.image_variant_1920, variant.display_name)
                    self.assertEqual(variant.image_1920, template.image_1920)
                else:
                    self.assertTrue(variant.image_variant_1920, variant.display_name)
                    self.assertNotEqual(variant.image_1920, template.image_1920)

    def test_xolotl(self):
        xolotl = self.env.ref('kawiil_base.product_template_xolotl')
        self.assertFalse(xolotl.sale_ok)
        self.assertEqual(xolotl.product_variant_count, 1)

    def test_vendors(self):
        for key in BOUGHT_IN_GOODS:
            template = self.env.ref(f'kawiil_base.product_template_{key}')
            self.assertTrue(template.seller_ids, template.name)
            self.assertTrue(template.is_storable)
        for xmlid in BIKES:
            self.assertFalse(self.env.ref(f'kawiil_base.{xmlid}').seller_ids)
        for key in ('extended_warranty', 'annual_service'):
            service = self.env.ref(f'kawiil_base.product_template_{key}')
            self.assertEqual(service.type, 'service')
            self.assertFalse(service.is_storable)

    def test_sale_orders(self):
        orders = self._module_records('sale.order')
        self.assertEqual(len(orders), 30)
        counts = {state: len(orders.filtered(lambda o, s=state: o.state == s)) for state in ('draft', 'sent', 'sale', 'cancel')}
        self.assertEqual(counts, {'draft': 5, 'sent': 3, 'sale': 20, 'cancel': 2})

        # Confirmed orders are dated on the install day: action_confirm sets date_order.
        # The quotations keep their dates in the past.
        today = fields.Date.today()
        for order in orders.filtered(lambda o: o.state != 'sale'):
            self.assertLess(order.date_order.date(), today, order.name)

        manager = self.env.ref('kawiil_base.user_sales_manager')
        rep = self.env.ref('kawiil_base.user_sales_rep')
        self.assertEqual(orders.user_id, manager | rep)
        self.assertGreaterEqual(len(orders.filtered(lambda o: o.user_id == manager)), 10)
        self.assertGreaterEqual(len(orders.filtered(lambda o: o.user_id == rep)), 10)
