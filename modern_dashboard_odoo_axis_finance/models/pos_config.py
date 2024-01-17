# -*- coding: utf-8 -*-

from odoo import models, fields

class PosConfig(models.Model):
    _inherit = 'pos.config'

    pos_dashboard = fields.Boolean(string="Sales Dashboard")
    today_sale_report = fields.Boolean("Today Sale Report")
    print_audit_report = fields.Boolean("Print Audit Report")
    x_report = fields.Boolean("X-Report")
