# -*- coding: utf-8 -*-
# This module and its content is copyright of Technaureus Info Solutions Pvt. Ltd.
# - © Technaureus Info Solutions Pvt. Ltd 2019. All rights reserved.

{
    'name': 'Tally Balance Sheet and Profit & Loss',
    'version': '13.0.0.2',
    'category': 'Accounting',
    'sequence': 1,
    'author': 'Technaureus Info Solutions Pvt. Ltd.',
    'summary': 'Tally Balance Sheet and Profit & Loss Report',
    'description': """
Add additional features
================================
    """,
    'website': 'http://www.technaureus.com',
    'price': 35,
    'currency': 'EUR',
    'license': 'Other proprietary',
    'depends': [
        'accounting_pdf_reports'
],
    'data': [
        'views/templates.xml',
        'views/account_report_menu.xml',
        'report/account_tally_bs_report_template.xml',
        'report/dynamic_financial_report_template.xml',
        'report/account_tally_bs_report.xml',
        'wizard/account_tally_balance_sheet_view.xml',
    ],
    'qweb': [
        'static/src/xml/financial_reports_view.xml',
    ],
    'images': ['images/main_screenshot.png'],
    'auto_install': False,
    'installable': True,
    'application': True
}
