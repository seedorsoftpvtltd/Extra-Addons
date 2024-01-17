from odoo import models, fields, api, _


class Account(models.Model):
    _inherit = "account.account"

    tax_flag = fields.Boolean('Is Tax')