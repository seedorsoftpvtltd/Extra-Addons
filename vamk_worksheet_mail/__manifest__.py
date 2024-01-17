# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name' : 'vamk worksheet mail',
    'version' : '1.1',
    'summary': 'vamk worksheet mail',
    'sequence': 1,
    'description': """vamk worksheet mail""",
    'category': 'MRP',
    'author': 'Banibro',
    'website': 'https://www.banibro.com',
    'license': 'LGPL-3',
    'support': 'info@banibro.com',
    'depends' : ['mrp','vamk_work_sheet'],
    'data': ['views/vamk_worksheet_mail.xml','views/vamk_templates.xml','views/vamk_report_views.xml'],
    'installable': True,
    'application': True,
    'auto_install': False,
    'images': [],
}



