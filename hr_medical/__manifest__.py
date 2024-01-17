# -*- coding: utf-8 -*-
# Part of Odoo. See COPYRIGHT & LICENSE files for full copyright and licensing details.

{
    'name': "Employee Insurance & claim",
    'summary': """ Employee Insurance & claim details""",
    'description': """
        Manage employee insurance details.
        Generate Expense invoice for Insurance premium.
        Automatic invoice creation for Insurance premium.
        Insurance details available on employees profile.
        Manage insurance claim details.

        Basic Flow of Insurance like this:
        New -> Confirm(HR Officer) -> Done(HR Officer) -> Create Invoice(HR Officer) -> Print Invoice(HR Officer)

        Basic Flow of Claim like this:
        New -> Confirm(Employee) -> Done(HR Officer)
        
        Employee insurance
insurance
employee insurance premium
insurance premium
insurance premium invoice
insurance claim
employee insurance claim
employee insurance details

insurance details
human resource
employee
overtime
overtime request
employee overtime request
overtime approve
overtime reject
employee overtime accept
employee overtime approve
employee overtime reject
HR
Employee grade
job position
hrm
grade
payslip
salary
timesheet
calendar
HR Manager
Attendance
Appraisal
Employee Letter
Passport Management
Payroll
assessments employees
employees assessments
designation
key area
strength
review
development
evolution
assessment
monitor timeline
employee expense
expense
reimbursement
employee expense reimbursement
employee travel bill reimbursement
register employee expense
employee expense on payslip
Amount refunded for costs incurred
payroll manager
monthly salary
Employee Expense Reimburse
Expense Manager
Post Journal Entries
Payslip Calculation
reimburse
airfare reimbursement
flight ticket
flight ticket reimbursement
airfare allowance

    """,
    'author': 'Synconics Technologies Pvt. Ltd.',
    'website': 'http://www.synconics.com',
    'category': 'HR',
    'version': '1.0',
    'license': 'OPL-1',
    'depends': ['hr', 'account','hr_payroll_community', 'hr_employee_updation'],
    'data': [
        'security/ir.model.access.csv',
        'security/security.xml',
        'data/product_data.xml',
        'data/email_template_data.xml',
        'data/cron.xml',
        'views/hr_employee_medical_view.xml',
        'views/insurance_salry_strt.xml',
        'reports/insurance_details_report.xml',
        'views/menu.xml',
    ],
    # 'demo': ['demo/employee_demo.xml'],
    "price": 80,
    "currency": "EUR",
    'images': [
        'static/description/main_screen.png'
    ],
    'installable': True,
    'auto_install': False,
}
