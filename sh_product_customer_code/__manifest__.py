# -*- coding: utf-8 -*-
# Copyright (C) Softhealer Technologies.
{
    "name": "Product Customer Code",
    "author": "Softhealer Technologies",
    "license": "OPL-1",
    "website": "https://www.softhealer.com",
    "support": "support@softhealer.com",
    "category": "Sales",
    "summary": "Sale Product Code,Manage Partner Product Code,SO Client Product Code,Quotation Product Code, Customer Product Code,Sale Order Product Code,Customers Product Code,Products Code,Product Codes,Product Variant Code,Client Code,Sales Code Odoo",
    "description": """Our module is useful to manage specific product codes for customers. You can show the customer product code in the sale order line and quotation order line. After the selection of the product, the product code field fills by default. You can find products/product variants using product codes.""",
    "version": "13.0.6",
    'depends': ['sale_management'],
    'data': [
        'security/ir.model.access.csv',
        'security/customer_product_code_security.xml',
        'views/sh_product_customer_code.xml',
        'views/sh_product_customer_code_menu.xml',
        'views/inherit_sale_order_view.xml',
        'views/inherit_reports.xml',
    ],
    'images': ['static/description/background.png', ],
    "installable": True,
    "auto_install": False,
    "application": True,
    "price": 15,
    "currency": "EUR"
}
