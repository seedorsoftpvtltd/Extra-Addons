# -*- coding: utf-8 -*-

# Part of Probuse Consulting Service Pvt Ltd.
# See LICENSE file for full copyright and licensing details.

from odoo import models, fields, api

class CustomAccountStage(models.Model):
    _name = 'custom.account.stage'
    _description = 'Account Stages'

    name = fields.Char(
        string='Name',
        required=True,
    )
    sequence = fields.Integer(
    	string='Sequence',
    )
    is_journal_entry = fields.Boolean(
    	string='Show To Journal Entry?'
    )
    is_customer_invoice = fields.Boolean(
    	string='Show To Customer Invoice?'
    )
    is_customer_credit_note = fields.Boolean(
    	string='Show To Credit Note?'
    )
    is_vendor_bill = fields.Boolean(
    	string='Show To Vendor Bill?'
    )
    is_vendor_credit_note = fields.Boolean(
    	string='Show To Debit Note?'
    )
    is_sales_receipt = fields.Boolean(
    	string='Show To Sales Receipt?'
    )
    is_purchase_receipt = fields.Boolean(
    	string='Show To Purchase Receipt?'
    )

            
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: