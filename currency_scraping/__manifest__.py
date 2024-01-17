# -*- coding: utf-8 -*-
{
    'name': "Auto Currency Update",

    'summary': """
        This module will update all your active currency from authorized website. Execution can be done by scheduled time or manually""",

    'description': """
        Long description of module's purpose
    """,

    'author': "Techspawn Solutions Pvt. Ltd.",
    'website': "http://www.techspawn.co",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',
    'license': 'OPL-1',
    'price': 25.00,
    'currency': 'USD',
    # any module necessary for this one to work correctly
    'depends': ['base'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
 "images": ['static/description/Currency Auto Update.gif'],
}
