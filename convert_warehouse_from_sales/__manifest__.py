# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.

{
    'name' : "Convert warehouse order from Sales Order",
    'version' : "13.0.0.1",
    'category' : "warehouses",
    'summary': 'This apps helps to Covert warehouse order from Sales Order',
    'description' : """
        Convert warehouse from Sales Order
        Convert warehouses from Sales Order
        Convert warehouse order from Sales Order
        Convert warehouses order from Sales Order

        create warehouse from Sales Order
        create warehouses from Sales Order
        create warehouse order from Sales Order
        create warehouses order from Sales Order


        Add warehouse from Sales Order
        Add warehouses from Sales Order
        ADD warehouse order from Sales Order
        ADD warehouses order from Sales Order

     """,
    'author' : "Herlin Breese",

    'depends'  : [ 'base','sale_management','warehouse'],
    'data'     : [  'security/ir.model.access.csv',
                    'wizard/warehouse_order_wizard_view.xml',
                    'views/inherit_sale_order_view.xml',
            ],      
    'installable' : True,
    'application' :  False,

}
