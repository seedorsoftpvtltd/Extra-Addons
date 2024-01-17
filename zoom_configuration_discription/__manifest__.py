# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name': 'Zoom Configuration Description ',
    'version': '1.1',
    'summary': 'Zoom Configuration Description',
    'sequence': 15,
    'description': """Zoom Configuration Description,
 """,
    'category': 'Productivity',
    'website': 'https://www.odoo.com/page/billing',
    # 'images': ['static/description/1.png'],
    'depends': [
        'zoom_integration',

    ],
    'data': [
        'security/ir.model.access.csv',
        'views/company_description_view.xml',
        'views/user_description_view.xml',

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
