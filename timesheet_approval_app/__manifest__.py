# -*- coding: utf-8 -*-
{
    'name': "Employee Timesheet Approval App",
    'author': "Edge Technologies",
    'version' : '13.0.1.0',
    'live_test_url':'https://youtu.be/HpPSnsEqFWk',
    "images":["static/description/main_screenshot.png"],
    'summary':'Hr Timesheet Approval Employee Timesheet Double Approval Timesheet Approval notification mass Timesheet Approval employee timesheet reminder hr timesheet reminder timesheet approve timesheet manager approval for hr timesheet sheet employee timesheet sheet',
    'description': """
       Employee Timesheet Approved and Reject by Manager, also get Approved and Reject notification by mail with attached timesheet details.
    """,
    'depends': ['base','hr_timesheet'],
    "license" : "OPL-1",
    'data': [
    'wizard/timesheet_wizard.xml',
    #'wizard/wizard.xml',
    'data/mail_template.xml',
    'views/timesheet_view.xml',
    'security/ir.model.access.csv'
    
    ],
    'demo': [],
    'installable': True,
    'auto_install': False,
    'price':25,
    'currency': "EUR",
    'category' :'Human Resources',
}
