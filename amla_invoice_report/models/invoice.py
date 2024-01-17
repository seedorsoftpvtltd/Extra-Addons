from odoo import api, fields, models, tools, _
from datetime import datetime, timedelta
import json


class invoice_report(models.Model):
    _inherit='account.move'
    payment=fields.Float(string='payment')
    payment_date = fields.Date(string='Payment Date')
    paid=fields.Float(string='Paid')
    bank = fields.Float(string='Bank')

    # @api.depends('invoice_payment_term_id')
    # def _compute_payment_date(self):
    #     for record in self:
    #         if record.invoice_payment_term_id:
    #             # Get the payment term details
    #             payment_term = record.invoice_payment_term_id
    #
    #             # Calculate the payment due date based on the invoice date and payment term details
    #             invoice_date = datetime.strptime(str(record.invoice_date), '%Y-%m-%d').date()
    #             due_date = invoice_date + timedelta(days=payment_term.line_ids[0].days)
    #
    #             # Get the payment date if a payment has been made for the invoice
    #             payment_date = False
    #             if record.state=='paid':
    #                 payment = self.env['account.payment'].search([('move_id', '=', record.id)], limit=1)
    #                 if payment:
    #                     payment_date = payment.payment_date.date()
    #
    #             # Store the payment date in the 'payment_date' field
    #             record.payment_date = payment_date or due_date





    # def _get_payment_type(self):
    #           #pay1 = self.env['account.payment'].search(
    #           #    [('partner_type', '=', 'customer'), ('state', '=', 'posted')])
    #           #for rec1 in pay1:
    #           #   if rec1.reconciled_invoice_ids:
    #           #       for invoice in rec1.reconciled_invoice_ids:
    #           #            if rec1.payment_method_id.id == 1:
    #
    #           #                invoice.paid = rec1.amount
    #           #                invoice.payment_date = rec1.payment_date
    #           #            else:
    #
    #           #                invoice.bank = rec1.amount
    #           #                invoice.payment_date = rec1.payment_date
    #           #self.payment = 1
    #           batch_size = 100
    #           payments = self.env['account.payment'].search([
    #              ('partner_type', '=', 'customer'),
    #               ('state', '=', 'posted'),
    #                ])
    #           invoices = self.filtered(lambda x: x.type == 'out_invoice')
    #           for index in range(0, len(payments), batch_size):
    #               batch_payments = payments[index:index + batch_size]
    #               batch_invoices = invoices.filtered(lambda x: x.id in batch_payments.reconciled_invoice_ids.ids)
    #               for invoice in batch_invoices:
    #                  rec_payments = batch_payments.filtered(lambda x: invoice in x.reconciled_invoice_ids)
    #                  if rec_payments:
    #                        rec1 = rec_payments[0]
    #                        if rec1.payment_method_id.id == 1:
    #                              invoice.write({
    #                                      'paid': rec1.amount,
    #                                      'payment_date': rec1.payment_date,
    #                                           })
    #                        else:
    #                                  invoice.write({
    #                                       'bank': rec1.amount,
    #                                        'payment_date': rec1.payment_date,
    #                                              })
    #           self.payment = 1

              #invoice=self.env['account.move'].search([('type','=','out_invoice'),('invoice_payment_state','=','paid')])
              #for rec1 in invoice:

               #               data = json.loads(rec1.invoice_payments_widget)
               #               payment_method_name = data['content'][0]['payment_method_name']
                              #print("------------------------------------------------------------------------------------------------>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
                              #print(payment_method_name)
                              #print(rec1.name)
                #              if payment_method_name == 'Manual':
                #                  rec1.paid=data['content'][0]['amount']
                #                  rec1.payment_date = data['content'][0]['date']
                              #else:
                #              else:
                #                 rec1.payment_date = data['content'][0]['date']
                #                 rec1.bank = data['content'][0]['amount']

              #self.payment=1

    def get_lines(self):

        inv_report =self.env['account.move'].search([('type', '=', 'out_invoice')])

        return inv_report

    def get_report_datas(self):
        return self.get_lines()

