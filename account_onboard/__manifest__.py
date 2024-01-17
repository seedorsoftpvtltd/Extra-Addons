# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name' : 'Account Onboard',
    'version' : '1.1',
    'summary': 'Account onboard issue solved',
    'sequence': 15,
    'description': """account onboard """,
    'category': 'Account',
    'depends' : ['account'],
    'data': [
        'wizard/setup_wizards_view.xml',
        #'views/account_dashboard_setup_bar.xml',        
        #'views/account_journal_dashboard_view.xml',
        'views/account_onboarding_templates.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}
