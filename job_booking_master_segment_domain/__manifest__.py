{
    'name': 'Configuration Domain in Job Booking Master Segment',
    'author': 'Arun Seedor',
    'summary': """
                   Based segment, transport, job type etc show product in services in job booking.
                   Also enable and disable the configuration.
               """,
    'description': """
                    
                    """,
    'depends': ['product','scs_freight','hb_freight_extend','sale'],
    'data': [
        'views/res_config_view.xml',
        'views/product_view.xml',
    ],
    'installable': True,
    'auto_install': False,
}