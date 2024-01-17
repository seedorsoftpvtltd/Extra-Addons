# -*- coding: utf-8 -*-
#################################################################################
#
#    Odoo, Open Source Management Solution
#    Copyright (C) 2020-today Ascetic Business Solution <www.asceticbs.com>
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
#################################################################################

from odoo import api, fields, models, _
from datetime import datetime

class Employee(models.Model):
    _inherit = "hr.employee"


    last_sign_in = fields.Datetime(string="Last Check In", readonly="1", compute="get_check_in_time")
    last_sign_out = fields.Datetime(string="Last Check Out", readonly="1", compute="get_check_out_time")

    def get_check_in_time(self):
        latest_sign_in = ''
        for emp in self:
            attn_ids = self.env['hr.attendance'].search([('employee_id', '=', emp.id)])
            if attn_ids:
                for a in attn_ids:
                    if emp.last_sign_in == False:
                        emp.last_sign_in = a.check_in
                    else:
                        latest_sign_in =  max(emp.last_sign_in,a.check_in)
                        emp.last_sign_in = latest_sign_in
            else:
                emp.last_sign_in = False

    def get_check_out_time(self):
        latest_sign_out = ''
        for emp in self:
            attn_ids = self.env['hr.attendance'].search([('employee_id', '=', emp.id)])
            if attn_ids:
                for a in attn_ids:
                    if emp.last_sign_out == False or a.check_out == False:
                        emp.last_sign_out = a.check_out
                    else:
                        latest_sign_out =  max(emp.last_sign_out,a.check_out)
                        emp.last_sign_out = latest_sign_out
            else:
                emp.last_sign_out = False
