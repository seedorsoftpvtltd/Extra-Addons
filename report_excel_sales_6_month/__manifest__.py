# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

# Copyright (C) 2019 GRIMMETTE,LLC <info@grimmette.com>

{
    'name': 'Product Sales by Customer for the last 6 Month Report (XLSX)',
    'version': '1.0.0',
    'category': 'Extra Tools',
    'summary': 'Product Sales by Customer for the last 6 Month Report (XLSX)',     
    'price': 0.00,
    'currency': 'EUR',
    "license": "OPL-1",     
    'description': """
Product Sales by Customer for the last 6 Month Report.
====================================
Product Sales by Customer for the last 6 Month in MS Excel format (XLSX)
Generate the Excel Report from a Template.
Report for Professional Reports Excel (XLSX, XLSM). 
    Odoo Report XLSX  Excel Report Excel Reports Accounting Reports Financial Report Financial Reports Stock Reports Inventory Reports \
    Dynamic Sale Analysis Reports Export Excel Export Project Reports Warehouse Reports Purchases Reports Marketing Reports Sales Reports \
    Report Designer Reports Designer Report Builder Reports Builder Product Report Customer Report POS Reports POS Report Analysis Report \
    BI Report BI Reports BI Business Intelligence Report Business Intelligence Reports BI Analytics BI Analytic Data Analysis
    """,
    'author': 'GRIMMETTE',
    'support': 'info@grimmette.com',
#     'live_test_url': "http://68.183.4.193:8069",
    'depends': ['delivery', 'account', 'sale'],
    'images': ['static/description/banner_rep.png'],
    'data': [
        'data/product_sales_for_the_last_6_month_xlsx.xml',
    ],
    'qweb': [
    ],
    'demo': [],
    'installable': True,
    'auto_install': False,
    "pre_init_hook": "pre_init_check",
}



