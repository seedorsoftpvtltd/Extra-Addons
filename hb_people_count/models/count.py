import datetime
from odoo import api, fields, models, _
import math
from dateutil.relativedelta import relativedelta


class PeopleCnthb(models.Model):
    _inherit = 'res.users'

    cnt_leave = fields.Integer(string="Leaves Count", compute='_cnt_leave')
    cnt_timesheets = fields.Integer(string="Timesheets Count", compute='_cnt_timesheets')
    cnt_announcement = fields.Integer(string="Announcement Count", compute='_cnt_announcement')
    cnt_custody = fields.Integer(string="Custody Count", compute='_cnt_custody')
    cnt_payslip = fields.Integer(string="Payslip Count", compute='_cnt_payslip')
    cnt_attendance = fields.Integer(string="Attendance Count", compute='_cnt_attendance')
    cnt_activity = fields.Integer(string="Activities Count", compute='_cnt_activity')
    cnt_tasks = fields.Integer(string="Tasks Count", compute='_cnt_tasks')
    cnt_leave_allocated = fields.Integer(string="Leave Allocation Count", compute='_cnt_leave_allocated')
    cnt_overtime = fields.Integer(string="Overtime Count", compute='_cnt_overtime')

    def _cnt_overtime(self):
        for rec in self:
            partner = rec.partner_id.id
            payslips = self.env['hr.overtime'].sudo().search_count([('employee_id.id', '=', rec.employee_id.id)])
            if payslips:
                rec['cnt_overtime'] = payslips
            else:
                rec['cnt_overtime'] = ''
            print(rec.cnt_overtime, 'cnt_overtime')

#    def _cnt_leave_allocated(self):
#        for rec in self:
#            partner = rec.partner_id.id
#            leaves = self.env['hr.leave.allocation'].sudo().search_count([('state', 'in', ['confirm', 'validate1']), ('employee_id', '=', rec.employee_id.id)])
#            if leaves:
#                rec['cnt_leave_allocated'] = leaves
#            else:
#                rec['cnt_leave_allocated'] = ''
#            print(rec.cnt_leave_allocated, 'cnt_leave_allocated')

    def _cnt_leave_allocated(self):
        # for rec in self:
        #     if rec.employee_id.allocation_display:
        #         r=rec.employee_id.allocation_display
        #         integer_part = r[:r.index('.')]
        #         rec['cnt_leave_allocated'] =integer_part
        #         print(rec.cnt_leave_allocated, 'cnt_leave_allocated')
        #     else:
        #         rec['cnt_leave_allocated'] = 0
        #         print(rec.cnt_leave_allocated, 'cnt_leave_allocated')
        for rec in self:
            if rec.employee_id.allocation_display:
                r = rec.employee_id.allocation_display
                try:
                    integer_part = r[:r.index('.')]
                except ValueError:
                    integer_part = rec.employee_id.allocation_display
                rec['cnt_leave_allocated'] = integer_part
                print(rec.cnt_leave_allocated, 'cnt_leave_allocated')
            else:
                rec['cnt_leave_allocated'] = 0
                print(rec.cnt_leave_allocated, 'cnt_leave_allocated')

    #    def _cnt_leave(self):
#        for rec in self:
#            partner = rec.partner_id.id
#            leaves = self.env['hr.leave'].sudo().search_count(
#                [('state', 'in', ['confirm', 'validate', 'validate1']), ('user_id', '=', rec.id)])
#            if leaves:
#                rec['cnt_leave'] = leaves
#            else:
#                rec['cnt_leave'] = ''
#            print(rec.cnt_leave, 'cnt_leave')


    def _cnt_leave(self):
        for rec in self:
            if rec.employee_id.allocation_used_display:
                r = rec.employee_id.allocation_used_display
                try:
                  integer_part = r[:r.index('.')]
                except ValueError:
                    integer_part = rec.employee_id.allocation_used_display
                rec['cnt_leave'] = integer_part
                print(rec.cnt_leave, 'cnt_leave')
            else:
                rec['cnt_leave'] = 0
                print(rec.cnt_leave, 'cnt_leave')

    def _cnt_timesheets(self):
        for rec in self:
            timesheets = self.env['account.analytic.line'].sudo().search_count(
                [('project_id', '!=', False), ('user_id', '=', rec.id)])
            if timesheets:
                rec['cnt_timesheets'] = timesheets
            else:
                rec['cnt_timesheets'] = ''
            print(rec.cnt_timesheets, 'cnt_timesheets')

    def _cnt_announcement(self):
        for rec in self:
            announcement = self.env['hr.announcement'].sudo().search_count(
                ['|', '|', '|', '|', ('state', '=', 'approved'), ('is_announcement', '=', True),
                 ('employee_ids.id', '=', rec.employee_id.id),
                 ('department_ids.id', '=', rec.employee_id.department_id.id),
                 ('position_ids.id', '=', rec.employee_id.job_id.id)])
            if announcement:
                rec['cnt_announcement'] = announcement
            else:
                rec['cnt_announcement'] = ''
            print(rec.cnt_announcement, 'cnt_announcement')

    def _cnt_custody(self):
        for rec in self:
            custodies = self.env['hr.custody'].sudo().search_count(
                [('employee.id', '=', rec.employee_id.id), ('state', '=', 'approved')])
            # print(rec)
            if custodies:
                rec['cnt_custody'] = custodies
            else:
                rec['cnt_custody'] = ''
            print(rec.cnt_custody, 'cnt_custody')

    def _cnt_payslip(self):
        for rec in self:
            partner = rec.partner_id.id
            payslips = self.env['hr.payslip'].sudo().search_count([('employee_id.id', '=', rec.employee_id.id)])
            if payslips:
                rec['cnt_payslip'] = payslips
            else:
                rec['cnt_payslip'] = ''
            print(rec.cnt_payslip, 'cnt_payslip')

    def _cnt_attendance(self):
        for rec in self:
            partner = rec.partner_id.id
            attendances = self.env['hr.attendance'].sudo().search_count([('employee_id.id', '=', rec.employee_id.id)])
            if attendances:
                rec['cnt_attendance'] = attendances
            else:
                rec['cnt_attendance'] = ''
            print(rec.cnt_attendance, 'cnt_attendance')

    def _cnt_activity(self):
        for rec in self:
            activities = self.env['mail.activity'].sudo().search_count([('user_id.id', '=', rec.id)])
            if activities:
                rec['cnt_activity'] = activities
            else:
                rec['cnt_activity'] = ''
            print(rec.cnt_activity, 'cnt_activity')

    def _cnt_tasks(self):
        for rec in self:
            tasks = self.env['project.task'].sudo().search_count([('user_id.id', '=', rec.id)])
            if tasks:
                rec['cnt_tasks'] = tasks
            else:
                rec['cnt_tasks'] = ''
            print(rec.cnt_tasks, 'cnt_tasks')
