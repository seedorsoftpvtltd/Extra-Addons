# -*- coding: utf-8 -*-

from odoo import fields, models, api
from datetime import date, datetime, timedelta


class ResCompany(models.Model):
    _inherit = "res.company"

    minimum_workload_hours = fields.Float('Minimum Workload Hours', help="This will set minimum hour assigned to employees", default=40.0)
    days_for_workload = fields.Integer('Set Days to Calculate Workload', help="Set no of days to calculate workload. eg. if you set 7 it will calculate workload for next 7 dyas.", default=7)


class ResUsers(models.Model):
    _inherit  = "res.users"

    is_workload_follower = fields.Boolean("Workload Notification", help="On Selection of this field ,notification will go for all employees", default=False) 


class Hremployee(models.Model):
    _inherit = 'hr.employee'

    def _compute_workload(self):
        """ Calculate workload for next configured days."""
        TaskObj = self.env['project.task'].sudo()
        for employee in self:
            hours = 0
            if employee.user_id:
                tasks = TaskObj.sudo().search([('kanban_state','!=','blocked'), ('date_deadline','>=',fields.Date.today()),('date_deadline','<=',fields.Date.today() + timedelta(days=employee.company_days_for_workload)), ('user_id', '=', employee.user_id.id)])
                for task in tasks:
                    hours += int(task.remaining_hours)
            employee.workload = hours

    workload = fields.Float('Current Workload', compute='_compute_workload', help="Total hours of work assigned to employee")
    company_minimum_workload_hours = fields.Float('Minimun Work load Hours For Company', related='company_id.minimum_workload_hours', readonly=True)
    company_days_for_workload = fields.Integer('Days to Calculate Workload', related='company_id.days_for_workload', readonly=True)

    @api.model
    def project_task_notification(self):
        CompanyObj = self.env['res.company'].sudo()
        UsersObj = self.env['res.users'].sudo()
        MailObj = self.env['mail.message'].sudo()
        DepartmentObj = self.env['hr.department'].sudo()
        email_from = MailObj._get_default_from()
        for company in CompanyObj.search([]):
            #list of follower users
            user_ids = UsersObj.search([('is_workload_follower','=',True), ('company_id', '=', company.id)])
            partner_ids=[]
            for user in user_ids:
                partner_ids.append(user.partner_id.id)
            # search all department
            departments = DepartmentObj.search([('company_id', '=', company.id)])
            for department in departments:
                employees = self.search([('department_id', '=', department.id)])
                if employees:
                    #send mail to manager of department
                    if department.manager_id and department.manager_id.user_id:
                        message = '<h4> Employee Workload Notification For %s</h4>' %(department.name)
                        message += " Following Employees have less Workload: "
                        message += '<table border=1 padding=10><tr><th> Employee </th><th> Workload </th></tr>'
                        for emp in employees:
                            if emp.workload <= company.minimum_workload_hours:
                                message += (('<tr><td> %s  </td><td> %s  </td></tr>') %(emp.name,emp.workload))
                        message += '</table>'
                        message += '<br/>'
    
                        mail = MailObj.create({
                            'subject': 'Employee Workload Notification For %s' %(department.name),
                            'body': message,
                            'record_name': 'Employee Workload Notification',
                            'email_from': email_from,
                            'reply_to': email_from,
                            'model': 'hr.department',
                            'res_id': department.id,
                            'no_auto_thread': True,
                            'partner_ids': [department.manager_id.user_id.partner_id.id]
                        })
                        
                        mail.write({'partner_ids': [(6, 0, [department.manager_id.user_id.partner_id.id] + partner_ids)]})

                        partner_to_notify = [department.manager_id.user_id.partner_id.id] + partner_ids
                        recipients_data = {'partners': [{
                            'id': pid,
                            'share': False,
                            'notif': 'email',
                            'type': 'customer',
                            'groups': []
                        } for pid in partner_to_notify]}
                        department._notify_record_by_email(mail, recipients_data, send_after_commit=False)

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: