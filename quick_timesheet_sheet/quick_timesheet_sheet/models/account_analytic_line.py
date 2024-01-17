# -*- coding: utf-8 -*-

from odoo import fields, models


class AccountAnalyticLine(models.Model):
    _inherit = 'account.analytic.line'

    work_type_id = fields.Many2one(
        'work.type.quick_timesheet',
        string='Work Type',
    )
    quick_timesheet_id = fields.Many2one(
        'quick.timesheet.sheet',
        string="Quick Timesheet"
    )
    is_timesheet_id = fields.Boolean(related="quick_timesheet_id.is_create_timesheet")
