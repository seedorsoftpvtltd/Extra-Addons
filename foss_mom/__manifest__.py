# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name': "Minutes of Meeting",
    'price': 130.0,
    'currency': 'USD',
    'version': '13.0.0.0.0',
    'live_test_url': 'http://165.227.3.14:8073/',
    'summary': """ Minutes of Meeting """,
    'author': 'FOSS INFOTECH PVT LTD',
    'license': 'Other proprietary',
    'category': 'Extra Tools',
    'website': "http://www.fossinfotech.com",
    'description': """
    """,
    'depends': ['base','calendar','project'],
    'data': [
        'security/ir.model.access.csv',
        'views/mom_views.xml',
        'report/layout.xml',
        'report/reports.xml',
        'report/mom_report_template.xml',
        'data/foss_mom_email_template.xml',
    ],
    'images': [
        'static/description/banner.png',
        'static/description/icon.png',
        'static/description/index.html',
    ],
    'installable': True,
    'auto_install': False,
    'application': True,
}