from odoo import models, fields, api ,_
from datetime import datetime


class reject_wizard(models.TransientModel):
    _name = 'reject.wizard'

    reason = fields.Char(string="Reason")

    def reject_button(self):
        current_id = self.env['account.analytic.line'].browse(self.env.context.get('active_ids'))
        a = self.reason
        current_id.timesheet_reject(current_id.id, a)

