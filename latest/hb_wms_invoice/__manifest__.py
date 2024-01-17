{
    'name':'WMS Invoice',
    'summary': """WMS Invoice""",
    'version': '13.0.1.0.0',
    'description': """""",
    'author': 'Herlin Breese J',
    'company': 'Seedorsoft Pvt Ltd',
    'website': 'https://www.seedorsoft.com',
    'category': 'Tools',
    'depends': ['base', 'stock', 'account', 'hb_agreement_extend', 'hb_storage_inv', 'product_dimension'],
    'license': 'AGPL-3',
    'data': [
        'security/ir.model.access.csv',
        'views/services.xml',
        'views/product_history.xml',
        'views/product.xml',

    ],
    'demo': [],
    'installable': True,
    'auto_install': False,
}
