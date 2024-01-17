# -*- coding: utf-8 -*-

{
    'name': 'ofd types',
    'author': "",
    'version': '13.0.1.1',
    'live_test_url': '',
    'summary': 'ofd types',
    'description': """

    """,
    'depends': ['scs_freight', 'hb_freight_extend', 'sale', 'jobbooking_custom_view','convert_quotation_to_job'],
    "license": "OPL-1",
    'data': [
        'security/ir.model.access.csv',
        'views/ofsd.xml',
        'views/menu.xml',
    ],
    'qweb': [],
    'demo': [],
    'installable': True,
    'auto_install': False,
    'category': 'freight',
}
