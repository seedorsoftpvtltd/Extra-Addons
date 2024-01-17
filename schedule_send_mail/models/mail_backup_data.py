# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.

from itertools import groupby
from datetime import datetime, timedelta, date
import pytz
from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError
from odoo.tools import float_is_zero, float_compare, DEFAULT_SERVER_DATETIME_FORMAT
from odoo.tools.misc import formatLang
from odoo.tools import html2plaintext
import odoo.addons.decimal_precision as dp
from odoo import http
from odoo.http import request
from odoo.exceptions import Warning

class ir_attachment_inherit(models.Model):
	_inherit = "ir.attachment"

	activity_data = fields.Many2one('mail.activity')

class mail_activity_inherit(models.Model):
	_inherit = "mail.activity"

	name = fields.Char("Activity Name")
	attachment_ids = fields.Many2many("ir.attachment" ,string = "attachment")
	schedule_date = fields.Datetime(string = "Schedule Date")
	subject = fields.Char("Subject")
	partner_ids = fields.Many2many("res.partner" ,string = "partner")
	date_schedule = fields.Datetime(string = "Schedule Date")
	recipient_ids = fields.Many2many('res.partner','resicpient_id',string='Recipients')
	
	def action_mail_message_for_scheduler(self):
		email_to = []
		mail_activity = self.env['mail.activity'].search([])
		for abc in mail_activity:
			for follower in abc.partner_ids:
				email_to.append(follower.id)
			schedule_date = self.search([],order = "id desc",limit=1)
			user_id = self.env['res.users']
			manager_id = self.env['ir.model.data'].sudo().get_object_reference('base','group_system')[1]
			group_manager = self.env['res.groups'].sudo().browse(manager_id)
			super_user = group_manager.users[0]
			tz = pytz.timezone(super_user.tz or 'UTC')
			tz_time = datetime.now(tz=tz).strftime("%H:%M:%S")
			backup_ids = self.search([('schedule_date',"=",datetime.now(tz=tz).strftime("%Y-%m-%d %H:%M"))])
			super_user = self.env['res.users'].browse(self.env.uid).partner_id
			
			template_id = self.env['ir.model.data'].get_object_reference(
																		  'schedule_send_mail',
																		  'mail_message_backup_template')[1]
			email_template_obj = self.env['mail.template'].browse(template_id)
			email_body = email_template_obj.body_html
			if abc.date_schedule:
				if abc.date_schedule <= datetime.now():
					for data in abc:
						partner_ids = []
						attach = []
						from_partner_id = self.env['res.users'].browse(data.user_id.id).partner_id
						values = email_template_obj.generate_email(self.id, fields=None)
						origin_data = self.env[data.res_model].search([('id','=',data.res_id)])
						values['email_from'] = from_partner_id.email
						partner_ids.append(from_partner_id.id)
						values['res_id'] = data.res_id
						values['recipient_ids'] = [(4, pid) for pid in email_to]
						partner_ids.append(super_user.id)
						values['reply_to'] = from_partner_id.email
						values['message_type'] = 'comment'
						values['notification'] = True
						values['model'] = data.res_model
						values['author_id'] = from_partner_id.id
						values['subject'] = data.summary
						values['body_html']  = data.note
						attachment = self.env['ir.attachment'].search([('activity_data','=',data.id)])
						values['attachment_ids']  = [(6, 0, attachment.ids)]
						mail_mail_obj = self.env['mail.mail']
						msg_id = mail_mail_obj.sudo().create(values)
						if msg_id:
							mail_mail_obj.send([msg_id])
							msg_id.send()
							mail_message_id = self.env['mail.message'].search([], limit=1, order="id desc")
							if mail_message_id:
								mail_message_id.update({'body' : data.note, 'partner_ids':email_to, 'attachment_ids' : attachment
								})
								for line in mail_message_id.notification_ids:
									line.is_read =  True
									line.is_email =  True
									
							data.unlink()

	def activity_format(self):
		activities = self.read()
		mail_template_ids = set([template_id for activity in activities for template_id in activity["mail_template_ids"]])
		mail_template_info = self.env["mail.template"].browse(mail_template_ids).read(['id', 'name'])
		mail_template_dict = dict([(mail_template['id'], mail_template) for mail_template in mail_template_info])
		for activity in activities:
			activity['mail_template_ids'] = [mail_template_dict[mail_template_id] for mail_template_id in activity['mail_template_ids']]
			attachment_ids =[]
			base = http.request.env['ir.config_parameter'].sudo().get_param('web.base.url')
			if len(activity['attachment_ids']) > 0:
				for i in activity['attachment_ids']:
					attachment_id = self.env['ir.attachment'].browse(i)
					attachment_ids.append({
							'id' : attachment_id.id,
							'name': attachment_id.name,
							'filename': attachment_id.name,
							'mimetype': attachment_id.mimetype,
							'url':base +'/web/content/'+str(attachment_id.id)+'?download: true'
						})
			res_id = self.env[activity['res_model']].browse(activity['res_id'])
			partner_name_list = []
			for i in activity['partner_ids']:
				partner = self.env['res.partner'].search([('id','=',i)])
				partner_name_list.append(partner.name)
			activity['partner_name'] = partner_name_list
			activity['attachment_ids'] = attachment_ids

		return activities			

