{
    'name': 'Stock Movement Report View',
    'summary': '',
    'author': '',
    'depends': ['stock','hb_warehouse_deliveryv2','hb_warehouse_fields','hb_batch_serial',
                'hb_stock_validation','hb_stock_fields','report_xlsx','product_harmonized_system',],
    'data': [
        'views/stock_move_line_view.xml',
        'wizard/stock_movement_view.xml',
    ],
    'installable': True,
    'auto_install': False,
}
