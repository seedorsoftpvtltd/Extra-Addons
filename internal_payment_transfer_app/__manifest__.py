# -*- coding: utf-8 -*-
{
    'name': 'Payment Transfer With Account/Journal Option',
    "author": "Edge Technologies",
    'version': '13.0.1.0',
    'live_test_url': "https://youtu.be/4_9w_0UIW3o",
    "images":['static/description/main_screenshot.png'],
    'summary': "Payment journal to account transfer payment account to journal transfer internal account transfer internal transfer payment account payment voucher payment account transfer payment account to account to transfer account cash transfer bank account transfer",
    'description': """This app helps user to transfer payment internally with many options like account to account, journal to account, and account to journal.

payment management for internal transfer
Journal to account transfer
Account to journal transfer
Manage payment
Internal transfer
Internal transfer payment 
Managing internal transfer payment
Account payment voucher
Generate payment
Account transfer
Payment account transfer
Account to account to transfer 
Payment management voucher
Account internal transfer request
Account type internal transfer request
Internal transfer request
Account type
Account payment type
Payment account type
Account types menu
Voucher account types
Odoo account types menu
Account payment internal transfer option
Account cash transfer bank account transfer bank account payment transfer cash account payment transfer
Account payment with journal transfer option transfer from account to account transfer from journal to journal transfer 
Odoo automatic payment transfer option from journal


    """,
    "license" : "OPL-1",
    'depends': ['base','sale_management','account','purchase','stock_account','sr_manual_currency_exchange_rate', 'dev_invoice_multi_payment'],
    'data': [
            'views/inherit_payment.xml',
            ],
    'installable': True,
    'auto_install': False,
    'price': 18,
    'currency': "EUR",
    'category': 'Accounting',

}

