# -*- coding: utf-8 -*-

import datetime
from datetime import datetime, timedelta
from odoo import SUPERUSER_ID
from odoo import api, fields, models, _
import calendar
import base64
import re

class AttendReminder(models.Model):
    _inherit = "hr.employee"

    hr_manager = fields.Many2one('hr.employee','HR Emp',store=True)
    att_mail = fields.Boolean('HR Attendance Reminder',store=True)
    att_mail1 = fields.Boolean('Manager Attendance Reminder', store=True)

    @api.model
    def manager_recsfd(self, task):
       
        vamk_new = [{'id': x.id, 'name': x.name} for x in
                    self.env['hr.employee'].search([('parent_id', '=', task)])]

        print(vamk_new)
        attend = self.env['hr.attendance'].search([])
        attend_vamk = []
        for x in vamk_new:

            curr = datetime.now().strftime('%Y-%m-%d')
            rms_list_in = []
            rms_list_out = []
            rms_list_ab = []
            for rms in attend:
                
                check_in = datetime.strptime(str(rms.check_in), '%Y-%m-%d %H:%M:%S').strftime('%Y-%m-%d')
                # check_out = datetime.strptime(rms.check_out, '%Y-%m-%d %H:%M:%S').strftime('%Y-%m-%d')
                if rms.check_out:
                    
                    check_out = datetime.strptime(str(rms.check_out), '%Y-%m-%d %H:%M:%S').strftime('%Y-%m-%d')
                    if check_out == curr:
                        rms_list_out.append(rms.employee_id.id)
                else:
                    
                    if check_in == curr:
                        rms_list_in.append(rms.employee_id.id)
                # if check_in==curr and rms.check_out == True:
                #  rms_list_out.append(rms.employee_id.id)

            if x['id'] in rms_list_in:
                attend_vamk.append({'name': x['name'], 'check_in': 'Yes', 'check_out': '-'})
                print(attend_vamk)
            elif x['id'] in rms_list_out:
                attend_vamk.append({'name': x['name'], 'check_in': 'Yes', 'check_out': 'Yes'})
                print(attend_vamk)
            else:
                attend_vamk.append({'name': x['name'], 'check_in': 'No', 'check_out': '-'})
                print(attend_vamk)

        return attend_vamk

    @api.model
    def hr_recsfd(self,task):
       
        vamk_new = [{'id':x.id,'name':x.name} for x in self.env['hr.employee'].search([('hr_manager','=',task)])]
        print(vamk_new)
        attend = self.env['hr.attendance'].search([])
        print(attend)
        attend_vamk = []
        for x in vamk_new:

            
            curr = datetime.now().strftime('%Y-%m-%d')
            rms_list_in = []
            rms_list_out = []
            rms_list_ab = []
            for rms in attend:
                check_in = datetime.strptime(str(rms.check_in), '%Y-%m-%d %H:%M:%S').strftime('%Y-%m-%d')
                #check_out = datetime.strptime(rms.check_out, '%Y-%m-%d %H:%M:%S').strftime('%Y-%m-%d')
                if rms.check_out:
                   
                   check_out = datetime.strptime(str(rms.check_out), '%Y-%m-%d %H:%M:%S').strftime('%Y-%m-%d')
                   if check_out == curr:
                      rms_list_out.append(rms.employee_id.id)
                else:
                   
                   if check_in == curr:
                      rms_list_in.append(rms.employee_id.id)
                #if check_in==curr and rms.check_out == True:
                 #  rms_list_out.append(rms.employee_id.id)
              
           
            if x['id'] in rms_list_in:
               attend_vamk.append({'name':x['name'],'check_in':'Yes','check_out':'-'})
               print(attend_vamk)
            elif x['id'] in rms_list_out: 
                 attend_vamk.append({'name':x['name'],'check_in':'Yes','check_out':'Yes'})
                 print(attend_vamk)
            else:
               attend_vamk.append({'name':x['name'],'check_in':'No','check_out':'-'})
               print(attend_vamk)

        return attend_vamk


    @api.model
    def new_hr_attach(self,task):
        
        report_name = 'Attendance'
        filename = "%s.%s" % (report_name, "pdf")
        result, format = self.env.ref('attend_mail_hr_manager.attendance_mail_report_id').render_qweb_pdf(task.id)
        result = base64.b64encode(result) # Use this in attachment creation in datas field
        ATTACHMENT_NAME = "Attendance Reminder"
        vamk_attac = self.env['ir.attachment'].create({
                    'name': filename,
                    'type': 'binary',           
                    'datas': result,

                    'store_fname': ATTACHMENT_NAME ,
                    'res_model': 'hr.employee',           
                    'res_id': task.id,           
                    'mimetype': 'application/x-pdf'           
                    })
        return vamk_attac

    @api.model
    def new_manager_attach(self, task):
        
        report_name = 'Attendance1'
        filename = "%s.%s" % (report_name, "pdf")
        result, format = self.env.ref('attend_mail_hr_manager.attendance_mail_report_manager_id').render_qweb_pdf(task.id)
        result = base64.b64encode(result)  # Use this in attachment creation in datas field
        ATTACHMENT_NAME = "Attendance Reminder"
        vamk_attac = self.env['ir.attachment'].create({
            'name': filename,
            'type': 'binary',
            'datas': result,

            'store_fname': ATTACHMENT_NAME,
            'res_model': 'hr.employee',
            'res_id': task.id,
            'mimetype': 'application1/x-pdf'
        })
        return vamk_attac


    @api.model
    def _cron_attendreminder_hr(self):
        
        su_id = self.env['res.partner'].browse(SUPERUSER_ID)
       # for task in self.env['hr.employee'].search(['|',('hr_manager', '=', None),('parent_id','=',None)]):
        for task in self.env['hr.employee'].search([('att_mail', '!=', False)]):
            print(task)
            template_id = self.env['ir.model.data'].get_object_reference(
                                                          'attend_mail_hr_manager',
                                                          'email_template_attend_mail_hr')[1]
            if template_id:
               email_template_obj = self.env['mail.template'].browse(template_id)
               values = email_template_obj.generate_email(task.id, fields=None)
               mail_mail_obj = self.env['mail.mail']
               msg_id = mail_mail_obj.create(values)

            if msg_id:
                  
                  msg_id.write({'attachment_ids': [(4, self.new_hr_attach(task).id)]})

                  msg_id.send()
        return True

    @api.model
    def _cron_attendreminder_manager(self):
       
        su_id = self.env['res.partner'].browse(SUPERUSER_ID)
        # for task in self.env['hr.employee'].search(['|',('hr_manager', '=', None),('parent_id','=',None)]):
        for task in self.env['hr.employee'].search([('att_mail1', '!=', False)]):
            print(task)
            template_id = self.env['ir.model.data'].get_object_reference(
                'attend_mail_hr_manager',
                'email_template_attend_mail_manager')[1]
            if template_id:
                email_template_obj = self.env['mail.template'].browse(template_id)
                values = email_template_obj.generate_email(task.id, fields=None)
                mail_mail_obj = self.env['mail.mail']
                msg_id = mail_mail_obj.create(values)

            if msg_id:
                    

                    msg_id.write({'attachment_ids': [(4, self.new_manager_attach(task).id)]})
                    msg_id.send()
        return True

    # @api.model
    # def _cron_attendreminder_manager(self):
    #     print("cccccccccccccccccccccccccccccccccccccc")
    #     su_id = self.env['res.partner'].browse(SUPERUSER_ID)
    #    # for task in self.env['hr.employee'].search(['|',('hr_manager', '=', None),('parent_id','=',None)]):
    #     for task in self.env['hr.employee'].search([('att_mail', '!=', False)]):
    #         template_id = self.env['ir.model.data'].get_object_reference(
    #                                                       'attend_mail_hr_manager',
    #                                                       'email_template_attend_mail_hr_manager')[1]
    #         if template_id:
    #            email_template_obj = self.env['mail.template'].browse(template_id)
    #            values = email_template_obj.generate_email(task.id, fields=None)
    #            mail_mail_obj = self.env['mail.mail']
    #            msg_id = mail_mail_obj.create(values)
    #
    #            if msg_id:
    #               print("weeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee")
    #               msg_id.write({'attachment_ids': [(4, self.new_manager_attach(task).id)]})
    #               msg_id.send()
    #     return True


