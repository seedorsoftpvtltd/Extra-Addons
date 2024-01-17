# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _



class HrAttendance(models.Model):
    _name = "hr.attendance"
    _inherit = ['hr.attendance', 'mail.thread', 'mail.activity.mixin']
    _description = "Attendance"
    
    