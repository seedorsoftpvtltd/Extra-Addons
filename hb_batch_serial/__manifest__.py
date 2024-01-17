{
        'name': 'Batch No & Serial No ',
        'version': '0.1',
        'category': 'Employee',
        'author': 'Herlin Breese',
        'summary': '',
        'description': """
        
    """,
    'depends': [
        'base','stock','hb_warehouse_deliveryv2','gio',
    ],

    'data': [
        # 'views/batch_serial.xml',
        # 'views/stock_bs.xml',
        # 'views/gio.xml',
        # 'security/ir.model.access.csv',
        'views/bs.xml',

    ],

    'installable': True,
    'application': True,
}
