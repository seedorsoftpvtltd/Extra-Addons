# -*- coding: utf-8 -*-

# Part of Probuse Consulting Service Pvt. Ltd. See LICENSE file for full copyright and licensing details.
{
    'name': 'Invoice / Bill / Journal Entries Stages',
    'version': '2.1.2',
    'price': 49.0,
    'currency': 'EUR',
    'license': 'Other proprietary',
    'depends': [
        'account',
    ],
    'category': 'Accounting/Accounting',
    'summary':  """Manage more configurable stages on invoice, bill and journal entry.""",
    'description': """
This app allows you to manage account invoice stages.
account stages
invoice stage
invoice stages
customer invoice stage
vendor bill stages
journal entry stages
    """,
    
    'author': 'Probuse Consulting Service Pvt. Ltd.',
    'website': 'www.probuse.com',
    'images': ['static/description/asimg.jpg'],
    'live_test_url': 'http://probuseappdemo.com/probuse_apps/account_invoice_bill_stages/17',#'https://youtu.be/cIwwVfr3tTk',
    'data': [
        'security/ir.model.access.csv',
        'views/account_stage_view.xml',
        'views/account_move_view.xml',
    ],
    'installable': True,
    'application': False,
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
