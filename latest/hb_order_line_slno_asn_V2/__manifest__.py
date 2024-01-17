# -*- coding: utf-8 -*-
{
    'name': "Order Line Serial Number[V2]",

    'summary': """
        Adds Serial Numbers to Order Lines[Extended Module]""",

    'description': """
        This Module Adds Serial Numbers to order Lines in Warehouse orders and in Goods Issue orders Dynamically After the Products added and Saved.
    """,

    'author': "Fousia Banu A.R",
    'website': "http://www.seedorsoft.com",

    'category': 'Others',
    'version': '0.1',

    'depends': ['base', 'warehouse','asn_views','hb_order_line_sl_no','warehouse_stock_fields_asn_V2'],

    'images': [
        # 'images/main.jpg',
    ],
    'data': [

        'views/views.xml',
    ],
}
