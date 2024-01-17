# -*- coding: utf-8 -*-
{
    'name': 'CRM Maps',
    'version': '13.0.1.0.0',
    'author': 'Yopi Angi',
    'license': 'AGPL-3',
    'maintainer': 'Yopi Angi<yopiangi@gmail.com>',
    'support': 'yopiangi@gmail.com',
    'category': 'Sales/CRM',
    'description': """
CRM Maps
========

Added google_map view on your pipeline
""",
    'depends': ['crm',
                #'web_google_maps',
                'google_map_route'],
    'website': '',
    'data': [
        'views/crm_lead.xml',
        'views/res_partner.xml',
    ],
    'demo': [],
    'installable': True
}
