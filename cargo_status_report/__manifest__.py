
{
        'name': 'Cargo Status Report',
        'version': '0.1',
        'category': 'Job Booking',
        'author': 'Fousia Banu A.R',
        'summary': 'Cargo Status Report',
        'description': """Cargo Status Report""",
        'depends': [
            'job_booking_sub_job',
            'scs_freight',
        ],

    'data': [
        'wizard/cargo_report.xml',
        'views/views.xml',
        'report/report.xml'
    ],

    'installable': True,
    'application': True,
}