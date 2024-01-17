# -*- coding: utf-8 -*-
{
    'name': ' Warehouse Custom Fields',
    'version': '13.0.1.0.0',
    'category': 'Inventory',
    'author': 'Herlin Breese J',
    'summary': 'Warehouse Custom Fields',
    'website': 'http://www.seedorsoft.com',
    'description': """""",
    'depends': [
        'stock',
        'stock_quant_package_dimension',
        'base',
        'product_uom_qty',
        'warehouse',
    ],
    'data': [
        'views/view.xml',
        'views/product_uom.xml',
    ],
    'images': [
    ],
    'installable': True,
}
