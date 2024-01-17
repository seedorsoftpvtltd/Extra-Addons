# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name': 'Account Sequence number',
    'version': '13.0.0.0.0',
    'category': 'Account',
    'sequence': 14,
    'summary': 'Sequence number',
    'description': """

        ==================

    """,
    'author':  'Poovarasan',
    'website': 'www.seedorsoft.com',
    'depends': ['account'],
    'data': [
        'views/invoice_sequence_views.xml',
            ],
    'demo': [
    ],
   
    'installable': True,
    'auto_install': False,
    'application': True,
}
