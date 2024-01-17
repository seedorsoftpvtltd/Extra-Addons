from odoo import models, fields, api


class DeductionDescription(models.Model):
    _name = 'deduction.description'

    _rec_name = 'name'

    name = fields.Char('Tax Deduction Description')

    active = fields.Boolean('Active', default=True)

