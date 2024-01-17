# -*- coding: utf-8 -*-
from odoo import models, fields, api, exceptions, _
import odoo.addons.decimal_precision as dp
from odoo.exceptions import UserError


class OutstandingLine(models.Model):
    _name = 'sh.outstanding.line'

    name = fields.Char("Reference")
    amount = fields.Float("Amount")
    date = fields.Date("Date")
    sh_boolean = fields.Boolean(" ")
    move_line_id = fields.Many2one('account.move.line')
    move_id = fields.Many2one(
        "account.move", string="", related="move_line_id.move_id")


class InvoiceWizard(models.TransientModel):
    _name = "sh.invoice.wizard"

    partner_id = fields.Many2one(
        'res.partner', string="Partner", required=True, )
    date = fields.Date(
        string="Date", default=fields.Date.context_today, required=True, )
    account_id = fields.Many2one(
        'account.account', string="Account", required=True, )
    # move_line_ids = fields.Many2many('account.move.line', string="")
    sh_move_line_ids = fields.Many2many('sh.outstanding.line', string="")
    sh_invoice_ids = fields.Many2many(
        'account.move', string="", readonly=True, )

    def add_outstanding_payment_wizard(self):

        if self.sh_move_line_ids.filtered(lambda x: x.sh_boolean):
            outstanding_lines = self.sh_move_line_ids.filtered(
                lambda x: x.sh_boolean)
            if outstanding_lines:
                for outstanding_line in outstanding_lines:
                    if outstanding_line.move_line_id:
                        lines = outstanding_line.move_line_id
                        lines += self.sh_invoice_ids.line_ids.filtered(
                            lambda line: line.account_id == lines[0].account_id and not line.reconciled)
                        lines.reconcile()

    def action_outstanding_payment(self):
        active_ids = self.env.context.get('active_ids')
        active_model = self.env.context.get('active_model')
        active_id = self.env.context.get('active_id')
        listt = []
        move_list = []
        if len(active_ids) > 0:
            active_ids.sort()
            account_move_model = self.env[active_model].browse(active_id)
            for each_id in active_ids:
                each_account_move_model = self.env[active_model].browse(
                    each_id)
                if each_account_move_model.partner_id.id != account_move_model.partner_id.id:
                    raise UserError("Partners Must be Same !")
                if each_account_move_model.state == 'draft' or each_account_move_model.state == 'cancel':
                    raise UserError(
                        "Only Posted Invoices are consider for outstanding payment !")
                if each_account_move_model.invoice_payment_state != 'paid':
                    listt.append(each_account_move_model.id)

            # get outstanding lines

            first_invoice = self.env[active_model].browse(active_ids[0])
            pay_term_line_ids = first_invoice.line_ids.filtered(
                lambda line: line.account_id.user_type_id.type in ('receivable', 'payable'))
            domain = [('account_id', 'in', pay_term_line_ids.mapped('account_id').ids),
                      '|', ('move_id.state', '=', 'posted'), '&', ('move_id.state',
                                                                   '=', 'draft'), ('journal_id.post_at', '=', 'bank_rec'),
                      ('partner_id', '=', first_invoice.commercial_partner_id.id),
                      ('reconciled', '=', False), '|', ('amount_residual', '!=', 0.0),
                      ('amount_residual_currency', '!=', 0.0)]
#            domain = [('account_id', 'in', pay_term_line_ids.mapped('account_id').ids),
#                      '|', ('move_id.state', '=', 'posted'), '&', ('move_id.state',
#                                                                   '=', 'draft'),
#                      ('journal_id.post_at', '=', 'bank_rec'),
#                      ('reconciled', '=', False), '|', ('amount_residual', '!=', 0.0),
#                      ('amount_residual_currency', '!=', 0.0)]

            if first_invoice.is_inbound():
                domain.extend([('credit', '>', 0), ('debit', '=', 0)])
                type_payment = _('Outstanding credits')
            else:
                domain.extend([('credit', '=', 0), ('debit', '>', 0)])
                type_payment = _('Outstanding debits')
            lines = self.env['account.move.line'].search(domain)

            if lines:
                for line in lines.sorted(lambda x: x.id):

                    if line.amount_residual < 0.0:
                        amount = line.amount_residual * (-1)
                    else:
                        amount = line.amount_residual
                    outstanding_line = self.env['sh.outstanding.line'].sudo().create({'date': line.date,
                                                                                      'name': line.name,
                                                                                      'amount': amount,
                                                                                      'move_line_id': line.id})
                    move_list.append(outstanding_line.id)

        return{
            'name': 'Add Outstanding Payment',
            'res_model': 'sh.invoice.wizard',
            'view_mode': 'form',
            'view_id': self.env.ref('sh_multi_outstanding_payment.view_invoice_outstanding_payment_wizard').id,
            'context': {
                'default_sh_invoice_ids': [(6, 0, listt)],
                'default_sh_move_line_ids': [(6, 0, move_list)],
                'default_partner_id': account_move_model.partner_id.id,
                'default_account_id': account_move_model.partner_id.property_account_receivable_id.id
            },
            'target': 'new',
            'type': 'ir.actions.act_window'
        }
