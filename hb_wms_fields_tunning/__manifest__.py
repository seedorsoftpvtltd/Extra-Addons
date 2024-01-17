{
        'name': 'WMS Fields Tunning',
        'version': '0.1',
        'category': 'WMS',
        'author': 'Herlin Breese J',
        'summary': '',
        'description': """
        
    """,
    'depends': [
        'base','warehouse_stock','sale','hb_warehouse_deliveryv2', 'convert_warehouse_from_sales','bi_convert_purchase_from_sales',
        'job_cost_estimate_customer',
    ],

    'data': [
        # 'views/map.xml',
    ],

    'installable': True,
    'application': True,
}