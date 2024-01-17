# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

{
    "name": "Employee Visa/Passport Management",
    "author": "Softhealer Technologies",
    "website": "https://www.softhealer.com",
    "support": "support@softhealer.com",
    "category": "Hr",
    "summary": "Manage Employee Document, Employee Passport Management Module, Manage Employee Visa App, Employee Visa Expired Notification, Employee Passport Detail, Employee Additional Information Odoo",
    "description": """
Do you want to manage employee visa information? This module helps to send email notification on reaching the expiration dates of the employee passport. You can notify the responsible person whom you were configured, before a day, week, month & you can set manually days. You can set the status of your employee passport based on the date. You can group by visa information by employee, application date & status. Status of employee visa will auto-change with the calendar dates.

 Employee Visa Management Odoo, Employee Passport Management Odoo
 Manage Employee Passport Module, Manage Employee Document, Manage Employee Visa, Employee Visa Expiry Date Notification, Get  Employee Passport Detail, Employee Additional Information Odoo
 Manage Employee Document, Manage Employee Passport Module, Manage Employee Visa App, Employee Visa Expired Notification, Employee Passport Detail, Employee Additional Information Odoo

                    """,
    "version": "13.0.1",
    "depends": ["base", "hr"],
    "application": True,
    "data": [
        'security/ir.model.access.csv',
        'data/passport_data.xml',
        'views/res_company_view.xml',
        'views/res_config_setting_view.xml',
        'data/passport_expired_email_template.xml',
        'views/employee.xml',
        'views/employee_passport.xml',
        'data/notify_visa_cron.xml',
            ],
    "images": ["static/description/background.png", ],
    "live_test_url": "https://youtu.be/qemXceWD9zg",
    "auto_install": False,
    "installable": True,
	"price": "35",
	"currency": "EUR"
}
