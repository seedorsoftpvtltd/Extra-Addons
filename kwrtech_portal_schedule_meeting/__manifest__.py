# -*- coding: utf-8 -*-

{
    'name': 'Schedule Meetings from Portal',
    'version': '13.0.0',
    'author': 'KathiawarTech',
    'website': 'http://kathiawartech.in',
    'currency': 'EUR',
    'depends': ['calendar', 'hr', 'website_form'],
    'summary': "Allow your customers to schedule meetings with you after checking your availability in their time zone.",
    'category': 'Productivity/Calendar',
    'data': [
        'data/website_calendar_data.xml',
        'data/website_data.xml',
        'views/templates.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
    'images': [
        'static/description/cover.png',
    ],
    'license': 'LGPL-3',
}
