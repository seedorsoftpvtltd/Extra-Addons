'''
Created on Jan 9, 2019

@author: Zuhair Hammadi
'''
from odoo import models, fields

class DepartmentTag(models.Model):
    _name = 'hr.department.tag'
    _description = 'Department Tag'
    
    name = fields.Char(required=True)
    code = fields.Char()
    active = fields.Boolean(default=True)

    _sql_constraints= [
            ('name_unqiue', 'unique(name)', 'Name must be unique!'),
            ('code_unqiue', 'unique(code)', 'Code must be unique!')
        ]    
