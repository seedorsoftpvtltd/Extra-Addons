# -*- coding: utf-8 -*-
#################################################################################
# Author      : Nexus Incorporation (<http://www.nexusgurus.com>)
# Copyright(c): 2021-Present Nexus Incorporation
# All Rights Reserved.
#
#
#
# This program is copyright property of the author mentioned above.
# You can`t redistribute it and/or modify it.
#
#
# You should have received a copy of the License along with this program.
# If not, see <http://www.nexusgurus.com/license/>
#################################################################################

{
    'name': 'Chatter Paste',
    'summary': """
        Paste images and drop files into the chatter and upload them directly
    """,
    'version': '13.0.1.0.0',
    'category': 'Web',
    'author': 'Nexus Incorporation',
    'website': 'http://www.nexusgurus.com',
    'license': 'OPL-1',
    'depends': [
        'mail',
        'base',
        'web'
    ],
    "price": 35,
    "currency": 'EUR',
    'data': [
        'templates/assets.xml'
    ],
    'installable': True,
    'application': False,
    "images": ["static/description/Banner.png"],
}
