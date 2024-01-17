{
    'name': 'Stock Picking Weight Details',
    'author': 'Arun Seedor',

    'summary': """ Net weight, gross weight, value of goods and volume computation and
    calculation in transfer (receipts, pick, delivery) and updation in stock balance and
    movement report.""",

    'description': """
                    
                    """,
    'depends': ['warehouse','warehouse_stock','stock','product'],
    'data': [
        'views/product_view.xml',
        'views/warehouse_view.xml',
        'views/stock_picking_view.xml',
        'views/stock_move_line_view.xml',
    ],
    'installable': True,
    'auto_install': False,
}