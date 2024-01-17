# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name': 'Automatic Item Master ',
    'version': '1.1',
    'summary': '',
    'sequence': 15,
    'description': """======================""",
    'category': 'Automatic Item Master',
    'depends': ['product','hb_warehouse_deliveryv2', 'product_dimension','estimate_sale_link'],
    'data': [
       'views/views.xml',

    ],
    'demo': [

    ],
    'qweb': [

    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}
