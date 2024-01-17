# -*- coding: utf-8 -*-
{
    'name': ' Warehouse Delivery Order',
    'version': '13.0.1.0.0',
    'category': 'Category',
    'author': 'Herlin Breese J',
    'summary': 'Warehouse delivery order',
    'website': 'http://www.seedorsoft.com',
    'description': """""",
    'depends': [
        'base','stock','quality_control_oca','warehouse','product'
    ],
    'data': [
        'views/stock.xml',
        'security/ir.model.access.csv',
        'views/sku_master.xml',
    ],
    'images': [
    ],
    'installable': True,
}
