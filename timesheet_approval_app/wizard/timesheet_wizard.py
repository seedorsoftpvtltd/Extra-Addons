from odoo import models, fields, api ,_
from datetime import datetime

class reject_wizard(models.TransientModel):
	_name='reject.wizard'

	
	reason=fields.Char(string="Reason")

	def reject_button(self):
		current_id = self.env['account.analytic.line'].browse(self.env.context.get('active_ids'))
		current_id.write({'rejected_reason':self.reason})
		for record in current_id:
			template_id = self.env['ir.model.data'].get_object_reference('timesheet_approval_app','timesheet_email_template2')[1]
			email_template_obj = self.env['mail.template'].browse(template_id)
			record.rejected_by_id = self.env.user
			record.rejected_date = datetime.today()
			if template_id:
				values = email_template_obj.generate_email(record.id, fields=None)
				values['email_from'] = self.env.user.email
				values['email_to'] = record.user_id.partner_id.email or ''
				values['author_id'] = self.env.user.partner_id.id
				html= """
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
				html+= "<tr><td>{}</td>".format(record.date)
				html+= "<td>{}</td>".format(record.name)
				html+= "<td>{}</td>".format(record.project_id.name)
				html+= "<td>{}</td>".format(record.task_id.name)
				html+= "<td>{}</td></tr>".format(record.unit_amount)
				html+="</table></html>"
				values['body_html'] = html 
#				mail_mail_obj = self.env['mail.mail']
#				msg_id = mail_mail_obj.sudo().create(values)
#				if msg_id:
#					msg_id.sudo().send()
			record.state = 'reject'
			

class approve_wizard(models.TransientModel):
	_name='approve.wizard'

	message = fields.Text(string="Please Approve Timesheet!!!", readonly=True, store=True)

	def approve_button(self):
		current_id = self.env['account.analytic.line'].browse(self.env.context.get('active_ids'))
		for record in current_id:
			template_id = self.env['ir.model.data'].get_object_reference('timesheet_approval_app','timesheet_email_template')[1]
			email_template_obj = self.env['mail.template'].browse(template_id)
			record.approved_by_id = self.env.user
			record.approved_date = datetime.today()
			if template_id:
				values = email_template_obj.generate_email(record.id, fields=None)
				values['email_from'] = self.env.user.email
				values['email_to'] = record.user_id.partner_id.email or ''
				values['author_id'] = self.env.user.partner_id.id
				html= """
							<html>
							<div style="margin: 0px; padding: 0px;">
										<p style="margin: 0px; padding: 0px; font-size: 13px;">
										Hello,
											<br/>
											Your Timesheet is Approved									<br/>
											<br/>
											<br>Details:</br>
											<br></br>
							<table border="1">
							<tr><th>Date</th><th>Description</th><th>Project</th><th>Task</th>
							<th>Duration</th></tr>"""

				html+= "<tr><td>{}</td>".format(record.date)
				html+= "<td>{}</td>".format(record.name)
				html+= "<td>{}</td>".format(record.project_id.name)
				html+= "<td>{}</td>".format(record.task_id.name)
				html+= "<td>{}</td></tr>".format(record.unit_amount)

				html+="</table></html>"
				values['body_html'] = html 
#				mail_mail_obj = self.env['mail.mail']
#				msg_id = mail_mail_obj.sudo().create(values)
#				if msg_id:
#					msg_id.sudo().send()
			record.state = 'approve'
