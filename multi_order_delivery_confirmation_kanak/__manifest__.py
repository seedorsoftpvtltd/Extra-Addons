# -*- coding: utf-8 -*-
#################################################################################
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
#################################################################################
{
    'name': 'Delivery Order Multi Confirmation',
    'version': '1.0',
    'summary': 'This module is used to confirming multiple Delivery orders at the same time.',
    'description': """
    This module is used to confirming multiple Delivery orders at the same time.'
    """,
    'category': 'Inventory',
    'license': 'OPL-1',
    'author': 'Kanak Infosystems LLP.',
    'website': 'https://www.kanakinfosystems.com',
    'depends': ['base', 'sale', 'purchase', 'stock'],
    'data': [
        'data/data.xml',
    ],
    'images': ['static/description/banner.jpg'],
    'sequence': 1,
    'installable': True,
    'price': 0,
    'currency': 'EUR',
}
