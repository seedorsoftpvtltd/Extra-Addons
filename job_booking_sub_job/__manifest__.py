{
    'name': 'Sub Job For Job Booking',
    'author': 'Arun Seedor',
    'summary': """
                   
               """,
    'description': """
                    
                    """,
    'depends': ['mail', 'scs_freight', 'jobbooking_custom_view', "hb_product_description", 'stock',
                'professional_templates', 'warehouse_stock_fields', 'hb_warehouse_deliveryv2', 'hb_storage_inv',
                'hb_agreement_extend'],
    'data': [
        'security/ir.model.access.csv',
        'security/security.xml',
        'reports/report.xml',
        'reports/pod.xml',
        'reports/cdr.xml',
        'data/sequence_data.xml',
        'views/sub_job_view.xml',
        'views/job_booking_view.xml',
        'views/stock_picking_view.xml',
    ],
    'installable': True,
    'auto_install': False,
}
