# -*- coding: utf-8 -*-
{
    'name': 'Transport Management for Purchase Order and Incoming Shipment',
    'price': 59.00,
    'category': 'Warehouse',
    'summary': 'Manage Transport information of your incoming shipments and Routes of Shipments.',
    'author': 'Probuse Consulting Service Pvt. Ltd.',
    'license': 'Other proprietary',
    'website': 'https://www.probuse.com',
    'live_test_url': 'https://probuseappdemo.com/probuse_apps/odoo_transport_management_purchase/1055',#'https://youtu.be/i4CR06_sqt0',
    'currency': 'EUR',
    'version': '2.1.2',
    'description':"""
Transport Management. This module allow create picking information 
Odoo Transport Management
Transport Management for Purchase Order and Incoming Shipment
Odoo Transport
Transport Management
""",
    'images': ['static/description/transport_image.jpg'],
    'depends': [
        'odoo_transport_management',
        'purchase',
    ],

    'data': [
        'views/purchase_view.xml',
        'views/picking_transport_info_view.xml',
        'views/stock_picking_view.xml',
        'report/picking_transport_info_report.xml',
    ],
    'installable': True,
    'auto_install': False,
}
