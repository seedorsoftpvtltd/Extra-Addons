# -*- coding: utf-8 -*-
{
    'name': "Order Line Serial Number depend",

    'summary': """
        Adds Serial Numbers to Order Lines""",

    'description': """
        This Module Adds Serial Numbers to order Lines in Warehouse orders and in Goods Issue orders Dynamically After the Products added and Saved.
    """,

    'author': "Herlin Breese J",
    'website': "http://www.seedorsoft.com",

    'category': 'Others',
    'version': '0.1',

    'depends': ['base', 'warehouse', 'gio','hb_order_line_sl_no','gio_custom_view','hb_freight_extend'],
    
    'images': [
        # 'images/main.jpg',
     ],
    'data': [
        # 'security/ir.model.access.csv',
        'templates.xml',
    ],
}
