from odoo import models, fields, api ,_
from datetime import datetime

class reject_wizard(models.TransientModel):
	_name='reject.wizard'

	reason=fields.Char(string="Reason")

	
	def reject_button(self):
		

		current_ids = self.env['account.analytic.line'].browse(self.env.context.get('active_ids'))
		abc=current_ids.write({'rejected_reason':self.reason})
		
		for rec in current_ids:
			template_id=self.env.ref('timesheet_approval_app.timesheet_email_template2').ids
			template=self.env['mail.template'].browse(template_id)
			template.send_mail(self.id, force_send=True)
			rec.rejected_by_id=self.env.user
			rec.rejected_date=datetime.today()

		return current_ids.write({'state': 'reject'})
			
		
			


class approve_wizard(models.TransientModel):
	_name='approve.wizard'

	approve_wizard=fields.Char(string="Are You sure want to approve?")

	def approve_button(self):

		current_ids = self.env['account.analytic.line'].browse(self.env.context.get('active_ids'))
		
		
		for rec in current_ids:
			template_id=self.env.ref('timesheet_approval_app.timesheet_email_template').ids
			template=self.env['mail.template'].browse(template_id)
			template.send_mail(self.id, force_send=True)
			rec.approved_by_id=self.env.user
			rec.approved_date=datetime.today()

		return current_ids.write({'state': 'approve'})