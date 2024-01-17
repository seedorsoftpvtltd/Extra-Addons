from odoo import models, fields, api


class IncomeDeduction(models.Model):
    _name = 'income.deduction'

    deduction_id = fields.Many2one('deduction.description', string='Deduction Description')
    amount = fields.Float('Amount')
    contract_id = fields.Many2one('hr.contract', string='Contract')


class ExtraCharges(models.Model):
    _name = 'extra.charges'

    extra_charges_description = fields.Char(string='Extra Charges')
    amount = fields.Float(string='Amount')

    contract_id = fields.Many2one('hr.contract', string='Contract')
