# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.
##############################################################################
{
    'name': 'Dynamic Report Custom Filter Fix',
    'category': 'Accounting',
    'version': '14.0.0.0',
    'description': """

""",
    'author': 'Fousia Banu A.R',
    'summary': 'This module fixes custom filter dropdown in all reports .',
    'website': '',
    'price': 29,
    'currency': "EUR",
    'depends': ['account', 'account_dynamic_reports', 'dynamic_xlsx','web'],

    'data': [
        'views/assets.xml',
    ],
    'installable': True,
    'auto_install': False,
    'application': True,
    "live_test_url": 'https://youtu.be/DuMt9in_RaE',
    "images": ['static/description/Banner.png'],
}
