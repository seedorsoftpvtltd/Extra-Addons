# -*- coding: utf-8 -*-
###############################################################################
# Author      : Kanak Infosystems LLP. (<https://www.kanakinfosystems.com/>)
# Copyright(c): 2012-Present Kanak Infosystems LLP.
# All Rights Reserved.
#
#
# This program is copyright property of the author mentioned above.
# You can`t redistribute it and/or modify it.
#
#
# You should have received a copy of the License along with this program.
# If not, see <https://www.kanakinfosystems.com/license>
###############################################################################


{
    'name': "Default Terms & Conditions (Stock).",
    'version': '1.0',
    'summary': 'Set Default Terms & Conditions for Stock.',
    'description': """
This module is used to set Default Terms & Conditions
on your Stock Picking(Delivery Orders) and report.
=================
    """,
    'license': 'OPL-1',
    'author': "Kanak Infosystems LLP.",
    'website': "https://www.kanakinfosystems.com",
    'category': 'Operations/Inventory',
    'depends': ['base', 'stock'],
    'images': ['static/description/banner.jpg'],
    'data': [
        'views/stock_view.xml',
    ],
    'sequence': 1,
    'installable': True,
    'application': True,
}
