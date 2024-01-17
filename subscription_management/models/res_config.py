# -*- coding: utf-8 -*-
##########################################################################
# Author      : Webkul Software Pvt. Ltd. (<https://webkul.com/>)
# Copyright(c): 2017-Present Webkul Software Pvt. Ltd.
# All Rights Reserved.
#
#
#
# This program is copyright property of the author mentioned above.
# You can`t redistribute it and/or modify it.
#
#
# You should have received a copy of the License along with this program.
# If not, see <https://store.webkul.com/license.html/>
##########################################################################

from odoo import api, fields, models, _
from odoo.exceptions import Warning

class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    journal_id = fields.Many2one('account.journal', string='Payment Method',
        required=True, domain=[('type', '=', 'sale')])
    
    invoice_generated =  fields.Selection([('draft','Draft'),('open','Open'),('paid','Paid')],help="Generate Invoice in particular State automatically",default='draft')

    invoice_email = fields.Boolean(help='Send subscription based invoice to the Customer by Email.')

    trial_period_setting=fields.Selection([('one_time','Give Trial to one time'),('product_based','Give Trial based on product')],help='Apply the Trial period policy.',default='one_time')


    @api.onchange('invoice_generated')
    def _onchange_invoice_generated(self):
        if self.invoice_generated == 'draft':
            self.invoice_email = False
    
   # @api.multi
    def get_values(self):
        res = super(ResConfigSettings, self).get_values()
        IrDefault = self.env['ir.default'].sudo()
        res.update({
            'journal_id':IrDefault.get('res.config.settings','journal_id'),
            'invoice_generated':IrDefault.get('res.config.settings','invoice_generated'),
            'invoice_email':IrDefault.get('res.config.settings','invoice_email'),
            'trial_period_setting':IrDefault.get('res.config.settings','trial_period_setting'),
            
        })
        return res

    #@api.multi
    def set_values(self):
        super(ResConfigSettings, self).set_values()
        IrDefault = self.env['ir.default'].sudo()
        IrDefault.set('res.config.settings','journal_id', self.journal_id.id )
        IrDefault.set('res.config.settings','invoice_generated', self.invoice_generated)
        IrDefault.set('res.config.settings','invoice_email', self.invoice_email)
        IrDefault.set('res.config.settings','trial_period_setting', self.trial_period_setting)
        
        return True

    # @api.one
    # def set_default_values(self):
    # 	self.env['ir.values'].set_default(
    # 		'sale.config.settings', 'journal_id', self.journal_id.id)
    # 	self.env['ir.values'].set_default(
    # 		'sale.config.settings', 'is_paid_invoice', self.is_paid_invoice)
    # 	return True

    # @api.model
    # def get_default_values(self, fields=None):
    # 	journal_id  = self.env['ir.values'].get_default('sale.config.settings', 'journal_id')
    # 	is_paid_invoice  = self.env['ir.values'].get_default('sale.config.settings', 'is_paid_invoice')
    # 	return {
    # 		'journal_id': journal_id,
    # 		'is_paid_invoice' : is_paid_invoice,
    # 		}
