# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2015 DevIntelle Consulting Service Pvt.Ltd (<http://www.devintellecs.com>).
#
#    For Module Support : devintelle@gmail.com  or Skype : devintelle
#
##############################################################################

from odoo import models, fields, api, _
from odoo.exceptions import UserError, AccessError, MissingError, ValidationError
import json

class account_move(models.Model):
    _inherit = 'account.move'

    inv_id = fields.Many2one('account.move', string='Invoice')


class account_payment(models.Model):
    _inherit = 'account.payment'

    payment_for = fields.Selection([('multi_payment', 'AP Payment')], string='Payment Method')
    line_ids = fields.One2many('advance.payment.line', 'account_payment_id')
    full_reco = fields.Boolean('Full Reconcile')
    allocation_amount = fields.Float('Total Amount', compute='get_allocation_amount')

    @api.depends('line_ids', 'line_ids.allocation')
    def get_allocation_amount(self):
        for payment in self:
            amount = 0
            payment.allocation_amount = 0
            for line in payment.line_ids:
                amount += line.allocation
            payment.allocation_amount = amount

    @api.onchange('payment_for')
    def onchange_payment_for(self):
        if self.payment_for != 'multi_payment':
            for line in self.line_ids:
                line.unlink()
            if self.invoice_ids:
                self.invoice_ids = False

    @api.onchange('currency_id')
    def onchange_currency(self):
        active_ids = self._context.get('active_ids') or self._context.get('active_id')
        active_model = self._context.get('active_model')
        invoices = self.env['account.move'].browse(active_ids).filtered(
            lambda move: move.is_invoice(include_receipts=True))
        if len(invoices) == 0:
            self.amount = 0
        else:
            # amount = self._compute_payment_amount(invoices, invoices[0].currency_id, invoices[0].journal_id,
            #                                       self._context.get('payment_date') or fields.Date.today())
            amount = self._compute_payment_amount(invoices, self.currency_id, invoices[0].journal_id,
                                                  self._context.get('payment_date') or fields.Date.today())
            self.amount = abs(amount)
        curr_pool = self.env['res.currency']
        if self.currency_id and self.line_ids:
            for line in self.line_ids:
                if line.currency_id.id != self.currency_id.id:
                    currency_id = self.currency_id.with_context(date=self.payment_date)
                    line.original_amount = curr_pool._compute(line.currency_id, currency_id, line.original_amount,
                                                              round=True)
                    line.balance_amount = curr_pool._compute(line.currency_id, currency_id, line.balance_amount,
                                                             round=True)
                    line.allocation = curr_pool._compute(line.currency_id, currency_id, line.allocation, round=True)
                    line.currency_id = self.currency_id and self.currency_id.id or False

    def remove_lines(self):
        invoice_ids = []
        if self.line_ids and self.payment_for == 'multi_payment':
            for line in self.line_ids:
                if line.allocation:
                    invoice_ids.append(line.invoice_id.id)
                else:
                    line.unlink()
        self.invoice_ids = [(6, 0, invoice_ids)]

    def create_other_lines(self, amount):
        company_currency = self.company_id.currency_id
        if self.payment_type in ('outbound', 'transfer'):
            counterpart_amount = amount
            liquidity_line_account = self.journal_id.default_debit_account_id
        else:
            counterpart_amount = -amount
            liquidity_line_account = self.journal_id.default_credit_account_id

        # Manage currency.
        if self.currency_id == company_currency:
            # Single-currency.
            balance = counterpart_amount
            counterpart_amount = 0.0
            currency_id = False
        else:
            # Multi-currencies.
            balance = self.currency_id._convert(counterpart_amount, company_currency, self.company_id,
                                                self.payment_date)
            currency_id = self.currency_id.id

        # Manage custom currency on journal for liquidity line.
        if self.journal_id.currency_id and self.currency_id != self.journal_id.currency_id:
            # Custom currency on journal.
            liquidity_line_currency_id = self.journal_id.currency_id.id
            liquidity_amount = company_currency._convert(
                balance, self.journal_id.currency_id, self.company_id, self.payment_date)
        else:
            # Use the payment currency.
            liquidity_line_currency_id = currency_id
            liquidity_amount = counterpart_amount

        # Compute 'name' to be used in receivable/payable line.
        rec_pay_line_name = ''
        if self.payment_type == 'transfer':
            rec_pay_line_name = self.name
        else:
            if self.partner_type == 'customer':
                if self.payment_type == 'inbound':
                    rec_pay_line_name += _("Customer Payment")
                elif self.payment_type == 'outbound':
                    rec_pay_line_name += _("Customer Credit Note")
            elif self.partner_type == 'supplier':
                if self.payment_type == 'inbound':
                    rec_pay_line_name += _("Vendor Credit Note")
                elif self.payment_type == 'outbound':
                    rec_pay_line_name += _("Vendor Payment")

        if self.payment_type == 'transfer':
            liquidity_line_name = _('Transfer to %s') % self.destination_journal_id.name
        else:
            liquidity_line_name = self.name
        move_vals = {
            'date': self.payment_date,
            'ref': self.communication,
            'journal_id': self.journal_id.id,
            'currency_id': self.journal_id.currency_id.id or self.company_id.currency_id.id,
            'partner_id': self.partner_id.id,
            'line_ids': [
                # Receivable / Payable / Transfer line.
                (0, 0, {
                    'name': rec_pay_line_name,
                    'amount_currency': counterpart_amount,
                    'currency_id': currency_id,
                    'debit': balance > 0.0 and balance or 0.0,
                    'credit': balance < 0.0 and -balance or 0.0,
                    'date_maturity': self.payment_date,
                    'partner_id': self.partner_id.id,
                    'account_id': self.destination_account_id.id,
                    'payment_id': self.id,
                }),
                # Liquidity line.
                (0, 0, {
                    'name': liquidity_line_name,
                    'amount_currency': -liquidity_amount,
                    'currency_id': liquidity_line_currency_id,
                    'debit': balance < 0.0 and -balance or 0.0,
                    'credit': balance > 0.0 and balance or 0.0,
                    'date_maturity': self.payment_date,
                    'partner_id': self.partner_id.id,
                    'account_id': liquidity_line_account.id,
                    'payment_id': self.id,
                }),
            ],
        }
        print(move_vals, 'move_vals')
        moves = self.env['account.move'].create(move_vals)
        print(moves, 'moves')
        moves.post()
        return True

    def _dev_prepare_payment_moves(self):
        print('----------------_dev_prepare_payment_moves----------------------')
        all_move_vals = []
        for payment in self:
            if payment.amount != payment.allocation_amount:
                raise UserError(_('Ensure the Allocation Amount matches the Payment Amount !'))
            liquidity_amount_tot = 0
            balance_tot = 0
            liquidity_line_currency_id_comm = payment.journal_id.currency_id.id
            if payment.payment_type in ('outbound', 'transfer'):
                liquidity_line_account_comm = payment.journal_id.default_debit_account_id
            else:
                liquidity_line_account_comm = payment.journal_id.default_credit_account_id
            move_name = self._get_move_name_transfer_separator().join(payment.mapped('name'))
            move_valss =[]
            for line in self.line_ids:
                if line.allocation <= 0:
                    continue
                o_move = []
                company_currency = payment.company_id.currency_id
                move_names = payment.move_name.split(
                    payment._get_move_name_transfer_separator()) if payment.move_name else None

                # Compute amounts.
                if payment.payment_type in ('outbound', 'transfer'):
                    counterpart_amount = line.allocation
                    liquidity_line_account = payment.journal_id.default_debit_account_id
                else:
                    counterpart_amount = -line.allocation
                    liquidity_line_account = payment.journal_id.default_credit_account_id

                # Manage currency.
                if payment.currency_id == company_currency:
                    # Single-currency.
                    balance = counterpart_amount
                    counterpart_amount = 0.0
                    currency_id = False
                    balance_tot += balance
                else:
                    # Multi-currencies.
                    balance = payment.currency_id._convert(counterpart_amount, company_currency, payment.company_id,
                                                           payment.payment_date)
                    currency_id = payment.currency_id.id
                    balance_tot += balance


                # Manage custom currency on journal for liquidity line.
                if payment.journal_id.currency_id and payment.currency_id != payment.journal_id.currency_id:
                    # Custom currency on journal.
                    liquidity_line_currency_id = payment.journal_id.currency_id.id
                    liquidity_amount = company_currency._convert(
                        balance, payment.journal_id.currency_id, payment.company_id, payment.payment_date)
                    liquidity_amount_tot += liquidity_amount
                else:
                    # Use the payment currency.
                    liquidity_line_currency_id = currency_id
                    liquidity_amount = counterpart_amount
                    liquidity_amount_tot += liquidity_amount


                # Compute 'name' to be used in receivable/payable line.
                rec_pay_line_name = ''
                if payment.payment_type == 'transfer':
                    rec_pay_line_name = payment.name
                else:
                    if payment.partner_type == 'customer':
                        if payment.payment_type == 'inbound':
                            rec_pay_line_name += _("Customer Payment")
                        elif payment.payment_type == 'outbound':
                            rec_pay_line_name += _("Customer Credit Note")
                    elif payment.partner_type == 'supplier':
                        if payment.payment_type == 'inbound':
                            rec_pay_line_name += _("Vendor Credit Note")
                        elif payment.payment_type == 'outbound':
                            rec_pay_line_name += _("Vendor Payment")
                    if payment.invoice_ids:
                        rec_pay_line_name += ': %s' % ', '.join(line.invoice_id.mapped('name'))

                # Compute 'name' to be used in liquidity line.
                if payment.payment_type == 'transfer':
                    liquidity_line_name = _('Transfer to %s') % payment.destination_journal_id.name
                else:
                    liquidity_line_name = payment.name

                # ==== 'inbound' / 'outbound' ====

                values =(0,0,{
                            'name': rec_pay_line_name,
                            'amount_currency': counterpart_amount,
                            'currency_id': currency_id,
                            'debit': balance > 0.0 and balance or 0.0,
                            'credit': balance < 0.0 and -balance or 0.0,
                            'date_maturity': payment.payment_date,
                            'partner_id': payment.partner_id.id,
                            'account_id': payment.destination_account_id.id,
                            'payment_id': payment.id,
                        })
                move_valss.append(values)

                # if move_names:
                #     move_vals['name'] = move_names[0]
            # print(move_valss, '-------move_valss--------')
            val = (0,0, {
                        'name': payment.name,
                        'amount_currency': -liquidity_amount_tot,
                        'currency_id': liquidity_line_currency_id_comm,
                        'debit': balance_tot < 0.0 and -balance_tot or 0.0,
                        'credit': balance_tot > 0.0 and balance_tot or 0.0,
                        'date_maturity': payment.payment_date,
                        'partner_id': payment.partner_id.id,
                        'account_id': liquidity_line_account_comm.id,
                        'payment_id': payment.id,
                    })
            # move_valss = val + val
            move_valss.append(val)
            move_vals = {
                'date': payment.payment_date,
                'ref': payment.communication,
                'journal_id': payment.journal_id.id,
                'currency_id': payment.journal_id.currency_id.id or payment.company_id.currency_id.id,
                'partner_id': payment.partner_id.id,
                'line_ids': move_valss,
            }
            AccountMove = self.env['account.move'].with_context(default_type='entry')
            moves = AccountMove.create(move_vals)
            moves.filtered(lambda move: move.journal_id.post_at != 'bank_rec').post()
            move_name = self._get_move_name_transfer_separator().join(moves.mapped('name'))
            if payment.payment_type in ('inbound', 'outbound'):
                c1 = []
                c = []
                for line in payment.line_ids.filtered(lambda l:l.allocation >= 1):
                    if line.invoice_id:
                        for m in moves.line_ids:
                            for li in line.invoice_id.line_ids:
                                if li not in c and m not in c1 and li.account_id == m.account_id:
                                    c.append(li)
                                    c1.append(m)
                                    lines = self.env['account.move.line'].browse(li.id)
                                    # print(li, li.account_id, li.reconciled, 'li')
                                    # print(m, m.account_id, m.reconciled, 'm')
                                    lines += m .filtered(
                                            lambda line: line.account_id == lines[0].account_id and not line.reconciled)
                                    # print(lines, '------')
                                    lines.reconcile()

            pay_amt = "{:.2f}".format(self.amount)
            amt = "{:.2f}".format(self.allocation_amount)
            pay_amt = float(pay_amt)
            amt = float(amt)
            if pay_amt > amt:
                other_amount = pay_amt - amt
                payment.create_other_lines(other_amount)
            p = payment.write({'state': 'posted', 'move_name': move_name})
            # print(p, '-------------------p-----------')
        return True

    def check_multi_payment(self):
        pay_amt = "{:.2f}".format(self.amount)
        amt = "{:.2f}".format(self.allocation_amount)
        pay_amt = float(pay_amt)
        amt = float(amt)
        if not amt and not self.amount:
            raise ValidationError(("Add Allocation Amount in payment item"))

        if pay_amt < amt:
            raise ValidationError(("Amount is must be greater or equal '%s'") % (amt))
        return True

    def post(self):
        if self.payment_for == 'multi_payment':
            self.check_multi_payment()
            AccountMove = self.env['account.move'].with_context(default_type='entry')
            for rec in self:
                if rec.state != 'draft':
                    raise UserError(_("Only a draft payment can be posted."))

                if any(inv.state != 'posted' for inv in rec.invoice_ids):
                    raise ValidationError(_("The payment cannot be processed because the invoice is not open!"))

                # keep the name in case of a payment reset to draft
                if not rec.name:
                    # Use the right sequence to set the name
                    if rec.payment_type == 'transfer':
                        sequence_code = 'account.payment.transfer'
                    else:
                        if rec.partner_type == 'customer':
                            if rec.payment_type == 'inbound':
                                sequence_code = 'account.payment.customer.invoice'
                            if rec.payment_type == 'outbound':
                                sequence_code = 'account.payment.customer.refund'
                        if rec.partner_type == 'supplier':
                            if rec.payment_type == 'inbound':
                                sequence_code = 'account.payment.supplier.refund'
                            if rec.payment_type == 'outbound':
                                sequence_code = 'account.payment.supplier.invoice'
                    rec.name = self.env['ir.sequence'].next_by_code(sequence_code, sequence_date=rec.payment_date)
                    if not rec.name and rec.payment_type != 'transfer':
                        raise UserError(_("You have to define a sequence for %s in your company.") % (sequence_code,))

                rec._dev_prepare_payment_moves()
            return True
        else:
            return super(account_payment, self).post()

    def load_payment_lines(self):
        if self.payment_for == 'multi_payment':
            self.line_ids.unlink()
            account_inv_obj = self.env['account.move']
            invoice_ids = []
            if self.partner_id:
                partner_ids = self.env['res.partner'].search([('parent_id', '=', self.partner_id.id)]).ids
                partner_ids.append(self.partner_id.id)
            else:
                partner_ids = self.env['res.partner'].search([]).ids
                # partner_ids.append(self.partner_id.id)
            # partner_ids = self.env['res.partner'].search([('parent_id', '=', self.partner_id.id)]).ids

            query = """ select id from account_move where partner_id in %s and invoice_date <= %s and state = %s and type in %s and company_id = %s and invoice_payment_state = %s"""
            if self.partner_type == 'customer':
                params = (tuple(partner_ids), self.payment_date, 'posted', ('out_invoice', 'out_refund'), self.company_id.id,'not_paid')
            else:
                params = (tuple(partner_ids), self.payment_date, 'posted', ('in_invoice', 'in_refund'), self.company_id.id,'not_paid')
            self.env.cr.execute(query, params)
            result = self.env.cr.dictfetchall()
            invoice_ids = [inv.get('id') for inv in result]
            invoice_ids = account_inv_obj.browse(invoice_ids)
            curr_pool = self.env['res.currency']
            for vals in invoice_ids:
                account_id = False
                if self.partner_type == 'customer':
                    account_id = vals.partner_id and vals.partner_id.property_account_receivable_id.id or False
                else:
                    account_id = vals.partner_id and vals.partner_id.property_account_payable_id.id or False

                original_amount = vals.amount_total
                balance_amount = vals.amount_residual
                allocation = vals.amount_residual
                if vals.currency_id.id != self.currency_id.id:
                    original_amount = vals.amount_total
                    balance_amount = vals.amount_residual
                    allocation = vals.amount_residual
                    if vals.currency_id.id != self.currency_id.id:
                        currency_id = self.currency_id.with_context(date=self.payment_date)
                        original_amount = curr_pool._compute(vals.currency_id, currency_id, original_amount, round=True)
                        balance_amount = curr_pool._compute(vals.currency_id, currency_id, balance_amount, round=True)
                        allocation = curr_pool._compute(vals.currency_id, currency_id, allocation, round=True)

                query = """ INSERT INTO advance_payment_line (invoice_id, account_id, date, due_date, original_amount, balance_amount, currency_id, account_payment_id) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"""
                params = (
                    vals.id, account_id, vals.invoice_date, vals.invoice_date_due, original_amount, balance_amount,
                    self.currency_id.id, self.id)
                self.env.cr.execute(query, params)
            self.invoice_ids = [(6, 0, invoice_ids.ids)]

        # vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:

    @api.depends('invoice_ids', 'amount', 'payment_date', 'currency_id', 'payment_type')
    def _compute_payment_difference(self):
        draft_payments = self.filtered(lambda p: p.invoice_ids and p.state == 'draft')
        print(draft_payments)
        active_ids = self._context.get('active_ids') or self._context.get('active_id')
        active_model = self._context.get('active_model')
        invoices = self.env['account.move'].browse(active_ids).filtered(
            lambda move: move.is_invoice(include_receipts=True))
        # print(self.payment_difference)
        if len(invoices) == 0:
            if draft_payments:
                for pay in draft_payments:
                    payment_amount = -pay.amount if pay.payment_type == 'outbound' else pay.amount
                    pay.payment_difference = pay._compute_payment_amount(pay.invoice_ids, pay.currency_id, pay.journal_id,
                                                                         pay.payment_date) - payment_amount
            else:
                self.payment_difference=0.0

        else:
            amount = self._compute_payment_amount(invoices, invoices[0].currency_id, invoices[0].journal_id,
                                                  self._context.get('payment_date') or fields.Date.today())

            for rec in self:
                rec.payment_difference = abs(amount) - self.amount

    # @api.depends('invoice_ids', 'amount', 'payment_date', 'currency_id', 'payment_type')
    # def _compute_payment_difference(self):
    #     draft_payments = self.filtered(lambda p: p.invoice_ids and p.state == 'draft')
    #     active_ids = self._context.get('active_ids') or self._context.get('active_id')
    #     active_model = self._context.get('active_model')
    #     invoices = self.env['account.move'].browse(active_ids).filtered(
    #         lambda move: move.is_invoice(include_receipts=True))
    #     if len(invoices) == 0:
    #         print("eeeeeeeee")
    #
    #         # self.payment_difference=0
    #         for pay in draft_payments:
    #             print("xxxxxxxxxxxxxxx")
    #             payment_amount = -pay.amount if pay.payment_type == 'outbound' else pay.amount
    #             pay.payment_difference = pay._compute_payment_amount(pay.invoice_ids, pay.currency_id, pay.journal_id,
    #                                                                  pay.payment_date) - payment_amount
    #
    #
    #     else:
    #         amount = self._compute_payment_amount(invoices, invoices[0].currency_id, invoices[0].journal_id,
    #                                               self._context.get('payment_date') or fields.Date.today())
    #
    #         for rec in self:
    #             rec.payment_difference = abs(amount) - self.amount
