# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.
{
    "name": "Sale Order Free/Sample Product",
   
    "author": "Softhealer Technologies",
    
    "website": "https://www.softhealer.com",    
    
    "support": "support@softhealer.com",   
    
    "version": "13.0.1",
    
    "category": "Sales",
    
    "summary": " Sales order Sample Product App, Quotation Free Product Module, SO Free Product, Manage Free Sample Product, Sales Free Product Request, Sale Order Product Management, Quote Free Product, SO Sample Product Odoo",   

    "description": """
	Do you want to send a free product sample to your clients to try new products? This module used to define free products in the sale order, quotation & invoice. Free sample products help you to improve product selling. We provide configuration for free product tax on-off. You can provide a free product using a tickbox in a single click. Cheers!
 Sale Order Free Product Odoo. So Sample Product Odoo
 Sales order Sample Product, Quotation Free Sample Product Module, SO Free Product, Manage Free Sample Product, Sales Free Sample Product Request, Sale Order Product Management, Quote Free Product Odoo
 Sales order Sample Product App, Quotation Free Product Module, SO Free Product, Manage Free Sample Product, Sales Free Product Request, Sale Order Product Management, Quote Free Product, SO Sample Product Odoo

                """,
         
    "depends": ['sale_management','account','stock'],
    
    "data": [
        "views/res_config_setting_view.xml",
        "views/sale_order_view.xml",       
        "views/account_move.xml", 
    ],    
    "images": ["static/description/background.png",],
    "live_test_url": "https://youtu.be/ZHiuF-ksFHc",             
    "installable": True,
    "auto_install": False,
    "application": True,    
    
    "price": 50,
    "currency": "EUR" 
}