#     @api.model
#     def _cron_attendance_in_mail(self):
#         su_id = self.env['res.partner'].browse(SUPERUSER_ID)
#         for task in self.env['hr.employee'].search([('user_id', '!=', None)]):
#             if task.user_id.login:
#                curr = datetime.now().strftime('%Y-%m-%d')
#                rms_list_in = []
#
#                for rms in task.attendance_ids:
#                    check_in = datetime.strptime(str(rms.check_in), '%Y-%m-%d %H:%M:%S').strftime('%Y-%m-%d')
#                 #check_out = datetime.strptime(rms.check_out, '%Y-%m-%d %H:%M:%S').strftime('%Y-%m-%d')
#                    if check_in == curr:
#                       rms_list_in.append(rms.id)
#                att = 'This is a reminder for you have not check-out yet.so please make sure that.'
#                if not rms_list_in:
#                   mail_body = ('\
# <p style="margin: 0px 0px 9px 0px; font-size: 13px; font-family: &quot;Lucida Grande&quot;, Helvetica, Verdana, Arial, sans-serif">Dear %s,</p>\
# <p style="margin: 0px 0px 9px 0px; font-size: 13px; font-family: &quot;Lucida Grande&quot;, Helvetica, Verdana, Arial, sans-serif">&nbsp; &nbsp; &nbsp; &nbsp; &nbsp;This is a reminder for you have not check-in yet.so please make sure your todays presence.</p>\
# <p style="margin: 0px 0px 9px 0px; font-size: 13px; font-family: &quot;Lucida Grande&quot;, Helvetica, Verdana, Arial, sans-serif">Date:&nbsp;<b><font style="background-color: rgb(179, 94, 155);">%s</font></b>,</p>') % (task.name,curr)
#
#                   mail_values_approval = {'email_to':task.user_id.login ,'subject': 'Attendance Check-in Reminder','body_html': mail_body,'notification': True}
#                   mail = self.env['mail.mail'].create(mail_values_approval)
#                   mail.send()
#         return True

    @api.model
    def _cron_attendance_in_mail(self):
    
     su_id = self.env['res.partner'].browse(SUPERUSER_ID)
     # for task in self.env['hr.employee'].search(['|',('hr_manager', '=', None),('parent_id','=',None)]):
     for task in self.env['hr.employee'].search([]):
         if task.user_id.login:
             curr = datetime.now().strftime('%Y-%m-%d')
             rms_list_in = []
             rms_list_out = []
             for rms in task.attendance_ids:
                 check_in = datetime.strptime(str(rms.check_in), '%Y-%m-%d %H:%M:%S').strftime('%Y-%m-%d')
                 # check_out = datetime.strptime(rms.check_out, '%Y-%m-%d %H:%M:%S').strftime('%Y-%m-%d')
                 if rms.check_out:
                     check_out = datetime.strptime(str(rms.check_out), '%Y-%m-%d %H:%M:%S').strftime('%Y-%m-%d')
                     if check_out == curr:
                         rms_list_out.append(rms.id)
                 else:
                     if check_in == curr:
                         rms_list_in.append(rms.id)

             if not rms_list_in:
                            print("suioo")
                            template_id = self.env['ir.model.data'].get_object_reference(
                            'attend_mail_hr_manager',
                            'email_template_attend_mail_checkin')[1]
                            if template_id:
                              email_template_obj = self.env['mail.template'].browse(template_id)
                              values = email_template_obj.generate_email(task.id, fields=None)
                              mail_mail_obj = self.env['mail.mail']
                              msg_id = mail_mail_obj.create(values)
                              msg_id.send()
     return True

