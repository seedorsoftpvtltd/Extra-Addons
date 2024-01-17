{
    'name': 'Check Availability Validation',
    'version': '13.0.1.0.0',
    'summary': 'This module checks if a move line has reserved quantity or not if reserved quanity is 0 or less than demand '
               'then it shows Validatio popup while clicking Check Availability Button',
    'description': """
       This module checks if a move line has reserved quantity or not if reserved quanity is 0 or less than demand '
               'then it shows Validatio popup while clicking Check Availability Button.
        """,
    'category': 'Inventory',
    'author': "Fousia Banu A R",
    'company': 'Seedorsoft Private Limited',
    'maintainer': 'Seedorsoft Private Limited',
    'website': "https://www.seedorsoft.com",
    'depends': [
        'stock'
    ],

    'data': [


    ],
    'demo': ['data/hr_overtime_demo.xml'],
    'images': ['static/description/banner.png'],
    'license': 'AGPL-3',
    'installable': True,
    'auto_install': False,
    'application': False,
}