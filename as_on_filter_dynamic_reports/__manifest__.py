# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.
##############################################################################
{
    'name': 'As On Filter Customization-Dynamic Reports',
    'category': 'Accounting',
    'version': '14.0.0.0',
    'description': """
    
""",
    'author': 'Fousia Banu A.R',
    'summary': 'This module provides as on filter for all dynamic reports.',
    'website': 'https://www.browseinfo.in',
    'price': 29,
    'currency': "EUR",
    'depends': ['account', 'account_dynamic_reports','dynamic_xlsx'],

    'data': [
         'views/views.xml'
    ],
    'installable': True,
    'auto_install': False,
    'application': True,
    "live_test_url": 'https://youtu.be/DuMt9in_RaE',
    "images": ['static/description/Banner.png'],
}
