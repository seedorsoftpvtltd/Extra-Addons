# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.
{
    "name" : "Supplier Statement Fields Additional",
    "author" : "Seedorsoft",
    "website": "",
    "support": "",
    "category": "Extra Tools",
    "summary": "Added Additional fields for supplier statement",
    "description": """Added Additional fields for supplier statement""",
    "version":"13.0.2",
    "depends" : [
                    "contacts",
                    "account_statement", "supplier_statement_fields", "account_invoice_supplier_ref_unique", "account"
                ],
    "application" : True,
    "data" : [

            "views/supplier_fields_views.xml",
            ],
    "auto_install":False,
    "installable" : True,
    "price": 25,
    "currency": "EUR" ,
    "images": ['static/description/background.png', ],
    "live_test_url": "https://www.youtube.com/watch?v=KrX_zvlWRdI&feature=youtu.be",
}
