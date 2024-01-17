# -*- coding: utf-8 -*-

# Part of Probuse Consulting Service Pvt. Ltd. See LICENSE file for full copyright and licensing details.

{
    'name':'Picking Lot/Serial Number Barcode Print',
    'version':'1.1.3',
    'category': 'Warehouse',
    'price': 50.0,
    'depends': ['print_report_label_lot'],
    'currency': 'EUR',
    'summary': 'This module allow you to print barcode of all lots assigned to picking/move lines.',
    'license': 'Other proprietary',
    'description': """
Print Report Label Lot. This module allow print product barcode and company information on lot barcode.
Report Label Lot
Product Barcode
Product Quantity
product Uom
print lot label
Print Report Label Lot. This module allow print product barcode and company information on lot barcode.
Report Label Lot
Product Barcode
Product Quantity
Print Report Label Lot
barcode print
print barcode
print barcode
ean13
barcode lable print
barcode print lot
lot print
print lot number
print lot barcode
print barcode lot
barcode printing
lot number
lot printer
printer lot number
printer barcode
barcode printer
lot print report
pdf lot barcode
barcode pdf report
barcode pdf
printer barcode
product barcode print
print product barcode
Lot/Serial Number
lot print
serial number print
print serial number barcode
serial number barcode
picking barcode
picking lot barcode
picking lot
lot number
print lot
picking lot barcode
picking lot number
picking lot
lot barcode print
delivery barcode
incoming shipment barcode
delivery order barcode
            """,
    'author': "Probuse Consulting Service Pvt. Ltd.",
    'website': "http://www.probuse.com",
    # 'live_test_url': 'https://youtu.be/48SRwztQTT4',
    'live_test_url': 'https://probuseappdemo.com/probuse_apps/print_picking_lot_label/860',#'https://youtu.be/m40kSJKJAIE',
    # 'images': ['static/description/img1.png'],
    'images': ['static/description/image.png'],
    'support': 'contact@probuse.com',
    'data':[
            'wizard/picking_lot_print_wizard_view.xml',
    ],
    'installable': True,
    'application': False,
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
