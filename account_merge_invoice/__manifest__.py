# -*- coding: utf-8 -*-

{
    'name': 'Merge Invoice for Same Partners',
    'category': 'account',
    'summary': 'This module will Merge invoice having same partners and in draft state.',
    'version': '13.0',
    'website': 'http://www.HITechSolutions.com',
    'author': 'HAK Solutions',
    'description': 'This module will Merge invoice having same partners and in draft state',
    'license': "AGPL-3",
    'depends': ['account'],
    'data': [
        'wizard/single_vendor_bill_wizard_view.xml'
    ],

    'images': ['static/description/banner.png'],
    "price": 0,
    "currency": "EUR",

    'installable': True,
}



