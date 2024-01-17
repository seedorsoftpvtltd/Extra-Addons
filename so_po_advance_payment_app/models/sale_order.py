# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError


class SaleOrder(models.Model):
	_inherit = 'sale.order'

	payment_history_ids = fields.One2many('advance.payment.history','order_id',string="Advanvce Payment Information")

	def set_sale_advance_payment(self):
		view_id = self.env.ref('so_po_advance_payment_app.sale_advance_payment_wizard')
		if view_id:
			pay_wiz_data={
				'name' : _('Sale Advance Payment'),
				'type' : 'ir.actions.act_window',
				'view_type' : 'form',
				'view_mode' : 'form',
				'res_model' : 'sale.advance.payment',
				'view_id' : view_id.id,
				'target' : 'new',
				'context' : {
							'name':self.name,
							'order_id':self.id,
							'total_amount':self.amount_total,
							'company_id':self.company_id.id,
							'currency_id':self.currency_id.id,
							'date_order':self.date_order,
							'currency_rate':self.currency_rate,
							'partner_id':self.partner_id.id,
							 },
			}
		return pay_wiz_data


class AccountPayment(models.Model):
	_inherit = "account.payment"

	check_advance_payment = fields.Boolean('Check Advance Payment', default=False)


	def _prepare_payment_moves(self):
		''' Prepare the creation of journal entries (account.move) by creating a list of python dictionary to be passed
		to the 'create' method.

		Example 1: outbound with write-off:

		Account             | Debit     | Credit
		---------------------------------------------------------
		BANK                |   900.0   |
		RECEIVABLE          |           |   1000.0
		WRITE-OFF ACCOUNT   |   100.0   |

		Example 2: internal transfer from BANK to CASH:

		Account             | Debit     | Credit
		---------------------------------------------------------
		BANK                |           |   1000.0
		TRANSFER            |   1000.0  |
		CASH                |   1000.0  |
		TRANSFER            |           |   1000.0

		:return: A list of Python dictionary to be passed to env['account.move'].create.
		'''
		all_move_vals = []
		for payment in self:
			company_currency = payment.company_id.currency_id
			move_names = payment.move_name.split(payment._get_move_name_transfer_separator()) if payment.move_name else None

			if not self.company_id.adv_account_id and not self.company_id.adv_account_creditors_id:
				raise UserError(_(
					"You can't create a new advance payment without an customer/supplier receivable/payable account"))

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
				balance = payment.currency_id._convert(counterpart_amount, company_currency, payment.company_id, payment.payment_date)
				write_off_balance = payment.currency_id._convert(write_off_amount, company_currency, payment.company_id, payment.payment_date)
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

			# ==== 'inbound' / 'outbound' ====

			# Destination Account Set base on configuration
			if self._context.get('check_advance_payment') == True:
				if payment.partner_type == 'customer':
					destination_account_id = payment.company_id.adv_account_id.id
				else:
					destination_account_id = payment.company_id.adv_account_creditors_id.id
			else:
				destination_account_id = payment.destination_account_id.id

			move_vals = {
				'date': payment.payment_date,
				'ref': payment.communication,
				'journal_id': payment.journal_id.id,
				'currency_id': payment.journal_id.currency_id.id or payment.company_id.currency_id.id,
				'partner_id': payment.partner_id.id,
				'line_ids': [
					# Receivable / Payable / Transfer line.
					(0, 0, {
						'name': rec_pay_line_name,
						'amount_currency': counterpart_amount + write_off_amount if currency_id else 0.0,
						'currency_id': currency_id,
						'debit': balance + write_off_balance > 0.0 and balance + write_off_balance or 0.0,
						'credit': balance + write_off_balance < 0.0 and -balance - write_off_balance or 0.0,
						'date_maturity': payment.payment_date,
						'partner_id': payment.partner_id.commercial_partner_id.id,
						'account_id': destination_account_id,
						'payment_id': payment.id,
					}),
					# Liquidity line.
					(0, 0, {
						'name': liquidity_line_name,
						'amount_currency': -liquidity_amount if liquidity_line_currency_id else 0.0,
						'currency_id': liquidity_line_currency_id,
						'debit': balance < 0.0 and -balance or 0.0,
						'credit': balance > 0.0 and balance or 0.0,
						'date_maturity': payment.payment_date,
						'partner_id': payment.partner_id.commercial_partner_id.id,
						'account_id': liquidity_line_account.id,
						'payment_id': payment.id,
					}),
				],
			}
			if write_off_balance:
				# Write-off line.
				move_vals['line_ids'].append((0, 0, {
					'name': payment.writeoff_label,
					'amount_currency': -write_off_amount,
					'currency_id': currency_id,
					'debit': write_off_balance < 0.0 and -write_off_balance or 0.0,
					'credit': write_off_balance > 0.0 and write_off_balance or 0.0,
					'date_maturity': payment.payment_date,
					'partner_id': payment.partner_id.commercial_partner_id.id,
					'account_id': payment.writeoff_account_id.id,
					'payment_id': payment.id,
				}))

			if move_names:
				move_vals['name'] = move_names[0]

			all_move_vals.append(move_vals)

			# ==== 'transfer' ====
			if payment.payment_type == 'transfer':
				journal = payment.destination_journal_id

				# Manage custom currency on journal for liquidity line.
				if journal.currency_id and payment.currency_id != journal.currency_id:
					# Custom currency on journal.
					liquidity_line_currency_id = journal.currency_id.id
					transfer_amount = company_currency._convert(balance, journal.currency_id, payment.company_id, payment.payment_date)
				else:
					# Use the payment currency.
					liquidity_line_currency_id = currency_id
					transfer_amount = counterpart_amount

				transfer_move_vals = {
					'date': payment.payment_date,
					'ref': payment.communication,
					'partner_id': payment.partner_id.id,
					'journal_id': payment.destination_journal_id.id,
					'line_ids': [
						# Transfer debit line.
						(0, 0, {
							'name': payment.name,
							'amount_currency': -counterpart_amount if currency_id else 0.0,
							'currency_id': currency_id,
							'debit': balance < 0.0 and -balance or 0.0,
							'credit': balance > 0.0 and balance or 0.0,
							'date_maturity': payment.payment_date,
							'partner_id': payment.partner_id.commercial_partner_id.id,
							'account_id': payment.company_id.transfer_account_id.id,
							'payment_id': payment.id,
						}),
						# Liquidity credit line.
						(0, 0, {
							'name': _('Transfer from %s') % payment.journal_id.name,
							'amount_currency': transfer_amount if liquidity_line_currency_id else 0.0,
							'currency_id': liquidity_line_currency_id,
							'debit': balance > 0.0 and balance or 0.0,
							'credit': balance < 0.0 and -balance or 0.0,
							'date_maturity': payment.payment_date,
							'partner_id': payment.partner_id.commercial_partner_id.id,
							'account_id': payment.destination_journal_id.default_credit_account_id.id,
							'payment_id': payment.id,
						}),
					],
				}

				if move_names and len(move_names) == 2:
					transfer_move_vals['name'] = move_names[1]

				all_move_vals.append(transfer_move_vals)
		return all_move_vals