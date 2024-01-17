# -*- coding: utf-8 -*-
{
    'name': ' Fleet Template',
    'version': '13.0.1.0.0',
    'category': 'Fleet',
    'author': 'Herlin Breese J',
    'summary': 'Fleet Template',
    'website': 'http://www.seedorsoft.com',
    'description': """""",
    'depends': [
        'fleet',
        'fleet_vehicle_inspection',
        'fleet_operations',
        'purchase',
        'job_cost_estimate_customer',
    ],
    'data': [
        'views/template.xml',
        'views/checklist.xml',
        'views/assets.xml',
        'views/view.xml',
        'views/reminder.xml',
        'views/purchase.xml',
        'security/security.xml',
        'views/estimation.xml',
        'views/invoice.xml',

    ],
    'images': [
    ],
    'installable': True,
}
