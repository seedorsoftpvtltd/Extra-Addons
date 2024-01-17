# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name': 'Recruitment Medium ',
    'version': '1.1',
    'summary': 'To add the medium in Recruitment',
    'sequence': 15,
    'description': """Recruitment Medium,
 """,
    'category': 'Productivity',
    'author': "Jincy",

    'depends': ['hr',
                'hr_recruitment',
                'utm',


                ],
    'data': [
        'security/ir.model.access.csv',

        'views/recruitment_medium.xml',


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
