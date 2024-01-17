# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.
{
    'name': 'Dynamic Product Labels',
    'author': 'Softhealer Technologies',
    'website': "https://www.softhealer.com",
    "support": "support@softhealer.com",
    'version': '13.0.3',
    "license": "OPL-1",
    'category': 'Productivity',
    'summary': "Product Custom Labels,Custom Product Label, Dynamic Product Label Template,Product Label Print,Dynamic Product Label Print,Dynamic Product Small Label,Dynamic Product Page Label,Print Dynamic Product Barcode Labels,Product Label With Fields Odoo",
    "description":  """Every company has its own label standard. so our module is helps to make dynamic product labels. We provide 3 predefine templates for product label. You can generate dynamic product label templates. You can add customizable extra fields in the product label. We provide label print option from the products, sales/quotation, purchase/request for quotation, inventory/incoming order/delivery order/internal transfer, invoice/bill/credit note/debit note. You can print the bulk quantity of labels. Cheers!""" ,
    'depends': [
        'sale_management',
        'purchase',
        'stock',
    ],
    'data': [
        'security/label_security.xml',
        'security/ir.model.access.csv',
        'views/sh_product_lable_dynamic_template_view.xml',
        'data/label_data.xml',
        'wizard/sh_product_lable_print.xml',
        'report/barcode_report.xml',
    ],
    "images": ["static/description/background.png"],
    "installable": True,
    "auto_install": False,
    "application": True,
    "price": "35",
    "currency": "EUR"
}
