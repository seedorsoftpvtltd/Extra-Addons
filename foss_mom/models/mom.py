# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _
from odoo.exceptions import UserError

class Meeting(models.Model):
	_inherit = 'calendar.event'

	discussion = fields.Html(string='Discussion')
	action_items = fields.Html(string='Action Items')
	project_id = fields.Many2one('project.project', string='Project')
	task_line = fields.One2many('task.line','event_id', string='Tasks')
	company_id = fields.Many2one('res.company', 'Company', default=lambda self: self.env['res.company']._company_default_get('product.conversion'))

	def create_tasks(self):
		count = 0
		count_1 = 0
		for task in self.task_line:
			if task and not task.task_id:
				vals = {
					'name' : task.name or '',
					'project_id': self.project_id.id or False,
					'description' : task.description or '',
					'user_id' : task.user_id.id or '',
					'date_deadline' : task.date_deadline or False,
					'stage_id' : task.stage_id.id or '',
					}
				task_obj = self.env['project.task'].create(vals)
				task.write({
					'task_id' : task_obj.id
					})
		task = [task for task in self.task_line]
		if not task:
			raise UserError(_('Warning! There are no tasks to be created'))
		return True

	def email_mom(self):
		self.ensure_one()
		ir_model_data = self.env['ir.model.data']
		try:
			template_id = ir_model_data.get_object_reference('foss_mom', 'email_template_foss_mom')[1]
		except ValueError:
			template_id = False
		try:
			compose_form_id = ir_model_data.get_object_reference('mail', 'email_compose_message_wizard_form')[1]
		except ValueError:
			compose_form_id = False
		ctx = ({

				'default_model': 'calendar.event',
				'default_res_id': self.ids[0],
				'default_use_template': bool(template_id),
				'default_template_id': template_id,
				'force_email': True,
				'default_partner_ids' :  [(6,0, [i.partner_id.id for i in self.attendee_ids if i.state == 'accepted'])]             
			})
		return {
			'type': 'ir.actions.act_window',
			'view_type': 'form',
			'view_mode': 'form',
			'res_model': 'mail.compose.message',
			'views': [(compose_form_id, 'form')],
			'view_id': compose_form_id,
			'target': 'new',
			'context': ctx,
		}

	def print_mom(self):
		return self.env.ref('foss_mom.action_report_foss_mom')\
			.with_context({'discard_logo_check': True}).report_action(self)

class TaskLine(models.Model):
	_name = 'task.line'

	event_id = fields.Many2one('calendar.event',string='Calendar')
	name = fields.Char(string='Name')
	description = fields.Char(string='Description')
	user_id = fields.Many2one('res.users',string='Assigned To')
	date_deadline = fields.Date(string='Deadline')
	stage_id = fields.Many2one('project.task.type',related="task_id.stage_id" ,string='Status')
	task_id = fields.Many2one('project.task', string="Task ID")

	def write(self, vals):
		res = super(TaskLine , self).write(vals)
		self.task_id.name = self.name
		self.task_id.description = self.description
		self.task_id.date_deadline = self.date_deadline
		self.task_id.user_id = self.user_id.id
		return res

	@api.onchange('date_deadline')
	def _onchange_date_deadline(self):
		meeting_start_date = ''
		if self.event_id.start_date or self.event_id.start_datetime:
			meeting_start_date = self.event_id.start_date or self.event_id.start_datetime.date()
		if self.event_id:
			if meeting_start_date:
				if self.date_deadline:
					if self.date_deadline < meeting_start_date:
						raise UserError(_('Warning! Date Deadline is lesser than the meeting start date'))
		return {}

	def unlink(self):
		for line in self:
			line.task_id.unlink()
		return super(TaskLine , self).unlink()




