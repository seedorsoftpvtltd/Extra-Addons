# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name': 'ASN Onboarding',
    'version': '1.1',
    'summary': '',
    'sequence': 15,
    'description': """======================""",
    'category': 'Warehouse',
    'website': ' ',
    'images': ['images/accounts.jpeg', 'images/bank_statement.jpeg', 'images/cash_register.jpeg',
               'images/chart_of_accounts.jpeg', 'images/customer_invoice.jpeg', 'images/journal_entries.jpeg'],
    'depends': ['warehouse','base','contacts'],
    'data': [

        'views/asn_views.xml',
        'views/asn_onboarding.xml',
        'views/onboard_default_asn.xml'

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
