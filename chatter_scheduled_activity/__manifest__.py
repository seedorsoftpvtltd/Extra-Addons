# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name': 'Chatter Scheduled Activity ',
    'version': '1.1',
    'summary': 'Chatter Scheduled Activity',
    'sequence': 15,
    'description': """Chatter Scheduled Activity,
 """,
    'category': 'Productivity',
    'website': 'https://www.odoo.com/page/billing',
    # 'images': ['static/description/1.png'],
    'depends': ['subscription_management',
                'account',
                'analytic',

                'mail',

                ],
    'data': [
        'security/ir.model.access.csv',
        'views/subscription_sale_chatter_view.xml',

        'views/contract_sale_chatter_view.xml',

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
