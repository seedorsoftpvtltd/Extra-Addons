{
        'name': 'WMS Client Consignee Invoice',
        'version': '0.1',
        'category': 'Warehouse',
        'author': 'Herlin Breese J',
        'summary': 'WMS Client Consignee Invoice',
        'description': """
        
    """,
    'depends': [
        'hb_wms_invoice_v1','hb_stock_validation',
        'hb_warehouse_deliveryv2_depend',
    ],

    'data': [
        'views/view.xml',
        'views/product_history_ext.xml',
        # 'security/ir.model.access.csv',
        'views/picking.xml',
        'views/wizard.xml',

    ],

    'installable': True,
    'application': True,
}