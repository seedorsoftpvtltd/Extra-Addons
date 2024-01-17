# from odoo import api, fields, models,

from odoo import models, fields, api, _


class OperationPriceList(models.Model):
    _name = 'operation.price.list'
    _inherit = ['operation.price.list', 'mail.thread', 'mail.activity.mixin', ]

    name = fields.Char(tracking=True)
