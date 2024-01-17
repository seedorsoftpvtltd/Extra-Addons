# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name': 'WareHouse Stock Fields',
    # 'version': '1.1',
    'summary': 'WareHouse Stock Fields',
    # 'sequence': 15,
 #    'description': """WareHouse Stock Fields,
 # """,

    'depends': ['warehouse',
                'stock',
                'scs_freight',
                'convert_freight_operation_to_warehouse',
                'convert_warehouse_from_sales',
                'sh_secondary_unit',

                ],
    'data': [
        'views/warehouse_field_inherited_view.xml',
        'views/stock_picking_inherited_view.xml',

    ],
    'installable': True,
    'application': True,
    'auto_install': False,
    'license': 'LGPL-3',
}

