from odoo import api, fields, models, _


class AccountMove(models.Model):
    _inherit = "account.move"

    pono = fields.Char(string='PO No')
    podate = fields.Date(string='PO Date')
    jobno = fields.Char(string='Job No')