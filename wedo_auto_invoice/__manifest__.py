# -*- coding: utf-8 -*-
# Copyright 2020 WeDo Technology
# Website: http://wedotech-s.com
# Email: apps@wedotech-s.com
# Phone:00249900034328 - 00249122005009

{
    'name': " Automatic Purchase Invoice",
    'version': "13.0.0.1",
    'sequence': 1,
    'author': "Wedo Technology",
    'website': "http://wedotech-s.com",
	'support': 'odoo.support@wedotech-s.com',
    'license': 'OPL-1',
    'category': "purchase",
     'summary': """
    Automatic Generate Invoice From Purchase Order and Picking
    """,
    'description': """
    Automatic Generate Invoice From Purchase Order and Picking
 
    """,
	'images': ['images/main_screenshot.png'], 
    'depends': ['purchase'],
    'data': [
        'views/res_config_settings_views.xml',
    ],

}
