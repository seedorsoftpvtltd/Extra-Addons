from odoo.http import request
from odoo import api, fields, models, tools, osv, http, _
import odoo.osv.osv
from odoo.exceptions import ValidationError, UserError


class Accmoveline(models.Model):
    _inherit = "account.move.line"

    internal_test = fields.Char('Internal', store=True)
    narration = fields.Char('Narration')

    def js_assign_outstanding_line(self, line_id):
        self.ensure_one()
        lines = self.env['account.move.line'].browse(line_id)
        # lines += self.line_ids.filtered(lambda line: line.account_id == lines[0].account_id and not line.reconciled)
        lines += self.line_ids.filtered(lambda line: not line.reconciled)
        return lines.reconcile()

    def _check_reconcile_validity(self):
        # Empty self can happen if there is no line to check.
        if not self:
            return

        #Perform all checks on lines
        company_ids = set()
        all_accounts = []
        for line in self:
            company_ids.add(line.company_id.id)
            all_accounts.append(line.account_id)
            if line.reconciled:
                raise UserError(_('You are trying to reconcile some entries that are already reconciled.'))
        if len(company_ids) > 1:
            raise UserError(_('To reconcile the entries company should be the same for all entries.'))
        # if len(set(all_accounts)) > 1:
        #     raise UserError(_('Entries are not from the same account.'))
        if not (all_accounts[0].reconcile or all_accounts[0].internal_type == 'liquidity'):
            raise UserError(_('Account %s (%s) does not allow reconciliation. First change the configuration of this account to allow it.') % (all_accounts[0].name, all_accounts[0].code))



class AccountPaymentLinee(models.Model):
    _inherit = "account.payment.linee"

    debit = fields.Float(string='Debit')
    credit = fields.Float(string='Credit')
    partner_id = fields.Many2one('res.partner', string="Partner")
    narration = fields.Char('Narration')



class AccountPaymentLineinh(models.Model):
    _inherit = "account.payment.linee"

    name = fields.Char(string='Label', required=False, compute='_compute_label', store=True)

    @api.depends('account_id')
    def _compute_label(self):
        for r in self:
            r.name = r.account_id.name or False


