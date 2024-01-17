# -*- coding: utf-8 -*-

{
    'name': 'Report',
    'author': "",
    'version': '13.0.1.1',
    'live_test_url': '',
    "images": ['static/description/main_screenshot.png'],
    'summary': 'Job to warehouse link',
    'description': """

    """,
    'depends': ['bi_payment_overdue_finance','account_statement'],
    "license": "OPL-1",
    'data': [
        'views/views.xml',
        'views/reports.xml',
        'views/template.xml'

    ],
    'qweb': [],
    'demo': [],
    'installable': True,
    'auto_install': False,
    'category': 'Warehouse',
}