
# -*- coding: utf-8 -*-
{
    'name': 'Sales Contract Seperate Module ',
    'version': '13.0.0.2',
    'category': '',
    'summary': """""",
    'description': """Sales Contract Seperate Module""",
    'depends': [
        'product',
        'sale',
        'sale_management',
        'account',
        'analytic'
    ],
    'data': [
        'security/ir.model.access.csv',
        'data/mail_data.xml',
        'data/data.xml',
        'views/assets.xml',
        'views/product_template_view.xml',
        'views/sale_order_view.xml',
        'views/menu_dashboard.xml',
        'views/analytic_account_view.xml',
        'views/report.xml',
        'report/contract_report.xml',
        'wizard/invoice_contract.xml',
    ],
    'qweb': ["static/src/xml/dashboard.xml"],


    'author': 'JKM',
    'website': '',
    'license': 'AGPL-3',
    'images': ['static/description/images/banner.jpg'],
    'application': True,
    'installable': True,
    'auto_install': False
}
