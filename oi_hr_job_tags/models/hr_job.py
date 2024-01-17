'''
Created on Jan 14, 2019

@author: Zuhair Hammadi
'''
from odoo import models, fields

class Job(models.Model):
    _inherit='hr.job'
    
    tag_ids = fields.Many2many('hr.job.tag', string='Tags')