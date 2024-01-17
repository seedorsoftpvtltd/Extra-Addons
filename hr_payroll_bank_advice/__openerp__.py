# -*- coding: utf-8 -*-

# Part of Probuse Consulting Service Pvt Ltd. See LICENSE file for full copyright and licensing details.

{
    'name': 'HR Payroll Bank Advice',
    'version': '1.0',
    'price': 45.0,
    'author' : 'Probuse Consulting Service Pvt. Ltd.',
    'website' : 'www.probuse.com',
    'currency': 'EUR',
    'license': 'Other proprietary',
    'category': 'Human Resources',
    'support': 'contact@probuse.com',
    'summary':  """This module add feature to give bank advice creation and send to bank.""",
    'depends': ['hr_payroll_community'],
    'description': """
    HR Payroll Bank Advice
This module add feature to give bank advice creation and send to bank.

payroll advice
bank advice
hr advice
payslip advice
payroll advice
pay advice
bank advice
salary advice
employee payroll advice
monthly payroll
payroll monthly statement
payroll report
advice bank
advice payslip
hr payslip advice
advice report
bank report advice
employee payroll advice
bank transfer salary
salary transfer to bank
salary transfer advice
Salary Payments by Bank Transfer with Payment Advice Printing 
Payment Advice Note 
hr_payroll
hr_payroll_advice
hr_payroll_bank_advice
bank payment voucher


    """,
    'data': [
        'views/hr_bank_payroll_advice_report.xml',
        'views/report_hr_bank_payroll_advice_template.xml',
        'views/hr_bank_payroll_advice_view.xml',
        'data/mail_template_data.xml',
        'data/hr_bank_payroll_advice_sequence_data.xml',
     ],
    'demo': [
    ],
    'installable': True,
    'application': False,
}
