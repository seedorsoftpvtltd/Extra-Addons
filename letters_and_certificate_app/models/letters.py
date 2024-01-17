from odoo import models, api, fields, http, _
import socket
import re
from odoo.http import request
from datetime import datetime, date

TAG_RE = re.compile(r'<[^>]+>')


class ResPartner(models.Model):
    _inherit = "res.partner"

    letters = fields.Integer('Letter', compute='_compute_letter_count')

    def _compute_letter_count(self):
        Letters = self.env['letters']
        for partner in self:
            partner.letters = Letters.search_count([('partner_id', '=', partner.id)])


class Letters(models.Model):
    _name = "letters"
    _description = 'Letters'
    _rec_name = 'subject'

    subject = fields.Char(string="Subject")
    letter_template = fields.Many2one('template', string="Letter Template")
    partner_id = fields.Many2one('res.partner', string="Partner")
    employee = fields.Many2one('hr.employee', string="Employee")
    date = fields.Date(string="Date")
    reference = fields.Text(string="Source")
    user_id = fields.Many2one('res.users', string='Salesperson', index=True, track_visibility='onchange',
                              track_sequence=2, default=lambda self: self.env.user)
    template = fields.Html()
    template_value = fields.Char()
    old_partner_id = fields.Many2one('res.partner', string="Partner")
    old_employee_id = fields.Many2one('hr.employee', string="Employee")
    state = fields.Selection([('draft', 'Draft'), ('approved', 'Approved')], default="draft")
    letter_type = fields.Selection(related='letter_template.letter_type',
                                   help="Technical field used for usability purposes", string='Base On')

    def letter_approved(self):
        for letter in self:
            self.write({'state': 'approved'})

    def cancel(self):
        for letter in self:
            self.write({'state': 'draft'})

    @api.onchange('letter_template')
    def on_change_template(self):
        self.template = self.letter_template.template

    @api.onchange('partner_id')
    def on_change_partner(self):
        if self.template:
            if self.old_partner_id:
                if self.old_partner_id.id != self.partner_id.id:
                    if self.old_partner_id.name in self.template:
                        partner_name = self.template.replace(self.old_partner_id.name, self.partner_id.name)
                        self.template = partner_name
                    if self.old_partner_id:
                        address = self.partner_id.street
                        if self.partner_id.street2:
                            address += ',' + self.partner_id.street2
                        else:
                            if self.partner_id.city:
                                address += ',' + self.partner_id.city
                            if self.partner_id.state_id:
                                address += "," + self.partner_id.state_id.name
                            if self.partner_id.country_id:
                                address += "," + self.partner_id.country_id.name
                            if self.partner_id.zip:
                                address += "," + self.partner_id.zip
                        partner_address = self.template.replace('partner_address', address)
                        self.template = partner_address
                    if self.old_partner_id.street and self.old_partner_id.street in self.template:
                        street = self.template.replace(self.old_partner_id.street, self.partner_id.street or '')
                        self.template = street
                    if self.old_partner_id.street2 and self.old_partner_id.street2 in self.template:
                        street2 = self.template.replace(self.old_partner_id.street2, self.partner_id.street2 or '')
                        self.template = street2
                    if self.old_partner_id.city and self.old_partner_id.city in self.template:
                        street = self.template.replace(self.old_partner_id.city, self.partner_id.city or '')
                        self.template = street
                    if self.old_partner_id.state_id and self.old_partner_id.state_id in self.template:
                        street = self.template.replace(self.old_partner_id.state_id.name,
                                                       self.partner_id.state_id.name or '')
                        self.template = street
                    if self.old_partner_id.country_id and self.old_partner_id.country_id in self.template:
                        country = self.template.replace(self.old_partner_id.country_id.name,
                                                        self.partner_id.country_id.name or '')
                        self.template = country
                    if self.old_partner_id.zip and self.old_partner_id.zip in self.template:
                        partner_zip = self.template.replace(self.old_partner_id.zip, self.partner_id.zip or '')
                        self.template = partner_zip
                    if self.old_partner_id.email and self.old_partner_id.email in self.template:
                        email = self.template.replace(self.old_partner_id.email, self.partner_id.email or '')
                        self.template = email
                    if self.old_partner_id.mobile and self.old_partner_id.mobile in self.template:
                        mobile = self.template.replace(self.old_partner_id.mobile, self.partner_id.mobile or '')
                        self.template = mobile
                    if self.old_partner_id.phone and self.old_partner_id.phone in self.template:
                        phone = self.template.replace(self.old_partner_id.phone, self.partner_id.phone or '')
                        self.template = phone
                    self.old_partner_id = self.partner_id.id
            else:
                self.old_partner_id = self.partner_id.id
                if 'partner_name' in self.template:
                    partner_name = self.template.replace('partner_name', self.partner_id.name)
                    self.template = partner_name
                if 'partner_address' in self.template:
                    if self.partner_id:
                        address = self.partner_id.street
                        if self.partner_id.street2:
                            address += ',' + self.partner_id.street2
                        else:
                            if self.partner_id.city:
                                address += ',' + self.partner_id.city
                            if self.partner_id.state_id:
                                address += "," + self.partner_id.state_id.name
                            if self.partner_id.country_id:
                                address += "," + self.partner_id.country_id.name
                            if self.partner_id.zip:
                                address += "," + self.partner_id.zip
                        partner_address = self.template.replace('partner_address', address)
                        self.template = partner_address
                if 'partner_street' in self.template:
                    street = self.template.replace('partner_street', self.partner_id.street or '')
                    self.template = street
                if 'partner_stree2' in self.template:
                    if self.partner_id.street2:
                        street2 = self.template.replace('partner_street', self.partner_id.street2 or '')
                        self.template = street2
                if 'partner_city' in self.template:
                    street = self.template.replace('partner_city', self.partner_id.city or '')
                    self.template = street
                if 'partner_state' in self.template:
                    street = self.template.replace('partner_state', self.partner_id.state_id.name or '')
                    self.template = street
                if 'partner_country' in self.template:
                    country = self.template.replace('partner_country', self.partner_id.country_id.name or '')
                    self.template = country
                if 'partner_zip' in self.template:
                    zip = self.template.replace('partner_zip', self.partner_id.zip or '')
                    self.template = zip
                if 'partner_email' in self.template:
                    email = self.template.replace('partner_email', self.partner_id.email or '')
                    self.template = email
                if 'partner_mobile' in self.template:
                    mobile = self.template.replace('partner_mobile', self.partner_id.mobile or '')
                    self.template = mobile
                if 'partner_phone' in self.template:
                    phone = self.template.replace('partner_phone', self.partner_id.phone or '')
                    self.template = phone
                template = TAG_RE.sub('\n', self.template)
                self.template_value = template

    @api.onchange('employee')
    def on_change_employee(self):
        print('helooo')
        if self.template:
            print('helooo1')

            if self.old_employee_id:
                print('helooo2')
                # print(self.employee.contract_id.wage)

                if self.old_employee_id.id != self.employee.id:
                    if self.old_employee_id.name in self.template:
                        print('helooo3')
                        employee_name = self.template.replace(self.old_employee_id.name, self.employee.name)
                        self.template = employee_name
                        print(employee_name)
                    if self.old_employee_id.user_id.partner_id:
                        print('helooo4')
                        address = self.employee.user_id.partner_id.street
                        if self.employee.user_id.partner_id.street2:
                            address += ',' + self.employee.user_id.partner_id.street2
                        else:
                            if self.employee.user_id.partner_id.city:
                                address += ',' + self.employee.user_id.partner_id.city
                            if self.employee.user_id.partner_id.state_id:
                                address += "," + self.employee.user_id.partner_id.state_id.name
                            if self.employee.user_id.partner_id.country_id:
                                address += "," + self.employee.user_id.partner_id.country_id.name
                            if self.employee.user_id.partner_id.zip:
                                address += "," + self.employee.user_id.partner_id.zip
                        partner_address = self.template.replace('employee_address', address)
                        self.template = partner_address
                    if self.old_employee_id.user_id.partner_id.street and self.old_employee_id.user_id.partner_id.street in self.template:
                        street = self.template.replace(self.old_employee_id.user_id.partner_id.street,
                                                       self.employee.user_id.partner_id.street or '')
                        self.template = street
                    if self.old_employee_id.user_id.partner_id.street2 and self.old_employee_id.user_id.partner_id.street2 in self.template:
                        street2 = self.template.replace(self.old_employee_id.user_id.partner_id.street2,
                                                        self.employee.user_id.partner_id.street2 or '')
                        self.template = street2
                    if self.old_employee_id.user_id.partner_id.city and self.old_employee_id.user_id.partner_id.city in self.template:
                        street = self.template.replace(self.old_employee_id.user_id.partner_id.city,
                                                       self.employee.user_id.partner_id.city or '')
                        self.template = street
                    if self.old_employee_id.user_id.partner_id.state_id and self.old_employee_id.user_id.partner_id.state_id.name in self.template:
                        street = self.template.replace(self.old_employee_id.user_id.partner_id.state_id.name,
                                                       self.employee.user_id.partner_id.state_id.name or '')
                        self.template = street
                    if self.old_employee_id.user_id.partner_id.country_id and self.old_employee_id.user_id.partner_id.country_id.name in self.template:
                        country = self.template.replace(self.old_employee_id.user_id.partner_id.country_id.name,
                                                        self.employee.user_id.partner_id.country_id.name or '')
                        self.template = country
                    if self.old_employee_id.user_id.partner_id.zip and self.old_employee_id.user_id.partner_id.zip in self.template:
                        employee_zip = self.template.replace(self.old_employee_id.user_id.partner_id.zip,
                                                             self.employee.user_id.partner_id.zip or '')
                        self.template = employee_zip
                    if self.old_employee_id.user_id.partner_id.email and self.old_employee_id.user_id.partner_id.email in self.template:
                        email = self.template.replace(self.old_employee_id.user_id.partner_id.email,
                                                      self.employee.user_id.partner_id.email or '')
                        self.template = email
                    if self.old_employee_id.user_id.partner_id.mobile and self.old_employee_id.user_id.partner_id.mobile in self.template:
                        mobile = self.template.replace(self.old_employee_id.user_id.partner_id.mobile,
                                                       self.employee.user_id.partner_id.mobile or '')
                        self.template = mobile
                    if self.old_employee_id.user_id.partner_id.phone and self.old_employee_id.user_id.partner_id.phone in self.template:
                        phone = self.template.replace(self.old_employee_id.user_id.partner_id.phone,
                                                      self.employee.user_id.partner_id.phone or '')
                        self.template = phone

                    # Employee Personal Information
                    if self.old_employee_id.job_title and self.old_employee_id.job_title in self.template:
                        job_title = self.template.replace(self.old_employee_id.job_title, self.employee.job_title or '')
                        self.template = job_title
                    if self.old_employee_id.mobile_phone and self.old_employee_id.mobile_phone in self.template:
                        mobile_phone = self.template.replace(self.old_employee_id.mobile_phone or '',
                                                             self.employee.mobile_phone or '')
                        self.template = mobile_phone
                    if self.old_employee_id.work_phone and self.old_employee_id.work_phone in self.template:
                        work_phone = self.template.replace(self.old_employee_id.work_phone or '',
                                                           self.employee.work_phone or '')
                        self.template = work_phone
                    if self.old_employee_id.work_email and self.old_employee_id.work_email in self.template:
                        work_email = self.template.replace(self.old_employee_id.work_email or '',
                                                           self.employee.work_email or '')
                        self.template = work_email
                    if self.old_employee_id.work_location and self.old_employee_id.work_location in self.template:
                        work_location = self.template.replace(self.old_employee_id.work_location or '',
                                                              self.employee.work_location or '')
                        self.template = work_location
                    if self.old_employee_id.department_id and self.old_employee_id.department_id.name in self.template:
                        department = self.template.replace(self.old_employee_id.department_id.name or '',
                                                           self.employee.department_id.name or '')
                        self.template = department
                    if self.old_employee_id.job_id and self.old_employee_id.job_id.name in self.template:
                        employeejob = self.template.replace(self.old_employee_id.job_id.name or '',
                                                            self.employee.job_id.name or '')
                        self.template = employeejob
                    if self.old_employee_id.parent_id and self.old_employee_id.parent_id.name in self.template:
                        employee_manager = self.template.replace(self.old_employee_id.parent_id.name or '',
                                                                 self.employee.parent_id.name or '')
                        self.template = employee_manager
                    if self.old_employee_id.birthday and self.old_employee_id.birthday in self.template:
                        employee_birthday = self.template.replace(self.old_employee_id.birthday or '',
                                                                  str(self.employee.birthday) or '')
                        self.template = employee_birthday
                        print(employee_birthday)
                    if self.old_employee_id.gender and self.old_employee_id.gender in self.template:
                        employee_gender = self.template.replace(self.old_employee_id.gender or '',
                                                                  self.employee.gender or '')
                        self.template = employee_gender
                    if self.old_employee_id.marital and self.old_employee_id.marital in self.template:
                        employee_marital = self.template.replace(self.old_employee_id.marital or '',
                                                                  self.employee.marital or '')
                        self.template = employee_marital
                   # if self.old_employee_id.emp_id and self.old_employee_id.emp_id in self.template:
                   #     employee_id = self.template.replace(self.old_employee_id.emp_id or '',
                   #                                           self.employee.emp_id or '')
                   #     self.template = employee_id
                    if self.old_employee_id.x_emp and self.old_employee_id.x_emp in self.template:
                        employee_idd = self.template.replace(self.old_employee_id.x_emp or '',
                                                              self.employee.x_emp or '')
                        self.template = employee_idd
                    if self.old_employee_id.joining_date and self.old_employee_id.joining_date in self.template:
                        employee_joining_date = self.template.replace(self.old_employee_id.joining_date or '',
                                                                      self.employee.joining_date or '')
                        self.template = employee_joining_date
                    if self.old_employee_id.contract_id.wage and self.old_employee_id.contract_id.wage in self.template:
                        contract_wage = self.template.replace(self.old_employee_id.contract_id.wage or '',
                                                              self.employee.contract_id.wage or '')
                        self.template = contract_wage
                        print(contract_wage)
                    if self.old_employee_id.contract_id.date_start and self.old_employee_id.contract_id.date_start in self.template:
                        contract_startdate = self.template.replace(self.old_employee_id.contract_id.date_start or '',
                                                              self.employee.contract_id.date_start or '')
                        self.template = contract_startdate
                    if self.old_employee_id.contract_id.date_end and self.old_employee_id.contract_id.date_end in self.template:
                        contract_enddate = self.template.replace(self.old_employee_id.contract_id.date_end or '',
                                                              self.employee.contract_id.date_end or '')
                        self.template = contract_enddate
                    if self.old_employee_id.contract_id.hra and self.old_employee_id.contract_id.hra in self.template:
                        contract_hra = self.template.replace(self.old_employee_id.contract_id.hra or '',
                                                              self.employee.contract_id.hra or '')
                        self.template = contract_hra
                    if self.old_employee_id.contract_id.x_leavellow and self.old_employee_id.contract_id.x_leavellow in self.template:
                        contract_leaveallow = self.template.replace(self.old_employee_id.contract_id.x_leavellow or '',
                                                              self.employee.contract_id.x_leavellow or '')
                        self.template = contract_leaveallow
                    if self.old_employee_id.contract_id.x_bonus and self.old_employee_id.contract_id.x_bonus in self.template:
                        contract_bonus = self.template.replace(self.old_employee_id.contract_id.x_bonus or '',
                                                              self.employee.contract_id.x_bonus or '')
                        self.template = contract_bonus
                    if self.old_employee_id.contract_id.x_pf and self.old_employee_id.contract_id.x_pf in self.template:
                        contract_pf = self.template.replace(self.old_employee_id.contract_id.x_pf or '',
                                                              self.employee.contract_id.x_pf or '')
                        self.template = contract_pf
                    if self.old_employee_id.contract_id.x_esi and self.old_employee_id.contract_id.x_esi in self.template:
                        contract_esi = self.template.replace(self.old_employee_id.contract_id.x_esi or '',
                                                              self.employee.contract_id.x_esi or '')
                        self.template = contract_esi
                    if self.old_employee_id.company_id.name and self.old_employee_id.company_id.name in self.template:
                        employee_company = self.template.replace(self.old_employee_id.company_id.name or '',
                                                              self.employee.company_id.name or '')
                        self.template = employee_company
                    for record in self.old_employee_id:
                        if record.stages_history:
                            for rec in record.stages_history:
                                if rec.start_date and rec.start_date in self.template:
                                    status_startdate = rec.template.replace(
                                        rec.start_date or '',
                                        rec.start_date or '')
                                    self.template = status_startdate
                    for record in self.old_employee_id:
                        if record.stages_history:
                            for rec in record.stages_history:
                                if rec.end_date and rec.end_date in self.template:
                                    status_enddate = rec.template.replace(
                                        rec.end_date or '',
                                        rec.end_date or '')
                                    self.template = status_enddate
                    if self.old_employee_id.resign_date and self.old_employee_id.resign_date in self.template:
                        employee_resigndate = self.template.replace(self.old_employee_id.resign_date or '',
                                                              self.employee.resign_date or '')
                        self.template = employee_resigndate
                    for record in self.old_employee_id:
                        if record.fam_ids:
                            for rec in record.fam_ids:
                                if rec.member_name in self.template:
                                    family = rec.member_name
                                    employee_family = rec.template.replace(
                                        family or '')
                                    self.template = employee_family
                    if self.date and self.date in self.template:
                        datee = self.template.replace(self.date or '',
                                                                  self.date or '')
                        self.template = datee
                    if self.old_employee_id.x_uan and self.old_employee_id.x_uan in self.template:
                        employee_uan = self.template.replace(self.old_employee_id.x_uan or '',
                                                              self.employee.x_uan or '')
                        self.template = employee_uan
                    if self.old_employee_id.x_nationalidentityno and self.old_employee_id.x_nationalidentityno in self.template:
                        employee_nationalidentityno = self.template.replace(self.old_employee_id.x_nationalidentityno or '',
                                                              self.employee.x_nationalidentityno or '')
                        self.template = employee_nationalidentityno
                    if self.old_employee_id.x_taxaccountno and self.old_employee_id.x_taxaccountno in self.template:
                        employee_taxaccountno = self.template.replace(self.old_employee_id.x_taxaccountno or '',
                                                              self.employee.x_taxaccountno or '')
                        self.template = employee_taxaccountno
                    if self.old_employee_id.x_emp_cate.name and self.old_employee_id.x_emp_cate.name in self.template:
                        employee_emp_cate = self.template.replace(self.old_employee_id.x_emp_cate.name or '',
                                                              self.employee.x_emp_cate.name or '')
                        self.template = employee_emp_cate
                    for record in self.old_employee_id:
                        if record.acting_job_ids:
                            for rec in record.acting_job_ids:
                                if rec.name in self.template:
                                    job = rec.name
                                    employee_acting_job = rec.template.replace(job or '')
                                    self.template = employee_acting_job
                    if self.old_employee_id.x_emp and self.old_employee_id.x_emp in self.template:
                        employee_idd = self.template.replace(self.old_employee_id.x_emp or '',
                                                              self.employee.x_emp or '')
                        self.template = employee_idd
                    if self.old_employee_id.x_esi and self.old_employee_id.x_esi in self.template:
                        employee_esi = self.template.replace(self.old_employee_id.x_esi or '',
                                                              self.employee.x_esi or '')
                        self.template = employee_esi
                    if self.old_employee_id.x_epf and self.old_employee_id.x_epf in self.template:
                        employee_epf = self.template.replace(self.old_employee_id.x_epf or '',
                                                              self.employee.x_epf or '')
                        self.template = employee_epf
                    if self.old_employee_id.user_id.name and self.old_employee_id.user_id.name in self.template:
                        employee_related_user = self.template.replace(self.old_employee_id.user_id.name or '',
                                                              self.employee.user_id.name or '')
                        self.template = employee_related_user
                    if self.old_employee_id.device_id and self.old_employee_id.device_id in self.template:
                        employee_device_id = self.template.replace(self.old_employee_id.device_id or '',
                                                              self.employee.device_id or '')
                        self.template = employee_device_id
                    if self.old_employee_id.pin and self.old_employee_id.pin in self.template:
                        employee_pin = self.template.replace(self.old_employee_id.pin or '',
                                                              self.employee.pin or '')
                        self.template = employee_pin
                    if self.old_employee_id.barcode and self.old_employee_id.barcode in self.template:
                        employee_badge = self.template.replace(self.old_employee_id.barcode or '',
                                                              self.employee.barcode or '')
                        self.template = employee_badge
                    if self.old_employee_id.bank_account_id.name and self.old_employee_id.bank_account_id.name in self.template:
                        employee_bank = self.template.replace(self.old_employee_id.bank_account_id.name or '',
                                                              self.employee.bank_account_id.name or '')
                        self.template = employee_bank
                    if self.old_employee_id.km_home_work and self.old_employee_id.km_home_work in self.template:
                        employee_km_home_work = self.template.replace(self.old_employee_id.km_home_work or '',
                                                              self.employee.km_home_work or '')
                        self.template = employee_km_home_work
                    if self.old_employee_id.passport_id and self.old_employee_id.passport_id in self.template:
                        employee_passport = self.template.replace(self.old_employee_id.passport_id or '',
                                                              self.employee.passport_id or '')
                        self.template = employee_passport
                    if self.old_employee_id.passport_expiry_date and self.old_employee_id.passport_expiry_date in self.template:
                        employeepassport_expiry_date = self.template.replace(self.old_employee_id.passport_expiry_date or '',
                                                              self.employee.passport_expiry_date or '')
                        self.template = employeepassport_expiry_date
                    if self.old_employee_id.emergency_contact and self.old_employee_id.emergency_contact in self.template:
                        employee_emergency_contact = self.template.replace(self.old_employee_id.emergency_contact or '',
                                                              self.employee.emergency_contact or '')
                        self.template = employee_emergency_contact
                    if self.old_employee_id.emergency_phone and self.old_employee_id.emergency_phone in self.template:
                        employee_emergency_phone = self.template.replace(self.old_employee_id.emergency_phone or '',
                                                              self.employee.emergency_phone or '')
                        self.template = employee_emergency_phone
                    if self.old_employee_id.certificate and self.old_employee_id.certificate in self.template:
                        employee_certificate = self.template.replace(self.old_employee_id.certificate or '',
                                                              self.employee.certificate or '')
                        self.template = employee_certificate
                    if self.old_employee_id.study_field and self.old_employee_id.study_field in self.template:
                        employee_study_field = self.template.replace(self.old_employee_id.study_field or '',
                                                              self.employee.study_field or '')
                        self.template = employee_study_field
                    if self.old_employee_id.study_school and self.old_employee_id.study_school in self.template:
                        employee_study_school = self.template.replace(self.old_employee_id.study_school or '',
                                                              self.employee.study_school or '')
                        self.template = employee_study_school
                    if self.old_employee_id.identification_id and self.old_employee_id.identification_id in self.template:
                        employee_identification_id = self.template.replace(self.old_employee_id.identification_id or '',
                                                              self.employee.identification_id or '')
                        self.template = employee_identification_id
                    if self.old_employee_id.id_expiry_date and self.old_employee_id.id_expiry_date in self.template:
                        employee_id_expiry_date = self.template.replace(self.old_employee_id.id_expiry_date or '',
                                                              self.employee.id_expiry_date or '')
                        self.template = employee_id_expiry_date
                    if self.old_employee_id.place_of_birth and self.old_employee_id.place_of_birth in self.template:
                        employee_place_of_birth = self.template.replace(self.old_employee_id.place_of_birth or '',
                                                              self.employee.place_of_birth or '')
                        self.template = employee_place_of_birth
                    if self.old_employee_id.country_of_birth and self.old_employee_id.country_of_birth in self.template:
                        employeecountry_of_birth = self.template.replace(self.old_employee_id.country_of_birth or '',
                                                              self.employee.country_of_birth or '')
                        self.template = employeecountry_of_birth
                    if self.old_employee_id.childern and self.old_employee_id.childern in self.template:
                        employee_childern = self.template.replace(self.old_employee_id.childern or '',
                                                              self.employee.childern or '')
                        self.template = employee_childern
                    if self.old_employee_id.visa_no and self.old_employee_id.visa_no in self.template:
                        employee_visa_no = self.template.replace(self.old_employee_id.visa_no or '',
                                                              self.employee.visa_no or '')
                        self.template = employee_visa_no
                    if self.old_employee_id.permit_no and self.old_employee_id.permit_no in self.template:
                        employee_permit_no = self.template.replace(self.old_employee_id.permit_no or '',
                                                              self.employee.permit_no or '')
                        self.template = employee_permit_no
                    if self.old_employee_id.visa_expire and self.old_employee_id.visa_expire in self.template:
                        employee_visa_expire = self.template.replace(self.old_employee_id.visa_expire or '',
                                                              self.employee.visa_expire or '')
                        self.template = employee_visa_expire

                    if self.old_employee_id.contract_id.x_days and self.old_employee_id.contract_id.x_days in self.template:
                        contract_wrk_days = self.template.replace(self.old_employee_id.contract_id.x_days or '',
                                                              self.employee.contract_id.x_days or '')
                        self.template = contract_wrk_days
                    if self.old_employee_id.contract_id.x_pr and self.old_employee_id.contract_id.x_pr in self.template:
                        contract_present_days = self.template.replace(self.old_employee_id.contract_id.x_pr or '',
                                                              self.employee.contract_id.x_pr or '')
                        self.template = contract_present_days
                    if self.old_employee_id.contract_id.x_wage and self.old_employee_id.contract_id.x_wage in self.template:
                        contract_fixed_wage = self.template.replace(self.old_employee_id.contract_id.x_wage or '',
                                                              self.employee.contract_id.x_wage or '')
                        self.template = contract_fixed_wage
                    if self.old_employee_id.contract_id.wage_type and self.old_employee_id.contract_id.wage_type in self.template:
                        contractwage_type = self.template.replace(self.old_employee_id.contract_id.wage_type or '',
                                                              self.employee.contract_id.wage_type or '')
                        self.template = contractwage_type
                    if self.old_employee_id.contract_id.x_vacationallowance and self.old_employee_id.contract_id.x_vacationallowance in self.template:
                        contract_vacationallowance = self.template.replace(self.old_employee_id.contract_id.x_vacationallowance or '',
                                                              self.employee.contract_id.x_vacationallowance or '')
                        self.template = contract_vacationallowance
                    if self.old_employee_id.contract_id.x_attbonus and self.old_employee_id.contract_id.x_attbonus in self.template:
                        contract_attbonus = self.template.replace(self.old_employee_id.contract_id.x_attbonus or '',
                                                              self.employee.contract_id.x_attbonus or '')
                        self.template = contract_attbonus
                    if self.old_employee_id.contract_id.over_day and self.old_employee_id.contract_id.over_day in self.template:
                        contract_daywage = self.template.replace(self.old_employee_id.contract_id.over_day or '',
                                                              self.employee.contract_id.over_day or '')
                        self.template = contract_daywage
                    if self.old_employee_id.contract_id.over_hour and self.old_employee_id.contract_id.over_hour in self.template:
                        contract_hourwage = self.template.replace(self.old_employee_id.contract_id.over_hour or '',
                                                              self.employee.contract_id.over_hour or '')
                        self.template = contract_hourwage
                    if self.old_employee_id.contract_id.da and self.old_employee_id.contract_id.da in self.template:
                        contract_da = self.template.replace(self.old_employee_id.contract_id.da or '',
                                                              self.employee.contract_id.da or '')
                        self.template = contract_da
                    if self.old_employee_id.contract_id.travel_allowance and self.old_employee_id.contract_id.travel_allowance in self.template:
                        contract_travel_allowance = self.template.replace(self.old_employee_id.contract_id.travel_allowance or '',
                                                              self.employee.contract_id.travel_allowance or '')
                        self.template = contract_travel_allowance
                    if self.old_employee_id.contract_id.x_busfare and self.old_employee_id.contract_id.x_busfare in self.template:
                        contract_busfare = self.template.replace(self.old_employee_id.contract_id.x_busfare or '',
                                                              self.employee.contract_id.x_busfare or '')
                        self.template = contract_busfare
                    if self.old_employee_id.contract_id.meal_allowance and self.old_employee_id.contract_id.meal_allowance in self.template:
                        contract_meal_allowance = self.template.replace(self.old_employee_id.contract_id.meal_allowance or '',
                                                              self.employee.contract_id.meal_allowance or '')
                        self.template = contract_meal_allowance
                    if self.old_employee_id.contract_id.x_uniformallow and self.old_employee_id.contract_id.x_uniformallow in self.template:
                        contract_uniformallow = self.template.replace(self.old_employee_id.contract_id.x_uniformallow or '',
                                                              self.employee.contract_id.x_uniformallow or '')
                        self.template = contract_uniformallow
                    if self.old_employee_id.contract_id.medical_allowance and self.old_employee_id.contract_id.medical_allowance in self.template:
                        contract_medical_allowance = self.template.replace(self.old_employee_id.contract_id.medical_allowance or '',
                            self.employee.contract_id.medical_allowance or '')
                        self.template = contract_medical_allowance
                    if self.old_employee_id.contract_id.x_internetallow and self.old_employee_id.contract_id.x_internetallow in self.template:
                        contract_internetallow = self.template.replace(self.old_employee_id.contract_id.x_internetallow or '',
                                                              self.employee.contract_id.x_internetallow or '')
                        self.template = contract_internetallow
                    if self.old_employee_id.contract_id.x_mobileallow and self.old_employee_id.contract_id.x_mobileallow in self.template:
                        contract_mobileallow = self.template.replace(self.old_employee_id.contract_id.x_mobileallow or '',
                                                              self.employee.contract_id.x_mobileallow or '')
                        self.template = contract_mobileallow
                    if self.old_employee_id.contract_id.x_maternityallow and self.old_employee_id.contract_id.x_maternityallow in self.template:
                        contract_maternityallow = self.template.replace(self.old_employee_id.contract_id.x_maternityallow or '',
                            self.employee.contract_id.x_maternityallow or '')
                        self.template = contract_maternityallow
                    if self.old_employee_id.contract_id.other_allowance and self.old_employee_id.contract_id.other_allowance in self.template:
                        contract_other_allowance = self.template.replace(self.old_employee_id.contract_id.other_allowance or '',
                            self.employee.contract_id.other_allowance or '')
                        self.template = contract_other_allowance
                    if self.old_employee_id.contract_id.x_pt and self.old_employee_id.contract_id.x_pt in self.template:
                        contract_pt = self.template.replace(self.old_employee_id.contract_id.x_pt or '',
                            self.employee.contract_id.x_pt or '')
                        self.template = contract_pt
                    if self.old_employee_id.contract_id.x_food and self.old_employee_id.contract_id.x_food in self.template:
                        contract_food = self.template.replace(self.old_employee_id.contract_id.x_food or '',
                            self.employee.contract_id.x_food or '')
                        self.template = contract_food
                    if self.old_employee_id.contract_id.trial_date_end and self.old_employee_id.contract_id.trial_date_end in self.template:
                        contract_trial_end_date = self.template.replace(self.old_employee_id.contract_id.trial_date_end or '',
                            self.employee.contract_id.trial_date_end or '')
                        self.template = contract_trial_end_date

                    self.old_employee_id = self.employee.id
            else:
                print('helooo00000')
                print(self.employee.contract_id.wage)

                self.old_employee_id = self.employee.id
                if 'employee_name' in self.template:
                    employee_name = self.template.replace('employee_name', self.employee.name)
                    self.template = employee_name
                if 'employee_address' in self.template:
                    if self.employee.user_id.partner_id:
                        address = self.employee.user_id.partner_id.street
                        if self.employee.user_id.partner_id.street2:
                            address += ',' + self.employee.user_id.partner_id.street2
                        else:
                            if self.employee.user_id.partner_id.city:
                                address += ',' + self.employee.user_id.partner_id.city
                            if self.employee.user_id.partner_id.state_id:
                                address += "," + self.employee.user_id.partner_id.state_id.name
                            if self.employee.user_id.partner_id.country_id:
                                address += "," + self.employee.user_id.partner_id.country_id.name
                            if self.employee.user_id.partner_id.zip:
                                address += "," + self.employee.user_id.partner_id.zip
                        partner_address = self.template.replace('employee_address', address)
                        self.template = partner_address
                if 'employee_street' in self.template:
                    street = self.template.replace('employee_street', self.employee.user_id.partner_id.street or '')
                    self.template = street
                if 'employee_stree2' in self.template:
                    street2 = self.template.replace('employee_street', self.employee.user_id.partner_id.street2 or '')
                    self.template = street2
                if 'employee_city' in self.template:
                    street = self.template.replace('employee_city', self.employee.user_id.partner_id.city or '')
                    self.template = street
                if 'employee_state' in self.template:
                    street = self.template.replace('employee_state',
                                                   self.employee.user_id.partner_id.state_id.name or '')
                    self.template = street
                if 'employee_country' in self.template:
                    country = self.template.replace('employee_country',
                                                    self.employee.user_id.partner_id.country_id.name or '')
                    self.template = country
                if 'employee_zip' in self.template:
                    zip = self.template.replace('employee_zip', self.employee.user_id.partner_id.zip or '')
                    self.template = zip
                if 'employee_email' in self.template:
                    email = self.template.replace('employee_email', self.employee.user_id.partner_id.email or '')
                    self.template = email
                if 'employee_mobile' in self.template:
                    mobile = self.template.replace('employee_mobile', self.employee.user_id.partner_id.mobile or '')
                    self.template = mobile
                if 'employee_phone' in self.template:
                    phone = self.template.replace('employee_phone', self.employee.user_id.partner_id.phone or '')
                    self.template = phone

                # Employee Personal Information
                if 'employee_job_title' in self.template:
                    job_title = self.template.replace('employee_job_title', self.employee.job_title or '')
                    self.template = job_title
                if 'employee_work_mobile' in self.template:
                    mobile_phone = self.template.replace('employee_work_mobile', self.employee.mobile_phone or '')
                    self.template = mobile_phone
                if 'employee_work_phone' in self.template:
                    work_phone = self.template.replace('employee_work_phone', self.employee.work_phone or '')
                    self.template = work_phone
                if 'employee_work_email' in self.template:
                    work_email = self.template.replace('employee_work_email', self.employee.work_email or '')
                    self.template = work_email
                if 'employee_work_location' in self.template:
                    work_location = self.template.replace('employee_work_location', self.employe.work_location or '')
                    self.template = work_location
                if 'department' in self.template:
                    department = self.template.replace('department', self.employee.department_id.name or '')
                    self.template = department
                if 'employeejob' in self.template:
                    employeejob = self.template.replace('employeejob', self.employee.job_id.name or '')
                    self.template = employeejob
                if 'employee_manager' in self.template:
                    employee_manager = self.template.replace('employee_manager', self.employee.parent_id.name or '')
                    self.template = employee_manager
                if 'employee_birthday' in self.template:
                    employee_birthday = self.template.replace('employee_birthday', str(self.employee.birthday) or '')
                    self.template = employee_birthday
                if 'employee_gender' in self.template:
                    employee_gender = self.template.replace('employee_gender',self.employee.gender or '')
                    self.template = employee_gender
                if 'employee_marital' in self.template:
                    employee_marital = self.template.replace('employee_marital',self.employee.marital or '')
                    self.template = employee_marital
               # if 'employee_id' in self.template:
               #     employee_id = self.template.replace('employee_id', self.employee.emp_id or '')
               #     self.template = employee_id
                if 'employee_idd' in self.template:
                    employee_idd = self.template.replace('employee_idd', self.employee.x_emp or '')
                    self.template = employee_idd
                if 'contract_wage' in self.template:
                    contract_wage = self.template.replace('contract_wage', str(self.employee.contract_id.wage) or '')
                    self.template = contract_wage
                    print(contract_wage)
                if 'contract_startdate' in self.template:
                    contract_startdate = self.template.replace('contract_startdate', str(self.employee.contract_id.date_start) or '')
                    self.template = contract_startdate
                if 'contract_enddate' in self.template:
                    contract_enddate = self.template.replace('contract_enddate', str(self.employee.contract_id.date_end) or '')
                    self.template = contract_enddate
                if 'contract_hra' in self.template:
                    contract_hra = self.template.replace('contract_hra', str(self.employee.contract_id.hra) or '')
                    self.template = contract_hra
                if 'contract_leaveallow' in self.template:
                    contract_leaveallow = self.template.replace('contract_leaveallow', str(self.employee.contract_id.x_leavellow) or '')
                    self.template = contract_leaveallow
                if 'contract_bonus' in self.template:
                    contract_bonus = self.template.replace('contract_bonus', str(self.employee.contract_id.x_bonus) or '')
                    self.template = contract_bonus
                if 'contract_pf' in self.template:
                    contract_pf = self.template.replace('contract_pf', str(self.employee.contract_id.x_pf) or '')
                    self.template = contract_pf
                if 'contract_esi' in self.template:
                    contract_esi = self.template.replace('contract_esi', str(self.employee.contract_id.x_esi) or '')
                    self.template = contract_esi
                if 'employee_company' in self.template:
                    employee_company = self.template.replace('employee_company', str(self.employee.company_id.name) or '')
                    self.template = employee_company

                if 'status_startdate' in self.template:
                    for record in self.employee:
                        for rec in record.stages_history:
                            if rec.state == 'employment':
                                status_startdate = self.template.replace('status_startdate',
                                                                         str(rec.start_date) or '')
                                self.template = status_startdate
                if 'status_enddate' in self.template:
                    for record in self.employee:
                        for rec in record.stages_history:
                            if rec.state == 'employment':
                                status_enddate = self.template.replace('status_enddate',
                                                                         str(rec.end_date) or '')
                                self.template = status_enddate
                if 'employee_resigndate' in self.template:
                    employee_resigndate = self.template.replace('employee_resigndate',
                                                             str(self.employee.resign_date) or '')
                    self.template = employee_resigndate
                if 'employee_family' in self.template:
                    for record in self.employee:
                        family = ''
                        for rec in record.fam_ids:
                            fam = rec.member_name
                            rel = rec.relation_id.name
                            family += fam
                            family += '-'
                            family += rel
                            family += '  '
                        employee_family = self.template.replace('employee_family',family or '')
                        self.template = employee_family
                if 'date' in self.template:
                    datee = self.template.replace('datee', str(self.date) or '')
                    self.template = datee
                if 'employee_uan' in self.template:
                    employee_uan = self.template.replace('employee_uan', self.employee.x_uan or '')
                    self.template = employee_uan
                if 'employee_nationalidentityno' in self.template:
                    employee_nationalidentityno = self.template.replace('employee_nationalidentityno', self.employee.x_nationalidentityno or '')
                    self.template = employee_nationalidentityno
                if 'employee_taxaccountno' in self.template:
                    employee_taxaccountno = self.template.replace('employee_taxaccountno', self.employee.x_taxaccountno or '')
                    self.template = employee_taxaccountno
                if 'employee_emp_cate' in self.template:
                    employee_emp_cate = self.template.replace('employee_emp_cate', self.employee.x_emp_cate.name or '')
                    self.template = employee_emp_cate
                if 'employee_acting_job' in self.template:
                    for record in self.employee:
                        job = ''
                        for rec in record.acting_job_ids:
                            j = rec.name
                            job += j
                            job += '  '
                        employee_acting_job = self.template.replace('employee_acting_job',job or '')
                        self.template = employee_acting_job
                if 'employee_esi' in self.template:
                    employee_esi = self.template.replace('employee_esi', self.employee.x_esi or '')
                    self.template = employee_esi
                if 'employee_epf' in self.template:
                    employee_epf = self.template.replace('employee_epf', self.employee.x_epf or '')
                    self.template = employee_epf
                if 'employee_related_user' in self.template:
                    employee_related_user = self.template.replace('employee_related_user', self.employee.user_id.name or '')
                    self.template = employee_related_user
                if 'employee_device_id' in self.template:
                    employee_device_id = self.template.replace('employee_device_id', self.employee.device_id or '')
                    self.template = employee_device_id
                if 'employee_pin' in self.template:
                    employee_pin = self.template.replace('employee_pin', self.employee.pin or '')
                    self.template = employee_pin
                if 'employee_badge' in self.template:
                    employee_badge = self.template.replace('employee_badge', self.employee.barcode or '')
                    self.template = employee_badge
                if 'employee_bank' in self.template:
                    employee_bank = self.template.replace('employee_bank', self.employee.bank_account_id.name or '')
                    self.template = employee_bank
                if 'employee_km_home_work' in self.template:
                    employee_km_home_work = self.template.replace('employee_km_home_work', self.employee.km_home_work or '')
                    self.template = employee_km_home_work
                if 'employee_passport' in self.template:
                    employee_passport = self.template.replace('employee_passport', self.employee.passport_id or '')
                    self.template = employee_passport
                if 'employeepassport_expiry_date' in self.template:
                    employeepassport_expiry_date = self.template.replace('employeepassport_expiry_date', self.employee.passport_expiry_date or '')
                    self.template = employeepassport_expiry_date
                if 'employee_emergency_contact' in self.template:
                    employee_emergency_contact = self.template.replace('employee_emergency_contact', self.employee.emergency_contact or '')
                    self.template = employee_emergency_contact
                if 'employee_emergency_phone' in self.template:
                    employee_emergency_phone = self.template.replace('employee_emergency_phone', self.employee.emergency_phone or '')
                    self.template = employee_emergency_phone
                if 'employee_certificate' in self.template:
                    employee_certificate = self.template.replace('employee_certificate', self.employee.certificate or '')
                    self.template = employee_certificate
                if 'employee_study_field' in self.template:
                    employee_study_field = self.template.replace('employee_study_field', self.employee.study_field or '')
                    self.template = employee_study_field
                if 'employee_study_school' in self.template:
                    employee_study_school = self.template.replace('employee_study_school', self.employee.study_school or '')
                    self.template = employee_study_school
                if 'employee_identification_id' in self.template:
                    employee_identification_id = self.template.replace('employee_identification_id', self.employee.identification_id or '')
                    self.template = employee_identification_id
                if 'employee_id_expiry_date' in self.template:
                    employee_id_expiry_date = self.template.replace('employee_id_expiry_date', self.employee.id_expiry_date or '')
                    self.template = employee_id_expiry_date
                if 'employee_place_of_birth'in self.template:
                    employee_place_of_birth = self.template.replace('employee_place_of_birth', self.employee.place_of_birth or '')
                    self.template = employee_place_of_birth
                if 'employeecountry_of_birth'in self.template:
                    employeecountry_of_birth = self.template.replace('employeecountry_of_birth', self.employee.country_of_birth.name or '')
                    self.template = employeecountry_of_birth
                if 'employee_children'in self.template:
                    employee_children = self.template.replace('employee_children', self.employee.children or '')
                    self.template = employee_children
                if 'employee_visa_no'in self.template:
                    employee_visa_no = self.template.replace('employee_visa_no', self.employee.visa_no or '')
                    self.template = employee_visa_no
                if 'employee_permit_no'in self.template:
                    employee_permit_no = self.template.replace('employee_permit_no', self.employee.permit_no or '')
                    self.template = employee_permit_no
                if 'employee_visa_expire'in self.template:
                    employee_visa_expire = self.template.replace('employee_visa_expire', str(self.employee.visa_expire) or '')
                    self.template = employee_visa_expire

                if 'contract_wrk_days'in self.template:
                    contract_wrk_days = self.template.replace('contract_wrk_days', str(self.employee.contract_id.x_days) or '')
                    self.template = contract_wrk_days
                if 'contract_present_days'in self.template:
                    contract_present_days = self.template.replace('contract_present_days', str(self.employee.contract_id.x_pr) or '')
                    self.template = contract_present_days
                if 'contract_fixed_wage'in self.template:
                    contract_fixed_wage = self.template.replace('contract_fixed_wage', self.employee.contract_id.x_wage or '')
                    self.template = contract_fixed_wage
                if 'contractwage_type'in self.template:
                    contractwage_type = self.template.replace('contractwage_type', self.employee.contract_id.wage_type or '')
                    self.template = contractwage_type
                if 'contract_vacationallowance'in self.template:
                    contract_vacationallowance = self.template.replace('contract_vacationallowance', str(self.employee.contract_id.x_vacationallowance) or '')
                    self.template = contract_vacationallowance
                if 'contract_attbonus'in self.template:
                    contract_attbonus = self.template.replace('contract_attbonus', str(self.employee.contract_id.x_attbonus) or '')
                    self.template = contract_attbonus
                if 'contract_daywage'in self.template:
                    contract_daywage = self.template.replace('contract_daywage', str(self.employee.contract_id.over_day) or '')
                    self.template = contract_daywage
                if 'contract_hourwage'in self.template:
                    contract_hourwage = self.template.replace('contract_hourwage', str(self.employee.contract_id.over_hour) or '')
                    self.template = contract_hourwage
                if 'contract_da'in self.template:
                    contract_da = self.template.replace('contract_da', str(self.employee.contract_id.da) or '')
                    self.template = contract_da
                if 'contract_travel_allowance'in self.template:
                    contract_travel_allowance = self.template.replace('contract_travel_allowance', str(self.employee.contract_id.travel_allowance) or '')
                    self.template = contract_travel_allowance
                if 'contract_busfare'in self.template:
                    contract_busfare = self.template.replace('contract_busfare', str(self.employee.contract_id.x_busfare) or '')
                    self.template = contract_busfare
                if 'contract_meal_allowance'in self.template:
                    contract_meal_allowance = self.template.replace('contract_meal_allowance', str(self.employee.contract_id.meal_allowance) or '')
                    self.template = contract_meal_allowance
                if 'contract_uniformallow' in self.template:
                    contract_uniformallow = self.template.replace('contract_uniformallow', str(self.employee.contract_id.x_uniformallow) or '')
                    self.template = contract_uniformallow
                if 'contract_medical_allowance'in self.template:
                    contract_medical_allowance = self.template.replace('contract_medical_allowance', str(self.employee.contract_id.medical_allowance) or '')
                    self.template = contract_medical_allowance
                if 'contract_internetallow' in self.template:
                    contract_internetallow = self.template.replace('contract_internetallow', str(self.employee.contract_id.x_internetallow) or '')
                    self.template = contract_internetallow
                if 'contract_mobileallow' in self.template:
                    contract_mobileallow = self.template.replace('contract_mobileallow', str(self.employee.contract_id.x_mobileallow) or '')
                    self.template = contract_mobileallow
                if 'contract_maternityallow' in self.template:
                    contract_maternityallow = self.template.replace('contract_maternityallow', str(self.employee.contract_id.x_maternityallow) or '')
                    self.template = contract_maternityallow
                if 'contract_other_allowance'in self.template:
                    contract_other_allowance = self.template.replace('contract_other_allowance', str(self.employee.contract_id.other_allowance) or '')
                    self.template = contract_other_allowance
                if 'contract_pt'in self.template:
                    contract_pt = self.template.replace('contract_pt', str(self.employee.contract_id.x_pt) or '')
                    self.template = contract_pt
                if 'contract_food'in self.template:
                    contract_food = self.template.replace('contract_food', str(self.employee.contract_id.x_food) or '')
                    self.template = contract_food
                if 'contract_trial_end_date'in self.template:
                    contract_trial_end_date = self.template.replace('contract_trial_end_date', str(self.employee.contract_id.trial_date_end) or '')
                    self.template = contract_trial_end_date
                

                template = TAG_RE.sub('\n', self.template)
                self.template_value = template

    def send_email(self):
        self.ensure_one()
        ir_model_data = self.env['ir.model.data']
        try:
            template_id = ir_model_data.get_object_reference('letters_and_certificate_app', 'email_template_letters')[1]
        except ValueError:
            template_id = False
        try:
            compose_form_id = ir_model_data.get_object_reference('mail', 'email_compose_message_wizard_form')[1]
        except ValueError:
            compose_form_id = False
        lang = self.env.context.get('lang')
        template = template_id and self.env['mail.template'].browse(template_id)
        if template and template.lang:
            lang = template._render_template(template.lang, 'letters', self.ids[0])
        ctx = {
            'default_model': 'letters',
            'default_res_id': self.ids[0],
            'default_use_template': bool(template_id),
            'default_template_id': template_id,
            'default_composition_mode': 'comment',
            'mark_so_as_sent': True,
            'force_email': True
        }
        return {
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'mail.compose.message',
            'views': [(compose_form_id, 'form')],
            'view_id': compose_form_id,
            'target': 'new',
            'context': ctx,
        }


class Template(models.Model):
    _name = 'template'
    _description = 'Template'
    _rec_name = 'template_name'

    template_name = fields.Char('Template Name')
    template = fields.Html()
    letter_type = fields.Selection([('partner', 'Partner'), ('employee', 'Employee')], string='Base On',
                                   default="partner", required=True)



