# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2015 DevIntelle Consulting Service Pvt.Ltd (<http://www.devintellecs.com>).
#
#    For Module Support : devintelle@gmail.com  or Skype : devintelle
#
##############################################################################

{
    'name': 'User Quick Setup',
    'version': '13.0.1.0',
    'sequence': 1,
    'category': 'Generic Modules/Human Resources',
    'description':
        """
        This Module add below functionality into odoo

        1.Create user with his/her contract, employee and leave allocation on a single click

Odoo user Quick setup 
Use Quick Setup 
Manage odoo user Quick Setup 
Odoo Manage User Quick Setup 
Create new user 
Odoo create new user 
Manage new user 
Odoo manage new user 
Quick user setup 
Odoo Quick user setup 
Manage Quick user setup 
Odoo manage Quick user setup 
Create new user Quickly 
Odoo create new user Quickly 
Add details of new Employee as a new user 
Odoo add details of new employee as a new user 
New user Quick Setup 
Odoo new user Quick setup 
Manage new user Quick setup 
Odoo manage new user Quick Setup 
New employee details 
Odoo new Employee details 
Manage new employee details 
Odoo manage new Employee details 


    """,
    'summary': 'Odoo app to setup User in one click (User, Employee, Contarct, Leave Allocatation) | user quick setup | Employee setup | user config | user employee creatation | employee from user',
    'depends': ['hr','hr_holidays','hr_contract','hr_payroll_community'],
    'data': [
        'security/ir.model.access.csv',
        'security/security.xml',
        'data/mail_template.xml',
        'views/user_quick_setup_view.xml',
    ],
    'demo': [],
    'test': [],
    'css': [],
    'qweb': [],
    'js': [],
    'images': ['images/main_screenshot.png'],
    'installable': True,
    'application': True,
    'auto_install': False,
    
    # author and support Details =============#
    'author': 'DevIntelle Consulting Service Pvt.Ltd',
    'website': 'http://www.devintellecs.com',    
    'maintainer': 'DevIntelle Consulting Service Pvt.Ltd', 
    'support': 'devintelle@gmail.com',
    'price':29.0,
    'currency':'EUR',
    'live_test_url':'https://www.youtube.com/watch?v=g-STrhMsrSc',
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
