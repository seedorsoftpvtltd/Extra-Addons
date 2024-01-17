# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import models, fields, api
from datetime import datetime
from dateutil.relativedelta import relativedelta
from datetime import date, timedelta


class ResCompany(models.Model):
    _inherit = 'res.company'

    sh_notify_days = fields.Integer(string="Days Before Expired Visa")
    sh_partner_ids = fields.Many2many("res.partner", string="Notify Users")
    sh_expired_visa_ids = fields.One2many('sh.expired.hr.employee.passport',
                                          'company_id',
                                          string="Expire Visa Line")

    @api.model
    def _run_notify_visa_email_from_employee(self):
        company_id = self.env['res.company'].sudo().search([('id', '=', 1)], limit=1)
        if company_id:
            company_id.sh_expired_visa_ids.unlink()
            notify_list = []
            for line in self.env['sh.employee.passport'].sudo().search([('states', 'in', ['approved'])]):
                date_obj = line.sh_expiry_date
                date_before = (date_obj-timedelta(days=company_id.sh_notify_days))
                if date.today() == date_before:
                    notify_vals = {
                            'company_id': company_id.id,
                            'sh_application_no': line.name,
                            'employee_id': line.employee_id.id,
                            'sh_application_date': line.sh_application_date,
                            'sh_duration': line.sh_duration,
                            'sh_expiry_date': line.sh_expiry_date,
                            'states': line.states,
                            }
                    notify_list.append((0, 0, notify_vals))
            if notify_list:
                company_id.sh_expired_visa_ids = notify_list
                template = self.env.ref('sh_employee_passport.sh_expired_visa_email_template', raise_if_not_found=False)
                if template:
                    field = ['subject', 'body_html', 'email_from', 'email_to', 'partner_to', 'email_cc',  'reply_to', 'attachment_ids', 'mail_server_id']
                    values=self.env['mail.template'].browse(template.id).generate_email(company_id.id, fields=field)
                    values.update({
                        'recipient_ids': [(6, 0, company_id.sh_partner_ids.ids)],
                    })
                    template.send_mail(company_id.id,
                    force_send = False,
                    email_values=values)


class ShExpiredVisaEmployeeLine(models.Model):
    _name = 'sh.expired.hr.employee.passport'
    _description = "Expired Visa"
    _rec_name = 'employee_id'

    company_id = fields.Many2one('res.company', string='Company')
    sh_application_no = fields.Char(string='Application No')
    employee_id = fields.Many2one('hr.employee', string="Employee")
    sh_application_date = fields.Date(string="Application Date")
    sh_duration = fields.Integer(string="Duration in (Months)")
    sh_expiry_date = fields.Date(string="Expiry Date")
    states = fields.Selection([('draft', 'New'),
                              ('progress', 'Under Progress'),
                              ('approved', 'Approved'),
                              ('cancelled', 'Cancelled'),
                              ('expired', 'Expired')],
                              default='draft',
                              string='Status')

class EmployeeConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    sh_notify_days = fields.Integer(string="Days Before Expired Visa",
                                    related="company_id.sh_notify_days",
                                    readonly=False)
    sh_partner_ids = fields.Many2many("res.partner",
                                      string="Notify Users",
                                      related='company_id.sh_partner_ids',
                                      readonly=False)


class Employee(models.Model):
    _inherit = 'hr.employee'

    sh_employee_passport_ids = fields.One2many('sh.employee.passport',
                                               'employee_id',
                                               string='Passport Line')
    states = fields.Selection([('draft', 'New'),
                              ('progress', 'Under Progress'),
                              ('approved', 'Approved'),
                              ('cancelled', 'Cancelled'),
                              ('expired', 'Expired')],
                              string='Status',
                              compute='_compute_state')

    def _compute_state(self):
        if self:
            for rec in self:
                rec.states = False
                if rec.sh_employee_passport_ids:
                    last_record = rec.sh_employee_passport_ids.ids[-1]
                    passport_id = self.env['sh.employee.passport'].browse(last_record)
                    if passport_id:
                        rec.states = passport_id.states

class EmployeePassport(models.Model):
    _name = 'sh.employee.passport'
    _description = 'Employee Passport'

    employee_id = fields.Many2one('hr.employee',
                                  string='Employee')
    name = fields.Char(string='Application No')
    sh_application_date = fields.Date(string='Application Date',
                                      required=True)
    sh_duration = fields.Integer(string='Duration in (Months)',
                                 required=True)
    sh_expiry_date = fields.Date(string='Expiry Date',
                                 compute='_compute_expiry_date')
    states = fields.Selection([('draft', 'New'),
                              ('progress', 'Under Progress'),
                              ('approved', 'Approved'),
                              ('cancelled', 'Cancelled'),
                              ('expired', 'Expired')],
                              default='draft',
                              string='Status')

    @api.model
    def _run_visa_expire(self):
        visa_ids = self.env['sh.employee.passport'].sudo().search([('states', 'in', ['approved'])])
        if visa_ids:
            for visa in visa_ids:
                if visa.sh_expiry_date == fields.Date.today():
                    visa.sudo().write({
                        'states': 'expired'
                        })

    @api.model
    def create(self, vals):
        if not vals.get('name', False):
            seq = self.env['ir.sequence'].next_by_code('sh.employee.passport')
            vals.update({
                'name': seq
                })
        return super(EmployeePassport, self).create(vals)

    @api.depends('sh_application_date', 'sh_duration')
    def _compute_expiry_date(self):
        if self:
            for rec in self:
                if rec.sh_application_date != False:
                    date_obj = rec.sh_application_date
                    expiry_date = date_obj + relativedelta(months = rec.sh_duration)
                    rec.sh_expiry_date = expiry_date
                else:
                    rec.sh_expiry_date = fields.Date.today()
