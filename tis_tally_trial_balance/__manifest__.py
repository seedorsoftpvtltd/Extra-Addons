# -*- coding: utf-8 -*-
# This module and its content is copyright of Technaureus Info Solutions Pvt. Ltd.
# - © Technaureus Info Solutions Pvt. Ltd 2020. All rights reserved.
{
    'name': 'Tally Trial Balance',
    'version': '13.0.0.6',
    'sequence': 1,
    'category': 'Accounting',
    'summary': 'Tally Type Trial Balance - Financial Report',
    'author': 'Technaureus Info Solutions Pvt. Ltd.',
    'website': 'http://www.technaureus.com/',
    'description': """
    Tally Type Trial Balance
        """,
    'depends': ['accounting_pdf_reports','base_accounting_kit'],
    'price': 35,
    'currency': 'EUR',
    'license': 'Other proprietary',
    'data': [
        'wizard/tally_trial_balance_wizard.xml',
        'report/tally_trial_balance_report.xml',
        'report/tally_trial_balance_report_template.xml',
    ],
    'images': ['images/main_screenshot.png'],
    'installable': True,
    'auto_install': False,
    'application': True,
    'live_test_url': 'https://www.youtube.com/watch?v=0OXaY-eqxq4'
}
