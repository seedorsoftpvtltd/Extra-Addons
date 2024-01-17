from odoo import models, fields, api,_
from datetime import datetime,date


class MyTimesheet(models.Model):
    _name="account.analytic.line"
    _inherit = ['account.analytic.line','mail.thread']

    def timesheet_reject(self, current_id, a):
        print("test")

        id = self.env['account.analytic.line'].browse(current_id)
        print(id)
        print(a)
        id.write({'rejected_reason': a})
        for record in id:
            template_id = \
                self.env['ir.model.data'].get_object_reference('timesheet_approval_app',
                                                               'timesheet_email_template2')[1]
            email_template_obj = self.env['mail.template'].browse(template_id)
            record.rejected_by_id = self.env.user
            record.rejected_date = datetime.today()
            if template_id:
                values = email_template_obj.generate_email(record.id, fields=None)
                values['email_from'] = self.env.user.email
                values['email_to'] = record.user_id.partner_id.email or ''
                values['author_id'] = self.env.user.partner_id.id
                html = """
                                        <html>
                                             <div style="margin: 0px; padding: 0px;">
                                                  <p style="margin: 0px; padding: 0px; font-size: 13px;">
                                                       Hello,
                                                           <br/>
                                                              Your Timesheet is Rejected									<br/>
                                                           <br/>
                                                           <br>Details:</br>
                                                           <br></br>
                                                       <table border="1">
                                                   <tr><th>Date</th><th>Description</th><th>Project</th><th>Task</th>
                                               <th>Duration</th></tr>"""
                html += "<tr><td>{}</td>".format(record.date)
                html += "<td>{}</td>".format(record.name)
                html += "<td>{}</td>".format(record.project_id.name)
                html += "<td>{}</td>".format(record.task_id.name)
                html += "<td>{}</td></tr>".format(record.unit_amount)
                html += "</table></html>"
                values['body_html'] = html
                mail_mail_obj = self.env['mail.mail']
                # msg_id = mail_mail_obj.sudo().create(values)
                # print(msg_id)
                # if msg_id:
                #     msg_id.sudo().send()
            record.state = 'reject'
        return True



