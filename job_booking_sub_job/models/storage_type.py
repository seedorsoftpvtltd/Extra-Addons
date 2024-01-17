from odoo import models, fields, api, _

class StorageType(models.Model):
    _name = 'storage.type'

    name = fields.Char(string="Name")