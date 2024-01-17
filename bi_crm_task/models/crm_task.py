# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.

from odoo.tools.translate import _
from datetime import datetime, timedelta, date
from dateutil.relativedelta import relativedelta
from odoo import tools, api
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT
from odoo import api, fields, models, _
import logging
from odoo.osv import  osv
from odoo import SUPERUSER_ID



class crm_lead(models.Model):
    """ CRM Lead Case """
    _inherit = "crm.lead"

    def task_count(self):
        task_obj = self.env['project.task']
        self.task_number = task_obj.search_count([('lead_id', 'in', [a.id for a in self])])

    task_number = fields.Integer(compute='task_count', string='Tasks')
    
class crm_task_wizard(models.TransientModel):
    _name = 'crm.task.wizard'
    
    
    def get_name(self):
        ctx = dict(self._context or {})
        active_id = ctx.get('active_id')
        crm_brw = self.env['crm.lead'].browse(active_id)
        name = crm_brw.name
        return name
    
    
    project_id = fields.Many2one('project.project','Project')
    dead_line = fields.Date('Deadline')
    start_date = fields.Date('Start Date')
    name = fields.Char('Task Name',default = get_name)
    user_id = fields.Many2one('res.users','Assigned To',default=lambda self: self.env.uid,
        index=True, track_visibility='always')

    def create_task(self):
        ctx = dict(self._context or {})
        active_id = ctx.get('active_id')
        crm_brw = self.env['crm.lead'].browse(active_id)
        vals = {'name': self.name,
                'project_id':self.project_id.id or False,
                'user_id': self.user_id.id or False,
                'date_deadline':  self.dead_line or False,
                'date_start':  self.start_date or False,
                'partner_id': crm_brw.partner_id.id or False,
                'lead_id': crm_brw.id or False
                }
        self.env['project.task'].create(vals)
        
class project_Task(models.Model):
    _inherit='project.task'
    
    lead_id =  fields.Many2one('crm.lead', 'Opportunity')

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
