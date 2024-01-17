
# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import models, fields, api
from datetime import datetime, timedelta
from datetime import *
from dateutil.relativedelta import *
import time
from odoo.exceptions import UserError

class PurchasePrice(models.Model):
    _inherit = 'purchase.order'

    def click_vendor_bills(self):
        if len(self.order_line) > 0:
            data = self.env['account.move']
            order_line = [(0, 0, {
                'name': vamk.name,
                'product_id': vamk.product_id.id,
                'quantity': vamk.product_qty,
                'product_uom_id': vamk.product_uom.id,
                'price_unit': vamk.price_unit,
                'tax_ids':[(6, 0, [tx.id for tx in vamk.taxes_id])],
                'purchase_line_id':vamk.id,
                #'product_uom': vamk.product_id.uom_id.id,
            }) for vamk in self.order_line]
            res = {
                   'partner_id': self.partner_id.id,                    
                   'type': 'in_invoice',
                   'invoice_origin':self.name,
                   #'purchase_id': self.id,                           
                   'invoice_line_ids': order_line,                
                  }
            fin = data.create(res)
            fin = self.action_view_invoice()
            return fin

    def click_vendor_bill(self):
        # for order in self:
        data = self.env['account.move']
        # res = data.create({
        # 'partner_id': self.partner_id.id,
        # 'order_line':  [(0, 0, {
        # 'name': self.product_list.name,
        # 'product_id': self.product_list.product.id,
        # 'product_uom_quantity': 1.0,
        # 'price_unit': 0.0,
        # })],
        # })
        if len(self.order_line) > 0:
            order_line = [(0, 0, {
                'name': vamk.name,
                'product_id': vamk.product_id.id,
                'product_uom_quantity': 1.0,
                'price_unit': 6.0,
                'product_uom': vamk.product_id.uom_id.id,
            }) for vamk in self.order_line]
            res = {
                'name': 'Vendor Bill Form',
                'view_type': 'form',
                'view_mode': 'form',
                'res_model': 'account.move',
                'target': 'current',
                'flags': {'form': {'action_buttons': True, 'options': {'mode': 'edit'}}},
                'type': 'ir.actions.act_window',
                'views': [(self.env.ref('account.view_move_form').id, 'form')],
                'view_id': self.env.ref('account.view_move_form').id,
                # 'res_id':self.id,
                'context': {'default_partner_id': self.partner_id.id,
                            #'default_equipment_type': self.assembly_unit_id.id if self.assembly_unit_id else "",                            
                            'default_type': 'in_invoice',
                            'default_purchase_id': self.id,
                            'default_order_line': order_line},
                # 'domain':[('form_id','=', self.id)],
            }
            return res
        else:
            raise UserError(_('There is no Product line to move.'))
