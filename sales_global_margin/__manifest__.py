# -*- coding: utf-8 -*-
# See LICENSE-DOC file for full copyright and licensing details
{
    'name': 'Sales Global Margin',
    'summary': 'Sales Global Margin',
    'version': '13.0.1.0.0',
    'category': 'Sales',
    'website': 'https://www.abrus.digital/',
    'description': """Sales Profit Margin.""",
    'images': ['static/description/banner.png'],
    'author': 'Abrus Digital',
    'company': 'Abrus Digital',
    'maintainer': 'Abrus Digital',
    'support':'info@abrusnetworks.com',
    'installable': True,
    'depends': [
        'base',
        'sale',
        'sale_management',
    ],
    'data': [
        'views/sale_order_views.xml',
    ],
    'license': 'AGPL-3',
    'installable': True,
    'auto_install': False,
    'application': False,
    'images': ['static/description/banner.png'],
}
