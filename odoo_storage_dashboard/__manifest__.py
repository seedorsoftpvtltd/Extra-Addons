# -*- coding: utf-8 -*-

{
    'name': 'Odoo Storage Dashboard',
    'version': '14.0.0.1',
    'summary': """Displays Storage Information Of the database.""",
    'description': """Displays Storage Information Of the database.""",
    'category': 'Extra Tools',
    'author': 'iKreative',
    'website': "",
    'license': 'AGPL-3',

    'price': 20.0,
    'currency': 'USD',

    'depends': ['base'],

    'data': [
        'security/ir.model.access.csv',
        'views/dashboard_view.xml',
    ],
    'demo': [

    ],
    'images': ['static/description/banner.png'],
    'qweb': [],

    'installable': True,
    'auto_install': False,
    'application': False,
}
