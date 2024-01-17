# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name': 'WareHouse Package V2 ',
    'version': '1.1',
    'summary': 'WareHouse Package V2[Extended]',
    'sequence': 15,
    'description': """WareHouse Package,
 """,
    'category': 'Productivity',
    'website': 'https://www.odoo.com/page/billing',
    # 'images': ['static/description/1.png'],
    'depends': ['warehouse',
                'stock', 'base',
                'warehouse_stock_fields',
                'warehouse_stock',
                'asn_views',
                'warehouse_type_packages'],
    'data': [
            'views/views.xml',
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

