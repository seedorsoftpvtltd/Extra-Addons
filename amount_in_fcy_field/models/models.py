from odoo import api, fields, models, tools, _

class AccountMoveLine(models.Model):
    _inherit = "account.move.line"


    amount_currency = fields.Monetary(string='Amount in FCY', store=True, copy=True,
                                  help="The amount expressed in an optional other currency if it is a multi-currency entry.")