# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name': 'Freight Management Chatter',
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

                ],
    'data': [
        'security/ir.model.access.csv',
        'views/freight_operation_chatter_view.xml',
        'views/operation_custom_chatter_view.xml',
        'views/freight_port_chatter_view.xml',
        'views/freight_vessels_chatter_view.xml',
        'views/freight_airline_chatter_view.xml',
        'views/freight_container_chatter_view.xml',
        'views/operation_price_list_chatter_view.xml',

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
