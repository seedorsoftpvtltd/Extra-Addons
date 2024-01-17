# -*- coding: utf-8 -*-
##############################################################################
##############################################################################
{
        'name': 'Stock Transfer Checklist',
        'version': '0.1',
        'category': 'purchase',
        'license': 'OPL-1',
        'price': 79.00,
        'images': ['static/description/check0010.PNG'],
        'author': 'oranga',
        'currency': 'EUR',
        'summary': 'Purchase order Checklist, Checklist Template, Checklist Points',
        'description': """
       Delivery Order Checklist
       Delivery Checklist
       Purchase Order Checklist
       Purchase Checklist
       internal transfer Checklist
    """,
    'depends': [
        'base',
        'stock',
    ],

    'data': [
        'security/ir.model.access.csv',
        'views/report_checklist_view.xml',
        'views/inventory_checklist_view.xml',
    ],

    'installable': True,
    'application': True,
}