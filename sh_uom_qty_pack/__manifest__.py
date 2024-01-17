# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.
{
    "name": "Product Quantity Pack",
   
    "author": "Softhealer Technologies",
    
    "website": "https://www.softhealer.com",    
    
    "support": "support@softhealer.com",   
    
    "version": "13.0.2",
    
    "category": "Sales",
    
    "summary": " Customize Bundle Product, Manage Product Package App, Product Quantity In Bags,Bunch Product Module, Combo Products Quantity, Mass Product Quantity, Multiple Product Quantity, Product Qty Pack Odoo",   

    "description": """
	This module will allow you to assign the product quantity in bags and then when you put bags quantity it will default count total quantity based on bags quantity in sale, purchase, inventory & invoicing. If you are selling some products in bulk quantity in the package, pack, bags. For example, a 25kg Sugar bag, so our module useful to add that bag quantity in line and it will auto calculate the final quantity. i,e 5 bags of 25kg sugar bag than auto calculate 125kg in the quantity field.
 Product Quantity Pack Odoo, Bundle Product Quantity Odoo
 Customize Bundle Product Module, Manage Product Package, Product Quantity In Bags, Put Products In Bunch, Combo Products Quantity, Mass Product Quantity, Multiple Product Quantity, Product Qty Pack Odoo
 Customize Bundle Product, Manage Product Package App, Product Quantity In Bags,Bunch Product Module, Combo Products Quantity, Mass Product Quantity, Multiple Product Quantity, Product Qty Pack, Products Package, Product Bags, Product Bunch, Product Quantity Bundle Odoo

                """,
         
    "depends": ['base','sale_management','purchase','account','stock'],
    
    "data": [
        'views/sh_product_template_custom.xml',
        'views/sh_sale_order_view.xml',
        'report/sh_report_sale_order.xml',
        'views/sh_purchase_order_view.xml',
        'report/sh_report_purchase_order.xml',
        'views/sh_account_invoice_view.xml',
        'report/sh_report_account_invoice_view.xml',
        'views/sh_stock_picking_view.xml',
        'report/sh_report_stock_picking_operation.xml',
        'report/sh_report_deliveryslip.xml',
        'views/res_config_setting.xml'
    ],    
    "images": ["static/description/background.png",],
    "live_test_url": "https://youtu.be/fkB3SEtFzrk",
                 
    "installable": True,
    "auto_install": False,
    "application": True,   
    "price": 50,
    "currency": "EUR" 	
}
