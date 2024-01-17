from odoo import api, fields, models
import itertools
from operator import itemgetter
import operator


class bulk_inv_payment(models.TransientModel):
    _inherit = 'bulk.inv.payment'

    # approval_ids = fields.One2many('approval.line', 'bulk_payment')

    # @api.model
    def write_post(self):
        # print("hiiisdffffffffffd")
        # for res in self:
        #     ress= self.env['account.payment'].write({
        #         'payment_type': res.payment_type,
        #         # 'payment_date': payment_date,
        #         'partner_type': res.partner_type,
        #         'payment_for': 'multi_payment',
        #         'partner_id': res.invoice_ids.partner_id,
        #         'journal_id': res.journal_id and self.journal_id.id or False,
        #         'communication': res.communication,
        #         # 'payment_method_id': payment_method_id and payment_method_id.id or False,
        #         'state': 'draft',
        #         # 'currency_id': res.get('values')[0].get('currency_id'),
        #         'amount': 0.0}
        #     )
        #
        #     print(ress)
        # return ress
        vals = []
        for line in self.invoice_ids:
            if line.paid_amount > 0.0:
                vals.append({
                    'invoice_id': line.invoice_id or False,
                    'partner_id': line.partner_id and line.partner_id.id or False,
                    'amount': line.amount or 0.0,
                    'paid_amount': line.paid_amount or 0.0,
                    'currency_id': line.invoice_id.currency_id.id or False,
                })
        new_vals = sorted(vals, key=itemgetter('partner_id'))
        groups = itertools.groupby(new_vals, key=operator.itemgetter('partner_id'))
        result = [{'partner_id': k, 'values': [x for x in v]} for k, v in groups]
        new_payment_ids = []
        for res in result:
            payment_method_id = self.env['account.payment.method'].search([('name', '=', 'Manual')], limit=1)
            if not payment_method_id:
                payment_method_id = self.env['account.payment.method'].search([], limit=1)
            payment_date = False
            if self.payment_date:
                payment_date = self.payment_date.strftime("%Y-%m-%d")
            pay_val = {
                'payment_type': self.payment_type,
                'payment_date': payment_date,
                'partner_type': self.partner_type,
                'payment_for': 'multi_payment',
                'partner_id': res.get('partner_id'),
                'journal_id': self.journal_id and self.journal_id.id or False,
                'communication': self.communication,
                'payment_method_id': payment_method_id and payment_method_id.id or False,
                'state': 'draft',
                'currency_id': res.get('values')[0].get('currency_id'),
                'amount': 0.0,
            }
            payment_id = self.env['account.payment'].create(pay_val)

            line_list = []
            paid_amt = 0
            inv_ids = []
            vals = []
            for inv_line in res.get('values'):
                invoice = inv_line.get('invoice_id')
                inv_ids.append(invoice.id)
                full_reco = False
                if invoice.amount_residual == inv_line.get('paid_amount'):
                    full_reco = True
                line_list.append((0, 0, {
                    'invoice_id': invoice.id,
                    'date': invoice.invoice_date,
                    'due_date': invoice.invoice_date_due,
                    'original_amount': invoice.amount_total,
                    'balance_amount': invoice.amount_residual,
                    'allocation': inv_line.get('paid_amount'),
                    'full_reconclle': full_reco,
                    'account_payment_id': payment_id and payment_id.id or False
                }))
                paid_amt += inv_line.get('paid_amount')
            payment_approver_ids = self.env['invoice.approval'].search([])
            # self.approval_ids = None
            if payment_approver_ids.approve_customer_payment and self.partner_type == 'customer':
                for user in payment_approver_ids.payment_approver_ids:
                    vals.append((0, 0, {
                        'approver_id': user.id,

                    }))
            elif payment_approver_ids.approve_vendor_payment and self.partner_type == 'supplier':
                for user in payment_approver_ids.vendor_payment_approver_ids:
                    vals.append((0, 0, {
                        'approver_id': user.id,

                    }))

            payment_id.write({
                'line_ids': line_list,
                'amount': paid_amt,
                'invoice_ids': [(6, 0, inv_ids)],
                'approval_ids': vals,
            })
            new_payment_ids.append(payment_id)

        return True