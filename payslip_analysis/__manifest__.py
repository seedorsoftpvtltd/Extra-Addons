# -*- coding: utf-8 -*-
{
    'name': 'Payslip Analysis, Pivot Report, Graph Report',
    'version': '0.1',
    'category': 'hr_leave',
    'license': 'OPL-1',
    'price': 50.00,
    'images': ['static/description/allowance_by_month.PNG'],
    'author': 'oranga',
    'currency': 'EUR',
    'summary': 'Payslip Report, Payslip Graph Report, Pivot Payroll Reports',
    'description': """
            Payslip Report, Payslip Graph Report, Pivot Payroll Reports
            Payslip Analysis""",
    "depends": [
        "base",
        "hr_payroll_community",
        "hr"
    ],
    "data": [
        "security/ir.model.access.csv",
        "reports/payslip_analysis.xml",
    ],
    'installable': True,
    'application': True,
}