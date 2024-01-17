{
    'name': 'Employee Absence Report',
    'category': 'Attendance',
    'version': '14.0.0.0',
    'description': """

""",
    'author': 'Fousia Banu A.R',
    'summary': 'This module provides absent report.',
    'website': 'https://www.browseinfo.in',
    'price': 29,
    'currency': "EUR",
    'depends': ['hr_attendance','project','hr'],

    'data': [

        'views/views.xml',
        'report/report.xml',
        'report/template.xml'
    ],
    'installable': True,
    'auto_install': False,
    'application': True,
    "live_test_url": 'https://youtu.be/DuMt9in_RaE',
    "images": ['static/description/Banner.png'],
}
