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
from odoo import api, fields, models, _
from odoo.exceptions import ValidationError

## Inherit class sale.order.line for validate amount of product
class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    @api.model
    def create(self,vals):
        result = super(SaleOrderLine,self).create(vals) 
   
        if vals.get('product_id'):
            product = self.env['product.product'].search([('id','=',vals['product_id'])])
            total_amount = vals['product_uom_qty'] * vals['price_unit']
            if total_amount < product.minimum_amount:
                raise ValidationError(_( "Minimum order amount of the product %s is %s.") % (vals['name'],product.minimum_amount))
        return result

