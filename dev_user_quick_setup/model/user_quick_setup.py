# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2015 DevIntelle Consulting Service Pvt.Ltd (<http://www.devintellecs.com>).
#
#    For Module Support : devintelle@gmail.com  or Skype : devintelle
#
##############################################################################

from odoo import models, fields, api


class user_quick_setup(models.Model):
    _name = 'user.quick.setup'
    _description = 'User Quick Setup'

    name = fields.Char(string='Name', required=True)
    u_email = fields.Char('Email Address', required=True)
    u_company_id = fields.Many2one('res.company', 'Company', default=lambda self: self.env.user.company_id, required=True)
    state = fields.Selection([('draft', 'Draft'), ('process', 'Process'), ('confirm', 'Confirmed')], string='State', default='draft')

    # employee information
    employee_create_flag = fields.Boolean(string='Create Employee')
    work_address = fields.Many2one('res.partner', string='Work Address', readonly=True)

    work_email = fields.Char(string='Work Email')
    work_mobile = fields.Char(string='Work Mobile')
    department_id = fields.Many2one('hr.department', string='Department')
    job_id = fields.Many2one('hr.job', string='Job Position')
    parent_id = fields.Many2one('hr.employee', string='Manager')
    working_hour = fields.Many2one('resource.calendar', string='Working Hours', default=lambda self: self.env['res.company']._company_default_get().resource_calendar_id, )
    timesheet_cost = fields.Float(string='Timesheet Cost')

    # contract information
    contract_create_flag = fields.Boolean(string='Create Contract')
    contract_name = fields.Char(string='Contract Name')
