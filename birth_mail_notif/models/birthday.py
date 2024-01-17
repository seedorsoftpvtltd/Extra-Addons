import datetime
from odoo import api, models, fields, _
from odoo.exceptions import UserError

class HrBirth(models.Model):
    _inherit = 'hr.employee'

    @api.model
    def employee_birth_not(self):
        cr_date = datetime.datetime.today()
        birth_env = self.env['hr.employee']
        birth_ids = birth_env.search([])
        birth_sr = len(birth_env.search([('birthday', 'like', cr_date.strftime("%m-%d"))]))
        for rcs in birth_ids:
            template_id = \
            self.env['ir.model.data'].get_object_reference('birth_mail_notif', 'employee_birthday_not_template')[1]

            if template_id and birth_sr != 0:
               email_template_obj = self.env['mail.template'].browse(template_id)
               values = email_template_obj.generate_email(rcs.id, fields=None)
               values['email_from'] = rcs.company_id.email
               values['email_to'] = rcs.work_email
               mail_mail_obj = self.env['mail.mail']
               msg_id = mail_mail_obj.sudo().create(values)
               if msg_id:
                  msg_id.sudo().send()
                  print(rcs.name)
        return True

    def get_birth_ids(self):
        cr_date = datetime.datetime.today()
        birth_ids = self.search([('birthday', 'like', cr_date.strftime("%m-%d"))])
        records=[]
        for emp_id in birth_ids:
            birt_list={}
            if emp_id:
               birt_list['emp_name'] =  emp_id.name
               birt_list['emp_role'] = emp_id.job_id.name
               records.append(birt_list)
        return records