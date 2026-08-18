from odoo import api, fields, models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    tool_name = fields.Char()
    cgun_test_field = fields.Integer()

    cgun_price = fields.Float()
    cgun_tax = fields.Float()
    cgun_total_price = fields.Float(compute="_compute_cgun_total_price")
    cgun_related = fields.Char(related="categ_id.property_account_expense_categ_id.name")

    @api.depends("cgun_price", "cgun_tax")
    def _compute_cgun_total_price(self):
        for product in self:
            product.cgun_total_price = product.cgun_price + product.cgun_tax