#    contract_type = fields.Many2one('hr.contract.type', string='Contract Type')
    structure_id = fields.Many2one('hr.payroll.structure', string='Salary Structure')

    wage = fields.Float(string="Wage", required=True)
    start_date = fields.Date(string="Start Date")
    end_date = fields.Date(string="End Date")

    # leave allocation
    leave_allocation_flag = fields.Boolean(string='Leave Allocation')
    leave_allocation_line = fields.One2many('leave.allocation.line', 'line_id', string='Leave Allocation')

    d_user_id = fields.Many2one('res.users', string='User', copy=False)
    d_employee_id = fields.Many2one('hr.employee', string='Employee', copy=False)
    d_contract_id = fields.Many2one('hr.contract', string='Contract', copy=False)

    def action_view_user(self):
        action = self.env.ref('base.action_res_users').read()[0]
        user = self.mapped('d_user_id')
        if len(user) > 1:
            action['domain'] = [('id', 'in', user.ids)]
        elif user:
            action['views'] = [(self.env.ref('base.view_users_form').id, 'form')]
            action['res_id'] = user.id
        return action

    @api.onchange('employee_create_flag')
    def onchange_employee_create_flag(self):
        if self.employee_create_flag == False:
            self.contract_create_flag = False
            self.leave_allocation_flag = False

    def action_view_employee(self):
        action = self.env.ref('hr.open_view_employee_list_my').read()[0]

        employee = self.mapped('d_employee_id')
        if len(employee) > 1:
            action['domain'] = [('id', 'in', employee.ids)]
        elif employee:
            action['views'] = [(self.env.ref('hr.view_employee_form').id, 'form')]
            action['res_id'] = employee.id
        return action

    def action_view_contract(self):
        action = self.env.ref('hr_contract.action_hr_contract').read()[0]

        contract = self.mapped('d_contract_id')
        if len(contract) > 1:
            action['domain'] = [('id', 'in', contract.ids)]
        elif contract:
            action['views'] = [(self.env.ref('hr_contract.hr_contract_view_form').id, 'form')]
            action['res_id'] = contract.id
        return action

    @api.onchange('name')
    def onchange_name(self):
        for data in self:
            name = str(data.name) + " Contract"
            data.contract_name = name

    @api.onchange('department_id')
    def onchange_department(self):
        for data in self:
            if data.department_id:
                data.parent_id = data.department_id.manager_id and data.department_id.manager_id.id or False

    def make_url(self):
        record_id = self.id
        model_name = 'user.quick.setup'
        menu_id = self.env.ref('dev_user_quick_setup.user_setup_menu_id').id
        action_id = self.env.ref('dev_user_quick_setup.action_user_quick_setup').id
        ir_param = self.env['ir.config_parameter'].sudo()
        base_url = ir_param.get_param('web.base.url')
        if base_url:
            base_url += \
                '/web?#id=%s&action=%s&model=%s&view_type=form&menu_id=%s' \
                % (record_id, action_id, model_name, menu_id)
        return base_url

    def action_process(self):
        acces_user = self.env.ref('dev_user_quick_setup.allow_quick_setup_confirm')
        acces_users = self.env['res.users'].search([('groups_id', '=', acces_user.id)])
        if acces_users:
            for au_user in acces_users:
                ir_model_data = self.env['ir.model.data']
                mail_template_id = ir_model_data.get_object_reference('dev_user_quick_setup', 'approve_user_setup_id')
                mtp = self.env['mail.template']
                mail_tem = mtp.browse(mail_template_id[1])
                mail_tem.write({'email_to': au_user.partner_id.email})
                mail_tem.send_mail(self.ids[0], True)
        self.write({'state': 'process'})

    def action_confirm(self):
        user_id = self.env['res.users'].create({'name': self.name,
                                                'login': self.u_email,
                                                'company_id': self.u_company_id.id
                                                })
        self.d_user_id = user_id.id
        print ("user_id========",user_id)
        employee_id = []
        if user_id and user_id.partner_id:
            user_id.partner_id.email = self.u_email
            print ("user_id====sss====",user_id)
            user_id.action_reset_password()
            print ("user_id========",user_id)
        if user_id and self.employee_create_flag:
            employee_work_address = False
            if user_id.company_id and user_id.company_id.partner_id:
                self.work_address = user_id.company_id.partner_id or False
                self.employee_work_address = user_id.company_id.partner_id or False
            employee_id = self.env['hr.employee'].create(
                {'name': self.name,
                 'address_id': self.work_address and self.work_address.id or False,
                 'work_email': self.work_email, 'work_phone': self.work_mobile,
                 'department_id': self.department_id and self.department_id.id or False,
                 'job_id': self.job_id and self.job_id.id or False,
                 'parent_id': self.parent_id and self.parent_id.id or False,
                 'resource_calendar_id': self.working_hour and self.working_hour.id or False,
                 'company_id': self.u_company_id.id,
                 'user_id': user_id.id,
                 # 'work_address': self.employee_work_address,
                 'timesheet_cost': self.timesheet_cost
                 })
            self.d_employee_id = employee_id.id
            print ("d_employee_id========",self.d_employee_id)
        if employee_id and self.contract_create_flag:
            contract_id = self.env['hr.contract'].create({'name': self.contract_name,
                                                          'employee_id': employee_id and employee_id.id or False,
                                                          'department_id': employee_id and employee_id.department_id and employee_id.department_id.id or False,
                                                          'job_id': employee_id and employee_id.job_id and employee_id.job_id.id or False,
                                                          'struct_id': self.structure_id.id,
                                                          'wage': self.wage,
                                                          'date_start': self.start_date,
                                                          'date_end': self.end_date,
                                                          'resource_calendar_id': self.working_hour.id,
                                                          'trial_date_end': self.end_date,
                                                          'state': 'draft'

                                                          })
            self.d_contract_id = contract_id.id
            print ("d_contract_id========",self.d_contract_id)
        if self.leave_allocation_flag:
            if self.leave_allocation_line:
                for line in self.leave_allocation_line:
                    leave_allocation_id = self.env['hr.leave.allocation'].create(
                        {'name': line.l_name, 'holiday_status_id': line.type.id,
                         'number_of_days': line.duration,
                         'employee_id': employee_id and employee_id.id or False
                         })
                    leave_allocation_id.action_approve()
                    print ("leave_allocation_id========",leave_allocation_id)
        self.write({'state': 'confirm'})


class leave_allocation(models.Model):
    _name = 'leave.allocation.line'
    _description = 'User Quick Setup Line'

    line_id = fields.Many2one('user.quick.setup', string="Line")
    l_name = fields.Char(string='Description', required=True)
    type = fields.Many2one('hr.leave.type', string='Leave Type', required=True)
    duration = fields.Float(string='Duration')

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