#     @api.model
#     def _cron_attendance_out_mail(self):
#         su_id = self.env['res.partner'].browse(SUPERUSER_ID)
#         for task in self.env['hr.employee'].search([('user_id', '!=', None)]):
#             if task.user_id.login:
#                curr = datetime.now().strftime('%Y-%m-%d')
#                rms_list_in = []
#                rms_list_out = []
#                for rms in task.attendance_ids:
#                    check_in = datetime.strptime(str(rms.check_in), '%Y-%m-%d %H:%M:%S').strftime('%Y-%m-%d')
#                 #check_out = datetime.strptime(rms.check_out, '%Y-%m-%d %H:%M:%S').strftime('%Y-%m-%d')
#                    if rms.check_out:
#                       check_out = datetime.strptime(str(rms.check_out), '%Y-%m-%d %H:%M:%S').strftime('%Y-%m-%d')
#                       if check_out == curr:
#                          rms_list_out.append(rms.id)
#                    else:
#                       if check_in == curr:
#                          rms_list_in.append(rms.id)
#
#                if rms_list_in:
#                   mail_body = ('\
# <p style="margin: 0px 0px 9px 0px; font-size: 13px; font-family: &quot;Lucida Grande&quot;, Helvetica, Verdana, Arial, sans-serif">Dear %s,</p>\
# <p style="margin: 0px 0px 9px 0px; font-size: 13px; font-family: &quot;Lucida Grande&quot;, Helvetica, Verdana, Arial, sans-serif">&nbsp; &nbsp; &nbsp; &nbsp; &nbsp;This is a reminder for you have not check-out yet.so please make sure that.</p>\
# <p style="margin: 0px 0px 9px 0px; font-size: 13px; font-family: &quot;Lucida Grande&quot;, Helvetica, Verdana, Arial, sans-serif">Date:&nbsp;<b><font style="background-color: rgb(179, 94, 155);">%s</font></b>,</p>') % (task.name,curr)
#
#                   mail_values_approval = {'email_to':task.user_id.login ,'subject': 'Attendance Check-out Reminder','body_html': mail_body,'notification': True}
#                   mail = self.env['mail.mail'].create(mail_values_approval)
#                   mail.send()
#
#
#         return True

    @api.model
    def _cron_attendance_out_mail(self):
            su_id = self.env['res.partner'].browse(SUPERUSER_ID)
            # for task in self.env['hr.employee'].search(['|',('hr_manager', '=', None),('parent_id','=',None)]):
            for task in self.env['hr.employee'].search([]):
                if task.user_id.login:
                               curr = datetime.now().strftime('%Y-%m-%d')
                               rms_list_in = []
                               rms_list_out = []
                               for rms in task.attendance_ids:
                                   check_in = datetime.strptime(str(rms.check_in), '%Y-%m-%d %H:%M:%S').strftime('%Y-%m-%d')
                                #check_out = datetime.strptime(rms.check_out, '%Y-%m-%d %H:%M:%S').strftime('%Y-%m-%d')
                                   if rms.check_out:
                                      check_out = datetime.strptime(str(rms.check_out), '%Y-%m-%d %H:%M:%S').strftime('%Y-%m-%d')
                                      if check_out == curr:
                                         rms_list_out.append(rms.id)
                                   else:
                                      if check_in == curr:
                                         rms_list_in.append(rms.id)

                               if not rms_list_out:
                                    template_id = self.env['ir.model.data'].get_object_reference(
                                    'attend_mail_hr_manager',
                                    'email_template_attend_mail_checkout')[1]
                                    if template_id:
                                         email_template_obj = self.env['mail.template'].browse(template_id)
                                         values = email_template_obj.generate_email(task.id, fields=None)
                                         mail_mail_obj = self.env['mail.mail']
                                         msg_id = mail_mail_obj.create(values)
                                         msg_id.send()
            return True
