{
    'name': 'Storage Type',
    'summary': ' Change existing selection storage field to Many2one field, menu conf in job booking',
    'author': 'Arun Seedor',
    'depends': ['hb_warehouse_deliveryv2','hb_agreement_extend'],
    'data': [
        'views/storage_type.xml',
    ],
    'installable': True,
    'auto_install': False,
}
