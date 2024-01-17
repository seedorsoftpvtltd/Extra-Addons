from odoo import models, fields, api,_
from datetime import datetime, time, date, timedelta
from dateutil.relativedelta import relativedelta
from odoo.exceptions import ValidationError
import calendar

class YourWizard(models.TransientModel):
    _name = 'absent.report'
    _description = 'Absent Report Wizard'

    start_date=fields.Date('Date',default=lambda self: fields.Date.today(),required='1')
    end_date=fields.Date('End Date',default=lambda self: fields.Date.today(),required='1')
    department_id=fields.Many2many('hr.department',string='Department')
    company_id=fields.Many2one('res.company',default=lambda self: self.env.company)


    def print_pdf(self):
        """ Button function for PDF """
        list=[]
        department_list=[]


        current_datetime = datetime.now()
        if self.start_date > current_datetime.date():
            raise ValidationError(_('The provided date is in the future.'))
        for rec in self:
            if rec.department_id:
                for dept in rec.department_id:
                    list.append(dept.name)

        # department=self.env['hr.department'].search([])
        # for all in department:
        #     department_list.append(all.name)
        # print(department_list)
        data = {
            'start_date': self.start_date,
            'end_date': self.end_date,
            'department_id': list,
            # 'department_list':department_list,
        }

        return self.env.ref(
            'absent_attendance_report.absent_report_pdf').report_action(self, data)