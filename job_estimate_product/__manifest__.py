# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name': 'Job Estimate Product',
    'version': '1.1',
    'summary': 'Job Estimate Product',
    'sequence': 15,
    'description': """Job Estimate Product,
 """,

    'depends': [
        'job_cost_estimate_customer',
        'estimate_sale_link',
        'sale',
        'project',
        'base',
        'account',

    ],
    'data': [
        'security/ir.model.access.csv',
        'views/job_estimate_product_view.xml',
        'views/sale_order_inherit_product.xml',

    ],
    'demo': [

    ],
    'qweb': [

    ],
    'installable': True,
    'application': True,
    'auto_install': False,

    'license': 'LGPL-3',
}
