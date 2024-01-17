# -*- coding: utf-8 -*-

from odoo import fields, models


class WorkTypeQuickTimesheet(models.Model):
    _name = 'work.type.quick_timesheet'
    _description = 'WorkType Quick Timesheet'

    name = fields.Char(
        string='Name',
        required = True
    )
#     timesheet_type = fields.Selection(
#         [('normal', 'Normal'),
#         ('overtime', 'Overtime'),
#         ('free', 'Free'),
#         ('sick', 'Sick'),
#         ('overnight', 'Overnight')],
#         string='Work Type',
#         required = True
#     )
