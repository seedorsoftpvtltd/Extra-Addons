# -*- coding: utf-8 -*-
{
    'name': "Additional Salesperson",

    'summary': """
        Additional Salesperson on Contact, Sale Order, and Opportunity""",

    'description': """
        You can add additional salesperson on Contact, Sale Order, or Opportunity. 
        For example, You can to assign salesperson assistant to responsible besides the salesperson itself.
    """,

    'author': "Punia Raharja",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Contact','Sales'
    'version': '0.1',
    'images': ['static/description/thumbnail.png'],

    # any module necessary for this one to work correctly
    'depends': ['base','sale','crm'],

    # always loaded
    'data': [
        'views/views.xml',
    ],

}
