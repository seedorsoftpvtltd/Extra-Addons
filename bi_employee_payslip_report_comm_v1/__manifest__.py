# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.

{
    'name': 'HR Employee Payslip Reports(PDF/Excel) Community Edition V1',
    'version': '13.0.0.1',
    'category': 'Human Resources',
    'summary': 'Employee Multiple Payslip Report print employee payslip report hr payslip report employee pay slip report mass employee payslip report print payslip report print employee payroll report print pay slip report print payslip excel report payslip xls report',
    'description': """ User can print multiple employee payslip report with salary computation group by with salary rule category and salary rules in both pdf and xls file format at a one click. """,
    'author': 'Arun Seedor',
    'depends':['hr_payroll_community', 'hr_payroll_account_community'],
    'data':[
        'wizard/payslip_report_wizard.xml',
        'report/employee_payslip_report.xml',
        'report/payslip_report_templatev2.xml',
        ],
    "auto_install": False,
    "installable": True,
    "images":["static/description/Banner.png"],
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
