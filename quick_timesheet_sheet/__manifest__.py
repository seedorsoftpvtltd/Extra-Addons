# -*- coding: utf-8 -*-

# Part of Probuse Consulting Service Pvt Ltd. See LICENSE file for full copyright and licensing details.

{
    'name': "Timsheet Sheet / Time Worksheet / Quick Timesheet",
    'version': '2.1.4',
    'category' : 'Human Resources',
    'depends': ['sale_timesheet'],
    'currency': 'EUR',
    'price': 99.0,
    'license': 'Other proprietary',
    'summary': """This app allow you to have filling of timesheet of employee on one place for whole week by project/task. This will save your time and make faster entry of timesheet lines in one place for employee.""",
    'description': """
Quick Timesheet Sheet
Employee and Timesheet User can Fill Timesheet and Timesheet Manager can Approve and Create Timesheet.
Quick Timesheet Sheet
Work Types
Work Types on Timesheet
Timesheet on Sheet
Quick Timesheet PDF Report,
My Timesheet sheet
Worksheet
time sheet
timesheet
employee sheet
employee work
regular work
overtime work
overnight work
overnight
payroll work
timesheet payroll
To Approve
Timesheets Sheet Approve
All Timesheet Sheets
Timesheet sheet PDF Report
Timesheet
Odoo Timesheet sheet
timesheet sheet
print timesheet
timesheet grid
timesheet grids
grid timesheet
timesheet grid sheet
print employee timesheet
timesheet report
timesheet pdf report
timsheet odoo report
timesheet odoo
odoo 11 timesheet
timesheet odoo 11
timesheet sheet
timesheet concept
quick timesheet
timesheet employee
employee timesheet
fill timesheet
my timesheet
my current timesheet
approve timesheet
approval timesheet
timesheet approve
timesheet approval
data timesheet
record timesheet
all timesheet
manager timesheet
user timesheet
odoo employee sheet
odoo employee timesheet
timesheet of employee
excel timesheet
timesheet excel
pdf timesheet    
    """,
    'author': "Probuse Consulting Service Pvt. Ltd.",
    'website': "http://www.probuse.com",
    'support': 'contact@probuse.com',
    'images': ['static/description/img1.jpeg'],
    # 'live_test_url': 'https://youtu.be/jCC4j5kuBbI',
    'live_test_url':'https://youtu.be/TUtW__BSPxU ',
    'data':[
        'data/work_type_data.xml',
        'security/ir.model.access.csv',
        'security/quick_timesheet_sheet_security.xml',
        'views/quick_timesheet_sheet_view.xml',
        'views/account_analytic_line_view.xml',
        'views/work_type_quick_timesheet_view.xml',
        'views/menu.xml',
        'views/report_quick_timesheet.xml',
    ],
    'installable' : True,
    'application' : False,
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
