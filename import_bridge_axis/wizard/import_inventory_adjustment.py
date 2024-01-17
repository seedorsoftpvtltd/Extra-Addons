# -*- coding: utf-8 -*-
#################################################################################
# Author      : AxisTechnolabs.com
# Copyright(c): 2011-Axistechnolabs.com.
# All Rights Reserved.
#
# This program is copyright property of the author mentioned above.
# You can`t redistribute it and/or modify it.
#
#################################################################################
from odoo import models, fields, _,api
from odoo.exceptions import Warning
import logging
import tempfile
import binascii
import datetime

_logger = logging.getLogger(__name__)
import io
import re

try:
    import csv
except ImportError:
    _logger.debug('Cannot `import csv`.')
try:
    import xlrd
except ImportError:
    _logger.debug('Cannot `import xlrd`.')
try:
    import base64
except ImportError:
    _logger.debug('Cannot `import base64`.')


class ImportClient(models.TransientModel):
    _name = "import.inventory.adjustment"
    _description = 'import inventory adjustment'

    import_file = fields.Binary(string="Add File")
    file_option = fields.Selection([('csv', 'CSV File'), ('xls', 'XLS File')], string='Select File', default='csv')

    
    def import_inventory_adjustment_action(self):
        if self.file_option == 'csv':
            
            csv_data = base64.b64decode(self.import_file)
            data_file = io.StringIO(csv_data.decode("utf-8"))
            data_file.seek(0)
            csv_reader = csv.DictReader(data_file, delimiter=',')
           
            product_name = self.env['product.product']
            lst =[]

            for line in csv_reader:
                if line.get('Product'):
                    product_name = product_name.search([('name', '=', line.get('Product'))])
                    if not product_name:
                        product_name = product_name.create({
                            'name': line.get('Product'),
                        })
                    partner_count = product_name.sudo().search_count([('name', '=', line.get('Product'))])
                    lst.append(partner_count)
                        
                       
                if line.get('Date'):
                    date = datetime.datetime.strptime(line['Date'], '%m/%d/%Y')
                else:
                    date = datetime.datetime.now()
                            
                inventory_adjustment_info = self.env['stock.inventory'].create({
                    'name':  line.get('Product Name'),
                    'product_ids' :product_name.ids,
                    'accounting_date': date,

                })
            get_count=0
            for rec in lst:
                get_count = get_count+rec
                
            model = self.env.context.get('active_model')
            if model == 'custom.dashboard':
               vendor_info = self.env['custom.dashboard'].sudo().search([['name','=','Inventory Adjustment']])
               if vendor_info.count == 0:
                  vendor_info.count = get_count
               else:
                  vendor_info.count += get_count

        elif self.file_option == 'xls':
            fp = tempfile.NamedTemporaryFile(delete=False, suffix=".xlsx")
            fp.write(binascii.a2b_base64(self.import_file))
            fp.seek(0)
            workbook = xlrd.open_workbook(fp.name)
            sheet = workbook.sheet_by_index(0)
            keys = sheet.row_values(0)
            xls_reader = [sheet.row_values(i) for i in range(1, sheet.nrows)]
           

            product_name = self.env['product.product']
            lst =[]
           

            for row in xls_reader:
                line = dict(zip(keys, row))

                if line.get('Product'):
                    product_name = product_name.search([('name', '=', line.get('Product'))])
                    if not product_name:
                        product_name = product_name.create({
                            'name': line.get('Product'),
                        })
                    partner_count = product_name.sudo().search_count([('name', '=', line.get('Product'))])
                    lst.append(partner_count)
                        
                       
                if line.get('Date'):
                    date = datetime.datetime.strptime(line['Date'], '%m/%d/%Y')
                else:
                    date = datetime.datetime.now()
                
            
                inventory_adjustment_info = self.env['stock.inventory'].create({
                    'name': line.get('Product Name'),
                    'product_ids' :product_name.ids,
                    'accounting_date': date,

                })

            get_count=0
            for rec in lst:
                get_count = get_count+rec
                
            model = self.env.context.get('active_model')
            if model == 'custom.dashboard':
               vendor_info = self.env['custom.dashboard'].sudo().search([['name','=','Inventory Adjustment']])
               if vendor_info.count == 0:
                  vendor_info.count = get_count
               else:
                  vendor_info.count += get_count
          

        else:
            raise Warning(_("Invalid file!"))


     
