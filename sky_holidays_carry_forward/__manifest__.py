# -*- encoding: utf-8 -*-
##############################################################################
#
#    Skyscend Business Solutions
#    Copyright (C) 2019 (http://www.skyscendbs.com)
#
##############################################################################
{
    'name': 'Carry Forward Holidays',
    'version': '13.0.0.1',
    'category': 'HR',
    'license': 'AGPL-3',
    'description': """
    This module is used to carry forward the leaves
    """,
    'author': 'Skyscend Business Solutions',
    'website': 'http://www.skyscendbs.com',
    'depends': ['hr_holidays'],
    'data': [
        'views/hr_holidays_view.xml',
        'data/ir_cron_data.xml'
    ],
    'images': ['static/description/main_screenshot.png'],
    'installable': True,
    'auto_install': False
}
