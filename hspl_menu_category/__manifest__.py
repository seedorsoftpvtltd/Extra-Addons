# -*- coding: utf-8 -*-
# Copyright 2018, 2020 Heliconia Solutions Pvt Ltd (https://heliconia.io)

{

    'name': "Menu Category",

    'summary': """

        Odoo 13.0 community backend Category wise Menu Dashboard

    """,

    'description': """

        To unable Categories you have to create categories and assign it to menus,

        Settings > User Interface > Menu Items Category (assign to menu items after that.)

    """,

    'author': "Heliconia Solutions Pvt. Ltd.",

    'website': "https://heliconia.io",

    'category': 'Tools',

    'version': '13.0.0.0.1',

    'depends': ['web_responsive'],

    'license': 'OPL-1',
    'price': 19.00,
    'currency': 'EUR',
    'data': [

        'security/ir.model.access.csv',
        'views/assets.xml',
        'views/ir_ui_menu.xml',
        'views/ir_ui_menu_category.xml',
    ],

    'qweb': [
        'static/src/xml/apps_category.xml',
    ],

    'images': ['static/description/heliconia_menu_category.gif'],

}
