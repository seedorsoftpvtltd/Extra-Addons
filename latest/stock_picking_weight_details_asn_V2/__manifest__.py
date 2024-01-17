{
    'name': 'Stock Picking Weight Details V2',
    'author': 'Fousia Banu A.R',

    'summary': """ Net weight, gross weight, value of goods and volume computation and
    calculation in transfer (receipts, pick, delivery) and updation in stock balance and
    movement report V2[Extend].""",

    'description': """

                    """,
    'depends': ['warehouse', 'warehouse_stock', 'stock', 'product','stock_picking_weight_details', 'asn_views','warehouse_stock_fields_asn_V2'],
    'data': [
        'views/views.xml',
    ],
    'installable': True,
    'auto_install': False,
}