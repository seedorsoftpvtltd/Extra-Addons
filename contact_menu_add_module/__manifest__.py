# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name': 'Contact Menu',
    'version': '1.1',
    'summary': 'To add the menu in contact module',
    'sequence': 15,
    'description': """To add the menu in contact module,
 """,
    # 'category': 'Productivity',
    'author': "JKM",

    'depends': ['contacts',




                ],
    'data': [
        'security/ir.model.access.csv',

        'views/company_menu.xml',
        'views/customer_menu.xml',
        'views/vendors_menu.xml',
        'views/agents_menu.xml'



    ],
    'demo': [

    ],
    'qweb': [

    ],
    'installable': True,
    'application': True,
    'auto_install': False,
    'license': 'LGPL-3',
}
