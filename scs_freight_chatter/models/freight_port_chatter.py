from odoo import models, fields, api, _


class FreightPort(models.Model):
    _name = 'freight.port'
    _inherit = ['freight.port', 'mail.thread', 'mail.activity.mixin', ]

    name = fields.Char(tracking=True)
