from odoo.http import request
from odoo import api, fields, models, tools, osv, http, _


class OvertimeInh(models.Model):
    _inherit = "hr.overtime"

    attendance_ids = fields.Many2many('hr.attendance', store=True, string='Attendance', index=True)

