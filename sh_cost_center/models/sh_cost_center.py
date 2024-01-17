# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import models,fields,api,_

class ShCostCenter(models.Model):
    _name='sh.cost.center'
    _description="Cost Centers"
    _rec_name = 'sh_code'
    _inherit = ['mail.thread', 'mail.activity.mixin', 'resource.mixin']
    
    
    sh_code = fields.Char('Code',track_visibility="onchange",required=True)
    sh_title = fields.Char('Title',track_visibility="onchange",required=True)
    sh_company = fields.Many2one('res.company',string="Company",track_visibility="onchange")
    