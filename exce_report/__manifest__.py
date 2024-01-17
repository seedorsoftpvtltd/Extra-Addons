# -*- coding: utf-8 -*-

{
    'name': 'Export',
    'author': "",
    'version': '13.0.1.1',
    'live_test_url': '',
    "images": ['static/description/main_screenshot.png'],
    'summary': 'Job to warehouse link',
    'description': """

    """,
    'depends': ['report_xlsx', 'account_statement','bi_payment_overdue_finance'],
    "license": "OPL-1",
    'data': [
             'views/views.xml',
             'report/report_xls.xml',


    ],
    'qweb': [],
    'demo': [],
    'installable': True,
    'auto_install': False,
    'category': 'Warehouse',
}