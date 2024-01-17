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

{
    'name': "Multiple Barcodes For Product",
    'version': "13.0.0.0",
    'summary': "You can register multiple barcode for single product and also select products in sale, purchase, invoice,  ETC... with that multiple barcode",
    'category': 'Sales',
    'description': """
    You can register multiple barcode for single product and also select products in sale, purchase, invoice,  ETC... with that multiple barcode
    """,
    'author': "Sitaram",
    'website':"http://www.sitaramsolutions.in",
    'depends': ['base', 'product'],
    'data': [
        'security/ir.model.access.csv',
        'views/inherited_product.xml',
        'wizard/sr_import_multi_barcode.xml'
    ],
    'demo': [],
    "external_dependencies": {},
    "license": "AGPL-3",
    'installable': True,
    'auto_install': False,
    'live_test_url':'https://youtu.be/E8mrNKGNdoE',
    'images': ['static/description/banner.png'],
    "price": 0.0,
    "currency": 'EUR',
    
}
