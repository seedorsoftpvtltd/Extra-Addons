from odoo import api, fields, models, _
from odoo.exceptions import AccessError

class AccountMove(models.Model):
    _inherit = 'account.move'
    _description = 'Account Move'

    x_freight_type = fields.Many2one('utm.medium', 'Freight Type')