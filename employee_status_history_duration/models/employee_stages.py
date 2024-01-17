
from datetime import date
from odoo import models, fields, api




class EmployeeStageHistory(models.Model):
    _inherit = 'hr.employee.status.history'
    _description = 'Status History'

    # start_date = fields.Date(string='Start Date')
    # end_date = fields.Date(string='End Date')
    # duration = fields.Integer(compute='get_duration', string='Duration(days)')

    def get_duration(self):
        self.duration = 0
        for each in self:
            if each.end_date and each.start_date:
                start_date = fields.Date.from_string(each.start_date)
                end_date = fields.Date.from_string(each.end_date)
                duration = (end_date - start_date).days + 1
                each.duration = duration


