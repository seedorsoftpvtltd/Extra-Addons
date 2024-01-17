'''
Created on Jan 9, 2019

@author: Zuhair Hammadi
'''
from odoo import models, fields

class Department(models.Model):
    _inherit='hr.department'
    
    tag_ids = fields.Many2many('hr.department.tag', string='Tags')