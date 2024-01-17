# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.
{
    "name" : "All In One Cost Center-Sales, Purchase, Account",
    "author" : "Softhealer Technologies",
    "website": "http://www.softhealer.com",
    "support": "support@softhealer.com",
    "category": "Extra Tools",
    "summary": "Different Cost Center,Manage Sales Cost Center, Purchase Cost Center, Sales Order Cost Center, Purchase Order Cost Center, Invoice Cost Center,Account Cost Center, Quote Cost Center, Request For Quotation, RFQ, Employee Expense Cost Center Odoo",       
    "description": """Cost center will provide manage different types of costs in sales, purchase, account, and expense.
 Cost Center Odoo, Management Of Different Cost Center Odoo

Manage Different Cost Center In Sales, Manage Different Cost Center In Purchase, Manage Different Cost Center In Sales Order, Manage Different Cost Center In Purchase Order, Manage Multiple Cost Center In Invoice,Manage Different Cost Center In Account Odoo.

 Manage Sales Cost Center, Manage Purchase Cost Center, Manage Sales Order Cost Center, Manage Purchase Order Cost Center, Manage Invoice Cost Center,Manage Account Cost Center Odoo.""",
    "version":"13.0.1",
    "depends" : [
                    "base",
                    "sale_management",
                    "purchase",
                    "stock",
                    "account",
                    "hr",
                    "hr_expense",
                ],
    'images': ['static/description/background.png', ],
    "live_test_url": "https://youtu.be/bhCenKETKF8",
    "application" : True,
    "data" : [
            "security/sh_cost_center_security.xml",
            "security/ir.model.access.csv",
            "views/sh_cost_center_view.xml",
            "views/sh_res_user_view.xml",
            "views/sh_sale_order_view.xml",
            "views/sh_purchase_order_view.xml",
            "views/sh_account_invoice_view.xml",
            "views/sh_hr_expense_view.xml",
            ],
    "auto_install":False,
    "installable" : True,
    "price": 30,
    "currency": "EUR"
}
