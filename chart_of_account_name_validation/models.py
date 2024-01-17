from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError

class AccountAccount(models.Model):
    _inherit='account.account'

    @api.constrains('name')
    def constrains_name(self):

        for account in self:
            existing_accounts = self.env['account.account'].search(
                [('name', '=', account.name), ('id', '!=', account.id)])
            if existing_accounts:
                raise ValidationError(_("An account with the name '%s' already exists.") % account.name)
