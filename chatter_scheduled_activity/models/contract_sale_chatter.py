# from odoo import api, fields, models,

from odoo import models, fields, api, _





class AccountAnalytic(models.Model):
    _name = 'account.analytic.account'
    _inherit = ['account.analytic.account', 'mail.thread', 'mail.activity.mixin', ]


