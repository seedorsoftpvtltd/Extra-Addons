
# -*- coding: utf-8 -*-
{
    'name': 'Sales Contract Subscription and Recurring Invoice in odoo, Sales Contract Subscription in odoo and Recurring Invoice in odoo, Subscription management in odoo',
    'version': '13.0.0.2',
    'category': 'Website',
    'summary': """Sales Contract Subscription management in odoo, 
                Sales Contract Subscription in odoo and Recurring Invoice in odoo,
                Dashboard for manage product for product subscription, invoice management 
                and sale contract, contract management, create bulk invoice, customer invoice 
                management""",
    'description': """Sales Contract Subscription management in odoo, 
                Sales Contract Subscription in odoo and Recurring Invoice in odoo, 
                Dashboard for manage product for product subscription, invoice management and 
                sale contract, contract management, create bulk invoice, customer invoice management """,
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
    'price': 85.00,
    'currency': 'USD',
    'support': 'business@axistechnolabs.com',
    'author': 'Axis Technolabs',
    'website': 'http://www.axistechnolabs.com',
    'license': 'AGPL-3',
    'images': ['static/description/images/banner.jpg'],
    'application': True,
    'installable': True,
    'auto_install': False
}
