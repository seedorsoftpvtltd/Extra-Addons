# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from datetime import datetime

class SaleOrder(models.Model):
    
    _inherit = 'sale.order'

    partner_credit = fields.Monetary(string="Credit", related='partner_id.commercial_partner_id.credit')
    partner_debit = fields.Monetary(string="Debit", related='partner_id.commercial_partner_id.debit')
    
    company_currency_id = fields.Many2one('res.currency',related="company_id.currency_id")
    partner_balance = fields.Monetary(string="In Company Currency",currency_field='company_currency_id',compute='_get_partner_balance')
    
    balance_in_partner_currency = fields.Monetary(
        "In Customer Currency",currency_field='currency_id',compute='_get_balance_in_partner_currency'
    )
    

    def _get_balance_in_partner_currency(self):
        for record in self:
            if record.pricelist_id:
                company = record.company_id or self.env.user.company_id
                rate = company.currency_id._get_conversion_rate(company.currency_id,record.pricelist_id.currency_id,company,datetime.now().date())
                record.balance_in_partner_currency = rate * record.partner_balance

    def _get_partner_balance(self):
        for record in self:
            record.partner_balance = record.partner_debit - record.partner_credit
            
    @api.onchange('pricelist_id')
    def onchange_pricelist_id(self):
        self._get_partner_balance()
        self._get_balance_in_partner_currency()
    
    @api.onchange('partner_id')
    def onchange_partner_id(self):
        super(SaleOrder,self).onchange_partner_id()
        self._get_partner_balance()
        self._get_balance_in_partner_currency()