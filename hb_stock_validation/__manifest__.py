{
        'name': 'Stock Validation ',
        'version': '0.1',
        'category': 'Stock',
        'author': 'Herlin Breese J',
        'summary': '',
        'description': """
        
    """,
    'depends': [
        'base','stock','product','warehouse', 'stock',
    ],

    'data': [
        'views/view.xml',
        'security/ir.model.access.csv',
    ],

    'installable': True,
    'application': True,
}