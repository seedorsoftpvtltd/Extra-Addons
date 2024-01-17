'''
Created on Jan 14, 2019

@author: Zuhair Hammadi
'''
from odoo import models, fields

class JobTag(models.Model):
    _name = 'hr.job.tag'
    _description = "Job Position Tag"
    
    name = fields.Char(required=True)
    active = fields.Boolean(default=True)

    _sql_constraints= [
            ('name_unqiue', 'unique(name)', 'Name must be unique!')
        ]    
