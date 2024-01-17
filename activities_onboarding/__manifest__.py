# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name': 'Activities Onboarding',
    'version': '1.1',
    'summary': '',
    'sequence': 15,
    'description': """======================""",
    'category': 'Activities',
    'website': ' ',
    'images': ['images/accounts.jpeg', 'images/bank_statement.jpeg', 'images/cash_register.jpeg',
               'images/chart_of_accounts.jpeg', 'images/customer_invoice.jpeg', 'images/journal_entries.jpeg'],
    'depends': ['rt_activity_mgmt'],
    'data': [

        'views/activities_views.xml',
        'views/activities_onboarding.xml',
        'views/onboard_default_activities.xml'

    ],
    'demo': [

    ],
    'qweb': [

    ],
    'installable': True,
    'application': True,
    'auto_install': False,
    # 'post_init_hook': '_auto_install_l10n',
}
