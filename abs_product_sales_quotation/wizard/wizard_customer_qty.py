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

class create_quotation_customer(models.TransientModel):
    _name = "product.customer.quantity"
    _description = 'Create Quotation Customer'

    partner_id = fields.Many2one('res.partner',string = "Customer")
    product_qty = fields.Float(string='Quantity',require = True)
    order_id = fields.Many2one('sale.order', string='Order Reference')

    def create_quotation(self):
        quotation_obj = self.env['sale.order']
        order_line_obj = self.env['sale.order.line']

        # create a new quotation using wizard in quotation 
        if self.env.context.get('active_model') == 'product.template':
            active_id = self.env.context.get('active_id',False)

            product_tmpl_id = self.env['product.product'].search([('product_tmpl_id','=',active_id)])

            quotation_dict = {'partner_id':self.partner_id.id,
                             }
            sale_order = quotation_obj.create(quotation_dict)

            # create a dictionary for product_id,product_name and product_qty
            order_dict = {'product_id' : product_tmpl_id.id,
                          'name':product_tmpl_id.name,
                          'product_uom_qty':self.product_qty,
                          'price_unit':product_tmpl_id.list_price,
                          'product_uom':product_tmpl_id.uom_id.id,
                          'order_id':sale_order.id
                         }

            order_line_obj.create(order_dict)

