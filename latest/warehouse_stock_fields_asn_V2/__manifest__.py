# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name': 'WareHouse Stock Fields V2',
    # 'version': '1.1',
    'summary': 'WareHouse Stock Fields V2 Extend',
    # 'sequence': 15,
 #    'description': """WareHouse Stock Fields,
 # """,

    'depends': ['warehouse',
                'stock',
                'scs_freight',
                'convert_freight_operation_to_warehouse',
                'convert_warehouse_from_sales',
                'sh_secondary_unit',
                'asn_views',
                'warehouse_stock_fields'

                ],
    'data': [
      'views/views.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
    'license': 'LGPL-3',
}

