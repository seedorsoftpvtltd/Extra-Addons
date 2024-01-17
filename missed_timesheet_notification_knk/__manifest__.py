# -*- coding: utf-8 -*-
# Powered by Kanak Infosystems LLP.
# © 2020 Kanak Infosystems LLP. (<https://www.kanakinfosystems.com>).

{
    'name': 'Missed Timesheet Notification',
    'version': '13.0.1.0',
    'category': 'Human Resource',
    'summary': 'This module used to get the status report of the missing timesheet of the employee in every week by mail.also print the missing timesheet report of employees.',
    'description': """ This module used to get the status report of the missing timesheet of the employee in every week by mail.also print the missing timesheet report of employees | mail | missing timesheet | via mail | timesheet | missing timesheet report | incomplete timesheet | timesheet report | incomplete timesheet report. """,
    'website': 'https://www.kanakinfosystems.com',
    'author': 'Kanak Infosystems LLP.',
    'depends': ['base', 'hr_timesheet', 'mail', 'hr'],
    'data': [
        'data/data.xml',
        'wizard/missed_timesheet_report_views.xml',
        'security/ir.model.access.csv',
        'report/timesheet_reports.xml',
        'report/timesheet_templates.xml',
        'views/mail.xml',
    ],
    'images': ['static/description/banner.gif'],
    "installable": True,
    'license': 'OPL-1',
    'price': 10,
    'currency': 'EUR',
}
