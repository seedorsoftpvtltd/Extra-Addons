# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.
{
    "name": "Customer RFQ Portal Package",
    "author": "Softhealer Technologies",
    "website": "http://www.softhealer.com",
    "support": "support@softhealer.com",
    "category": "Sales",
    "summary": "Quotation Portal Package, Quotation Pack Portal, Bags Quotation at Portal, Customer Website portal, Website Portal for Box, Quotation Portal, Customer Portal, Client Portal, Vendor Portal, Portal Quotation  Odoo",
    "description": """This module helps customers to send a request for the quotation at the portal. They can create a quotation with product pack quantity. When customers put bags quantity it will default count total quantity based on bags quantity. Customers can add notes in the quotation at the portal.""",
    "version": "13.0.1",
    "depends": [
        "sh_customer_rfq_portal",
        "sh_uom_qty_pack",
    ],
    "data": [
        "views/portal_templates.xml",
    ],
    "images": ["static/description/background.png", ],
    "license": "OPL-1",
    "application": True,
    "auto_install": False,
    "installable": True,
    "price": "20",
    "currency": "EUR"
}
