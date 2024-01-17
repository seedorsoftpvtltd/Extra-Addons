from odoo import api, fields, models, _
import requests

class overtimeinh(models.Model):
    _inherit = "hr.overtime"

    user_id = fields.Many2one('res.users', related='employee_id.user_id')

class hrattendinh(models.Model):
    _inherit = "hr.attendance"

    user_id = fields.Many2one('res.users', related='employee_id.user_id')

