from odoo import api, fields, models, tools, _
from datetime import datetime, timedelta
import json


class hr_employee(models.Model):
    _inherit='hr.attendance'

    checkin_date=fields.Date(string='Checkin Date',store=True,index=True)

    @api.constrains('check_in')
    def constraints_checkin_date(self):
        for rec in self:
            if rec.check_in:
                rec['checkin_date']=rec.check_in.date()