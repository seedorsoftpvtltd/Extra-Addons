# -*- coding: utf-8 -*-
# Part of Softhealer Technologies

{
    "name": "Period Lock - Community Edition",
    "author": "Softhealer Technologies",
    "website": "https://www.softhealer.com",
    "support": "support@softhealer.com",
    "category": "Accounting",
    "license": "OPL-1",
    "summary": "Periods Lock,Accounting Period Lock,Invoice Period Lock,Account Period Lock,Lock Period,Fiscal Year Lock,Account Lock To Date,Lock Periods for Employee,Lock Periods,Block Period,Lock Journal  Odoo",
    "description": """"Period Lock" module blocks respective journals like customer invoices, vendor bills. of selected journals so you can lock transactions for the given date range. We provide unlock option to revert the lock when required. It prevents users from posting journals on a date after the defined period.""",
    "version": "13.0.3",
    "depends": ["account"],
    "data": [
        'data/ir_sequence_data.xml',
        'security/ir.model.access.csv',
        'security/period_lock_security.xml',
        'views/period_lock.xml',

    ],


    "auto_install": False,
    "installable": True,
    "application": True,
    "images": ["static/description/background.png", ],
    "price": 50,
    "currency": "EUR"
}
