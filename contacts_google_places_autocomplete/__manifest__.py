# -*- coding: utf-8 -*-
{
    'name': 'Contacts Google Places Autocomplete',
    'version': '13.0.1.0.0',
    'author': 'Yopi Angi',
    'license': 'AGPL-3',
    'maintainer': 'Yopi Angi<yopiangi@gmail.com>',
    'support': 'yopiangi@gmail.com',
    'category': 'Base',
    'sequence': 1000,
    'description': """
Contact Google Places Autocomplete
==================================

Use Google Address Form autocomplete to help you find address
""",
    'depends': [
        'base_geolocalize',
       # 'web_google_maps',
        'google_map_route'
    ],
    'website': 'https://github.com/gityopie/odoo-addons',
    'data': [
        'views/res_partner.xml',
    ],
    'demo': [],
    'installable': True
}