class AccountPaymentLine(models.Model):
    _inherit = "account.payment"

    journal_add = fields.Boolean(string='Add Journals')

    @api.onchange('account_payment_line_ids')
    def _onchange_account_payment_line_ids(self):
        print('....................')
        if self.journal_add == True:
            for rec in self.account_payment_line_ids:
                if self.partner_type == 'customer':
                    # rec.amount = rec.credit
                    rec.amount = rec.credit
                    print(rec.amount, 'rec.amount')
                else:
                    rec.amount = rec.debit
                    print(rec.amount, 'rec.amount')
            # self.amount = sum(self.account_payment_line_ids.mapped('debit')) - sum(self.account_payment_line_ids.mapped('credit'))
            debit = sum(self.account_payment_line_ids.mapped('debit'))
            credit = sum(self.account_payment_line_ids.mapped('credit'))
            if self.partner_type == 'customer':
                bal = credit - debit
            else:
                bal = debit - credit
            self.amount = bal
            print('self.amount', self.amount)
        else:
            self.amount = sum(self.account_payment_line_ids.mapped('amount'))

    @api.constrains('account_payment_line_ids', 'amount')
    def _check_account_payment_line_ids(self):
        for r in self:
            if r.journal_add == True:
                return True
            else:
                if r.account_payment_line_ids:
                    sum_payment_lines_amount = sum(r.account_payment_line_ids.mapped('amount'))
                    if r.currency_id.compare_amounts(sum_payment_lines_amount, r.amount) != 0:
                        raise UserError(
                            _("Payment Amount of the payment %s must be equal to the summary of its lines amount")
                            % (r.display_name,))

    def blaa(self, move_id):
        for rec in self:
            z = self.env['account.move.line'].search([('internal_test','!=','Required'),('move_id','=',move_id.id)])
            z.write({
                # 'matched_debit_ids':False,
                # 'matched_credit_ids':False,
                # 'move_id':False

            })
            # z.move_id.write({'state':'draft'})
            print(z, 'unlink z')
            z.unlink()

    def postt(self):
        print('pppppppppppppppppppppppppppppppp')
        AccountMove = self.env['account.move'].with_context(default_type='entry')

        for rec in self:
            # if rec.state != 'draft':
            # 	raise UserError(_("Only a draft payment can be posted."))

            if any(inv.state != 'posted' for inv in rec.invoice_ids):
                raise ValidationError(_("The payment cannot be processed because the invoice is not open!"))

            # keep the name in case of a payment reset to draft
            if not rec.name:

                # Use the right sequence to set the name
                if rec.payment_type == 'transfer':
                    print(rec.partner_type, 'rec.partner_type')
                    if rec.partner_type == 'customer':
                        sequence_code = 'account.payment.customer.invoice'
                    elif rec.partner_type == 'supplier':
                        sequence_code = 'account.payment.supplier.invoice'
                    else:
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

            moves = AccountMove.create(rec._prepare_payment_movest())  # Modified method name
            print(moves, 'moves')
            moves.filtered(lambda move: move.journal_id.post_at != 'bank_rec').post()
            # Update the state / move before performing any reconciliation.
            move_name = self._get_move_name_transfer_separator().join(moves.mapped('name'))
            rec.write({'state': 'posted', 'move_name': move_name})

        if rec.payment_type in ('inbound', 'outbound'):
            # ==== 'inbound' / 'outbound' ====
            if rec.invoice_ids:
                (moves[0] + rec.invoice_ids).line_ids \
                    .filtered(lambda line: not line.reconciled and line.account_id == rec.destination_account_id) \
                    .reconcile()

        elif rec.payment_type == 'transfer':
            # ==== 'transfer' ====
            moves.mapped('line_ids') \
                .filtered(lambda line: line.account_id == rec.company_id.transfer_account_id) \
                .reconcile()

        print('self.move_line_ids', self.move_line_ids)
        return True

    def _prepare_payment_movest(self):  # Corrected method name
        """
        Override to process payments that have payment lines
        """
        all_move_vals = super(AccountPaymentLine, self)._prepare_payment_moves()  # Corrected method name

        for move_vals in all_move_vals:
            for line in move_vals['line_ids']:
                payment = self.filtered(lambda p: p.id == line[2].get('payment_id', False))
                if payment and payment.communication:
                    line[2].update({'name': payment.communication})

        to_process = self.filtered(lambda p: p.account_payment_line_ids and p.payment_type != 'transfer')
        for idx, payment in enumerate(to_process):
            move_vals = all_move_vals[idx]
            move_vals['line_ids'].pop(0)
            liquidity_balance = 0

            for payment_line in payment.account_payment_line_ids:
                company_currency = payment.company_id.currency_id

                # Compute amounts.
                if payment.payment_type == 'outbound':
                    counterpart_amount = payment_line.credit - payment_line.debit
                else:
                    counterpart_amount = payment_line.debit - payment_line.credit

                # Manage currency.
                if payment.currency_id == company_currency:
                    balance = counterpart_amount
                    counterpart_amount = 0.0
                    currency_id = False
                else:
                    balance = payment.currency_id._convert(counterpart_amount, company_currency, payment.company_id,
                                                           payment.payment_date)
                    currency_id = payment.currency_id.id
                    liquidity_balance += balance

                move_vals['line_ids'].insert(0, (0, 0, {
                    'name': payment_line.name,
                    'amount_currency': counterpart_amount if currency_id else 0.0,
                    'currency_id': currency_id,
                    'credit': balance > 0.0 and balance or 0.0 if payment.payment_type == 'outbound' else balance < 0.0 and -balance or 0.0,
                    'debit': balance < 0.0 and -balance or 0.0 if payment.payment_type == 'outbound' else balance > 0.0 and balance or 0.0,
                    'date_maturity': payment.payment_date,
                    'partner_id': payment_line.partner_id.id or payment.partner_id.commercial_partner_id.id,
                    'account_id': payment_line.account_id.id,
                    'payment_id': payment.id,
                    'amount_residual': 100,
                }))

            if payment.currency_id != company_currency:
                move_vals['line_ids'][-1][2].update({
                    'debit': liquidity_balance < 0.0 and -liquidity_balance or 0.0,
                    'credit': liquidity_balance > 0.0 and liquidity_balance or 0.0,
                })

        return all_move_vals

    def postt1(self):
        print('pppppppppppppppppppppppppppppppp')
        AccountMove = self.env['account.move'].with_context(default_type='entry')

        for rec in self:
            # if rec.state != 'draft':
            # 	raise UserError(_("Only a draft payment can be posted."))

            if any(inv.state != 'posted' for inv in rec.invoice_ids):
                raise ValidationError(_("The payment cannot be processed because the invoice is not open!"))

            # keep the name in case of a payment reset to draft
            if not rec.name:

                # Use the right sequence to set the name
                if rec.payment_type == 'transfer':
                    print(rec.partner_type, 'rec.partner_type')
                    if rec.partner_type == 'customer':
                        sequence_code = 'account.payment.customer.invoice'
                    elif rec.partner_type == 'supplier':
                        sequence_code = 'account.payment.supplier.invoice'
                    else:
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

            moves = AccountMove.create(rec._prepare_payment_moves())
            # ids = []
            # for l in moves.line_ids:
            #     if l.internal_test != 'Required':
            #         print(l.internal_test, 'llll')
            #         l.write({
            #             'payment_id': False,
            #             # 'move_id':False,
            #         })
            #         ids.append(l.id)
            #         # l.unlink()
            #     print('l', l)
            # print(ids, 'ids')
            # for r in ids:
            #     l = self.env['account.move.line'].search([('id','=',r)])
            #     print(l.move_id.type, 'type')
            #     # l.write({'move_id': False})
            #     # l.unlink()
            # self.blaa(move_id=moves)
            # print(moves, 'moves')

            moves.filtered(lambda move: move.journal_id.post_at != 'bank_rec').post()
            # Update the state / move before performing any reconciliation.
            move_name = self._get_move_name_transfer_separator().join(moves.mapped('name'))
            rec.write({'state': 'posted', 'move_name': move_name})

        if rec.payment_type in ('inbound', 'outbound'):
            # ==== 'inbound' / 'outbound' ====
            if rec.invoice_ids:
                (moves[0] + rec.invoice_ids).line_ids \
                    .filtered(lambda line: not line.reconciled and line.account_id == rec.destination_account_id) \
                    .reconcile()

        elif rec.payment_type == 'transfer':
            # ==== 'transfer' ====
            moves.mapped('line_ids') \
                .filtered(lambda line: line.account_id == rec.company_id.transfer_account_id) \
                .reconcile()

        print('self.move_line_ids', self.move_line_ids)
        # for jou in self.move_line_ids:
        #     print(jou, 'jou')
        #     if jou.credit == 0 and jou.debit == 0:
        #         print(jou, 'unlink')
        #         # jou.unlink()
        #         jou.write({'payment_id': False})
        #     if jou.name == 'bal':
        #         jou.write({'payment_id': False})
        # self.bla()
        return True
        # return super(account_payment, self).post()

    def _prepare_payment_movest1(self):
        """
        Override to process payments that have payment lines
        """
        all_move_vals = super(AccountPaymentLine, self)._prepare_payment_moves()

        for move_vals in all_move_vals:
            for line in move_vals['line_ids']:
                payment = self.filtered(lambda p: p.id == line[2].get('payment_id', False))
                if payment and payment.communication:
                    line[2].update({'name': payment.communication})

        to_process = self.filtered(lambda p: p.account_payment_line_ids and p.payment_type != 'transfer')
        for idx, payment in enumerate(to_process):
            move_vals = all_move_vals[idx]
            move_vals['line_ids'].pop(0)
            liquidity_balance = 0

            for payment_line in payment.account_payment_line_ids:
                company_currency = payment.company_id.currency_id

                # Compute amounts.
                if payment.payment_type == 'outbound':
                    counterpart_amount = payment_line.credit - payment_line.debit
                else:
                    counterpart_amount = payment_line.debit - payment_line.credit

                # Manage currency.
                if payment.currency_id == company_currency:
                    balance = counterpart_amount
                    counterpart_amount = 0.0
                    currency_id = False
                else:
                    balance = payment.currency_id._convert(counterpart_amount, company_currency, payment.company_id,
                                                           payment.payment_date)
                    currency_id = payment.currency_id.id
                    liquidity_balance += balance

                move_vals['line_ids'].insert(0, (0, 0, {
                    'name': payment_line.name,
                    'amount_currency': counterpart_amount if currency_id else 0.0,
                    'currency_id': currency_id,
                    'debit': balance > 0.0 and balance or 0.0,
                    'credit': balance < 0.0 and -balance or 0.0,
                    'date_maturity': payment.payment_date,
                    'partner_id': payment.partner_id.commercial_partner_id.id,
                    'account_id': payment_line.account_id.id,
                    'payment_id': payment.id,
                }))

            if payment.currency_id != company_currency:
                move_vals['line_ids'][-1][2].update({
                    'debit': liquidity_balance < 0.0 and -liquidity_balance or 0.0,
                    'credit': liquidity_balance > 0.0 and liquidity_balance or 0.0,
                })

        return all_move_vals

    def _prepare_payment_movestt(self):

        all_move_vals = []
        for payment in self:
            company_currency = payment.company_id.currency_id
            move_names = payment.move_name.split(
                payment._get_move_name_transfer_separator()) if payment.move_name else None

            # Compute amounts.
            write_off_amount = payment.payment_difference_handling == 'reconcile' and -payment.payment_difference or 0.0
            if payment.payment_type in ('outbound', 'transfer'):
                counterpart_amount = payment.amount
                liquidity_line_account = payment.journal_id.default_debit_account_id
            else:
                counterpart_amount = -payment.amount
                liquidity_line_account = payment.journal_id.default_credit_account_id

            # Manage currency.
            if payment.currency_id == company_currency:
                # Single-currency.
                balance = counterpart_amount
                write_off_balance = write_off_amount
                counterpart_amount = write_off_amount = 0.0
                currency_id = False
            else:
                # Multi-currencies.
                balance = payment.currency_id._convert(counterpart_amount, company_currency, payment.company_id,
                                                       payment.payment_date)
                write_off_balance = payment.currency_id._convert(write_off_amount, company_currency, payment.company_id,
                                                                 payment.payment_date)
                currency_id = payment.currency_id.id

            # Manage custom currency on journal for liquidity line.
            if payment.journal_id.currency_id and payment.currency_id != payment.journal_id.currency_id:
                # Custom currency on journal.
                if payment.journal_id.currency_id == company_currency:
                    # Single-currency
                    liquidity_line_currency_id = False
                else:
                    liquidity_line_currency_id = payment.journal_id.currency_id.id
                liquidity_amount = company_currency._convert(
                    balance, payment.journal_id.currency_id, payment.company_id, payment.payment_date)
            else:
                # Use the payment currency.
                liquidity_line_currency_id = currency_id
                liquidity_amount = counterpart_amount

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
                    rec_pay_line_name += ': %s' % ', '.join(payment.invoice_ids.mapped('name'))

            # Compute 'name' to be used in liquidity line.
            if payment.payment_type == 'transfer':
                liquidity_line_name = _('Transfer to %s') % payment.destination_journal_id.name
            else:
                liquidity_line_name = payment.name
            # all_move_vals = []
            # ==== 'inbound' / 'outbound' ====
            for payment_line in payment.account_payment_line_ids:

                company_currency = payment.company_id.currency_id

                # Compute amounts.
                if payment.payment_type == 'outbound':
                    counterpart_amount = payment_line.amount
                else:
                    counterpart_amount = -payment_line.amount

                # Manage currency.
                if payment.currency_id == company_currency:
                    # Single-currency.
                    balance = counterpart_amount
                    counterpart_amount = 0.0
                    currency_id = False
                else:
                    # Multi-currencies.
                    balance = payment.currency_id._convert(counterpart_amount, company_currency,
                                                           payment.company_id, payment.payment_date)
                    currency_id = payment.currency_id.id
                    # liquidity_balance += balance
                # print(payment_line.debit, payment_line.credit)

                move_valss = {
                    'date': payment.payment_date,
                    'ref': payment.communication,
                    'journal_id': payment.journal_id.id,
                    'currency_id': payment.journal_id.currency_id.id or payment.company_id.currency_id.id,
                    'partner_id': payment.partner_id.id,
                    'line_ids': [
                        # Receivable / Payable / Transfer line.
                        (0, 0, {
                            'name': payment_line.name,
                            'amount_currency': counterpart_amount if currency_id else 0.0,
                            'currency_id': currency_id,
                            # 'debit': balance > 0.0 and balance  or 0.0,
                            # 'credit': balance < 0.0 and -balance or 0.0,
                            'debit': payment_line.debit,
                            'credit': payment_line.credit,
                            'date_maturity': payment.payment_date,
                            'partner_id': payment_line.partner_id.id,
                            # 'partner_id': payment.partner_id.commercial_partner_id.id,
                            'account_id': payment_line.account_id.id,
                            'payment_id': payment.id,
                            'internal_test': 'Required',
                            # 'exclude_from_invoice_tab': False,
                        }),
                    ],

                }
                print('abc', move_valss['line_ids'])
                all_move_vals.append(move_valss)

                # move_vals['line_ids'].insert(0, (0, 0, {
                #     'name': payment.communication,
                #     'amount_currency': counterpart_amount if currency_id else 0.0,
                #     'currency_id': currency_id,
                #     # 'debit': balance > 0.0 and balance  or 0.0,
                #     # 'credit': balance < 0.0 and -balance or 0.0,
                #     # 'debit': abs(amn) if payment.partner_type == 'customer' else 0.0,
                #     # 'credit': abs(amn) if payment.partner_type == 'supplier' else 0.0,
                #     'credit': bal if payment.partner_type == 'supplier' else 0.0,
                #     'debit': bal if payment.partner_type == 'customer' else 0.0,
                #     'date_maturity': payment.payment_date,
                #     'partner_id': payment.partner_id.id,
                #     # 'partner_id': payment.partner_id.commercial_partner_id.id,
                #     'account_id': payment.journal_id.default_debit_account_id.id,
                #     'payment_id': payment.id,
                #     # 'exclude_from_invoice_tab': False,
                # }))

                # if move_names:
                #     move_vals['name'] = move_names[0]

                # all_move_vals.append(move_vals)
                # print(all_move_vals)
            debit = sum(self.account_payment_line_ids.mapped('debit'))
            credit = sum(self.account_payment_line_ids.mapped('credit'))
            if payment.partner_type == 'customer':
                bal = credit - debit
            else:
                bal = debit - credit
            amn = sum(self.account_payment_line_ids.mapped('debit')) - sum(
                self.account_payment_line_ids.mapped('credit'))
            amn1 = sum(self.account_payment_line_ids.mapped('credit')) - sum(
                self.account_payment_line_ids.mapped('debit'))
            if amn > amn1:
                amnt = amn
            else:
                amnt = amn1
            print(amn, amn1, '************************', bal)
            move_vals = {
                'date': payment.payment_date,
                'ref': payment.communication,
                'journal_id': payment.journal_id.id,
                'currency_id': payment.journal_id.currency_id.id or payment.company_id.currency_id.id,
                'partner_id': payment.partner_id.id,
                'line_ids': [
                    # Receivable / Payable / Transfer line.
                    (0, 0, {
                        'name': payment.communication,
                        'amount_currency': counterpart_amount if currency_id else 0.0,
                        'currency_id': currency_id,
                        # 'debit': balance > 0.0 and balance  or 0.0,
                        # 'credit': balance < 0.0 and -balance or 0.0,
                        # 'debit': abs(amn) if payment.partner_type == 'customer' else 0.0,
                        # 'credit': abs(amn) if payment.partner_type == 'supplier' else 0.0
                        'debit': bal if payment.partner_type == 'customer' else 0.0,
                        'credit': bal if payment.partner_type == 'supplier' else 0.0,
                        'date_maturity': payment.payment_date,
                        'partner_id': payment.partner_id.id,
                        # 'partner_id': payment.partner_id.commercial_partner_id.id,
                        'account_id': payment.journal_id.default_debit_account_id.id,
                        'payment_id': payment.id,
                        'internal_test': 'Required',
                        # 'exclude_from_invoice_tab': False,
                    }),
                ],

            }
            all_move_vals.append(move_vals)
            for rec in all_move_vals:
                print('rec', dict(rec))

            # move_valss = {
            #     'date': payment.payment_date,
            #     'ref': payment.communication,
            #     'journal_id': payment.journal_id.id,
            #     'currency_id': payment.journal_id.currency_id.id or payment.company_id.currency_id.id,
            #     'partner_id': payment.partner_id.id,
            #     'line_ids': [
            #         # Receivable / Payable / Transfer line.
            #         (0, 0, {
            #             'name': rec_pay_line_name,
            #             'amount_currency': counterpart_amount + write_off_amount if currency_id else 0.0,
            #             'currency_id': currency_id,
            #             'debit': balance + write_off_balance > 0.0 and balance + write_off_balance or 0.0,
            #             'credit': balance + write_off_balance < 0.0 and -balance - write_off_balance or 0.0,
            #             'date_maturity': payment.payment_date,
            #             'partner_id': payment.partner_id.commercial_partner_id.id,
            #             'account_id': payment.destination_account_id.id,
            #             'payment_id': payment.id,
            #         }),
            #         # Liquidity line.
            #         (0, 0, {
            #             'name': liquidity_line_name,
            #             'amount_currency': -liquidity_amount if liquidity_line_currency_id else 0.0,
            #             'currency_id': liquidity_line_currency_id,
            #             'debit': balance < 0.0 and -balance or 0.0,
            #             'credit': balance > 0.0 and balance or 0.0,
            #             'date_maturity': payment.payment_date,
            #             'partner_id': payment.partner_id.commercial_partner_id.id,
            #             'account_id': liquidity_line_account.id,
            #             'payment_id': payment.id,
            #         }),
            #     ],
            # }
            # if write_off_balance:
            #     # Write-off line.
            #     move_vals['line_ids'].append((0, 0, {
            #         'name': payment.writeoff_label,
            #         'amount_currency': -write_off_amount,
            #         'currency_id': currency_id,
            #         'debit': write_off_balance < 0.0 and -write_off_balance or 0.0,
            #         'credit': write_off_balance > 0.0 and write_off_balance or 0.0,
            #         'date_maturity': payment.payment_date,
            #         'partner_id': payment.partner_id.commercial_partner_id.id,
            #         'account_id': payment.writeoff_account_id.id,
            #         'payment_id': payment.id,
            #     }))

            # ==== 'transfer' ====
            # if payment.payment_type == 'transfer':
            #     journal = payment.destination_journal_id
            #
            #     # Manage custom currency on journal for liquidity line.
            #     if journal.currency_id and payment.currency_id != journal.currency_id:
            #         # Custom currency on journal.
            #         liquidity_line_currency_id = journal.currency_id.id
            #         transfer_amount = company_currency._convert(balance, journal.currency_id, payment.company_id, payment.payment_date)
            #     else:
            #         # Use the payment currency.
            #         liquidity_line_currency_id = currency_id
            #         transfer_amount = counterpart_amount
            #
            #     transfer_move_vals = {
            #         'date': payment.payment_date,
            #         'ref': payment.communication,
            #         'partner_id': payment.partner_id.id,
            #         'journal_id': payment.destination_journal_id.id,
            #         'line_ids': [
            #             # Transfer debit line.
            #             (0, 0, {
            #                 'name': payment.name,
            #                 'amount_currency': -counterpart_amount if currency_id else 0.0,
            #                 'currency_id': currency_id,
            #                 'debit': balance < 0.0 and -balance or 0.0,
            #                 'credit': balance > 0.0 and balance or 0.0,
            #                 'date_maturity': payment.payment_date,
            #                 'partner_id': payment.partner_id.commercial_partner_id.id,
            #                 'account_id': payment.company_id.transfer_account_id.id,
            #                 'payment_id': payment.id,
            #             }),
            #             # Liquidity credit line.
            #             (0, 0, {
            #                 'name': _('Transfer from %s') % payment.journal_id.name,
            #                 'amount_currency': transfer_amount if liquidity_line_currency_id else 0.0,
            #                 'currency_id': liquidity_line_currency_id,
            #                 'debit': balance > 0.0 and balance or 0.0,
            #                 'credit': balance < 0.0 and -balance or 0.0,
            #                 'date_maturity': payment.payment_date,
            #                 'partner_id': payment.partner_id.commercial_partner_id.id,
            #                 'account_id': payment.destination_journal_id.default_credit_account_id.id,
            #                 'payment_id': payment.id,
            #             }),
            #         ],
            #     }
            #
            #     if move_names and len(move_names) == 2:
            #         transfer_move_vals['name'] = move_names[1]
            #
            #     all_move_vals.append(transfer_move_vals)
            return all_move_vals

    def _prepare_payment_movesthi(self):
        """
        Override to process payments that have payment lines
        """
        print('_prepare_payment_movess', '---------------------------------------hb----------------------------------')
        all_move_vals = self._prepare_payment_moves()
        # all_move_vals = []
        print('--------------all_move_vals---------------')
        print(all_move_vals)
        print('--------------all_move_vals---------------')

        # update label of all move lines to value of memo
        for move_vals in all_move_vals:
            for line in move_vals['line_ids']:
                payment = self.filtered(lambda p: p.id == line[2].get('payment_id', False))
                if payment and payment.communication:
                    line[2].update({'name': payment.communication})
                print(';;;;;;;;;;;;;;;;;;;;;;;;;', line)
                print('%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%', self.move_line_ids, line[2])
            for jo in self.move_line_ids:
                print(jo, 'jo')
                jo.unlink()

        to_process = self.filtered(lambda p: p.account_payment_line_ids and p.payment_type != 'transfer')
        for idx, payment in enumerate(to_process):
            # move_vals = all_move_vals[idx]
            # remove the Receivable / Payable line which is the very first line in lines_ids
            # move_vals['line_ids'].pop(0)
            liquidity_balance = 0
            # update data in payment lines
            for payment_line in payment.account_payment_line_ids:

                company_currency = payment.company_id.currency_id

                # Compute amounts.
                if payment.payment_type == 'outbound':
                    counterpart_amount = payment_line.amount
                else:
                    counterpart_amount = -payment_line.amount

                # Manage currency.
                if payment.currency_id == company_currency:
                    # Single-currency.
                    balance = counterpart_amount
                    counterpart_amount = 0.0
                    currency_id = False
                else:
                    # Multi-currencies.
                    balance = payment.currency_id._convert(counterpart_amount, company_currency,
                                                           payment.company_id, payment.payment_date)
                    currency_id = payment.currency_id.id
                    liquidity_balance += balance
                print(payment_line.debit, payment_line.credit)

                move_vals['line_ids'].insert(0, (0, 0, {
                    'name': payment_line.name,
                    'amount_currency': counterpart_amount if currency_id else 0.0,
                    'currency_id': currency_id,
                    # 'debit': balance > 0.0 and balance  or 0.0,
                    # 'credit': balance < 0.0 and -balance or 0.0,
                    'debit': payment_line.debit,
                    'credit': payment_line.credit,
                    'date_maturity': payment.payment_date,
                    'partner_id': payment_line.partner_id.id,
                    # 'partner_id': payment.partner_id.commercial_partner_id.id,
                    'account_id': payment_line.account_id.id,
                    'payment_id': payment.id,
                    'internal_test': 'Required',
                    # 'exclude_from_invoice_tab': False,
                }))
            debit = sum(self.account_payment_line_ids.mapped('debit'))
            credit = sum(self.account_payment_line_ids.mapped('credit'))
            if payment.partner_type == 'customer':
                bal = credit - debit
            else:
                bal = debit - credit
            amn = sum(self.account_payment_line_ids.mapped('debit')) - sum(
                self.account_payment_line_ids.mapped('credit'))
            amn1 = sum(self.account_payment_line_ids.mapped('credit')) - sum(
                self.account_payment_line_ids.mapped('debit'))
            if amn > amn1:
                amnt = amn
            else:
                amnt = amn1
            print(amn, amn1, '************************', bal)
            move_vals['line_ids'].insert(0, (0, 0, {
                'name': payment.name,
                'amount_currency': counterpart_amount if currency_id else 0.0,
                'currency_id': currency_id,
                # 'debit': balance > 0.0 and balance  or 0.0,
                # 'credit': balance < 0.0 and -balance or 0.0,
                # 'debit': abs(amn) if payment.partner_type == 'customer' else 0.0,
                # 'credit': abs(amn) if payment.partner_type == 'supplier' else 0.0,
                'credit': bal if payment.partner_type == 'supplier' else 0.0,
                'debit': bal if payment.partner_type == 'customer' else 0.0,
                'date_maturity': payment.payment_date,
                'partner_id': payment.partner_id.id,
                # 'partner_id': payment.partner_id.commercial_partner_id.id,
                'account_id': payment.journal_id.default_debit_account_id.id,
                'payment_id': payment.id,
                'internal_test': 'Required',
                # 'exclude_from_invoice_tab': False,
            }))
            # move_vals['line_ids'].insert(0, (0, 0, {
            #     'name': 'bal',
            #     'amount_currency': counterpart_amount if currency_id else 0.0,
            #     'currency_id': currency_id,
            #     # 'debit': balance > 0.0 and balance  or 0.0,
            #     # 'credit': balance < 0.0 and -balance or 0.0,
            #     # 'debit': abs(amn) if payment.partner_type == 'customer' else 0.0,
            #     # 'credit': abs(amn) if payment.partner_type == 'supplier' else 0.0,
            #     'credit': payment.amount if payment.partner_type != 'supplier' else 0.0,
            #     'debit': payment.amount if payment.partner_type != 'customer' else 0.0,
            #     'date_maturity': payment.payment_date,
            #     'partner_id': payment.partner_id.id,
            #     # 'partner_id': payment.partner_id.commercial_partner_id.id,
            #     'account_id': payment.journal_id.default_debit_account_id.id,
            #     'payment_id': payment.id,
            #     # 'exclude_from_invoice_tab': False,
            # }))
            # break
            # print(move_vals, 'move_vals')
            print(move_vals['line_ids'], 'ooooooooooooooooooooooooooo')
            # move_vals['line_ids']._check_balanced()
            # break

            if payment.currency_id != company_currency:
                # update after exchanging currency to avoid difference between debit and credit in journal entries
                move_vals['line_ids'][-1][2].update({
                    'debit': liquidity_balance < 0.0 and -liquidity_balance or 0.0,
                    'credit': liquidity_balance > 0.0 and liquidity_balance or 0.0,
                })

            ml = self.env['account.move.line'].search([('payment_id', '=', 146)])
            print(ml, 'ml')
        return all_move_vals
