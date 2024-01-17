# -*- coding: utf-8 -*-

# Part of Probuse Consulting Service Pvt Ltd. See LICENSE file for full copyright and licensing details.

{
    'name' : 'Administrator Users Password Change with Secure PIN',
    'version' : '1.1.4',
    'license': 'Other proprietary',
    'price': 59.0,
    'currency': 'EUR',
    'summary': 'Administrator Users Password Change with Secure PIN',
    'description': ''' 
Administrator Users Password Change with Secure PIN

 ''',
    'category': 'Tools',
    'depends' : [
        'base',
     ],
    'author': 'Probuse Consulting Service Pvt. Ltd.',
    'images': ['static/description/apc.jpg'],
    'support': 'contact@probuse.com',
    'website': 'www.probuse.com',
    'live_test_url' : 'http://probuseappdemo.com/probuse_apps/admin_password_change_control/32',#'https://youtu.be/L_lUpKv3kFM',    
    'data' : [
        'views/res_users_view.xml',
        'wizard/change_passwrod_user_view.xml',
    ],
    'installable': True,
    'application': False,
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
