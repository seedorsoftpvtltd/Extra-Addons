# -*- coding: utf-8 -*-

# Part of Probuse Consulting Service Pvt. Ltd. See LICENSE file for full copyright and licensing details.

{
    'name':'Print Lot BarCode Extended',
    'price': 99.0,
    'version':'1.3',
    'category': 'Warehouse',
    'currency': 'EUR',
    'summary': 'This module extend Print Lot BarCode Report',
    'license': 'Other proprietary',
    'description': """
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
            """,
    'author': 'Probuse Consulting Service Pvt. Ltd.',
    'website': 'http://www.probuse.com',
    # 'images': ['static/description/img1.png'],
    'images': ['static/description/image.png'],
    # 'live_test_url': 'https://youtu.be/X_vOl1UEQ3c',
    'live_test_url': 'http://probuseappdemo.com/probuse_apps/print_report_label_lot/127',#'https://youtu.be/3iegrTuOUpY',
    'depends': [
         'stock'
    ],
    'data':[
            'data/report_paperformat.xml',
            'views/report_label.xml',
    ],
    'installable': True,
    'support': 'contact@probuse.com',
    'application': False,
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
