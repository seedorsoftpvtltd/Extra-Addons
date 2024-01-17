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
#################################################################################s

from odoo import api,fields,models,_
from datetime import datetime
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT

class PurchaseOrder(models.Model):
    _inherit="purchase.order"

    purchase_order_line_template = fields.Boolean(string='Purchase Order Line Template',help="This fielda allows to add order line template in purchase order")
    
    '''This function set Scheduled Date of Purchase Order. if purchase_order_line_template is true then set default current date'''
    @api.model
    @api.onchange('purchase_order_line_template')
    def set_date_planned(self):
        for record in self:
            if record.purchase_order_line_template == True:
                record.date_planned = datetime.today().strftime(DEFAULT_SERVER_DATETIME_FORMAT)
            else:
                record.date_planned = ""
	
	   
    '''if checkbox "Use Purchase Order Line Template" is True then according vendor find order_line records from purchase.order.line.templates and display in purchase.order form '''
    @api.model
    def create(self,vals):
        result = super(PurchaseOrder,self).create(vals)
        if vals['purchase_order_line_template'] == True:
            if self.env['purchase.order.line.templates'].search([('partner_id','=',vals['partner_id'])]):
                template_ids = self.env['purchase.order.line.templates'].search([('partner_id','=',vals['partner_id'])])
                for temp_record in template_ids:
                    p_id = temp_record.product_id.id
                    p_desc = temp_record.product_description
                    p_qty = temp_record.product_qty
                    p_date_planned = temp_record.date_planned
                    p_price_qty = temp_record.price_unit
                    p_product_uom = temp_record.product_uoms.id
                    p_tax_id = temp_record.tax_ids
                    p_tax_id_list = [] 
                    for record_tax_id in p_tax_id:
                        p_tax_id_list.append(record_tax_id.id)
                    orderlineTemplate = {"product_id":p_id,
                                        "name":p_desc,
                                        "product_qty":p_qty,
                                        "date_planned":p_date_planned,
                                        "price_unit":p_price_qty,
                                        "product_uom":p_product_uom,
                                        "taxes_id":[(6,0,p_tax_id_list)],
                                        "order_id":result.id,
                                        }
                    self.env['purchase.order.line'].create(orderlineTemplate)
        return result

