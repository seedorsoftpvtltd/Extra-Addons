{
    'name': 'Stock Picking Weight Details',
    'author': 'Arun Seedor',

    'summary': """ Net weight, gross weight, value of goods and volume computation and
    calculation in transfer (receipts, pick, delivery) and updation in stock balance and
    movement report.""",

    'description': """
                    
                    """,
    'depends': ['stock_picking_weight_details'],
    'data': [
        'views/picking.xml',
    ],
    'installable': True,
    'auto_install': False,
}