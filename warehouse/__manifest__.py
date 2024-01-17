# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'warehouse',
    'version': '1.2',
    'category': 'Operations/warehouse',
    'sequence': 60,
    'summary': 'Warehouse Booking, tenders and agreements',
    'description': "",
    'depends': ['account'],
    'data': [
        'security/warehouse_security.xml',
        'security/ir.model.access.csv',
        #'views/account_move_views.xml',
        'data/warehouse_data.xml',
        'report/warehouse_reports.xml',
        'views/warehouse_views.xml',
       # 'views/res_config_settings_views.xml',
        #'views/product_views.xml',
       # 'views/res_partner_views.xml',
        'views/warehouse_template.xml',
        # 'report/warehouse_bill_views.xml',
        # 'report/warehouse_report_views.xml',
         'data/mail_template_data.xml',
        'views/portal_templates.xml',
        'report/warehouse_order_templates.xml',
        'report/warehouse_quotation_templates.xml',
        'views/warehouse_tag.xml',
        'views/add_multiprod.xml'

    ],
    'demo': [
        'data/warehouse_demo.xml',
    ],
    'installable': True,
    'auto_install': False,
    'application': True,
}
