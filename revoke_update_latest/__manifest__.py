# -*- coding: utf-8 -*-
{
    'name': 'Update Revoke Button For Selected Services in Job Booking',
    'summary': "Update Revoke Button For Selected Services in Job Booking",
    'description': "Update Revoke Button For Selected Services in Job Booking",

    'author': 'Fousia Banu A R.',


    'category': 'Extra Tools',
    'version': '13.0.0.1.0',
    'depends': ['web','scs_freight','revoke_update_button_job'],

    'data': [
        'wizard/update_invoice_views.xml',
        'views/button_views.xml'
    ],

    'license': "OPL-1",
    'price': 20,
    'currency': "EUR",

    'auto_install': False,
    'installable': True,

    'images': ['static/description/banner.png'],
}