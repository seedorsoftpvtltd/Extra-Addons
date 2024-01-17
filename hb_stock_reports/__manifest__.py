{
        'name': 'Stock Reports',
        'version': '0.1',
        'category': 'Stock',
        'author': 'Herlin Breese J',
        'summary': '',
        'description': """
        
    """,
    'depends': [
        'stock', 'hb_stock_validation', 'stock_balance', 'warehouse'
    ],

    'data': [
        'views/stock.xml',
    ],

    'installable': True,
    'application': True,
}