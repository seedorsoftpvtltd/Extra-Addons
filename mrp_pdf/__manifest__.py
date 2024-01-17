# -*- coding: utf-8 -*-
{
    'name': "Manufacturing Report",

    'summary': """Manufacturing Report""",

    'description': """
       
    """,

    'author': "DA",
    'website': "http://www.banibro.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Manufacturing',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base',],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'mrp_view.xml',
		'mrp_template.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'mrp_view.xml',
    ],
}