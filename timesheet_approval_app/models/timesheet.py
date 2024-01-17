from odoo import models, fields, api,_ 
from datetime import datetime,date


class MyTimesheet(models.Model):
	_name='account.analytic.line'
	_inherit = ['account.analytic.line','mail.thread']
#	_inherit ='mail.thread'
	
	approved_by_id=fields.Many2one('res.users',string="Approved By",readonly=True)
	approved_date = fields.Datetime(string="Approved Date",readonly=True)
	rejected_by_id=fields.Many2one('res.users',string="Rejected By")
	rejected_date = fields.Datetime(string="Rejected Date",readonly=True)
	rejected_reason=fields.Char(string="Rejected Reason",readonly=True)
	state = fields.Selection([
		('draft', 'Draft'),
		('submitted', 'Submitted'),
		('approve', 'Approved'),
		('reject', 'Rejected'),
		], string='Status',default='draft')

	def submit_to_manager(self):
		return self.write({'state': 'submitted'})

	def set_to_draft(self):
		return self.write({'state': 'draft'})

	def approve_by_manager(self):
#		template_id = self.env['ir.model.data'].get_object_reference('timesheet_approval_app','timesheet_email_template')[1]
#		email_template_obj = self.env['mail.template'].browse(template_id)
		self.approved_by_id=self.env.user
		self.approved_date=datetime.today()
#		if template_id:
#			values = email_template_obj.generate_email(self.id, fields=None)
#			values['email_from'] = self.env.user.email
#			values['email_to'] = self.user_id.partner_id.email or ''
#			values['author_id'] = self.env.user.partner_id.id
#			html= """
#						<html>
#						<div style="margin: 0px; padding: 0px;">
#									<p style="margin: 0px; padding: 0px; font-size: 13px;">
#										Hello,
#										<br/>
#										Your Timesheet is Approved									<br/>
#										<br/>
#										<br>Details:</br>
#										<br></br>
#						<table border="1">
#						<tr><th>Date</th><th>Description</th><th>Project</th><th>Task</th>
#						<th>Duration</th></tr>
#					"""
#			html+= "<tr><td>{}</td>".format(self.date)
#			html+= "<td>{}</td>".format(self.name)
#			html+= "<td>{}</td>".format(self.project_id.name)
#			html+= "<td>{}</td>".format(self.task_id.name)
#			html+= "<td>{}</td></tr>".format(self.unit_amount)
#			html+="</table></html>"
#			values['body_html'] = html 
#			mail_mail_obj = self.env['mail.mail']
#			msg_id = mail_mail_obj.sudo().create(values)
#			if msg_id:
#				msg_id.sudo().send()
		return self.write({'state': 'approve'})
			
