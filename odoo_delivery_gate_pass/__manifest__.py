# -*- coding: utf-8 -*-
{
    'name': "Delivery Gate Pass",
    'version': '1.1.2',
    'price': 9.0,
    'currency': 'EUR',
    'license': 'Other proprietary',
    'category': 'Operations/Inventory',
    'summary': """Delivery Gate Pass from Warehouse in Odoo""",
    'description': """
Odoo Delivery Gate Pass.
company visitor
visitor process 
visitor pass
visitor report
company visit
odoo visitor
visit company
pass print
    """,
    'author': "Probuse Consulting Service Pvt. Ltd.",
    'website': 'www.probuse.com',
    'images': ['static/description/gate_pass.jpg'],
    'live_test_url': 'https://probuseappdemo.com/probuse_apps/odoo_delivery_gate_pass/825',#'https://youtu.be/YydeL3m3IcQ',
    'depends': [
        'visitor_gate_pass',
        'stock',
    ],

    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'wizard/gate_pass_wizard_view.xml',
        'views/stock_picking_view.xml',
        'views/visitor_gate_pass_view.xml',
        'report/stock_gate_visitor_report.xml',

    ],
    'installable': True,
    'application': False,
}
