# from odoo import api, fields, models,

from odoo import models, fields, api, _


class FreightVessels(models.Model):
    _name = 'freight.vessels'
    _inherit = ['freight.vessels', 'mail.thread', 'mail.activity.mixin', ]
