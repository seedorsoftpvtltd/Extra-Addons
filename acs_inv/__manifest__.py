# -*- coding: utf-8 -*-
{
    'name': "ACS-13 Invoice Template",

    'summary': """ACS Invoice""",

    'description': """
       
    """,

    'author': "Dharani",
    'website': "http://www.seedorsoft.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','account',],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'view.xml',
        'del_view.xml',
		
    ],
    # only loaded in demonstration mode
    'demo': [
        'view.xml',
    ],
}