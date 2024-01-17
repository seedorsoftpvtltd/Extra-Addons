{
        'name': 'Storage Invoice ',
        'version': '0.1',
        'category': 'WMS',
        'author': 'Herlin Breese J',
        'summary': '',
        'description': """
        
    """,
    'depends': [
        'contacts','hb_warehouse_deliveryv2','warehouse','stock',
    ],

    'data': [
        'views/sto.xml',
        'security/ir.model.access.csv',
#        'data/res_partner.xml',

    ],

    'installable': True,
    'application': True,
}
