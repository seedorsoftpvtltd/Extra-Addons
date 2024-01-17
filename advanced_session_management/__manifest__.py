# -*- coding: utf-8 -*-
#################################################################################
# Author      : Ashish Hirpara (<www.ashish-hirpara.com>)
# Copyright(c): 2021
# All Rights Reserved.
#
# This module is copyright property of the author mentioned above.
# You can`t redistribute it and/or modify it.
#
#################################################################################
{
    'name': 'Advanced User Audit | User Activity Audit | Login Notification',
    'version': '13.0.0.0',
    'summary': 'User Activity Log, User Activity Audit,  Session Management, Record Log, Activity Traces, Login Notification, User Activity Record, Record History, Login History, Login location, Login IP',
    'sequence': 6,
    'author': 'Ashish Hirpara',
    'license': 'OPL-1',
    'website': 'https://ashish-hirpara.com/r/odoo',
    'description':"""
        Advanced User Audit makes it-
	Easy to track all the activities performed by the internal users in odoo. 
	East to trace which activity performed by which user on which login session.
	Easy to audit the user activities in odoo.
        Easy to track all the sessions started by internal users.
        Easy to track the operations like create, update and delete performed in individual sessions.
        User can see the information of any session like: IP, date, device, location, os & browser.
        User will get instant email notification if any new sessions starts to alarm the users
    """,
    "price": "149.99",
    "currency": "USD",
    'depends':['mail'],
    'data':[
        'security/ir.model.access.csv',
        'security/res_groups.xml',
        'data/cron.xml',
        'data/email_template.xml',
        'views/res_config_settings_view.xml',
        'views/login_log_view.xml',
        'views/edit_value_view.xml',
        'views/activity_log_view.xml',
        'views/res_user_view.xml',
        'views/assets.xml',
    ],
    'external_dependencies': {
        'python': ['user_agents']
    },
    'application': True,
    'installable': True,
    'auto_install': False,
    'post_init_hook': 'post_init_hook',
    'uninstall_hook': 'uninstall_hook',
    'live_test_url': 'https://youtu.be/rgW9rnD0sJM',
    'images': ['static/description/banner.gif'],
}
