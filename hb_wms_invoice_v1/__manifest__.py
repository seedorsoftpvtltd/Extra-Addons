{
        'name': 'WMS Invoice ',
        'version': '0.1',
        'category': 'Warehouse',
        'author': 'Herlin Breese J',
        'summary': '',
        'description': """
        
    """,
    'depends': [
        'product','warehouse','hb_agreement_extend','account','hb_wms_invoice'
    ],

    'data': [
        'views/view.xml',
        'views/product_history_ext.xml',
        'security/ir.model.access.csv',
        'views/picking.xml',
        'views/wizard.xml',

    ],

    'installable': True,
    'application': True,
}