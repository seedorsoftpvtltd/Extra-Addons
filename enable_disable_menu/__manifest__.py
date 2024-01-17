# -*- coding: utf-8 -*-

# Klystron Global LLC
# Copyright (C) Klystron Global LLC
# All Rights Reserved
# https://www.klystronglobal.com/


{
    'name': "Enable/Disable",
    'summary': """
       This module allow to  Enable/Disable Menu. Both API and Manual Options are available""",
    'description': """
        This module allow to  Enable/Disable Menu. Both API and Manual Options are available""",
    'author': 'Fousia Banu A.R',
    'maintainer':'',
    'website': "https://www.seedors.com/",
    'images': ["static/description/banner.png"],
    'category': 'Extra Rights',
    'version': "13.0.1.0.0",
    'license': 'AGPL-3',
    'depends': [
        'base'
    ],
    'data': ['views/views.xml',
             'security/security.xml',
             'security/ir.model.access.csv',
             'views/menu.xml'
             ],
}