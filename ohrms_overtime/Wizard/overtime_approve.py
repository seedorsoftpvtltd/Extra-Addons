from odoo import models, fields, api, _
from datetime import datetime


class reject_overtime_wizard(models.TransientModel):
    _name = 'reject.overtime.wizard'

    reason = fields.Char(string="Reason")
    approve_dur = fields.Float(string="Approved Hours", store=True)
    def reject_overtime_button(self):
        current_id = self.env['hr.overtime'].browse(self.env.context.get('active_ids'))
        current_id.write({'rejected_reason': self.reason})
        for record in current_id:
            template_id = \
            self.env['ir.model.data'].get_object_reference('ohrms_overtime', 'overtime_email_template2')[1]
            email_template_obj = self.env['mail.template'].browse(template_id)
            record.rejected_by_id = self.env.user
            record.rejected_date = datetime.today()
            # if template_id:
            #     values = email_template_obj.generate_email(record.id, fields=None)
            #     values['email_from'] = self.env.user.email
            #     values['email_to'] = record.employee_id.user_id.email or ''
            #     values['author_id'] = self.env.user.partner_id.id
            #     html = """
			# 				<html>
			# 				<div style="margin: 0px; padding: 0px;">
			# 							<p style="margin: 0px; padding: 0px; font-size: 13px;">
			# 								Hello """+str(record.employee_id.name)+""", </br>
			# 								<br/>
			# 								Your Overtime is Rejected
			#
			# 								<br/>
			# 								Rejected Reason:
			# 								</br>
			# 								"""+str(record.rejected_reason)+"""								<br/>
			# 								<br/>
			# 				"""
            #
            #     # html += "<tr><td>{}</td>".format(record.employee_id)
            #     # html += "<td>{}</td>".format(record.date_from)
            #     # html += "<td>{}</td>".format(record.date_to)
            #     # html += "<td>{}</td>".format(record.type)
            #     # html += "<td>{}</td></tr>".format(record.days_no_tmp)
            #     html += "</table></html>"
            #     values['body_html'] = html
            #     mail_mail_obj = self.env['mail.mail']
            #     msg_id = mail_mail_obj.sudo().create(values)
            #     if msg_id:
            #         msg_id.sudo().send()
            record.state = 'refused'


class approve_overtime_wizard(models.TransientModel):
    _name = 'approve.overtime.wizard'

    message = fields.Text(string="Please Approve Overtime!!!", readonly=True, store=True)

    def approve_overtime_button(self):
        current_id = self.env['hr.overtime'].browse(self.env.context.get('active_ids'))
        for record in current_id:
            template_id = \
            self.env['ir.model.data'].get_object_reference('ohrms_overtime', 'overtime_email_template')[1]
            email_template_obj = self.env['mail.template'].browse(template_id)
            record.approved_by_id = self.env.user
            record.approved_date = datetime.today()
            # if template_id:
            #     values = email_template_obj.generate_email(record.id, fields=None)
            #     values['email_from'] = self.env.user.email
            #     values['email_to'] = record.employee_id.user_id.email or ''
            #     values['author_id'] = self.env.user.partner_id.id
            #     html = """
			# 				<html>
			# 				<div style="margin: 0px; padding: 0px;">
			# 							<p style="margin: 0px; padding: 0px; font-size: 13px;">
			# 								Hello """+str(record.employee_id.name)+""",
			# 								<br/>
			# 								Your Overtime is Approved.								<br/>
			# 								<br/>
			#
			#
			#
			# 				"""
            #
            #     # html += "{}".format(record.employee_id.name)
            #     # html += "<td>{}</td>".format(record.date_from)
            #     # html += "<td>{}</td>".format(record.date_to)
            #     # html += "<td>{}</td>".format(record.type)
            #     # html += "<td>{}</td></tr>".format(record.days_no_tmp)
            #     # html += "<td>{}</td>".format(record.project_id.name)
            #     # html += "<td>{}</td>".format(record.task_id.name)
            #     # html += "<td>{}</td></tr>".format(record.unit_amount)
            #     # #
            #     html += "</table></html>"
            #     values['body_html'] = html
            #     mail_mail_obj = self.env['mail.mail']
            #     msg_id = mail_mail_obj.sudo().create(values)
            #     if msg_id:
            #         msg_id.sudo().send()
            record.state = 'approved'
