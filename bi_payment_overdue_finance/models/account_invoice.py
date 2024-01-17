# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.
##############################################################################
from odoo import api, fields, models, _

class account_invoice_finance(models.Model):
    
    _inherit = 'account.move'

    def _get_result_over(self):

        for aml in self:

            aml.update({
                'result_over' : aml.amount_total - (aml.amount_total - aml.amount_residual),
                'credit_amount_over' : (aml.amount_total - aml.amount_residual)
            })



    credit_amount_over = fields.Float(compute ='_get_result_over',   string="Credit/paid")
    result_over = fields.Float(compute ='_get_result_over',   string="Balance") #'balance' field is not the same
    # invoice_currency = fields.Many2one('res.currency', compute='_invoice_currency')
    #
    # @api.depends('partner_id')
    # def _invoice_currency(self):
    #     for rec in self:
    #         rec['invoice_currency'] =rec.currency_id
    #         print(rec.invoice_currency)
    #         print(rec.invoice_currency.name)



