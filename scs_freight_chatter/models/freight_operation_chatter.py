# from odoo import api, fields, models,

from odoo import models, fields, api, _





class FreightOperation(models.Model):
    _name = 'freight.operation'
    _inherit = ['freight.operation', 'mail.thread', 'mail.activity.mixin', ]


