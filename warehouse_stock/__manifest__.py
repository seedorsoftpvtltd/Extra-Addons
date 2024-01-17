# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'warehouse Stock',
    'version': '1.2',
    'category': 'Operations/warehouse',
    'sequence': 60,
    'summary': 'warehouse Orders, Receipts, Vendor Bills for Stock',
    'description': "",
    'depends': ['stock_account', 'warehouse','sh_secondary_unit'],
    'data': [
        'security/ir.model.access.csv',
        'data/warehouse_stock_data.xml',
        'data/mail_data.xml',
        'views/warehouse_views.xml',
        'views/stock_views.xml',
        'views/stock_rule_views.xml',
        #'views/res_config_settings_views.xml',
        'views/stock_production_lot_views.xml',
       # 'report/warehouse_report_views.xml',
       # 'report/warehouse_report_templates.xml',
        'report/report_stock_rule.xml',
    ],
    'demo': [
        'data/warehouse_stock_demo.xml',
    ],
    'installable': True,
    'auto_install': True,
    'post_init_hook': '_create_buy_rules',
}
