# -*- coding: utf-8 -*-

# Part of Probuse Consulting Service Pvt Ltd.
# See LICENSE file for full copyright and licensing details.

from odoo import models, fields, api, _

class AccountMove(models.Model):
    _inherit = 'account.move'

    def _get_default_stage_id(self):
        """ Gives minimum sequence stage """
        stages = ''
        if self._context.get('default_type') == 'out_invoice':
            out_invoice = True
            stages =  self.env['custom.account.stage'].search(
            [('is_customer_invoice','=',out_invoice)],order="sequence, id desc", limit=1).id
            return stages
        elif self._context.get('default_type') == 'in_invoice':
            in_invoice = True
            return stages
            stages =  self.env['custom.account.stage'].search(
            [('is_vendor_bill','=',in_invoice)],order="sequence, id desc", limit=1).id
        elif self._context.get('default_type') == 'in_refund':
            in_refund = True
            return stages
            stages =  self.env['custom.account.stage'].search(
            [('is_vendor_credit_note','=',in_refund)],order="sequence, id desc", limit=1).id
        elif self._context.get('default_type') == 'out_refund':
            out_refund = True
            return stages
            stages =  self.env['custom.account.stage'].search(
            [('is_customer_credit_note','=',out_refund)],order="sequence, id desc", limit=1).id
            return stages
        elif self._context.get('default_type') == 'entry':
            entry = True
            stages =  self.env['custom.account.stage'].search(
            [('is_journal_entry','=',entry),],order="sequence, id desc", limit=1).id
            return stages
        elif self._context.get('default_type') == 'out_receipt':
            out_receipt = True
            stages =  self.env['custom.account.stage'].search(
            [('is_sales_receipt','=',out_receipt)],order="sequence, id desc", limit=1).id
            return stages
        elif self._context.get('default_type') == 'in_receipt':
            in_receipt = True
            stages =  self.env['custom.account.stage'].search(
            [('is_purchase_receipt','=',in_receipt)],order="sequence, id desc", limit=1).id
            return stages

    
    def _prepare_domain(self):
        stage_domain_dict = {
            'out_invoice': [('is_customer_invoice', '=', True)],
            'in_invoice': [('is_vendor_bill', '=', True)],
            'in_refund': [('is_vendor_credit_note','=',True)],
            'out_refund': [('is_customer_credit_note','=',True)],
            'entry': [('is_journal_entry','=',True)],
            'out_receipt': [('is_sales_receipt','=',True)],
            'in_receipt': [('is_purchase_receipt','=',True)],
        }
       
        type = self.type or self._context.get('default_type')
        stage_domain = stage_domain_dict.get(type) if type and type in stage_domain_dict.keys() else []
        return stage_domain     

    custom_stage_id = fields.Many2one(
        'custom.account.stage',
        string="Stage",
        ondelete='restrict',
        tracking=True, 
        index=True,
        default=_get_default_stage_id,
        domain=lambda self:self._prepare_domain(),
        copy=False
    )
 
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: