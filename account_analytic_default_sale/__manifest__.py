# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing
# details.

{
    'name':'Account Analytic Defaults for Sale.',
    'version':'13.0.0.1',
    'category':'Accounting/Accounting',
    'author':'Osis',
    'website':"https://osis.dz",
    'license':'OPL-1',
    'description':"""
Set default values for your analytic accounts.
==================================================================

Allows to automatically select analytic accounts based on Product
    """,
    'depends':[
        'sale', 'account_analytic_default'
    ],
    'data':[
        'views/sale_order_views.xml',
    ],
    'qweb':[],
    'installable':True,
    'application':False
}