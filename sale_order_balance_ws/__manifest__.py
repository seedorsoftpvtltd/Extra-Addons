# -*- coding: utf-8 -*-
{
    'name': 'Customer Balance in Sale Order',
    'version': '1.0',
    'category': 'Tools',
    'author':'Craftsync Technologies',
    'maintainer': 'Craftsync Technologies',
    'website' : 'https://www.craftsync.com',
    'summary': """Check for your customer balance on Sale Order
        Keywords
        =============================
        Customer Balance Balance credit debit customer credit customer debit Balance in SO Balance in sale order Balance in sales order Customer credit in SO Customer credit in sale order Customer credit in sales order customer credit current balance of partner current balance of customer Show customer balance in sale order Show balance Show credit Show Customer credit Customer outstanding payment Outstanding amount amount due
     """,
    'license': 'OPL-1',
    'support':'info@craftsync.com',
    'sequence': 1,
    'depends': [
        'sale'
    ],
    'data': [
       'views/sale_order.xml'
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
    'images': ['static/description/main_screen.png'],
    'price': 10.00,
    'currency': 'EUR',
}
