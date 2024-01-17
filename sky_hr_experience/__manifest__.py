# -*- encoding: utf-8 -*-
##############################################################################
#
#    Skyscend Business Solutions
#    Copyright (C) 2019 (http://www.skyscendbs.com)
#
##############################################################################
{
    'name': 'Employee Experience',
    'version': '13.0.0.1',
    'category': 'HR',
    'license': 'AGPL-3',
    'description': """
    Experience calculation module of an employee
    """,
    'author': 'Skyscend Business Solutions',
    'website': 'http://www.skyscendbs.com',
    'depends': ['hr_skills'],
    'data': ['views/hr_skills_view.xml'],
    'images': ['static/description/main_screenshot.png'],
    'installable': True,
    'auto_install': False
}
