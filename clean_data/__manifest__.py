# -*- coding: utf-8 -*-
{
    'name': "Mass Clean Data (Clear Data)",
    'summary': '''This module allows to user clear the unwanted data using wizard.
    Clean, Clear, Delete, Clean Data, data clean,
    Clear data, data clear, Delete Data,
    Bulk, Bulk delete, bulk clear, clear bulk, delete bulk, multiple, multiple delete, multi, multi delete, 
    multi clear, multi remove, multi clean,
    SQl, SQl delete, Delete records, remove records, remove accounting, delete accounting,
    journal entries, journal items, journal entry, Delete all, all delete, data cleaner, DB cleaner, cleaner, 
    Database, Database cleaner, bulk cleaner, tool, Db tool, DB delete tool, Database delete tool, purchase, sales, 
    transfers, invoice, invoices, customer,
    payments, vendor, data delete, delete data''',
    'author': "Aktiv Software",
    'website': "http://www.aktivsoftware.com",
    'description': "User can easily clean the data",
    'category': 'Tools',
    'version': '13.0.0.0.2',
    'license': 'AGPL-3',
    'price': 7.00,
    'currency': "EUR",
    # any module necessary for this one to work correctly
    'depends': ['base'],

    # always loaded
    'data': [
        'wizards/clean_data_view.xml',
    ],
    'live_test_url': 'https://www.youtube.com/watch?v=p7DajltA4Rg',
    'images': ['static/description/banner.png'],
    'installable': True,
    'auto_install': False,
}
