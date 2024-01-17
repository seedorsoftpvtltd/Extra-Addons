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

from odoo import api,fields,models,_

class SaleAdvancePaymentInv(models.TransientModel):
    _inherit ='sale.advance.payment.inv' 
   
    ##inherit class for create a invoice of advance payment system and display tags into many2many field of account.invoice
    @api.model
    def _create_invoice(self,order, so_line, amount): 
        result=super(SaleAdvancePaymentInv,self)._create_invoice(order, so_line, amount)
        if self.env.context.get('active_model') == 'sale.order': 
            active_model_id = self.env.context.get('active_id')
            sale_obj = self.env['sale.order'].search([('id','=',active_model_id)])
            tag_list=[]
       	    tag_ids=self.env['sale.order'].browse(sale_obj.id).tag_ids
            for record in tag_ids: 
                tags = self.env['crm.lead.tag'].search([('name','=',record.name)])
                tag_list.append(tags.id)
                result['invoice_tag_ids'] = [(6, 0,tag_list)]
        return result
