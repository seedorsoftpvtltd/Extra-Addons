# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.

{
    "name" : "Link Customer to Lead/Pipeline in Odoo",
    "version" : "13.0.0.0",
    "category" : "Sales",
    'summary': 'User to link customer properly on lead/Pipeline when email address comes with <> sign link crm lead customer link customer in crm link crm customer incoming mail create customer from lead add follower lead auto add followers in lead auto set follower link',
    "description": """
    
    odoo link crm lead customer,
    odoo link customer in crm link crm customer from incoming mail create customer from lead,
    odoo add follower in lead auto add followers in lead auto set follower link on lead

    This odoo app helps user to link customer to crm lead created from incoming mail and 
    created partner will automatically added as lead followers.
    customer email with <> linked properly as customer.

    
    odoo link crm pipeline customer
    odoo link customer in crm link crm customer from incoming mail create customer from pipeline,
    odoo add follower in pipeline auto add followers in pipeline auto set follower link on pipeline

    This odoo app helps user to link customer to crm pipeline created from incoming mail and 
    created partner will automatically added as pipeline followers.

    This odoo app helps user to link customer to crm lead created from incoming mail and 
    created partner will automatically added as lead followers.
    When lead comes with incoming mail server then email doesn't link properly with customer 
    this modules helps to link customer properly on CRM lead/pipeline.
    """,
    "author": "BrowseInfo",
    "website" : "https://www.browseinfo.in",
    "price": 4.99,
    "currency": 'EUR',
    "depends" : ['base','sale_management','crm'],
    "data": [ ],
    'qweb': [],
    "auto_install": False,
    "installable": True,
    "live_test_url":'https://youtu.be/BcUG_CG8zh8',
    "images":["static/description/Banner.png"],
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
