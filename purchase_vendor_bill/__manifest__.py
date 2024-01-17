# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name': 'Purchase Price Amount',
    'version': '13.0.0.0.0',
    'category': 'Account',
    'sequence': 14,
    'summary': 'Purchase Price Amount',
    'description': """

        ==================

    """,
    'author':  'Poovarasan',
    'website': 'www.seedorsoft.com',
    'depends': ['account'],
    'data': [
        'views/purchase_price_views.xml',
            ],
    'demo': [
    ],
   
    'installable': True,
    'auto_install': False,
    'application': True,
}
