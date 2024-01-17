{
    'name' : 'Select all Button for Bill & Voice Wizard in Job Booking',
    'version' : '1.0.0',
    'summary': '',
    'category': '',
    'depends' : ['jobbooking_service_salecost_read','jobbooking_service_salecost_read_depend'],
    'data': [
        'wizard/jobbooking_invoice_bill.xml',
        'wizard/jobbooking_bill_view.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
    'license': 'LGPL-3',
}
