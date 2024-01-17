# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name': 'Invoice Total price update',
    # 'version': '1.1',
    'summary': 'In invoice untaxed amount field was not update the value',
    # 'sequence': 15,
 #    'description': """WareHouse Stock Fields,
 # """,

    'depends': ['account',
                'account_invoice_pricelist',

                ],
    'data': [
        'security/ir.model.access.csv',

    ],
    'demo': [

    ],
    'qweb': [

    ],
    'installable': True,
    'application': True,
    'auto_install': False,
    # 'post_init_hook': '_auto_install_l10n',
    # 'images': ['static/description/icon.png'],
    'license': 'LGPL-3',
}

