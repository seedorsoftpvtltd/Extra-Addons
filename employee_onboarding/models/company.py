# -*- coding: utf-8 -*-

from datetime import timedelta, datetime
import calendar
from dateutil.relativedelta import relativedelta

from odoo import fields, models, api, _
from odoo.exceptions import ValidationError, UserError, RedirectWarning
from odoo.tools.misc import DEFAULT_SERVER_DATE_FORMAT, format_date
from odoo.tools.float_utils import float_round, float_is_zero
from odoo.tools import date_utils
from odoo.tests.common import Form


class HrEmployee(models.Model):
    _inherit = "res.company"

    def get_employee_dashboard_onboarding_steps_states_names(self):

        return [
            'onboarding_step1_state',
            'onboarding_step2_state',
            'onboarding_step3_state',
            'onboarding_step4_state',
            'onboarding_step5_state',
        ]

    def get_and_update_onbarding_state(self, onboarding_state, steps_states):
        old_values = {}
        all_done = True
        for step_state in steps_states:
            old_values[step_state] = self[step_state]
            if self[step_state] == 'just_done':
                self[step_state] = 'done'
            all_done = all_done and self[step_state] == 'done'

        if all_done:
            if self[onboarding_state] == 'not_done':
                old_values['onboarding_state'] = 'just_done'
            else:
                old_values['onboarding_state'] = 'done'
            self[onboarding_state] = 'done'
        return old_values

    onboarding_step1_state = fields.Selection([
        ('not_done', "Not done"), ('just_done', "Just done"), ('done', "Done")],
        string="State of the step1", default='not_done')
    onboarding_step2_state = fields.Selection([('not_done', "Not done"), ('just_done', "Just done"), ('done', "Done")],
                                              string="State of the step2", default='not_done')
    onboarding_step3_state = fields.Selection([('not_done', "Not done"), ('just_done', "Just done"), ('done', "Done")],
                                              string="State of the step3", default='not_done')
    onboarding_step4_state = fields.Selection([('not_done', "Not done"), ('just_done', "Just done"), ('done', "Done")],
                                              string="State of the step4", default='not_done')
    onboarding_step5_state = fields.Selection([('not_done', "Not done"), ('just_done', "Just done"), ('done', "Done")],
                                              string="State of the step5", default='not_done')
    account_onboarding_employee_layout_state = fields.Selection(
        [('not_done', "Not done"), ('just_done', "Just done"), ('done', "Done")],
        string="State of the onboarding invoice layout step", default='not_done')
    account_onboarding_sample_invoice_state = fields.Selection(
        [('not_done', "Not done"), ('just_done', "Just done"), ('done', "Done")],
        string="State of the onboarding sample invoice step", default='not_done')
    account_onboarding_sale_tax_state = fields.Selection(
        [('not_done', "Not done"), ('just_done', "Just done"), ('done', "Done")],
        string="State of the onboarding sale tax step", default='not_done')

    # account_invoice_onboarding_state = fields.Selection(
    #     [('not_done', "Not done"), ('just_done', "Just done"), ('done', "Done"), ('closed', "Closed")],
    #     string="State of the account invoice onboarding panel", default='not_done')
    employee_dashboard_onboarding_state = fields.Selection(
        [('not_done', "Not done"), ('just_done', "Just done"), ('done', "Done"), ('closed', "Closed")],
        string="State of the account dashboard onboarding panel", default='not_done')

    @api.model
    def onboarding_step_action(self):
        idd = self.env.ref('hr.view_department_tree').id
        company = self.env.company
        # company.sudo().set_onboarding_step_done('onboarding_step1_state')
        return {
            'type': 'ir.actions.act_window',
            'name': _('Departments'),
            'res_model': 'hr.department',
            'view_mode': 'tree',
            'limit': 99999999,
            'views': [[False, 'kanban'], [False, 'list'], [False, 'form']],
        }

    @api.model
    def onboarding_step1_action(self):
        company = self.env.company
        # company.sudo().set_onboarding_step_done('onboarding_step2_state')
        return {
            'type': 'ir.actions.act_window',
            'name': _('Job Positions'),
            'res_model': 'hr.job',
            'view_mode': 'form',
            # 'limit': 99999999,
            'views': [[False, 'form']],
        }

    @api.model
    def onboarding_step3_action(self):
        company = self.env.company
        # company.sudo().set_onboarding_step_done('onboarding_step3_state')
        id = self.env['hr.employee']
        return {
            'type': 'ir.actions.act_window',
            'name': _('Employee'),
            'res_model': 'hr.employee',
            'view_mode': 'form',
            # 'limit': 99999999,
            'views': [[False, 'form']],
        }

    @api.model
    def onboarding_step4_action(self):
        company = self.env.company
        menu_id = self.env.ref('hr.menu_hr_root').id
        print(menu_id)
        return {
            'type': 'ir.actions.act_window',
            'name': _('Import'),
            'res_model': 'hr.document',
            'view_mode': 'kanban',
            'limit': 99999999,
            'views': [[False, 'kanban'],[False, 'tree'],[False, 'form']],
        }

    @api.model
    def onboarding_step5_action(self):
        company = self.env.company
        # company.sudo().set_onboarding_step_done('onboarding_step3_state')
        id = self.env['hr.employee']
        return {
            'type': 'ir.actions.act_window',
            'name': _('Import Googlesheet'),
            'res_model': 'google.spreadsheet.import',
            'view_mode': 'kanban',
            'domain': [('document_sheet', '=', 'hr.employee'),('name','=','Bulk Employee Import')],
            'limit': 99999999,
            'views': [[False, 'kanban'],[False, 'tree'],[False, 'form']],
        }

    @api.model
    def onboarding_step6_action(self):
        company = self.env.company
        # company.sudo().set_onboarding_step_done('onboarding_step4_state')
        return {
            'type': 'ir.actions.act_window',
            'name': _('Assign'),
            'res_model': 'hr.contract',
            'view_mode': 'form',
            # 'limit': 99999999,
            'views': [[False, 'form'],[False, 'list']],
        }

    @api.model
    def onboarding_step7_action(self):
        company = self.env.company
        # company.sudo().set_onboarding_step_done('onboarding_step5_state')
        return {
            'type': 'ir.actions.act_window',
            'name': _('Shift'),
            'res_model': 'resource.calendar',
            'view_mode': 'tree',
            'limit': 99999999,
            'views': [[False, 'list'], [False, 'form'],],
        }
    @api.model
    def onboarding_step8_action(self):
        company = self.env.company
        # company.sudo().set_onboarding_step_done('onboarding_step5_state')
        return {
            'type': 'ir.actions.act_window',
            'name': _('Review'),
            'res_model': 'hr.payroll.structure',
            'view_mode': 'tree',
            'limit': 99999999,
            'views': [[False, 'list'], [False, 'form'], [False, 'activity']],
        }

    @api.model
    def onboarding_step9_action(self):
        company = self.env.company
        # company.sudo().set_onboarding_step_done('onboarding_step5_state')
        return {
            'type': 'ir.actions.act_window',
            'name': _('Allocate'),
            'res_model': 'hr.leave.allocation',
            'view_mode': 'tree',
            'limit': 99999999,
            'views': [[False, 'list'], [False, 'form'], [False, 'activity']],
        }


    def get_and_update_employee_dashboard_onboarding_state(self):
        return self.get_and_update_onbarding_state(
            'employee_dashboard_onboarding_state',
            self.get_employee_dashboard_onboarding_steps_states_names()
        )

    @api.model
    def onboarding_step1_count(self):
        emp_dept_count = self.env['hr.department'].sudo().search_count([])
        print(emp_dept_count)
        return emp_dept_count

    @api.model
    def onboarding_step2_count(self):
        emp_job_count = self.env['hr.job'].sudo().search_count([])
        print(emp_job_count)
        return emp_job_count

    @api.model
    def onboarding_step3_count(self):
        emp_count = self.env['hr.employee'].sudo().search_count([])
        print(emp_count)
        return emp_count

    @api.model
    def onboarding_step4_count(self):
        emp_contract_count = self.env['hr.contract'].sudo().search_count([])
        print(emp_contract_count)
        return emp_contract_count

    @api.model
    def onboarding_step5_count(self):
        emp_leave_alloc_count = self.env['hr.leave.allocation'].sudo().search_count([])
        print(emp_leave_alloc_count)
        return emp_leave_alloc_count


