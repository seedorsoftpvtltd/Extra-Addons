# -*- coding: utf-8 -*-
{
    'name': "Adding Sale-Purchase Order Lines In Menu",

    'summary': """
        Sale order lines and purchase order lines are included in the module menu.
        """,

    'description': """
        Sale order lines and purchase order lines are included in the sale and purchase module menu.
        A group is created and only those who are approved by the admin will be added in the group.
        Only those users will be having the permission to view the addons.
    """,

    'author': "Amzsys",
    'website': "https://amzsys.com/",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.8',

    # any module necessary for this one to work correctly
    'depends': ['base', 'sale', 'sale_management', 'purchase'],

    # always loaded
    'data': [
        'security/multi_product_security.xml',
        'views/views.xml',
    ],
    'images':[
        'images/cover-sale_purchase.png',
        ],
    # only loaded in demonstration mode

    'demo': [
        'demo/demo.xml',
    ],
    "license": "OPL-1",
}

