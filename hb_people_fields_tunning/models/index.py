from odoo.http import request
from odoo import api, fields, models, tools, osv, http, _


class HrEmployee(models.Model):
    _inherit = "hr.employee"

    parent_id = fields.Many2one('hr.employee', 'Manager',
                                domain="['|', ('company_id', '=', False), ('company_id', '=', company_id)]", index=True)


class HrAttendance(models.Model):
    _inherit = "hr.attendance"

    def _default_employee(self):
        return self.env.user.employee_id

    employee_id = fields.Many2one('hr.employee', string="Employee", default=_default_employee, required=True,
                                  ondelete='cascade', index=True)
    check_in = fields.Datetime(string="Check In", default=fields.Datetime.now, required=True, index=True)
    check_out = fields.Datetime(string="Check Out", index=True)
    state = fields.Selection([('draft', 'Draft'),
                              ('validated', 'Validated'),
                              ('approved', 'Approved'),
                              ('refused', 'Refused')], string="state",
                             default="draft", index=True)


class HrOvertime(models.Model):
    _inherit = "hr.overtime"

    def _get_employee_domain(self):
        employee = self.env['hr.employee'].search(
            [('user_id', '=', self.env.user.id)], limit=1)
        domain = [('id', '=', employee.id)]
        if self.env.user.has_group('hr.group_hr_user'):
            domain = []
        return domain

    date_from = fields.Datetime('Date From', index=True)
    date_to = fields.Datetime('Date to', index=True)
    employee_id = fields.Many2one('hr.employee', string='Employee',
                                  domain=_get_employee_domain, default=lambda self: self.env.user.employee_id.id,
                                  required=True, index=True)
    state = fields.Selection([('draft', 'Draft'),
                              ('f_approve', 'Waiting'),
                              ('approved1', 'First Level Approved'),
                              ('approved', 'Approved'),
                              ('refused', 'Refused')], string="state",
                             default="draft", index=True)


class HrTimeoff(models.Model):
    _inherit = "hr.leave"

    date_to = fields.Datetime(
        'End Date', readonly=True, copy=False, required=True,
        default=fields.Datetime.now,
        states={'draft': [('readonly', False)], 'confirm': [('readonly', False)]}, tracking=True, index=True)
    state = fields.Selection([
        ('draft', 'To Submit'),
        ('cancel', 'Cancelled'),  # YTI This state seems to be unused. To remove
        ('confirm', 'To Approve'),
        ('refuse', 'Refused'),
        ('validate1', 'Second Approval'),
        ('validate', 'Approved')
    ], string='Status', readonly=True, tracking=True, copy=False, default='draft',
        help="The status is set to 'To Submit', when a time off request is created." +
             "\nThe status is 'To Approve', when time off request is confirmed by user." +
             "\nThe status is 'Refused', when time off request is refused by manager." +
             "\nThe status is 'Approved', when time off request is approved by manager.", index=True)


class HrAppraisalFormext(models.Model):
    _inherit = 'hr.appraisal'

    response_id = fields.Many2one('survey.user_input', "Response", ondelete="set null")