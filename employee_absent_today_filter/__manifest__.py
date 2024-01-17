# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name': 'Employee Absent Today Filter',
    'version': '1.1',
    'summary': 'Employee Absent Today Filter',
    'sequence': 15,
    'description': """Employee Absent Today Filter,
 """,
    'category': 'Productivity',
    'website': 'https://www.odoo.com/page/billing',
    # 'images': ['static/description/1.png'],
    'depends': ['hr',
                'hr_attendance',
                'hr_holidays',

                ],
    'data': [
        'security/ir.model.access.csv',

        'views/employee_absent_today_filter_view.xml',


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
