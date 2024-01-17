# -*- coding: utf-8 -*-

{
    'name': 'Attach Medical Certificate for Sick Leave.',
    'version': '1.0',
    'author': 'Craftsync Technologies',
    'maintainer': 'Craftsync Technologies',
    'summary': 'Attach Medical certificate for sick Leave.',
    'description': """
Sick Leave:
=====================
You can attach documents like Medical certificate for Sick leave.""",
    'website': 'https://www.craftsync.com',
    'category': 'Human Resources',
    'depends': ['hr_holidays'],
    'data': [
        'views/hr_leave_type_view.xml',
        'views/hr_leave_view.xml',
    ],
    'license': 'OPL-1',
    'support':'info@craftsync.com',
    'demo': [],
    'images': ['static/description/main_screen.png'],
    'price': 4.99,
    'currency': 'EUR',
    'installable': True,
    'application': True,
    'auto_install': False,
}
