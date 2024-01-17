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

from odoo import models, fields, api, _
from odoo.exceptions import UserError
from datetime import datetime
import sys
import tempfile
import binascii
import xlrd
import base64
import io
import csv


class srImportMultipleBarcode(models.TransientModel):
    _name = 'sr.import.multiple.barcode'
    _description = 'Import Multiple Barcode'

    file = fields.Binary('File')
    import_product_by = fields.Selection([('name', 'Name'), ('code', 'Default Code')], string='Import Product By', default='name')
    import_barcode_for = fields.Selection([('product', 'Products'), ('template', 'Product Template')], string='Import Barcode For', default='product')

    def _import_barcode(self, line):
        domain = []
        if self.import_product_by == 'name':
            if self.import_barcode_for == 'product':
                product_id = self.env['product.product'].search([('name', '=', line[0])])
                if product_id:
                    for barcode in line[1].split(','):
                        self.env['sr.multi.barcode'].create({
                            'name':barcode,
                            'product_id':product_id.id
                            })
                else:
                    raise UserError(_('%s Product Not Found in the system.' %line[0]))
            else:
                product_tmpl_id = self.env['product.template'].search([('name', '=', line[0])])
                if product_tmpl_id:
                    for barcode in line[1].split(','):
                        self.env['sr.multi.barcode'].create({
                            'name':barcode,
                            'product_tmpl_id':product_tmpl_id.id
                            })
                else:
                    raise UserError(_('%s Template Not Found in the system.' %line[0]))
        else:
            if self.import_barcode_for == 'product':
                product_id = self.env['product.product'].search([('default_code', '=', line[0])])
                if product_id:
                    for barcode in line[1].split(','):
                        self.env['sr.multi.barcode'].create({
                            'name':barcode,
                            'product_id':product_id.id
                            })
                else:
                    raise UserError(_('%s Default Code Not Found in the system.' %line[0]))
            else:
                product_tmpl_id = self.env['product.template'].search([('default_code', '=', line[0])])
                if product_tmpl_id:
                    for barcode in line[1].split(','):
                        self.env['sr.multi.barcode'].create({
                            'name':barcode,
                            'product_tmpl_id':product_tmpl_id.id
                            })
                else:
                    raise UserError(_('%s Default Code Not Found in the system.' %line[0]))
        
    def import_multiple_barcode(self):
        try:
            fp = tempfile.NamedTemporaryFile(suffix=".xlsx")
            fp.write(binascii.a2b_base64(self.file))
            fp.seek(0)
            values = {}
            workbook = xlrd.open_workbook(fp.name)
            sheet = workbook.sheet_by_index(0)
            for row_no in range(sheet.nrows):
                val = {}
                if row_no >= 1:
                    line = list(map(lambda row:isinstance(row.value, bytes) and row.value.encode('utf-8') or str(row.value), sheet.row(row_no)))
                    self._import_barcode(line)
        except Exception as e:
            raise UserError(_(e))
