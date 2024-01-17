# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name': 'Warehouse Picking Onchange',
    'version': '1.1',
    'summary': 'If select the warehouse field automatically  fetch the Deliver To field',
    'sequence': 15,
    'description': """Warehouse Picking Onchange,
 """,

    'depends': [
         'warehouse', 'sh_secondary_unit','warehouse_stock',

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

    'license': 'LGPL-3',
}
