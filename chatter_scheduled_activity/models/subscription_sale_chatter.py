# from odoo import api, fields, models,

from odoo import models, fields, api, _





class ScheduledActivity(models.Model):
    _name = 'subscription.subscription'
    _inherit = ['subscription.subscription', 'mail.activity.mixin', ]


