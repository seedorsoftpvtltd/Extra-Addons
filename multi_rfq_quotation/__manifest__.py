{
    'name': 'Create Multi RFQ With Multi Vendor In Sales',
    'author': 'Arun Seedor',
    'summary': """
                   Create RFQ for the services from the quotation. Can able to select the multiple vendors.
               """,
    'description': """
                    
                    """,
    'depends': ['sale', 'purchase',],
    'data': [
        'security/ir.model.access.csv',
        'wizard/purchase_order_wizard_view.xml',
        'wizard/validation_pop_view.xml',
        'views/sale_view.xml',
        'views/purchase_views.xml'
    ],
    'installable': True,
    'auto_install': False,
}
