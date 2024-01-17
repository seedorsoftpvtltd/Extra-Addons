# -*- coding: utf-8 -*-
#################################################################################
# Author      : Acespritech Solutions Pvt. Ltd. (<www.acespritech.com>)
# Copyright(c): 2012-Present Acespritech Solutions Pvt. Ltd.
# All Rights Reserved.
#
# This program is copyright property of the author mentioned above.
# You can`t redistribute it and/or modify it.
#
#################################################################################
{
    'name': 'Product UOM Quantity',
    'version' : '1.0',
    'category' : 'Inventory',
    'summary': """Product UOM Quantity """,
    'description': """Product UOM Quantity """,
    'author': 'Acespritech Solutions Pvt. Ltd.',
    'website': 'http://www.acespritech.com',
    'depends': ['base', 'product', 'stock'],
    'data': [
        # 'security/ir.model.access.csv',
         'views/product_view.xml'
    ],
    'price': 15,
    'currency': 'EUR',
    'images': ['static/description/main_screenshot.png'],
    'installable': True,
    'auto_install': False,
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
