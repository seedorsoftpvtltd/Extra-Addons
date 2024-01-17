# -*- coding: utf-8 -*-

from odoo import fields, models, api, _
from datetime import datetime
from dateutil.relativedelta import relativedelta
from odoo.exceptions import ValidationError
from datetime import date, timedelta
from odoo.tools import pycompat, DEFAULT_SERVER_DATE_FORMAT
from odoo.exceptions import Warning


class QuickTimesheetSheet(models.Model):
    _name = 'quick.timesheet.sheet'
    _description = 'Quick Timesheet Sheet'
    _rec_name = 'employee_id'
    _inherit = ['mail.thread', 'mail.activity.mixin', 'portal.mixin']

    @api.depends('start_date')
    def _compute_label_day1(self):
        for rec in self:
            datetime_object = datetime.strptime(str(rec.start_date), DEFAULT_SERVER_DATE_FORMAT)
            rec.label_day1 = str(datetime_object.date()) + ' ' + str(datetime_object.strftime("%a"))

    @api.depends('start_date')
    def _compute_label_day2(self):
        for rec in self:
            datetime_object = datetime.strptime(str(rec.start_date), DEFAULT_SERVER_DATE_FORMAT) + relativedelta(days=1)
            rec.label_day2 = str(datetime_object.date()) + ' ' + str(datetime_object.strftime("%a"))

    @api.depends('start_date')
    def _compute_label_day3(self):
        for rec in self:
            datetime_object = datetime.strptime(str(rec.start_date), DEFAULT_SERVER_DATE_FORMAT) + relativedelta(days=2)
            rec.label_day3 = str(datetime_object.date()) + ' ' + str(datetime_object.strftime("%a"))

    @api.depends('start_date')
    def _compute_label_day4(self):
        for rec in self:
            datetime_object = datetime.strptime(str(rec.start_date), DEFAULT_SERVER_DATE_FORMAT) + relativedelta(days=3)
            rec.label_day4 = str(datetime_object.date()) + ' ' + str(datetime_object.strftime("%a"))

    @api.depends('start_date')
    def _compute_label_day5(self):
        for rec in self:
            datetime_object = datetime.strptime(str(rec.start_date), DEFAULT_SERVER_DATE_FORMAT) + relativedelta(days=4)
            rec.label_day5 = str(datetime_object.date()) + ' ' + str(datetime_object.strftime("%a"))

    @api.depends('start_date')
    def _compute_label_day6(self):
        for rec in self:
            datetime_object = datetime.strptime(str(rec.start_date), DEFAULT_SERVER_DATE_FORMAT) + relativedelta(days=5)
            rec.label_day6 = str(datetime_object.date()) + ' ' + str(datetime_object.strftime("%a"))

    @api.depends('start_date')
    def _compute_label_day7(self):
        for rec in self:
            datetime_object = datetime.strptime(str(rec.start_date), DEFAULT_SERVER_DATE_FORMAT) + relativedelta(days=6)
            rec.label_day7 = str(datetime_object.date()) + ' ' + str(datetime_object.strftime("%a"))

    @api.constrains('end_date')
    def _check_end_date(self):
        for rec in self:
            start_date = datetime.strptime(str(rec.start_date), DEFAULT_SERVER_DATE_FORMAT)
            end_date = datetime.strptime(str(rec.end_date), DEFAULT_SERVER_DATE_FORMAT)
            if end_date < start_date:
                raise ValidationError('Please Select Correct END Date')
            diff = end_date - start_date
            if diff.days > 6:
                raise ValidationError('Please Select Correct Date For one week')
            if end_date.weekday() != 6:
                raise ValidationError('Always select sunday for end date.')
        return True

    @api.constrains('start_date')
    def _check_start_date(self):
        for rec in self:
            start_date = datetime.strptime(str(rec.start_date), DEFAULT_SERVER_DATE_FORMAT)
            end_date = datetime.strptime(str(rec.end_date), DEFAULT_SERVER_DATE_FORMAT)
            diff = end_date - start_date
            if diff.days > 6:
                raise ValidationError('Please Select Correct Date For one week')
            if start_date.weekday() != 0:
                raise ValidationError('Always select monday for start date.')
        return True

    @api.onchange('start_date')
    def onchnage_start_date(self):
        for rec in self:
            start_date = datetime.strptime(str(rec.start_date), DEFAULT_SERVER_DATE_FORMAT) + relativedelta(days=6)
            rec.end_date = start_date.date()

    today = datetime.now().date()
    start = today - timedelta(days=today.weekday())

    is_create_timesheet = fields.Boolean(
        string="Is Create Timesheet"
    )
    create_date = fields.Date(
        string="Create Date",
        default = datetime.now().date(),
        readonly=True
    )
    create_by = fields.Many2one(
        'res.users',
        string="Created by",
        default=lambda self: self.env.user,
        readonly=True
    )
    timesheet_count = fields.Integer(
        string='# of Timesheet',
        compute='_get_timesheet',
        readonly=True
    )
    state = fields.Selection(
        [('draft', 'New'),
        ('confirm', 'Confirmed'),
        ('approve', 'Approved'),
        ('create_timesheet', 'Timesheet Created'),
        ('cancel', 'Cancel')],
        default='draft',
        string='Status',
        track_visibility='onchange',
    )
    project_id = fields.Many2one(
        'project.project',
        string="Project",
        required = True
    )
    task_id = fields.Many2one(
        'project.task',
        string="Task"
    )
    employee_id = fields.Many2one(
        'hr.employee',
        string="Employee",
        required = True
    )
    amount = fields.Float(
        string="Amount",
        default = 0.0,
        required = True
    )
    company_id = fields.Many2one(
        'res.company',
        default=lambda self: self.env.user.company_id,
        string='Company',
        readonly=True,
        required = True
    )

    start_date = fields.Date(
        string="Start Date",
        default= start,
        required = True
    )
    end_date = fields.Date(
        string="End Date",
        required = True
    )

    label_day1 = fields.Char(
        string="Label1",
        compute='_compute_label_day1',
    )
    label_day2 = fields.Char(
        string="Label2",
        compute='_compute_label_day2',
    )
    label_day3 = fields.Char(
        string="Label3",
        compute='_compute_label_day3',
    )
    label_day4 = fields.Char(
        string="Label4",
        compute='_compute_label_day4',
    )
    label_day5 = fields.Char(
        string="Label5",
        compute='_compute_label_day5',
    )
    label_day6 = fields.Char(
        string="Label6",
        compute='_compute_label_day6',
    )
    label_day7 = fields.Char(
        string="Label7",
        compute='_compute_label_day7',
    )

    normal_type_id = fields.Many2one(
        'work.type.quick_timesheet',
        string='Work Type',
        states={'draft': [('readonly', False)]},
        readonly=True,
    )
    normal1 = fields.Float(
        string="Normal1",
        states={'draft': [('readonly', False)]},
        readonly=True,
    )
    normal_des1 = fields.Char(
        string="Normal description1",
        states={'draft': [('readonly', False)]},
        readonly=True,
    )
    normal2 = fields.Float(
        string="Normal2",
        states={'draft': [('readonly', False)]},
        readonly=True,
    )
    normal_des2 = fields.Char(
        string="Normal description2",
        states={'draft': [('readonly', False)]},
        readonly=True,
    )
    normal3 = fields.Float(
        string="Normal3",
        states={'draft': [('readonly', False)]},
        readonly=True,
    )
    normal_des3 = fields.Char(
        string="Normal description3",
        states={'draft': [('readonly', False)]},
        readonly=True,
    )
    normal4 = fields.Float(
        string="Normal4",
        states={'draft': [('readonly', False)]},
        readonly=True,
    )
    normal_des4 = fields.Char(
        string="Normal description4",
        states={'draft': [('readonly', False)]},
        readonly=True,
    )
    normal5 = fields.Float(
        string="Normal5",
        states={'draft': [('readonly', False)]},
        readonly=True,
    )
    normal_des5 = fields.Char(
        string="Normal description5",
        states={'draft': [('readonly', False)]},
        readonly=True,
    )
    normal6 = fields.Float(
        string="Normal6",
        states={'draft': [('readonly', False)]},
        readonly=True,
    )
    normal_des6 = fields.Char(
        string="Normal description6",
        states={'draft': [('readonly', False)]},
        readonly=True,
    )
    normal7 = fields.Float(
        string="Normal7",
        states={'draft': [('readonly', False)]},
        readonly=True,
    )
    normal_des7 = fields.Char(
        string="Normal description7",
        states={'draft': [('readonly', False)]},
        readonly=True,
    )
    overtime_type_id = fields.Many2one(
        'work.type.quick_timesheet',
        string='Work Type',
        states={'draft': [('readonly', False)]},
        readonly=True,
    )
    overtime1 = fields.Float(
        string="Overtim1",
        states={'draft': [('readonly', False)]},
        readonly=True,
    )
    overtime_des1 = fields.Char(
        string="Overtime description1",
        states={'draft': [('readonly', False)]},
        readonly=True,
    )
    overtime2 = fields.Float(
        string="Overtime2",
        states={'draft': [('readonly', False)]},
        readonly=True,
    )
    overtime_des2 = fields.Char(
        string="Overtime description2",
        states={'draft': [('readonly', False)]},
        readonly=True,
    )
    overtime3 = fields.Float(
        string="Overtime3",
        states={'draft': [('readonly', False)]},
        readonly=True,
    )
    overtime_des3 = fields.Char(
        string="Overtime description3",
        states={'draft': [('readonly', False)]},
        readonly=True,
    )
    overtime4 = fields.Float(
        string="Overtime4",
        states={'draft': [('readonly', False)]},
        readonly=True,
    )
    overtime_des4 = fields.Char(
        string="Overtime description4",
        states={'draft': [('readonly', False)]},
        readonly=True,
    )
    overtime5 = fields.Float(
        string="Overtime5",
        states={'draft': [('readonly', False)]},
        readonly=True,
    )
    overtime_des5 = fields.Char(
        string="Overtime description5",
        states={'draft': [('readonly', False)]},
        readonly=True,
    )
    overtime6 = fields.Float(
        string="Overtime6",
        states={'draft': [('readonly', False)]},
        readonly=True,
    )
    overtime_des6 = fields.Char(
        string="Overtime description6",
        states={'draft': [('readonly', False)]},
        readonly=True,
    )
    overtime7 = fields.Float(
        string="Overtime7",
        states={'draft': [('readonly', False)]},
        readonly=True,
    )
    overtime_des7 = fields.Char(
        string="Overtime description7",
        states={'draft': [('readonly', False)]},
        readonly=True,
    )
    free_type_id = fields.Many2one(
        'work.type.quick_timesheet',
        string='Work Type',
        states={'draft': [('readonly', False)]},
        readonly=True,
    )
    free1 = fields.Float(
        string="Free1",
        states={'draft': [('readonly', False)]},
        readonly=True,
    )
    free_des1 = fields.Char(
        string="Free description1",
        states={'draft': [('readonly', False)]},
        readonly=True,
    )
    free2 = fields.Float(
        string="Free2",
        states={'draft': [('readonly', False)]},
        readonly=True,
    )
    free_des2 = fields.Char(
        string="Free description2",
        states={'draft': [('readonly', False)]},
        readonly=True,
    )
    free3 = fields.Float(
        string="Free3",
        states={'draft': [('readonly', False)]},
        readonly=True,
    )
    free_des3 = fields.Char(
        string="Free description3",
        states={'draft': [('readonly', False)]},
        readonly=True,
    )
    free4 = fields.Float(
        string="Free4",
        states={'draft': [('readonly', False)]},
        readonly=True,
    )
    free_des4 = fields.Char(
        string="Free description4",
        states={'draft': [('readonly', False)]},
        readonly=True,
    )
    free5 = fields.Float(
        string="Free5",
        states={'draft': [('readonly', False)]},
        readonly=True,
    )
    free_des5 = fields.Char(
        string="Free description5",
        states={'draft': [('readonly', False)]},
        readonly=True,
    )
    free6 = fields.Float(
        string="Free6",
        states={'draft': [('readonly', False)]},
        readonly=True,
    )
    free_des6 = fields.Char(
        string="Free description6",
        states={'draft': [('readonly', False)]},
        readonly=True,
    )
    free7 = fields.Float(
        string="Free7",
        states={'draft': [('readonly', False)]},
        readonly=True,
    )
    free_des7 = fields.Char(
        string="Free description7",
        states={'draft': [('readonly', False)]},
        readonly=True,
    )
    sick_type_id = fields.Many2one(
        'work.type.quick_timesheet',
        string='Work Type',
        states={'draft': [('readonly', False)]},
        readonly=True,
    )
    sick1 = fields.Float(
        string="Sick1",
        states={'draft': [('readonly', False)]},
        readonly=True,
    )
    sick_des1 = fields.Char(
        string="Sick description1",
        states={'draft': [('readonly', False)]},
        readonly=True,
    )
    sick2 = fields.Float(
        string="Sick2",
        states={'draft': [('readonly', False)]},
        readonly=True,
    )
    sick_des2 = fields.Char(
        string="Sick description2",
        states={'draft': [('readonly', False)]},
        readonly=True,
    )
    sick3 = fields.Float(
        string="Sick3",
        states={'draft': [('readonly', False)]},
        readonly=True,
    )
    sick_des3 = fields.Char(
        string="Sick description3",
        states={'draft': [('readonly', False)]},
        readonly=True,
    )
    sick4 = fields.Float(
        string="Sick4",
        states={'draft': [('readonly', False)]},
        readonly=True,
    )
    sick_des4 = fields.Char(
        string="Sick description4",
        states={'draft': [('readonly', False)]},
        readonly=True,
    )
    sick5 = fields.Float(
        string="Sick5",
        states={'draft': [('readonly', False)]},
        readonly=True,
    )
    sick_des5 = fields.Char(
        string="Sick description5",
        states={'draft': [('readonly', False)]},
        readonly=True,
    )
    sick6 = fields.Float(
        string="Sick6",
        states={'draft': [('readonly', False)]},
        readonly=True,
    )
    sick_des6 = fields.Char(
        string="Sick description6",
        states={'draft': [('readonly', False)]},
        readonly=True,
    )
    sick7 = fields.Float(
        string="Sick7",
        states={'draft': [('readonly', False)]},
        readonly=True,
    )
    sick_des7 = fields.Char(
        string="Sick description7",
        states={'draft': [('readonly', False)]},
        readonly=True,
    )
    overnight_type_id = fields.Many2one(
        'work.type.quick_timesheet',
        string='Work Type',
        states={'draft': [('readonly', False)]},
        readonly=True,
    )
    overnight1 = fields.Float(
        string="Overnight1",
        states={'draft': [('readonly', False)]},
        readonly=True,
    )
    overnight_des1 = fields.Char(
        string="Overnight description1",
        states={'draft': [('readonly', False)]},
        readonly=True,
    )
    overnight2 = fields.Float(
        string="Overnight2",
        states={'draft': [('readonly', False)]},
        readonly=True,
    )
    overnight_des2 = fields.Char(
        string="Overnight description2",
        states={'draft': [('readonly', False)]},
        readonly=True,
    )
    overnight3 = fields.Float(
        string="Overnight3",
        states={'draft': [('readonly', False)]},
        readonly=True,
    )
    overnight_des3 = fields.Char(
        string="Overnight description3",
        states={'draft': [('readonly', False)]},
        readonly=True,
    )
    overnight4 = fields.Float(
        string="Overnight4",
        states={'draft': [('readonly', False)]},
        readonly=True,
    )
    overnight_des4 = fields.Char(
        string="Overnight description4",
        states={'draft': [('readonly', False)]},
        readonly=True,
    )
    overnight5 = fields.Float(
        string="Overnight5",
        states={'draft': [('readonly', False)]},
        readonly=True,
    )
    overnight_des5 = fields.Char(
        string="Overnight description5",
        states={'draft': [('readonly', False)]},
        readonly=True,
    )
    overnight6 = fields.Float(
        string="Overnight6",
        states={'draft': [('readonly', False)]},
        readonly=True,
    )
    overnight_des6 = fields.Char(
        string="Overnight description6",
        states={'draft': [('readonly', False)]},
        readonly=True,
    )
    overnight7 = fields.Float(
        string="Overnight7",
        states={'draft': [('readonly', False)]},
        readonly=True,
    )
    overnight_des7 = fields.Char(
        string="Overnight description7",
        states={'draft': [('readonly', False)]},
        readonly=True,
    )
    
    @api.depends()
    def _get_timesheet(self):
        for rec in self:
            timesheet_count = self.env['account.analytic.line'].search_count([
                    ('quick_timesheet_id', '=', rec.id)
            ])
            rec.timesheet_count = timesheet_count
    
    # @api.multi #odoo13
    def create_timesheet_sheet(self):
        for rec in self:
            start_date = datetime.strptime(str(rec.start_date), DEFAULT_SERVER_DATE_FORMAT)
            end_date = datetime.strptime(str(rec.end_date), DEFAULT_SERVER_DATE_FORMAT)
            delta = end_date - start_date
            self.is_create_timesheet = True
            dates = []
            dict = {}
            for i in range(delta.days + 1):
                date = start_date + timedelta(i)
                if date not in dict:
                    dict.update({str(date.date()):{}})
                if date.date().weekday() == 0:
                    if str(date.date()) in dict:
                         if rec.normal1 != 0.0:

                             vals ={
                                'name': rec.normal_des1 or '/',
                                'unit_amount': rec.normal1,
                                'work_type_id':  rec.normal_type_id.id,
                                'date': date.date(),
                                'project_id': rec.project_id.id,
                                'task_id': rec.task_id.id or False,
                                'employee_id':rec.employee_id.id,
                                'quick_timesheet_id': rec.id,
                                'account_id': rec.project_id.analytic_account_id.id,
                                'user_id': rec.employee_id.user_id.id or False,
                             }
                             dict[str(date.date())].update({'1':vals})
                         if rec.overtime1 != 0.0:
                             vals={
                                'name': rec.overtime_des1 or '/',
                                'unit_amount': rec.overtime1,
                                'work_type_id':  rec.overtime_type_id.id,
                                'date': date.date(),
                                'project_id': rec.project_id.id,
                                'task_id': rec.task_id.id or False,
                                'employee_id':rec.employee_id.id,
                                'quick_timesheet_id': rec.id,
                                'account_id': rec.project_id.analytic_account_id.id,
                                'user_id': rec.employee_id.user_id.id or False,
                             }
                             dict[str(date.date())].update({'2':vals})
                         if rec.free1 != 0.0:
                             vals={
                                'name': rec.free_des1 or '/',
                                'unit_amount': rec.free1,
                                'work_type_id':  rec.free_type_id.id,
                                'date': date.date(),
                                'project_id': rec.project_id.id,
                                'task_id': rec.task_id.id or False,
                                'employee_id':rec.employee_id.id,
                                'quick_timesheet_id': rec.id,
                                'account_id': rec.project_id.analytic_account_id.id,
                                'user_id': rec.employee_id.user_id.id or False,
                             }
                             dict[str(date.date())].update({'3':vals})
                         if rec.sick1 != 0.0:
                             vals={
                                'name': rec.sick_des1 or '/',
                                'unit_amount': rec.sick1,
                                'work_type_id':  rec.sick_type_id.id,
                                'date': date.date(),
                                'project_id': rec.project_id.id,
                                'task_id': rec.task_id.id or False,
                                'employee_id':rec.employee_id.id,
                                'quick_timesheet_id': rec.id,
                                'account_id': rec.project_id.analytic_account_id.id,
                                'user_id': rec.employee_id.user_id.id or False,
                             }
                             dict[str(date.date())].update({'4':vals})
                         if rec.overnight1 != 0.0:
                             vals={
                                'name': rec.overnight_des1 or '/',
                                'unit_amount': rec.overnight1,
                                'work_type_id':  rec.overnight_type_id.id,
                                'date': date.date(),
                                'project_id': rec.project_id.id,
                                'task_id': rec.task_id.id or False,
                                'employee_id':rec.employee_id.id,
                                'quick_timesheet_id': rec.id,
                                'account_id': rec.project_id.analytic_account_id.id,
                                'user_id': rec.employee_id.user_id.id or False,
                             }
                             dict[str(date.date())].update({'5':vals})
                if date.date().weekday() == 1:
                   if str(date.date()) in dict:
                        if rec.normal2 != 0.0:
                            vals ={
                               'name': rec.normal_des2 or '/',
                               'unit_amount': rec.normal2,
                               'work_type_id':  rec.normal_type_id.id,
                               'date': date.date(),
                               'project_id': rec.project_id.id,
                                'task_id': rec.task_id.id or False,
                               'employee_id':rec.employee_id.id,
                               'quick_timesheet_id': rec.id,
                               'account_id': rec.project_id.analytic_account_id.id,
                               'user_id': rec.employee_id.user_id.id or False,
                            }
                            dict[str(date.date())].update({'1':vals})
                        if rec.overtime2 != 0.0:
                            vals={
                               'name': rec.overtime_des2 or '/',
                               'unit_amount': rec.overtime2,
                               'work_type_id':  rec.overtime_type_id.id,
                               'date': date.date(),
                               'project_id': rec.project_id.id,
                                'task_id': rec.task_id.id or False,
                               'employee_id':rec.employee_id.id,
                               'quick_timesheet_id': rec.id,
                               'account_id': rec.project_id.analytic_account_id.id,
                               'user_id': rec.employee_id.user_id.id or False,
                            }
                            dict[str(date.date())].update({'2':vals})
                        if rec.free2 != 0.0:
                            vals={
                               'name': rec.free_des2 or '/',
                               'unit_amount': rec.free2,
                               'work_type_id':  rec.free_type_id.id,
                               'date': date.date(),
                               'project_id': rec.project_id.id,
                                'task_id': rec.task_id.id or False,
                               'employee_id':rec.employee_id.id,
                               'quick_timesheet_id': rec.id,
                               'account_id': rec.project_id.analytic_account_id.id,
                               'user_id': rec.employee_id.user_id.id or False,
                            }
                            dict[str(date.date())].update({'3':vals})
                        if rec.sick2 != 0.0:
                            vals={
                               'name': rec.sick_des2 or '/',
                               'unit_amount': rec.sick2,
                               'work_type_id':  rec.sick_type_id.id,
                               'date': date.date(),
                               'project_id': rec.project_id.id,
                                'task_id': rec.task_id.id or False,
                               'employee_id':rec.employee_id.id,
                               'quick_timesheet_id': rec.id,
                               'account_id': rec.project_id.analytic_account_id.id,
                               'user_id': rec.employee_id.user_id.id or False,
                            }
                            dict[str(date.date())].update({'4':vals})
                        if rec.overnight2 != 0.0:
                            vals={
                               'name': rec.overnight_des1 or '/',
                               'unit_amount': rec.overnight2,
                               'work_type_id':  rec.overnight_type_id.id,
                               'date': date.date(),
                               'project_id': rec.project_id.id,
                                'task_id': rec.task_id.id or False,
                               'employee_id':rec.employee_id.id,
                               'quick_timesheet_id': rec.id,
                               'account_id': rec.project_id.analytic_account_id.id,
                               'user_id': rec.employee_id.user_id.id or False,
                            }
                            dict[str(date.date())].update({'5':vals})
                if date.date().weekday() == 2:
                   if str(date.date()) in dict:
                        if rec.normal3 != 0.0:
                            vals ={
                               'name': rec.normal_des3 or '/',
                               'unit_amount': rec.normal3,
                               'work_type_id':  rec.normal_type_id.id,
                               'date': date.date(),
                               'project_id': rec.project_id.id,
                                'task_id': rec.task_id.id or False,
                               'employee_id':rec.employee_id.id,
                               'quick_timesheet_id': rec.id,
                               'account_id': rec.project_id.analytic_account_id.id,
                               'user_id': rec.employee_id.user_id.id or False,
                            }
                            dict[str(date.date())].update({'1':vals})
                        if rec.overtime3 != 0.0:
                            vals={
                               'name': rec.overtime_des3 or '/',
                               'unit_amount': rec.overtime3,
                               'work_type_id':  rec.overtime_type_id.id,
                               'date': date.date(),
                               'project_id': rec.project_id.id,
                                'task_id': rec.task_id.id or False,
                               'employee_id':rec.employee_id.id,
                               'quick_timesheet_id': rec.id,
                               'account_id': rec.project_id.analytic_account_id.id,
                               'user_id': rec.employee_id.user_id.id or False,
                            }
                            dict[str(date.date())].update({'2':vals})
                        if rec.free3 != 0.0:
                            vals={
                               'name': rec.free_des3 or '/',
                               'unit_amount': rec.free3,
                               'work_type_id':  rec.free_type_id.id,
                               'date': date.date(),
                               'project_id': rec.project_id.id,
                                'task_id': rec.task_id.id or False,
                               'employee_id':rec.employee_id.id,
                               'quick_timesheet_id': rec.id,
                               'account_id': rec.project_id.analytic_account_id.id,
                               'user_id': rec.employee_id.user_id.id or False,
                            }
                            dict[str(date.date())].update({'3':vals})
                        if rec.sick3 != 0.0:
                            vals={
                               'name': rec.sick_des3 or '/',
                               'unit_amount': rec.sick3,
                               'work_type_id':  rec.sick_type_id.id,
                               'date': date.date(),
                               'project_id': rec.project_id.id,
                                'task_id': rec.task_id.id or False,
                               'employee_id':rec.employee_id.id,
                               'quick_timesheet_id': rec.id,
                               'account_id': rec.project_id.analytic_account_id.id,
                               'user_id': rec.employee_id.user_id.id or False,
                            }
                            dict[str(date.date())].update({'4':vals})
                        if rec.overnight3 != 0.0:
                            vals={
                               'name': rec.overnight_des3 or '/',
                               'unit_amount': rec.overnight3,
                               'work_type_id':  rec.overnight_type_id.id,
                               'date': date.date(),
                               'project_id': rec.project_id.id,
                                'task_id': rec.task_id.id or False,
                               'employee_id':rec.employee_id.id,
                               'quick_timesheet_id': rec.id,
                               'account_id': rec.project_id.analytic_account_id.id,
                               'user_id': rec.employee_id.user_id.id or False,
                            }
                            dict[str(date.date())].update({'5':vals})
                if date.date().weekday() == 3:
                   if str(date.date()) in dict:
                        if rec.normal4 != 0.0:
                            vals ={
                               'name': rec.normal_des4 or '/',
                               'unit_amount': rec.normal4,
                               'work_type_id':  rec.normal_type_id.id,
                               'date': date.date(),
                               'project_id': rec.project_id.id,
                                'task_id': rec.task_id.id or False,
                               'employee_id':rec.employee_id.id,
                               'quick_timesheet_id': rec.id,
                               'account_id': rec.project_id.analytic_account_id.id,
                               'user_id': rec.employee_id.user_id.id or False,
                            }
                            dict[str(date.date())].update({'1':vals})
                        if rec.overtime4 != 0.0:
                            vals={
                               'name': rec.overtime_des4 or '/',
                               'unit_amount': rec.overtime4,
                               'work_type_id':  rec.overtime_type_id.id,
                               'date': date.date(),
                               'project_id': rec.project_id.id,
                                'task_id': rec.task_id.id or False,
                               'employee_id':rec.employee_id.id,
                               'quick_timesheet_id': rec.id,
                               'account_id': rec.project_id.analytic_account_id.id,
                               'user_id': rec.employee_id.user_id.id or False,
                            }
                            dict[str(date.date())].update({'2':vals})
                        if rec.free4 != 0.0:
                            vals={
                               'name': rec.free_des4 or '/',
                               'unit_amount': rec.free4,
                               'work_type_id':  rec.free_type_id.id,
                               'date': date.date(),
                               'project_id': rec.project_id.id,
                                'task_id': rec.task_id.id or False,
                               'employee_id':rec.employee_id.id,
                               'quick_timesheet_id': rec.id,
                               'account_id': rec.project_id.analytic_account_id.id,
                               'user_id': rec.employee_id.user_id.id or False,
                            }
                            dict[str(date.date())].update({'3':vals})
                        if rec.sick4 != 0.0:
                            vals={
                               'name': rec.sick_des4 or '/',
                               'unit_amount': rec.sick4,
                               'work_type_id':  rec.sick_type_id.id,
                               'date': date.date(),
                               'project_id': rec.project_id.id,
                                'task_id': rec.task_id.id or False,
                               'employee_id':rec.employee_id.id,
                               'quick_timesheet_id': rec.id,
                               'account_id': rec.project_id.analytic_account_id.id,
                               'user_id': rec.employee_id.user_id.id or False,
                            }
                            dict[str(date.date())].update({'4':vals})
                        if rec.overnight4 != 0.0:
                            vals={
                               'name': rec.overnight_des4 or '/',
                               'unit_amount': rec.overnight4,
                               'work_type_id':  rec.overnight_type_id.id,
                               'date': date.date(),
                               'project_id': rec.project_id.id,
                                'task_id': rec.task_id.id or False,
                               'employee_id':rec.employee_id.id,
                               'quick_timesheet_id': rec.id,
                               'account_id': rec.project_id.analytic_account_id.id,
                               'user_id': rec.employee_id.user_id.id or False,
                            }
                            dict[str(date.date())].update({'5':vals})
                if date.date().weekday() == 4:
                   if str(date.date()) in dict:
                        if rec.normal5 != 0.0:
                            vals ={
                               'name': rec.normal_des5 or '/',
                               'unit_amount': rec.normal5,
                               'work_type_id':  rec.normal_type_id.id,
                               'date': date.date(),
                               'project_id': rec.project_id.id,
                                'task_id': rec.task_id.id or False,
                               'employee_id':rec.employee_id.id,
                               'quick_timesheet_id': rec.id,
                               'account_id': rec.project_id.analytic_account_id.id,
                               'user_id': rec.employee_id.user_id.id or False,
                            }
                            dict[str(date.date())].update({'1':vals})
                        if rec.overtime5 != 0.0:
                            vals={
                               'name': rec.overtime_des5 or '/',
                               'unit_amount': rec.overtime5,
                               'work_type_id':  rec.overtime_type_id.id,
                               'date': date.date(),
                               'project_id': rec.project_id.id,
                                'task_id': rec.task_id.id or False,
                               'employee_id':rec.employee_id.id,
                               'quick_timesheet_id': rec.id,
                               'account_id': rec.project_id.analytic_account_id.id,
                               'user_id': rec.employee_id.user_id.id or False,
                            }
                            dict[str(date.date())].update({'2':vals})
                        if rec.free5 != 0.0:
                            vals={
                               'name': rec.free_des5 or '/',
                               'unit_amount': rec.free5,
                               'work_type_id':  rec.free_type_id.id,
                               'date': date.date(),
                               'project_id': rec.project_id.id,
                                'task_id': rec.task_id.id or False,
                               'employee_id':rec.employee_id.id,
                               'quick_timesheet_id': rec.id,
                               'account_id': rec.project_id.analytic_account_id.id,
                               'user_id': rec.employee_id.user_id.id or False,
                            }
                            dict[str(date.date())].update({'3':vals})
                        if rec.sick5 != 0.0:
                            vals={
                               'name': rec.sick_des5 or '/',
                               'unit_amount': rec.sick5,
                               'work_type_id':  rec.sick_type_id.id,
                               'date': date.date(),
                               'project_id': rec.project_id.id,
                                'task_id': rec.task_id.id or False,
                               'employee_id':rec.employee_id.id,
                               'quick_timesheet_id': rec.id,
                               'account_id': rec.project_id.analytic_account_id.id,
                               'user_id': rec.employee_id.user_id.id or False,
                            }
                            dict[str(date.date())].update({'4':vals})
                        if rec.overnight5 != 0.0:
                            vals={
                               'name': rec.overnight_des5 or '/',
                               'unit_amount': rec.overnight5,
                               'work_type_id':  rec.overnight_type_id.id,
                               'date': date.date(),
                               'project_id': rec.project_id.id,
                                'task_id': rec.task_id.id or False,
                               'employee_id':rec.employee_id.id,
                               'quick_timesheet_id': rec.id,
                               'account_id': rec.project_id.analytic_account_id.id,
                               'user_id': rec.employee_id.user_id.id or False,
                            }
                            dict[str(date.date())].update({'5':vals})
                if date.date().weekday() == 5:
                   if str(date.date()) in dict:
                        if rec.normal6 != 0.0:
                            vals ={
                               'name': rec.normal_des6 or '/',
                               'unit_amount': rec.normal6,
                               'work_type_id':  rec.normal_type_id.id,
                               'date': date.date(),
                               'project_id': rec.project_id.id,
                                'task_id': rec.task_id.id or False,
                               'employee_id':rec.employee_id.id,
                               'quick_timesheet_id': rec.id,
                               'account_id': rec.project_id.analytic_account_id.id,
                               'user_id': rec.employee_id.user_id.id or False,
                            }
                            dict[str(date.date())].update({'1':vals})
                        if rec.overtime6 != 0.0:
                            vals={
                               'name': rec.overtime_des6 or '/',
                               'unit_amount': rec.overtime6,
                               'work_type_id':  rec.overtime_type_id.id,
                               'date': date.date(),
                               'project_id': rec.project_id.id,
                                'task_id': rec.task_id.id or False,
                               'employee_id':rec.employee_id.id,
                               'quick_timesheet_id': rec.id,
                               'account_id': rec.project_id.analytic_account_id.id,
                               'user_id': rec.employee_id.user_id.id or False,
                            }
                            dict[str(date.date())].update({'2':vals})
                        if rec.free6 != 0.0:
                            vals={
                               'name': rec.free_des6 or '/',
                               'unit_amount': rec.free6,
                               'work_type_id':  rec.free_type_id.id,
                               'date': date.date(),
                               'project_id': rec.project_id.id,
                                'task_id': rec.task_id.id or False,
                               'employee_id':rec.employee_id.id,
                               'quick_timesheet_id': rec.id,
                               'account_id': rec.project_id.analytic_account_id.id,
                               'user_id': rec.employee_id.user_id.id or False,
                            }
                            dict[str(date.date())].update({'3':vals})
                        if rec.sick6 != 0.0:
                            vals={
                               'name': rec.sick_des6 or '/',
                               'unit_amount': rec.sick6,
                               'work_type_id':  rec.sick_type_id.id,
                               'date': date.date(),
                               'project_id': rec.project_id.id,
                                'task_id': rec.task_id.id or False,
                               'employee_id':rec.employee_id.id,
                               'quick_timesheet_id': rec.id,
                               'account_id': rec.project_id.analytic_account_id.id,
                               'user_id': rec.employee_id.user_id.id or False,
                            }
                            dict[str(date.date())].update({'4':vals})
                        if rec.overnight6 != 0.0:
                            vals={
                               'name': rec.overnight_des6 or '/',
                               'unit_amount': rec.overnight6,
                               'work_type_id':  rec.overnight_type_id.id,
                               'date': date.date(),
                               'project_id': rec.project_id.id,
                                'task_id': rec.task_id.id or False,
                               'employee_id':rec.employee_id.id,
                               'quick_timesheet_id': rec.id,
                               'account_id': rec.project_id.analytic_account_id.id,
                               'user_id': rec.employee_id.user_id.id or False,
                            }
                            dict[str(date.date())].update({'5':vals})
                if date.date().weekday() == 6:
                   if str(date.date()) in dict:
                        if rec.normal7 != 0.0:
                            vals ={
                               'name': rec.normal_des7 or '/',
                               'unit_amount': rec.normal7,
                               'work_type_id':  rec.normal_type_id.id,
                               'date': date.date(),
                               'project_id': rec.project_id.id,
                                'task_id': rec.task_id.id or False,
                               'employee_id':rec.employee_id.id,
                               'quick_timesheet_id': rec.id,
                               'account_id': rec.project_id.analytic_account_id.id,
                               'user_id': rec.employee_id.user_id.id or False,
                            }
                            dict[str(date.date())].update({'1':vals})
                        if rec.overtime7 != 0.0:
                            vals={
                               'name': rec.overtime_des7 or '/',
                               'unit_amount': rec.overtime7,
                               'work_type_id':  rec.overtime_type_id.id,
                               'date': date.date(),
                               'project_id': rec.project_id.id,
                                'task_id': rec.task_id.id or False,
                               'employee_id':rec.employee_id.id,
                               'quick_timesheet_id': rec.id,
                               'account_id': rec.project_id.analytic_account_id.id,
                               'user_id': rec.employee_id.user_id.id or False,
                            }
                            dict[str(date.date())].update({'2':vals})
                        if rec.free7 != 0.0:
                            vals={
                               'name': rec.free_des7 or '/',
                               'unit_amount': rec.free7,
                               'work_type_id':  rec.free_type_id.id,
                               'date': date.date(),
                               'project_id': rec.project_id.id,
                                'task_id': rec.task_id.id or False,
                               'employee_id':rec.employee_id.id,
                               'quick_timesheet_id': rec.id,
                               'account_id': rec.project_id.analytic_account_id.id,
                               'user_id': rec.employee_id.user_id.id or False,
                            }
                            dict[str(date.date())].update({'3':vals})
                        if rec.sick7 != 0.0:
                            vals={
                               'name': rec.sick_des7 or '/',
                               'unit_amount': rec.sick7,
                               'work_type_id':  rec.sick_type_id.id,
                               'date': date.date(),
                               'project_id': rec.project_id.id,
                                'task_id': rec.task_id.id or False,
                               'employee_id':rec.employee_id.id,
                               'quick_timesheet_id': rec.id,
                               'account_id': rec.project_id.analytic_account_id.id,
                               'user_id': rec.employee_id.user_id.id or False,
                            }
                            dict[str(date.date())].update({'4':vals})
                        if rec.overnight7 != 0.0:
                            vals={
                               'name': rec.overnight_des7 or '/',
                               'unit_amount': rec.overnight7,
                               'work_type_id':  rec.overnight_type_id.id,
                               'date': date.date(),
                               'project_id': rec.project_id.id,
                                'task_id': rec.task_id.id or False,
                               'employee_id':rec.employee_id.id,
                               'quick_timesheet_id': rec.id,
                               'account_id': rec.project_id.analytic_account_id.id,
                               'user_id': rec.employee_id.user_id.id or False,
                            }
                            dict[str(date.date())].update({'5':vals})
            for date in dict:
                for line in dict[date]:
                    self.env['account.analytic.line'].sudo().create(dict[date][line])

            timesheet_count = self.env['account.analytic.line'].search_count([
                ('quick_timesheet_id', '=', rec.id)
            ])
            rec.timesheet_count = timesheet_count
            rec.state = 'create_timesheet'


    # @api.multi #odoo13
    def action_view_timesheet(self):
        action = self.env.ref('hr_timesheet.act_hr_timesheet_line').read()[0]
        for rec in self:
            action['domain'] = [('quick_timesheet_id', '=', rec.id)]
        return action

    # @api.multi #odoo13
    def action_confirm(self):
        for rec in self:
            rec.state = 'confirm'

    # @api.multi #odoo13
    def action_approve(self):
        for rec in self:
            rec.state = 'approve'

    # @api.multi #odoo13
    def action_cancel(self):
        for rec in self:
            rec.state = 'cancel'

    # @api.multi #odoo13
    def action_reset_to_draft(self):
        for rec in self:
            rec.state = 'draft'

    # @api.one #odoo13
    def unlink(self):
        for rec in self:
            if rec.state != 'draft':
                raise Warning(_('You can not delete record which are not in draft state.'))
        return super(QuickTimesheetSheet, self).unlink()

    
