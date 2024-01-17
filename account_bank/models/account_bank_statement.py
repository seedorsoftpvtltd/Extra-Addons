# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError


class AccountBankStatement(models.Model):
    _inherit = 'account.bank.statement'

    is_from_payment = fields.Boolean(string='Is From Payment', default=False, copy=False)

    def button_reopen(self):
        res = super(AccountBankStatement, self).button_reopen()
        if self.is_from_payment:
            raise ValidationError(_('Warning! You are not allowed to do this action. \n This statement is created automatically from Payment, Use Cancel option in Payment.'))
        return res
