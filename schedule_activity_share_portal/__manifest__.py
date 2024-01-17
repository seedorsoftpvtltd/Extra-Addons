# -*- coding: utf-8 -*-

# Part of Probuse Consulting Service Pvt. Ltd. See LICENSE file for full copyright and licensing details.

{
    'name': "Portal Schedule Activities for External Agents",
    'version': '1.0.2',
    'license': 'Other proprietary',
    'price': 29.0,
    'currency': 'EUR',
    'summary':  """Schedule Activity Share to External Agents / Portal Users / Customers""",
    'description': """
This app allows your external agents / portal user / contacts 
to view activities on my account portal of your website and 
send a message using portal login as shown in below screenshots.
    """,
    'author': "Probuse Consulting Service Pvt. Ltd.",
    'website': "http://www.probuse.com",
    'support': 'contact@probuse.com',
    'images': ['static/description/image.png'],
    'live_test_url':'http://probuseappdemo.com/probuse_apps/schedule_activity_share_portal/68',# 'https://youtu.be/92KcxUCBpd4',
    'category': 'Discuss',
    'depends': ['schedule_activity_global','portal'],
    'data': [
            'security/ir.model.access.csv',
            'views/activity_message_view.xml',
            'views/mail_activity_view.xml',
            'views/activity_template.xml',
            'views/activity_portal_templates.xml',
            ],
    'installable': True,
    'application': False,
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
