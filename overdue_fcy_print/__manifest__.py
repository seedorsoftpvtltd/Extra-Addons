{
    'name': 'Print Option for FCY and base currency in overdue',
    'version': '13.0.1.0.0',
    'summary': 'Print Option for FCY and base currency in overdue',
    'description': """
        Print Option for FCY and base currency in overdue.
        """,
    'category': 'Accounting',
    'author': "Fousia Banu A R",
    'company': 'Seedorsoft Private Limited',
    'maintainer': 'Seedorsoft Private Limited',
    'website': "https://www.seedorsoft.com",
    'depends': [
        'bi_payment_overdue_finance'
    ],

    'data': [

        'views/overdue.xml',
        'views/template.xml',

    ],
    'demo': ['data/hr_overtime_demo.xml'],
    'images': ['static/description/banner.png'],
    'license': 'AGPL-3',
    'installable': True,
    'auto_install': False,
    'application': False,
}