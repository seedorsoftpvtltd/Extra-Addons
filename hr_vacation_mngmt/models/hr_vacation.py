# -*- coding: utf-8 -*-

from datetime import datetime, timedelta, date
from odoo import models, fields, api, _
from odoo.exceptions import UserError


class LeaveValidationStatus(models.Model):
    """ Model for leave validators and their status for each leave request """
    _inherit = 'leave.validation.status'

    holiday_status = fields.Many2one('hr.leave')
    validating_users = fields.Many2one('res.users', string='Leave Validators', help="Leave validators",
                                       domain="[('share','=',False)]")


class HrLeaveRequest(models.Model):
    _inherit = 'hr.leave'

    remaining_leaves = fields.Float(string='Remaining Legal Leaves', related='employee_id.remaining_leaves',
                                    help="Remaining legal leaves")
    overlapping_leaves = fields.Many2many('hr.leave', compute='get_overlapping_leaves', string='Overlapping Leaves',
                                          help="Overlapping leaves")
    pending_tasks = fields.One2many('pending.task', 'leave_id', string='Pending Tasks', help="Pending tasks")
    holiday_managers = fields.Many2many('res.users', compute='get_hr_holiday_managers', help="Holiday managers")
    flight_ticket = fields.One2many('hr.flight.ticket', 'leave_id', string='Flight Ticket', help="Flight ticket")
    # Commented for odoo 13 compatibility
    # double_validation = fields.Boolean(string='Apply Double Validation', related='holiday_status_id.double_validation')
    expense_account = fields.Many2one('account.account')
    leave_salary = fields.Selection([('0', 'Basic'), ('1', 'Gross')], string='Leave Salary')
    validation_type = fields.Selection('hr.leave.type', String='Validation')

    def get_overlapping_leaves(self):
        for rec in self:
            if rec.date_from and rec.date_to:
                overlap_leaves = []
                from_date = rec.date_from
                to_date = rec.date_to
                r = (to_date + timedelta(days=1) - from_date).days
                leave_dates = [str(from_date + timedelta(days=i)) for i in range(r)]
                leaves = rec.env['hr.leave'].search([('state', '=', 'validate'),
                                                     ('department_id', '=', rec.department_id.id)])
                other_leaves = leaves - rec
                for leave in other_leaves:
                    frm_dte = leave.date_from
                    to_dte = leave.date_to
                    r = (to_dte + timedelta(days=1) - frm_dte).days
                    leave_dtes = [str(frm_dte + timedelta(days=i)) for i in range(r)]
                    if set(leave_dtes).intersection(set(leave_dates)):
                        overlap_leaves.append(leave.id)
                rec.update({'overlapping_leaves': [(6, 0, overlap_leaves)]})

    #    def get_overlapping_leaves(self):
    #        self.ensure_one()
    #        if self.date_from and self.date_to:
    #            overlap_leaves = []
    #            from_date = self.date_from
    #            to_date = self.date_to
    #            r = (to_date + timedelta(days=1) - from_date).days
    #            leave_dates = [str(from_date + timedelta(days=i)) for i in range(r)]
    #            leaves = self.env['hr.leave'].search([('state', '=', 'validate'),
    #                                                     ('department_id', '=', self.department_id.id)])
    #            other_leaves = leaves - self
    #            for leave in other_leaves:
    #                frm_dte = leave.date_from
    #                to_dte = leave.date_to
    #                r = (to_dte + timedelta(days=1) - frm_dte).days
    #                leave_dtes = [str(frm_dte + timedelta(days=i)) for i in range(r)]
    #                if set(leave_dtes).intersection(set(leave_dates)):
    #                    overlap_leaves.append(leave.id)
    #            self.update({'overlapping_leaves': [(6, 0, overlap_leaves)]})

    def action_approve(self):
        # line 66 to 83 additional code for multi approval
        print(self)
        for rec in self:
            if rec.validation_type == "multi":
                print("multi")
                li = []
                if self.env.context.get('active_id'):
                    active_id = self.env.context.get('active_id')
                else:
                    active_id = self.id
                user = self.env['hr.leave'].search([('id', '=', active_id)])
                for user_obj in user.leave_approvals:
                    li.append(user_obj.validating_users.id)
                if self.env.uid in li:
                    validation_obj = user.leave_approvals.search(
                        [('holiday_status', '=', user.id),
                         ('validating_users', '=', self.env.uid)])
                    if validation_obj.validation_status == True:
                        raise UserError(_('Approval already done!'))
                # if validation_type == 'both':
                #  if validation_type != 'both':
                if any(holiday.state != 'confirm' for holiday in self):
                    raise UserError(_(
                        'Leave request must be confirmed ("To Approve") in order to approve it.'))

                current_employee = self.env['hr.employee'].search(
                    [('user_id', '=', self.env.uid)])
                ohrmspro_vacation_project = self.sudo().env['ir.module.module'].search(
                    [('name', '=', 'ohrmspro_vacation_project')],
                    limit=1).state

                if ohrmspro_vacation_project == 'installed':
                    return self.env['hr.leave'].check_pending_task(self)
                else:
                    return self.approval_check()

            elif not self.env.user.has_group('hr_holidays.group_hr_holidays_user'):
                raise UserError(_('Only an HR Officer or Manager can approve leave requests.'))
            print("hello")

        manager = self.env['hr.employee'].search([('user_id', '=', self.env.uid)])
        for holiday in self:
            if holiday.state != 'confirm':
                raise UserError(_('Leave request must be confirmed ("To Approve") in order to approve it.'))

            if holiday.pending_tasks:
                if holiday.user_id:
                    ctx = dict(self.env.context or {})
                    ctx.update({
                        'default_leave_req_id': self.id,
                    })
                    return {
                        'name': _('Re-Assign Task'),
                        'type': 'ir.actions.act_window',
                        'view_mode': 'form',
                        'res_model': 'task.reassign',
                        'target': 'new',
                        'context': ctx,
                    }
            else:
                if holiday:
                    print(holiday)
                    if holiday.validation_type == "both":
                        # return holiday.write({'state': 'validate1', 'manager_id': manager.id if manager else False})
                        holiday.write({'state': 'validate1'})
                    elif holiday.validation_type == "hr" or "manager":
                        holiday.write({'state': 'validate'})
                else:
                    holiday.action_validate()

    def book_ticket(self):
        if not self.env.user.has_group('hr_holidays.group_hr_holidays_user'):
            raise UserError(_('Only an HR Officer or Manager can book flight tickets.'))
        ctx = dict(self.env.context or {})
        ctx.update({
            # 'default_employee_id': self.employee_id.id,
            'default_leave_id': self.id,
        })

        return {
            'name': _('Book Flight Ticket'),
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'view_id': self.env.ref('hr_vacation_mngmt.view_hr_book_flight_ticket_form').id,
            'res_model': 'hr.flight.ticket',
            'target': 'new',
            'context': ctx,
        }

    def get_hr_holiday_managers(self):
        self.holiday_managers = self.env.ref('hr_holidays.group_hr_holidays_manager').users

    def view_flight_ticket(self):
        return {
            'name': _('Flight Ticket'),
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'hr.flight.ticket',
            'target': 'current',
            'res_id': self.flight_ticket[0].id,
        }

    @api.model
    def send_leave_reminder(self):
        leave_request = self.env['hr.leave'].search([('state', '=', 'validate')])
        leave_reminder = self.env['ir.config_parameter'].sudo().get_param('leave_reminder')
        reminder_day_before = int(self.env['ir.config_parameter'].sudo().get_param('reminder_day_before'))
        mail_template = self.env.ref('hr_vacation_mngmt.email_template_hr_leave_reminder_mail')
        holiday_managers = self.env.ref('hr_holidays.group_hr_holidays_manager').users
        today = date.today()
        if leave_reminder:
            for request in leave_request:
                if request.date_from:
                    from_date = request.date_from
                    if reminder_day_before == 0:
                        prev_reminder_day = request.date_from
                    else:
                        prev_reminder_day = from_date - timedelta(days=reminder_day_before)
                    if prev_reminder_day == today:
                        for manager in holiday_managers:
                            template = mail_template.sudo().with_context(
                                email_to=manager.email,
                            )
                            template.send_mail(request.id, force_send=True)


