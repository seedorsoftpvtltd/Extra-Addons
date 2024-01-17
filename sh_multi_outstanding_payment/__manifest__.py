# -*- coding: utf-8 -*-

{
    "name": "Multiple Outstanding Payments",
    "author": "Softhealer Technologies",
    "website": "https://www.softhealer.com",
    "support": "support@softhealer.com",
    "license": "OPL-1",
    "category": "Accounting",
    "summary": "Manage Outstanding Payment, Multi Outstanding Payment,Payment Distribution, Payment Reconciliation,Outstanding Invoice Report,Bunch Outstanding Payment, Out Standing Payment,Outstanding Invoice,Outstanding Bills,Advance Payment Allocation Odoo",
    "description": """This module allows the outstanding payment of the partner (customer/vendor) for the invoice/bill from each outstanding payment. This module supports multiple outstanding payments for multiple payments of the same partner.""",
    "version": "13.0.2",
    "depends": ["sale_management", "account"],
    "data": [

        'security/ir.model.access.csv',
        'security/payment_security.xml',
        'wizard/invoice_wizard_multi_action_view.xml',
        'wizard/payment_wizard_multi_action.xml',
        'views/invoice_payment.xml',
        

    ],
    "images": ["static/description/background.png", ],
    "auto_install": False,
    "installable": True,
    "application": True,
    "price": 70,
    "currency": "EUR"
}
