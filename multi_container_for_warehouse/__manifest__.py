{
    'name': 'Warehouse Multiple Container',
    'author': 'Arun Seedor',
    'summary': 'Add multiple container in Advance shipping',
    'depends': ['base', 'warehouse', 'scs_freight','stock','sh_secondary_unit','warehouse_stock_fields'],
    'data': [
        'security/ir.model.access.csv',
        'views/warehouse_views.xml',
        'views/pattern_tag.xml',
        'views/stock_picking_views.xml',

    ],
    'installable': True,
    'auto_install': False,
}
