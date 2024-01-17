{
        'name': 'Journal - Payment Selection',
        'version': '0.1',
        'category': 'Accounting',
        'author': 'Herlin Breese',
        'summary': '',
        'description': """
        
    """,
    'depends': [
        'base','to_account_payment',
        #'sh_secondary_unit'
    ],

    'data': [
        'views/payment.xml',

    ],

    'installable': True,
    'application': True,
}
