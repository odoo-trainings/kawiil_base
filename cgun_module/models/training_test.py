from odoo import fields, models


class TrainingTest(models.Model):
    _name = "training.test"
    _description = "Training Test"

    name = fields.Char()
    test_selection = fields.Selection([("option_1", "1"), ("option_2", "2")])
    product_id = fields.Many2one("product.template")
    product_price = fields.Float(related="product_id.cgun_price")
