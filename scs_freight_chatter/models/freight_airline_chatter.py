# from odoo import api, fields, models,

from odoo import models, fields, api, _





class FreightAirline(models.Model):
    _name = 'freight.airline'
    _inherit = ['freight.airline', 'mail.thread', 'mail.activity.mixin', ]


