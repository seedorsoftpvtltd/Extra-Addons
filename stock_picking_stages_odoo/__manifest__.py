# -*- coding: utf-8 -*-

# Part of Probuse Consulting Service Pvt. Ltd. See LICENSE file for full copyright and licensing details.
{
    'name': 'Stock Picking Stages / Shipment Stages',
    'version': '2.1.2',
    'price': 9.0,
    'currency': 'EUR',
    'license': 'Other proprietary',
    'depends': [
        'stock',
    ],
    'category': 'Operations/Inventory',
    'summary':  """This app allows you to manage transfer stages.""",
    'description': """
       This app allows you to manage transfer stages.

    """,
    
    'author': 'Probuse Consulting Service Pvt. Ltd.',
    'website': 'www.probuse.com',
    'images': ['static/description/ss553.jpg'],
    'live_test_url': 'http://probuseappdemo.com/probuse_apps/stock_picking_stages_odoo/447',#'https://youtu.be/nPhL6G56oqQ',
    'data': [
        'security/ir.model.access.csv',
        'views/stock_stage_view.xml',
        'views/stock_view.xml',
    ],
    'installable': True,
    'application': False,
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
