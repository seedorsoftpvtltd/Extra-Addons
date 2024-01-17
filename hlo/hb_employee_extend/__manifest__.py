{
        'name': 'Employee Additional Details',
        'version': '0.1',
        'category': 'Employee',
        'author': 'Herlin Breese',
        'summary': 'This Module contains Print option in employee.',
        'description': """
        
    """,
    'depends': [
        'base','hr','access_limit_records_number',
    ],

    'data': [
        'views/report_view.xml',
        'views/user.xml',
    ],

    'installable': True,
    'application': True,
}