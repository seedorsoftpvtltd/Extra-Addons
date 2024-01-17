# -*- coding: utf-8 -*-
#╔══════════════════════════════════════════════════════════════════╗
#║                                                                  ║
#║                ╔═══╦╗       ╔╗  ╔╗     ╔═══╦═══╗                 ║
#║                ║╔═╗║║       ║║ ╔╝╚╗    ║╔═╗║╔═╗║                 ║
#║                ║║ ║║║╔╗╔╦╦══╣╚═╬╗╔╬╗ ╔╗║║ ╚╣╚══╗                 ║
#║                ║╚═╝║║║╚╝╠╣╔╗║╔╗║║║║║ ║║║║ ╔╬══╗║                 ║
#║                ║╔═╗║╚╣║║║║╚╝║║║║║╚╣╚═╝║║╚═╝║╚═╝║                 ║
#║                ╚╝ ╚╩═╩╩╩╩╩═╗╠╝╚╝╚═╩═╗╔╝╚═══╩═══╝                 ║
#║                          ╔═╝║     ╔═╝║                           ║
#║                          ╚══╝     ╚══╝                           ║
#║ SOFTWARE DEVELOPED AND SUPPORTED BY ALMIGHTY CONSULTING SERVICES ║
#║                   COPYRIGHT (C) 2016 - TODAY                     ║
#║                   http://www.almightycs.com                      ║
#║                                                                  ║
#╚══════════════════════════════════════════════════════════════════╝
{
    'name': 'Employee Payslip Access from Portal',
    'version': '1.0.1',
    'category': 'Human Resources',
    'author': 'Almighty Consulting Solutions Pvt. Ltd.',
    'support': 'info@almightycs.com',
    'summary': """Allow Employees to get their Payslip from Seedor portal view.""",
    'description': """
    Employee Payslip Access from Portal
    """,
    'website': 'https://www.almightycs.com',
    'license': 'OPL-1',
    'depends': ['hr_payroll_community', 'portal'],
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'views/template.xml',
        'report/payslip_report.xml',
    ],
    'images': [
        'static/description/hr_payslip_portal_odoo_almightycs_cover.jpg',
    ],
    'application': False,
    'sequence': 1,
    'price': 51,
    'currency': 'USD',
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: