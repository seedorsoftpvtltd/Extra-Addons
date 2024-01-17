from odoo import api, models, fields, _
import re
import collections
from collections import Counter
from datetime import datetime, time, date, timedelta


class absent_report(models.AbstractModel):
    _name = "report.absent_attendance_report.report_pdf"

    @api.model
    def _get_report_values(self, docids, data):

        ids=[]
        list2=[]
        list1=[]
        remove_list = []
        leave_list=[]

        start_date=data.get('start_date')
        department_id=data['department_id']
        department_list=[]
        dept_all=[]

        DayOfWeek=[]
        input=''
        employee = self.env['hr.employee'].search([])
        for names in employee:
            leave_date_d = ''
            leaves=self.env['hr.leave'].search([('employee_id','=',names.id)])
            for rec in leaves:
                if not rec.request_unit_half and not rec.request_unit_hours:
                    if rec.state == 'validate':
                        leave_from = rec.request_date_from
                        leave_to = rec.request_date_to
                        delta = leave_to - leave_from  # returns timedelta


                        for i in range(delta.days + 1):
                            date_list = []
                            day = leave_from + timedelta(days=i)
                            date_list.append(day)
                            for final_list in date_list:
                                if start_date == str(final_list):
                                    leave_list.append(rec.employee_id)



            if names.resource_calendar_id:
                if  names.resource_calendar_id.attendance_ids:
                    day = datetime.strptime(str(start_date), "%Y-%m-%d").strftime('%A')

                    for calendar in names.resource_calendar_id.attendance_ids:
                        if calendar:
                            if calendar.dayofweek == str(0):
                                input = 'Monday'
                            if calendar.dayofweek == str(1):
                                    input = 'Tuesday'
                            if calendar.dayofweek == str(2):
                                        input = 'Wednesday'
                            if calendar.dayofweek == str(3):
                                            input = 'Thursday'
                            if calendar.dayofweek == str(4):
                                            input = 'Friday'
                            if calendar.dayofweek == str(5):
                                            input = 'Saturday'
                            if calendar.dayofweek == str(6):
                                            input = 'Sunday'
                        if names.resource_calendar_id.global_leave_ids:
                            for leaves in names.resource_calendar_id.global_leave_ids:
                                leave_date=leaves.date_from

                                leave_date_d = leave_date.date()

                        if day == input:

                           if leave_date_d:

                                   if str(leave_date_d) != start_date:

                                        list1.append(names)
                           else:

                               list1.append(names)


        list2 = list(set(list1))

        date_format = '%Y-%m-%d'

        s_date = datetime.strptime(start_date, date_format)
        attendance=self.env['hr.attendance'].search([('checkin_date','=',s_date.date())])
        for att in attendance:
            remove_list.append(att.employee_id)
            remove_list = remove_list+leave_list
        for emp in remove_list:
            if emp in list2:
                list2.remove(emp)


        if not department_id:
            department = self.env['hr.department'].search([])
            for dep in department:
                dept_all.append(dep)
        else:
            for rec in department_id:
                a = self.env['hr.department'].search([('name', '=', rec)])

                department_list.append(a)

        return{
            'employee': list2,
            'department_id': dept_all,
            'start_date': start_date,
            'department_list': department_list,


         }