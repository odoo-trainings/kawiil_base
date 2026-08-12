from odoo import fields, models


class TrainingTestModel(models.Model):
    _name = "training.test.model"
    _description = "Training Test Model"

    name = fields.Char()
    test_selection = fields.Selection([("option_1", "1"), ("option_2", "2")])
