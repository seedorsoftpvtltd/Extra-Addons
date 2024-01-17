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
from odoo.osv import expression


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    product_barcode_ids = fields.One2many('sr.multi.barcode', 'product_tmpl_id', 'Multi Barcode')


class ProductProduct(models.Model):
    _inherit = 'product.product'

    product_barcode_ids = fields.One2many('sr.multi.barcode', 'product_id', 'Multi Barcode')


    @api.model
    def _name_search(self, name, args=None, operator='ilike', limit=100, name_get_uid=None):
        args = args or []
        product_id = self._search(expression.AND(
            [
                ['|', '|', ('name', operator, name), ('default_code', operator, name),
                  '|', ('product_barcode_ids', operator, name), ('barcode', operator, name)
                ],args
            ]), limit=limit)
        return self.browse(product_id).name_get()
        
        