class ScheduleSendMessage(models.Model):
	_name = 'schedule.send.message'
	
	note = fields.Html('Note')
	subject = fields.Char("Subject")
	attachment_ids = fields.Many2many("ir.attachment" ,string = "Attachments")
	schedule_date = fields.Datetime(string = "Schedule Date Time")
	partner_ids = fields.Many2many('res.partner', string='Recipients')



	def action_add_schedule_send_message(self):
		local_tz = pytz.timezone(self.env.context.get('tz') or self.env.user.tz or 'UTC')  
		record_data = datetime.strftime(pytz.utc.localize(datetime.strptime(str(self.schedule_date), DEFAULT_SERVER_DATETIME_FORMAT)).astimezone(local_tz),"%Y-%m-%d %H:%M:%S")
		dt = datetime.combine(date.today(), datetime.min.time())
		if self.schedule_date:
			if self.schedule_date < dt:
				raise ValidationError(_('Please Select Valid Schedule Date.'))
		email_to = []
		mail_message_id = self.env['ir.attachment'].search([], limit=1, order="id desc")
		attachment_obj = self.env['ir.attachment']
		model_id = self.env['ir.model']._get(self._name).id
		abc = self.env['mail.activity'].search([],order="id desc",limit=1)
		model_name = self.env.context.get('default_model',False)
		origin_id = self.env[model_name].search([('id','=',self.env.context.get('default_res_id',False))])
				
		for follower in origin_id.message_follower_ids:
			email_to.append(follower.partner_id.id)
			for i in self.partner_ids:
				email_to.append(i.id)

			
		activity_type1 = self.env['mail.activity.type'].search([('name','=','Scheduled Email')])
		if not activity_type1:
			self.env['mail.activity.type'].create({'name' : 'Scheduled Email'})
		activity_type = self.env['mail.activity.type'].search([('name','=','Scheduled Email')])
		mdl = self.env.context.get('default_model',False)
		if mdl and activity_type:
			model = self.env['ir.model'].search([('model','=',mdl)])
			list_attach = []
			for i in self.attachment_ids:
				list_attach.append(i.id)


			for form in self:
				data_created = {
					'note': form.note,
					'summary': form.subject,
					'res_id': self.env.context.get('default_res_id',False),
					'res_model_id': model.id,
					'activity_type_id':activity_type.id,
					'date_deadline': date.today(),
					'attachment_ids' : [(6,0,list_attach)],
					'partner_ids' : [(6,0,email_to)],
					'schedule_date' : record_data,
					'date_schedule' : self.schedule_date,
					'recipient_ids' : self.partner_ids
				}
				res = self.env['mail.activity'].create(data_created)
				res.action_close_dialog()
				attachment_detail = []
				for i in self.attachment_ids:
					attachment_detail.append(i.id)
					i.update({
						'res_model' :model_name,
						'res_id' : origin_id.id,
						'activity_data':res.id
						})
				res.attachment_ids = attachment_detail
				
		return {
			'type': 'ir.actions.client',
			'tag': 'reload',
		}	

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: