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
    'name': 'Employee Workload Calculation and Notification',
    'version': '1.0',
    'category': 'Human Resources, Project',
    'summary': 'Employee Workload Calculation and Notification for next given days based on Project Tasks',
    'description': """
    Employee Workload Calculation and Notification for next given days based on Project Tasks.
    Task Workload
    Workload Notification
    Project Workload
    User Workload
    Total Workload of user
    """,
    'author': 'Almighty Consulting Solutions Pvt. Ltd.',
    'depends': ['hr_timesheet', 'project'],
    'website': 'https://www.almightycs.com',
    'license': 'OPL-1',
    'data': [
        'views/employee_workload_view.xml',
        'views/template.xml',
        'data/data.xml',
    ],
    'images': [
        'static/description/workload_cover.png',
    ],
    'installable': True,
    'auto_install': False,
    'application': False,
    'price': 26,
    'currency': 'USd',
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
