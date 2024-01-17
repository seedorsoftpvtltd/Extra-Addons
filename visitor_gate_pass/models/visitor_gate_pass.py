# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import datetime
from odoo.exceptions import ValidationError

class VisitorGatePass(models.Model):
    _name = 'visitor.gate.pass.custom'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'id desc, gate_in_datetime desc'
    _rec_name = 'gate_name'

    gate_name = fields.Char(string="Number", readonly=True)
    gate_visitor_name = fields.Char(required=True, string="Visitor Name")
    gate_visitor_company_id = fields.Many2one('res.partner', required=False, string="Visitor Company")
    gate_partner_id = fields.Many2one('hr.employee', required=True, string="Employee")
    gate_in_datetime = fields.Datetime(string="Date Time In")
    gate_out_datetime = fields.Datetime(string="Date Time Out")
    gate_mobile_number = fields.Char(required=True,  string="Phone/Mobile")
    gate_email = fields.Char(string="Email")
    gate_purpose = fields.Text(required=True, string="Purpose")
    gate_department_id = fields.Many2one('hr.department', required=True, string="Department")
    gate_user_id = fields.Many2one('res.users', required=True, default=lambda self: self.env.user, string='Created By', readonly=True)
    gate_company_id = fields.Many2one('res.company', required=True, default=lambda self: self.env.user.company_id, string='Company', readonly=True)
    gate_state = fields.Selection([
         ('draft', 'Draft'),
         ('check_in', 'Check In'),
         ('check_out', 'Check Out'),
         ('cancel', 'Cancelled')], default='draft',
        track_visibility='onchange',
        copy=False, string="Status")
    
    def action_confirm(self):
        self.gate_state = 'check_in'
        self.gate_name = self.env['ir.sequence'].next_by_code('visitor.gate.pass.custom')
        if self.gate_in_datetime == False:
            self.gate_in_datetime = fields.datetime.now()

    def action_exit(self):
        for record in self:
            record.gate_state = 'check_out'
            if record.gate_out_datetime == False:
                record.gate_out_datetime = fields.datetime.now()
                # raise ValidationError("Please Enter The Date Time Out.")

    def action_cancel(self):
        self.gate_state = 'cancel'
        
    def action_reset_to_draft(self):
        self.gate_state = 'draft'

    def print_visitor_card(self):
        return self.env.ref('visitor_gate_pass.gate_visitor_pass_report').report_action(self)
    
    @api.onchange('gate_partner_id')
    def _onchange_partner(self):
        self.gate_department_id = self.gate_partner_id.department_id
        
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
