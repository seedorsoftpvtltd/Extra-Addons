# from odoo import api, fields, models,

from odoo import models, fields, api, _





class FreightContainers(models.Model):
    _name = 'freight.container'
    _inherit = ['freight.container', 'mail.thread', 'mail.activity.mixin', ]


