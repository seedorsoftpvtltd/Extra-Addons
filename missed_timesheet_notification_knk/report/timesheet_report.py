# -*- coding: utf-8 -*-
# Powered by Kanak Infosystems LLP.
# © 2020 Kanak Infosystems LLP. (<https://www.kanakinfosystems.com>).

from odoo import api, models


class ReportTimesheet(models.AbstractModel):
    _name = 'report.missed_timesheet_notification_knk.report_timesheets'
    _description = 'Timesheet Report'

    def get_timesheets(self, docs):
        domain = []
        if docs.employee_id:
            domain.append(('employee_id', '=', docs.employee_id.id))
        else:
            domain.append(('user_id', '=', docs.user_id.id))
        if docs.from_date and docs.to_date:
            domain += [('date', '<=', docs.to_date),('date', '>=', docs.from_date)]
        elif docs.from_date:
            domain.append(('date', '>=', docs.from_date))
        elif docs.to_date:
            domain.append(('date', '<=', docs.to_date))
        record = self.env['account.analytic.line'].read_group(
            domain,
            fields=['employee_id', 'date', 'unit_amount'],
            groupby=['date:day'])
        records = []
        total = 0
        for rec in record:
            vals = {
                    'manager': docs.employee_id.parent_id.name,
                    'duration': rec['unit_amount'],
                    'missing_duration': docs.employee_id.resource_calendar_id.hours_per_day - rec['unit_amount'],
                    'date': rec['date:day'],
                    }
            total += rec['unit_amount']
            records.append(vals)
        return [records, total]

    @api.model
    def _get_report_values(self, docids, data=None):
        docs = self.env['timesheet.report'].browse(
            self.env.context.get('active_id'))
        identification = []
        if docs.employee_id:
            identification.append({'id': docs.employee_id.id, 'name': docs.employee_id.name})
        else:
            for rec in self.env['hr.employee'].search(
                    [('user_id', '=', docs.user_id.id)]):
                if rec:
                    identification.append({'id': rec.id, 'name': rec.name})
        timesheets = self.get_timesheets(docs)
        company_id = self.env['res.company'].search(
            [('name', '=', docs.user_id.company_id.name)])
        period = None
        if docs.from_date and docs.to_date:
            period = "From " + str(docs.from_date) + " To " + str(docs.to_date)
        elif docs.from_date:
            period = "From " + str(docs.from_date)
        elif docs.to_date:
            period = "To " + str(docs.to_date)
        if len(identification) > 1:
            return {
                'doc_ids': self.ids,
                'docs': docs,
                'timesheets': timesheets[0],
                'total': timesheets[1],
                'company': company_id,
                'identification': identification,
                'period': period,
            }
        else:
            return {
                'doc_ids': self.ids,
                'docs': docs,
                'timesheets': timesheets[0],
                'total': timesheets[1],
                'identification': identification,
                'company': company_id,
                'period': period,
            }
