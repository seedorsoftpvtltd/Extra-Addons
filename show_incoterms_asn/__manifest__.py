{
    'name': 'Show Incoterm in ASN',
    'author': 'Arun Seedor',
    'summary': """
                created a manyone field in ASN to show incoterm data in ASN   
               """,
    'depends': ['account','warehouse','stock'],
    'data': [
        'views/warehouse_views.xml',
        'views/stock_picking_views.xml'
    ],
    'installable': True,
    'auto_install': False,
}