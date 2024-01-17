# from odoo import api, fields, models,

from odoo import models, fields, api, _


class OperationCustom(models.Model):
    _name = 'operation.custom'
    _inherit = ['operation.custom', 'mail.thread', 'mail.activity.mixin', ]
