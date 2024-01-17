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
    'name': 'Expense Reimburse by Employee Payslip',
    'version': '13.0.1.0',
    'sequence': 1,
    'category': 'Generic Modules/Human Resources',
    'description':
        """
        Odoo app will help to Reimburse hr expense by employee payslip 
        
        Pay employee expense by employee payslip monthly by salary 
Expense Reimburse by Employee Payslip
Odoo Expense Reimburse by Employee Payslip
Employee expense reimburse 
Odoo employee expense reimburse 
Manage employee expense 
Odoo manage emploee expense 
manage employee reimburse expense 
Odoo manage employee reimburse expense 
Manage employee monthly expense 
Odoo manage employee monthly expense 
Reimburse Employee's expense into his/her salary Payslip
Odoo Reimburse Employee's expense into his/her salary Payslip
Linking employee's payslip with with employee's expenses while confirming Payslip
Odoo Linking employee's payslip with with employee's expenses while confirming Payslip
Employee expense allowance 
Odoo employee expense allowance 
Manage employee expense allowance 
Odoo manage employee expense allowance 
Employee payslip 
Odoo employee payslip 
Odoo manage employee payslip 
Manage payslip
        
    """,
    'summary': 'Odoo app Reimburse hr expense by employee payslip, Expense Reimburse by Employee Payslip,Pay employee expense by employee payslip monthly,Employee expense reimburse,employee payslip with employee expense, Employee expense allowance',
    'depends': ['hr_expense', 'hr_payroll_community'],
    'data': [
        'data/salary_rul.xml',
        'views/hr_payslip_view.xml',
        'views/hr_expense_view.xml',
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
    'price':35.0,
    'currency':'EUR',
    'live_test_url':'https://youtu.be/cLLVaWmzkxk',
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
