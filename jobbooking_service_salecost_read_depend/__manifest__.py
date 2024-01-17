# -*- coding: utf-8 -*-
{
    'name': 'Job Booking Service Sale Cost Depend',
    'version': '13.0.1.0.0',
    'category': 'Category',
    'author': 'JKM',
    'summary': 'Create job booking in service tab ',
    'website': 'http://www.seedorsoft.com',
    'description': """""",
    'depends': [
        'scs_freight', 'convert_quotation_to_job', 'jobbooking_custom_view','jobbooking_service_salecost_read'
    ],
    'data': [
        'views/freight.xml',
        # 'security/ir.model.access.csv',
        'wizard/jobbooking_invoice_wizard_view.xml',
        'wizard/jobbooking_bill_wizard_view.xml',
    ],
    'images': [
    ],
    'installable': True,
}
