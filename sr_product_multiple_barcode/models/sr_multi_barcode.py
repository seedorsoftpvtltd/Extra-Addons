# -*- coding: utf-8 -*-
##############################################################################
#
#    This module uses OpenERP, Open Source Management Solution Framework.
#    Copyright (C) 2017-Today Sitaram
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>
#
##############################################################################

from odoo import models, fields, api

class srMultiBarcode(models.Model):
    _name = 'sr.multi.barcode'
    
    name = fields.Char('Barcode', required=True)
    product_tmpl_id = fields.Many2one('product.template','Product')
    product_id = fields.Many2one('product.product','Product Variant')

    _sql_constraints = [
        ('multi_barcode_unique', 'unique (name)', 'Barcode Must be different !')
    ]

