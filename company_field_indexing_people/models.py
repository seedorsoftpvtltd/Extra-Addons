from odoo import models, fields, api


class Contract(models.Model):
    _inherit = 'hr.contract'

    employee_id = fields.Many2one('hr.employee', string='Employee', tracking=True, index=True,
                                  domain="['|', ('company_id', '=', False), ('company_id', '=', company_id)]")

    company_id = fields.Many2one('res.company', default=lambda self: self.env.company, required=True, index=True)

class AccountAnalyticLine(models.Model):
    _inherit = 'account.analytic.line'

    employee_id = fields.Many2one('hr.employee', "Employee", index=True)
    project_id = fields.Many2one('project.project', 'Project',index=True, domain=[('allow_timesheets', '=', True)])

class HrAttendance(models.Model):
    _inherit = "hr.attendance"

    department_id = fields.Many2one('hr.department', string="Department", related="employee_id.department_id",index=True,
        readonly=True)

class HolidaysRequest(models.Model):

    _inherit = "hr.leave"

    department_id = fields.Many2one(
        'hr.department', string='Department', readonly=True, index=True,
        states={'draft': [('readonly', False)], 'confirm': [('readonly', False)]})

    mode_company_id = fields.Many2one(
        'res.company', string='Company', readonly=True, index=True,
        states={'draft': [('readonly', False)], 'confirm': [('readonly', False)]})

class HolidaysAllocation(models.Model):

    _inherit = "hr.leave.allocation"

    department_id = fields.Many2one(
        'hr.department', string='Department', readonly=True, index=True,
        states={'draft': [('readonly', False)], 'confirm': [('readonly', False)]})

    mode_company_id = fields.Many2one(
        'res.company', string='Company', readonly=True, index=True,
        states={'draft': [('readonly', False)], 'confirm': [('readonly', False)]})


class HrExpense(models.Model):

    _inherit = "hr.expense"

    company_id = fields.Many2one('res.company', string='Company', required=True, readonly=True,index=True,
                                 states={'draft': [('readonly', False)], 'refused': [('readonly', False)]},
                                 default=lambda self: self.env.company)