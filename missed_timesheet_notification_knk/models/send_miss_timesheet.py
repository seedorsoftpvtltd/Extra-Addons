# -*- coding: utf-8 -*-
# Powered by Kanak Infosystems LLP.
# © 2020 Kanak Infosystems LLP. (<https://www.kanakinfosystems.com>).

from odoo import models
from datetime import datetime, timedelta
import base64


class AccountAnalyticLine(models.Model):
    _inherit = "account.analytic.line"

    def _send_miss_timesheet_notification(self):
        employees = self.env['hr.employee'].search([])
        end_date = datetime.now()
        start_date = end_date - timedelta(days=7)
        for emp in employees:
            timesheet_report = self.env['timesheet.report'].create({'employee_id': emp.id, 'from_date': start_date, 'to_date': end_date})
            context = self.env.context.copy()
            context.update({'active_id': timesheet_report.id})
            report_timesheet = self.env.ref('missed_timesheet_notification_knk.action_report_print_timesheets').with_context(context).render_qweb_pdf(timesheet_report.id)[0]
            data_record = base64.b64encode(report_timesheet)
            ir_values = {
               'name': "Employee Missing Report",
               'type': 'binary',
               'datas': data_record,
               'store_fname': data_record,
               'mimetype': 'application/x-pdf',
               }
            data_id = self.env['ir.attachment'].create(ir_values)
            template = self.env.ref('missed_timesheet_notification_knk.reminder_timesheet_fill')
            template.attachment_ids = [(6, 0, [data_id.id])]
            email_values = {'email_to': timesheet_report.user_id.work_email,
                            'email_from': self.env.user.email}
            if timesheet_report.employee_id:
                email_values['email_to'] = timesheet_report.employee_id.work_email
            template.send_mail(self.id, email_values=email_values, force_send=True)
        return True
