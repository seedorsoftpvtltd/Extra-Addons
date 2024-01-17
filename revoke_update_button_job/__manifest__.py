# -*- coding: utf-8 -*-
{
    'name': 'Update Revoke Button in Job Booking',
    'summary': "Update Revoke Button in Job Booking",
    'description': "Update Revoke Button in Job Booking",

    'author': 'Fousia Banu A R.',


    'category': 'Extra Tools',
    'version': '13.0.0.1.0',
    'depends': ['web','scs_freight','sh_secondary_unit'],

    'data': [
        'views/button_views.xml',
        'security/security.xml',
        'wizard/wizard.xml',
    ],

    'license': "OPL-1",
    'price': 20,
    'currency': "EUR",

    'auto_install': False,
    'installable': True,

    'images': ['static/description/banner.png'],
}
