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
from odoo.exceptions import ValidationError
from datetime import date

#extend the class to add functionality of duplicate quotation.
class SaleOrder(models.Model):
    _inherit = "sale.order"

    duplicate_quotation = fields.Boolean(string='Duplicate quotation')
    duplicate_quotation_ids = fields.One2many('duplicate.quotation','order_id',string='Duplicate Date') 

    #create function for added duplicate date and Whenever those dates same come,quotations should be duplicated
    def duplicate(self):
        today = date.today()  
        current_date = str(today)
        sale_order_object = self.env['sale.order']
        order_line_object = self.env['sale.order.line']
        order_ids = self.env['sale.order'].search([]) 
        if order_ids:
            for order_id in order_ids:
                if order_id.duplicate_quotation_ids:
                    for duplicate_quotation_id in order_id.duplicate_quotation_ids:
                        if duplicate_quotation_id and duplicate_quotation_id.duplicate_date:
                            duplicate_date= str(duplicate_quotation_id.duplicate_date)
                            if order_id.duplicate_quotation == True and duplicate_date == current_date:
                                 order_dict = {'partner_id':order_id.partner_id.id,
                                               'payment_term_id':order_id.payment_term_id.id,
                                               'user_id':order_id.user_id.id}
                                 order = sale_order_object.create(order_dict)
                                 for line in order_id.order_line:
                                     if line.product_id:
                                         order_line_dict = {'order_id':order.id,'product_id':line.product_id.id}
                                         order_line_object.create(order_line_dict)   

class DuplicateQuotation(models.Model):
    _name = "duplicate.quotation"
    _description = "Duplicate Quotation"

    order_id = fields.Many2one('sale.order')
    duplicate_date = fields.Date('Duplicate Date') 

    #create constraints for duplictae_date. 
    @api.constrains('duplicate_date')
    def check_duplicate_date(self):
        today = date.today()  
        today_date = str(today)
        for rec in self:
            duplicate_date = str(rec.duplicate_date)   
            if rec and duplicate_date < today_date:
                raise ValidationError("Invalid Date")
