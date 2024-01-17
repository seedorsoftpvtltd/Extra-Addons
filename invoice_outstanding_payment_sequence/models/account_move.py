from odoo import api, fields, models, _
from odoo.exceptions import RedirectWarning, UserError, ValidationError, AccessError
from odoo.tools import float_is_zero, float_compare, safe_eval, date_utils, email_split, email_escape_char, email_re
from odoo.tools.misc import formatLang, format_date, get_lang

from collections import defaultdict
from datetime import date, timedelta
from itertools import groupby
from itertools import zip_longest
from hashlib import sha256
from json import dumps

import json
import re


class AccountMove(models.Model):
    _inherit = "account.move"

    @api.model
    def _compute_payments_widget_to_reconcile_info(self):
        for move in self:
            move.invoice_outstanding_credits_debits_widget = json.dumps(False)
            move.invoice_has_outstanding = False

            if move.state != 'posted' or move.invoice_payment_state != 'not_paid' or not move.is_invoice(
                    include_receipts=True):
                continue
            pay_term_line_ids = move.line_ids.filtered(
                lambda line: line.account_id.user_type_id.type in ('receivable', 'payable'))

            domain = [('account_id', 'in', pay_term_line_ids.mapped('account_id').ids),
                      '|', ('parent_state', '=', 'posted'), '&', ('parent_state', '=', 'draft'),
                      ('journal_id.post_at', '=', 'bank_rec'),
                      ('partner_id', '=', move.commercial_partner_id.id),
                      ('reconciled', '=', False), '|', ('amount_residual', '!=', 0.0),
                      ('amount_residual_currency', '!=', 0.0)]

            if move.is_inbound():
                domain.extend([('credit', '>', 0), ('debit', '=', 0)])
                type_payment = _('Outstanding credits')
            else:
                domain.extend([('credit', '=', 0), ('debit', '>', 0)])
                type_payment = _('Outstanding debits')
            info = {'title': '', 'outstanding': True, 'content': [], 'move_id': move.id}
            lines = self.env['account.move.line'].search(domain)
            currency_id = move.currency_id
            if len(lines) != 0:
                for line in lines:
                    # get the outstanding residual value in invoice currency
                    if line.currency_id and line.currency_id == move.currency_id:
                        amount_to_show = abs(line.amount_residual_currency)
                    else:
                        currency = line.company_id.currency_id
                        amount_to_show = currency._convert(abs(line.amount_residual), move.currency_id, move.company_id,
                                                           line.date or fields.Date.today())
                    if float_is_zero(amount_to_show, precision_rounding=move.currency_id.rounding):
                        continue
                    info['content'].append({
                        'journal_name': line.payment_id.display_name or line.move_id.name,
                        'amount': amount_to_show,
                        'currency': currency_id.symbol,
                        'id': line.id,
                        'position': currency_id.position,
                        'digits': [69, move.currency_id.decimal_places],
                        'payment_date': fields.Date.to_string(line.date),
                    })
                info['title'] = type_payment
                move.invoice_outstanding_credits_debits_widget = json.dumps(info)
                move.invoice_has_outstanding = True


#     def _compute_payments_widget_to_reconcile_info(self):
#         for move in self:
#             print('perfect')
#             move.invoice_outstanding_credits_debits_widget = json.dumps(False)
#             move.invoice_has_outstanding = False
#
#             if move.state != 'posted' or move.invoice_payment_state != 'not_paid' or not move.is_invoice(
#                     include_receipts=True):
#                 continue
#             pay_term_line_ids = move.line_ids.filtered(
#                 lambda line: line.account_id.user_type_id.type in ('receivable', 'payable'))
#
#             domain = [('account_id', 'in', pay_term_line_ids.mapped('account_id').ids),
#                       '|', ('parent_state', '=', 'posted'), '&', ('parent_state', '=', 'draft'),
#                       ('journal_id.post_at', '=', 'bank_rec'),
#                       ('partner_id', '=', move.commercial_partner_id.id),
#                       ('reconciled', '=', False), '|', ('amount_residual', '!=', 0.0),
#                       ('amount_residual_currency', '!=', 0.0)]
#
#             if move.is_inbound():
#                 domain.extend([('credit', '>', 0), ('debit', '=', 0)])
#                 type_payment = _('Outstanding credits')
#             else:
#                 domain.extend([('credit', '=', 0), ('debit', '>', 0)])
#                 type_payment = _('Outstanding debits')
#             info = {'title': '', 'outstanding': True, 'content': [], 'move_id': move.id}
#             lines = self.env['account.move.line'].search(domain)
#             currency_id = move.currency_id
#             if len(lines) != 0:
#                 for line in lines:
#                     pay_lines = self.env['account.payment'].search([('move_name', '=', line.move_id.name or line.ref)])
# #                    pay_lines = self.env['account.payment'].search([('move_name', '=', line.ref or line.move_id.name)])
#                     for pay_line in pay_lines:
#                         # get the outstanding residual value in invoice currency
#                         if line.currency_id and line.currency_id == move.currency_id:
#                             amount_to_show = abs(line.amount_residual_currency)
#                         else:
#                             currency = line.company_id.currency_id
#                             amount_to_show = currency._convert(abs(line.amount_residual), move.currency_id, move.company_id,
#                                                                line.date or fields.Date.today())
#                         if float_is_zero(amount_to_show, precision_rounding=move.currency_id.rounding):
#                             continue
#                         info['content'].append({
#                             'journal_name': pay_lines.name or line.ref or line.move_id.name,
#                             'amount': amount_to_show,
#                             'currency': currency_id.symbol,
#                             'id': line.id,
#                             'position': currency_id.position,
#                             'digits': [69, move.currency_id.decimal_places],
#                             'payment_date': fields.Date.to_string(line.date),
#                         })
#                 info['title'] = type_payment
#                 move.invoice_outstanding_credits_debits_widget = json.dumps(info)
#                 move.invoice_has_outstanding = True

