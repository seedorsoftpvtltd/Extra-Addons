# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name': 'Employee Contract Monthly Variables',
    'version': '1.1',
    'summary': 'Employee Contract Monthly Variables',
    'sequence': 15,
    'description': """Employee Contract add new tab on Monthly Variables ,
 """,

    'depends': [
        'hr','hr_contract'

    ],
    'data': [
        'security/ir.model.access.csv',

        'views/employee_contract_tab_view.xml',

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
