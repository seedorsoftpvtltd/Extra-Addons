# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name': 'Pattern Template ',
    'version': '1.1',
    'summary': 'Pattern Template',
    'sequence': 15,
    'description': """Pattern Template,
 """,
    'category': 'Productivity',
    'author': "Jincy",
    # 'images': ['static/description/1.png'],
    'depends': ['warehouse',
                'stock', 'base',
                # 'warehouse_stock_fields',
                'sh_secondary_unit',


                ],
    'data': [
        'security/ir.model.access.csv',

        'views/pattern_template.xml',
        'views/warehouse_order_inherited_view.xml',

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
