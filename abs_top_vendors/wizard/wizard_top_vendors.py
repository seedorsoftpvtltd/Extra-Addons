# -*- coding: utf-8 -*-
#################################################################################
#
#    Odoo, Open Source Management Solution
#    Copyright (C) 2020-today Ascetic Business Solution <www.asceticbs.com>
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
#################################################################################

from odoo import api, fields, models,_
from datetime import datetime
from odoo.exceptions import ValidationError

class TopVendors(models.TransientModel):
    _name = "top.vendors"
    _description = 'Top Vendors'

    date_from = fields.Date('From Date')
    date_to = fields.Date('To Date')

    @api.onchange('date_to')
    def onchange_date_to(self):
        for record in self:
            if record.date_to < record.date_from:
                raise ValidationError("Please select right date")
            else:
                pass

    def top_vendors(self):
        vendor_list = []
        top_vendor_list = []
        top_vendor = self.env['top.vendor']
        purchase_order_ids = self.env['purchase.order'].search([('date_order','<=',self.date_to),('date_order','>=',self.date_from),('state','in',('purchase','done'))])
        if purchase_order_ids:
            for order in purchase_order_ids:
                total_amount = 0
                if order.partner_id not in vendor_list:
                    vendor_list.append(order.partner_id)
                    for vendor in purchase_order_ids:
                        if order.partner_id == vendor.partner_id:
                            total_amount = total_amount + vendor.amount_total
                    vendor_dict = {'vendors' : order.partner_id.id, 'amount' : total_amount}
                    top_vendor_id = top_vendor.create(vendor_dict)
                    if top_vendor_id:
                       top_vendor_list.append(top_vendor_id)
        return {
            'name': _('Top Vendors'),
            'type': 'ir.actions.act_window',
            'domain': [('id','in',[x.id for x in top_vendor_list])],
            'view_mode': 'tree',
            'res_model': 'top.vendor',
            'view_id': False,
            'action' :'view_vendor_tree',
            'target' : 'current'
        }
