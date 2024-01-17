# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name': 'Freight Management Chatter Depend',
    'version': '1.1',
    'summary': 'Freight Management Chatter',
    'sequence': 15,
    'description': """Freight Management Chatter,
 """,
    'category': 'Productivity',
    'website': 'https://www.odoo.com/page/billing',
    # 'images': ['static/description/1.png'],
    'depends': ['scs_freight',
                'mail',
                'jobbooking_custom_view',
                ],
    'data': [
        'views/freight_operation_chatter_view.xml',

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
