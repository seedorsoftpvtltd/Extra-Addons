from odoo import api, fields, models, _
from odoo.exceptions import AccessError

class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'
    _description = 'Account Move Line'

    narration = fields.Text(related='move_id.narration')