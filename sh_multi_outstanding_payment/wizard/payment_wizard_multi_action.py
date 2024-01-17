# -*- coding: utf-8 -*-
from odoo import models, fields, api, exceptions, _
import odoo.addons.decimal_precision as dp
from odoo.exceptions import UserError


class OutstandingLine(models.Model):
    _name = 'sh.payment.line'

    name = fields.Char("Reference")
    amount = fields.Float("Amount")
    date = fields.Date("Date")
    sh_boolean = fields.Boolean(" ")
    move_line_id = fields.Many2one('account.move.line')
    move_id = fields.Many2one(
        "account.move", string="", related="move_line_id.move_id")


class PaymentWizard(models.TransientModel):
    _name = "sh.payment.wizard"

    partner_id = fields.Many2one(
        'res.partner', string="Partner", required=True, readonly=True)
    date = fields.Date(
        string="Date", default=fields.Date.context_today, required=True, readonly=True)
    account_id = fields.Many2one(
        'account.account', string="Account", required=True, readonly=True)
    sh_account_move_ids = fields.Many2many(
        'account.move', string="", readonly=True, )
    sh_move_line_ids = fields.Many2many('sh.payment.line', string="",)

    def add_payment_wizard(self):

        if self.sh_move_line_ids.filtered(lambda x: x.sh_boolean == True):

            payment_lines = self.sh_move_line_ids.filtered(
                lambda x: x.sh_boolean)

            if payment_lines:
                for payment_line in payment_lines:
                    if payment_line.move_line_id:

                        lines = payment_line.move_line_id

                        lines += self.sh_account_move_ids.line_ids.filtered(
                            lambda line: line.account_id == lines[0].account_id and not line.reconciled)

                        lines.reconcile()

    def action_payment_allocation(self):

        active_ids = self.env.context.get('active_ids')
        active_model = self.env.context.get('active_model')
        active_id = self.env.context.get('active_id')
        listt = []
        payment_list = []
        account_payment_model = self.env[active_model].browse(active_id)
        if len(active_ids) > 0:
            active_ids.sort()
            account_payment_model = self.env[active_model].browse(active_id)
            for each_id in active_ids:
                account_payment_model = self.env[active_model].browse(active_id)
                each_account_payment_model = self.env[active_model].browse(
                    each_id)
                if each_account_payment_model.partner_id.id != account_payment_model.partner_id.id:
                    raise UserError("Partners Must be Same !")
                if each_account_payment_model.state != 'posted':
                    raise UserError(
                        "Only Posted Payments are consider for payment of Invoice/Bill !")
                if each_account_payment_model.payment_type != account_payment_model.payment_type or each_account_payment_model.partner_type != account_payment_model.partner_type:
                    raise UserError(
                        "Payment type and partner type must be same !")

            first_payment = self.env[active_model].browse(active_ids[0])

            if first_payment.partner_type == 'customer' and first_payment.payment_type == 'inbound':

                invoice_ids = self.env['account.move'].search([('partner_id', '=', first_payment.partner_id.id), (
                    'type', '=', 'out_invoice'), ('state', 'not in', ['draft', 'cancel'])])
#                invoice_ids = self.env['account.move'].search([(
#                    'type', '=', 'out_invoice'), ('state', 'not in', ['draft', 'cancel'])])

                not_paid_invoice_ids = invoice_ids.filtered(
                    lambda x: x.invoice_payment_state != 'paid')

                for invoice in not_paid_invoice_ids:
                    listt.append(invoice.id)

            if first_payment.partner_type == 'supplier' and first_payment.payment_type == 'outbound':

                bill_ids = self.env['account.move'].search([('partner_id', '=', first_payment.partner_id.id), (
                    'type', '=', 'in_invoice'), ('state', 'not in', ['draft', 'cancel'])])
#                bill_ids = self.env['account.move'].search([(
#                    'type', '=', 'in_invoice'), ('state', 'not in', ['draft', 'cancel'])])

                not_paid_bill_ids = bill_ids.filtered(
                    lambda x: x.invoice_payment_state != 'paid')

                for bill in not_paid_bill_ids:
                    listt.append(bill.id)

            domain = ['|', ('amount_residual_currency', '!=', 0.0), ('amount_residual', '!=', 0.0), ('reconciled', '=', False), (
                'partner_id', '=', first_payment.partner_id.id), ('account_id', '=', first_payment.destination_account_id.id)]

            if first_payment.partner_type == 'customer' and first_payment.payment_type == 'inbound':

                domain.extend([('credit', '>', 0), ('debit', '=', 0)])

            if first_payment.partner_type == 'supplier' and first_payment.payment_type == 'outbound':

                domain.extend([('credit', '=', 0), ('debit', '>', 0)])

            move_lines = self.env['account.move.line'].search(domain)

            lines = move_lines.filtered(
                lambda x: x.payment_id.move_reconciled == False)

            if lines:
                for line in lines.sorted(lambda x: x.id):

                    if line.amount_residual < 0.0:
                        amount = line.amount_residual * (-1)

                    else:
                        amount = line.amount_residual

                    payment_line = self.env['sh.payment.line'].sudo().create({'date': line.date,
                                                                              'name': line.name,
                                                                              'amount': amount,
                                                                              'move_line_id': line.id})

                    payment_list.append(payment_line.id)

        return{
            'name': 'Add Payment Allocation',
            'res_model': 'sh.payment.wizard',
            'view_mode': 'form',
            'view_id': self.env.ref('sh_multi_outstanding_payment.view_sh_payment_wizard_form').id,
            'context': {
                'default_sh_account_move_ids': [(6, 0, listt)],
                'default_sh_move_line_ids': [(6, 0, payment_list)],
                'default_partner_id': account_payment_model.partner_id.id,
                'default_account_id': account_payment_model.destination_account_id.id
            },
            'target': 'new',
            'type': 'ir.actions.act_window'
        }
