# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name' : 'Basic Document',
    'version' : '13.0.1.1',
    'author' : 'Arivarasan',
    'summary': 'This module is used to manage Document',
    'description': """
Easily Maintain paperless document""",
    'category': 'Web',
    'live_test_url': 'https://youtu.be/2qp9DCG1alM',
    'website': 'https://linkedin.com/in/arivarasan-dk-67a58a195',
    'license': 'LGPL-3',
    'currency': 'USD',
    'images' : ['static/description/banner.jpg'],
    'depends' : ['base'],
    'data': [
        'security/groups.xml', 'security/ir.model.access.csv',
        'views/document.xml'
    ],
    'installable': True,
    'auto_install': False,
}
