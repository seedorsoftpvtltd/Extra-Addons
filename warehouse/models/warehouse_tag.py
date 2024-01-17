from odoo import api,fields,models,_

class warehouseTagMenu(models.Model):
    _name ='warehouse.tag'
    _description = 'warehouse Tag'

    name = fields.Char(string="warehouse Tag")