from odoo import models, fields, api
from datetime import datetime

class ProjectTask(models.Model):
    _inherit = 'project.task'

    completion_date = fields.Date(string='Completion Date', compute="_compute_completion_date")

    def _compute_completion_date(self):
        for rec in self:
            if rec.state == 'done':
#                rec.completion_date = rec.date_last_stage_update.date()
                if rec.date_last_stage_update:
                    rec.completion_date = rec.date_last_stage_update.date()
                else:
                    rec.completion_date = datetime.now()
            else:
                rec.completion_date = ''
