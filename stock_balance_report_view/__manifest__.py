{
    'name': 'Stock Balance Excel',
    'summary': '',
    'author': '',
    'depends': ['stock_balance','hb_warehouse_deliveryv2','stock_storage_type','hb_stock_fields',
                'product_harmonized_system','stock_3dbase', 'stock_location_zone'],
    'data': [
        'views/stock_quant_view.xml',
        'wizard/balance_view.xml',
    ],
    'installable': True,
    'auto_install': False,
}