class PendingTask(models.Model):
    _name = 'pending.task'

    name = fields.Char(string='Task', required=True)
    leave_id = fields.Many2one('hr.leave', string='Leave Request', help="Leave request")
    dept_id = fields.Many2one('hr.department', string='Department', related='leave_id.department_id', help="Department")
    project_id = fields.Many2one('project.project', string='Project', required=True, help="Project")
    description = fields.Text(string='Description', help="Description")
    assigned_to = fields.Many2one('hr.employee', string='Assigned to', help="Employee who is assigned to",
                                  domain="[('department_id', '=', dept_id)]")
    unavailable_employee = fields.Many2many('hr.employee', string='Unavailable Employees', help="unavailable employee",
                                            compute='get_unavailable_employee')

    def get_unavailable_employee(self):
        unavail_emp = []
        for leave in self.leave_id.overlapping_leaves:
            unavail_emp.append(leave.employee_id.id)
        self.update({'unavailable_employee': unavail_emp})


class HrVacationConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    leave_reminder = fields.Boolean(string='Leave Reminder Email', help="Send leave remainder emails to hr managers")
    reminder_day_before = fields.Integer(string='Reminder Day Before')
    default_expense_account = fields.Many2one('account.account', string='Travel Expense Account',
                                              default_model='hr.leave')

    def get_values(self):
        res = super(HrVacationConfigSettings, self).get_values()
        res.update(
            leave_reminder=self.env['ir.config_parameter'].sudo().get_param('leave_reminder'),
            reminder_day_before=int(self.env['ir.config_parameter'].sudo().get_param('reminder_day_before')),
            default_expense_account=int(self.env['ir.config_parameter'].sudo().get_param('travel_expense_account', ))
        )
        return res

    def set_values(self):
        super(HrVacationConfigSettings, self).set_values()
        self.env['ir.config_parameter'].sudo().set_param('leave_reminder', self.leave_reminder)
        self.env['ir.config_parameter'].sudo().set_param('reminder_day_before', self.reminder_day_before)
        self.env['ir.config_parameter'].sudo().set_param('travel_expense_account', self.default_expense_account.id)
