# -*- coding: utf-8 -*-
# Powered by Kanak Infosystems LLP.
# © 2020 Kanak Infosystems LLP. (<https://www.kanakinfosystems.com>).

from odoo import fields, models


class TimesheetReport(models.TransientModel):
    _name = 'timesheet.report'
    _description = 'Timesheet Report Wizard'

    user_id = fields.Many2one('res.users', string='User')
    employee_id = fields.Many2one('hr.employee', string="Employee")
    from_date = fields.Date(string="Starting Date")
    to_date = fields.Date(string="Ending Date")

    def print_timesheet(self):
        data = {
        }
        if self.employee_id:
            data['employee'] = self.employee_id.id,
        if self.user_id:
            data['user_id'] = self.user_id.id
        if self.from_date:
            data['start_date'] = self.from_date
        elif self.to_date:
            data['end_date'] = self.to_date
        return self.env.ref(
            'missed_timesheet_notification_knk.action_report_print_timesheets').\
            report_action(self, data=data)
