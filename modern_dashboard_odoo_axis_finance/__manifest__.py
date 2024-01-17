# -*- coding: utf-8 -*-
{
    'name': "Modern Odoo Dashboards - Odoo Inventory Dashboard, Sales Dashboard, Account Dashboard",

   'summary': """
       Dashboard - inventory dashboard in odoo, sales dashboard 
       in odoo, account dashboard in odoo with chart and graphs and table view.""",
    'live_test_url': 'https://www.youtube.com/watch?v=7KnOICS9q7s&feature=youtu.be',

    'depends': ['base','sale_management','stock','account'],


    'data': [
        'security/security.xml',
        'views/assets.xml',
        'views/sale_search_view.xml',
        # 'views/pos_config.xml',
        'views/account_search_view.xml',
        # 'views/crm_search_view.xml',
        'views/inventory_searcch_view.xml',
        'views/menu_dashboard_view.xml',
    ],

    'qweb': ["static/src/xml/sale_dashboard.xml",

             "static/src/xml/inventory_dashboard.xml",
             "static/src/xml/account_dashboard.xml",

             "static/src/xml/backend_dashboard.xml",
             ],
             
    'application': True,
    'license': 'AGPL-3',
    'price': 150,
    'currency': 'USD',
    'support': 'business@axistechnolabs.com',
    'author': 'Axis Technolabs',
    'website': 'http://www.axistechnolabs.com',
    'images': ['static/description/images/Banner-Img.png'],
}