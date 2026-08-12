from odoo import fields, models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    cgun_test_field = fields.Integer()
