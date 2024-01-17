{
    'name': 'Transport Fields in Transfers',
    'author': 'Arun Seedor',
    'summary': """
    change custom field to backend field with the case of show only operation type
    is DO and Receipts
                   
               """,
    'description': """
                    
                    """,
    'depends': ['base','stock'],
    'data': [
        'views/stock_picking_view.xml',
    ],
    'installable': True,
    'auto_install': False,
}