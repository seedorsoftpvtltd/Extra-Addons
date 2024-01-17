from odoo import models, fields


class JournalEntries(models.Model):
    _inherit = 'account.move.line'

    account_types=fields.Selection('Account Type',related='account_id.user_type_id.type')