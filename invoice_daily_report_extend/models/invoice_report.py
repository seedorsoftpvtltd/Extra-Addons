from odoo import api, fields, models



# class paymentmethod(models.Model):
#     _inherit='account.payment'
#
#
#     @api.model
#     def default_get(self, default_fields):
#         rec = super(account_payment, self).default_get(default_fields)
#         active_ids = self._context.get('active_ids') or self._context.get('active_id')
#         active_model = self._context.get('active_model')
#
#         # Check for selected invoices ids
#         if not active_ids or active_model != 'account.move':
#             return rec
#
#         invoices = self.env['account.move'].browse(active_ids).filtered(lambda move: move.is_invoice(include_receipts=True))
#
#         # Check all invoices are open
#         if not invoices or any(invoice.state != 'posted' for invoice in invoices):
#             raise UserError(_("You can only register payments for open invoices"))
#         # Check if, in batch payments, there are not negative invoices and positive invoices
#         dtype = invoices[0].type
#         for inv in invoices[1:]:
#             if inv.type != dtype:
#                 if ((dtype == 'in_refund' and inv.type == 'in_invoice') or
#                         (dtype == 'in_invoice' and inv.type == 'in_refund')):
#                     raise UserError(_("You cannot register payments for vendor bills and supplier refunds at the same time."))
#                 if ((dtype == 'out_refund' and inv.type == 'out_invoice') or
#                         (dtype == 'out_invoice' and inv.type == 'out_refund')):
#                     raise UserError(_("You cannot register payments for customer invoices and credit notes at the same time."))
#
#         amount = self._compute_payment_amount(invoices, invoices[0].currency_id, invoices[0].journal_id, rec.get('payment_date') or fields.Date.today())
#         rec.update({
#             'currency_id': invoices[0].currency_id.id,
#             'amount': abs(amount),
#             'payment_type': 'inbound' if amount > 0 else 'outbound',
#             'partner_id': invoices[0].commercial_partner_id.id,
#             'partner_type': MAP_INVOICE_TYPE_PARTNER_TYPE[invoices[0].type],
#             'communication': invoices[0].invoice_payment_ref or invoices[0].ref or invoices[0].name,
#             'invoice_ids': [(6, 0, invoices.ids)],
#             'x_invoice_lin': invoices[0].id ,
#         })
#         return rec

class accounting(models.Model):
    _inherit = 'account.move'
    x_rpd_cash = fields.Monetary(compute='_calculate_cash_total', string="Cash")
    x_rpd_pos = fields.Monetary(compute='_calculate_pos_total', string="Pos")
    x_rpd_cheque = fields.Monetary(compute='_calculate_cheque_total', string="Cheque")
# class paymentclass(models.Model):
#     _inherit = 'account.payment'
#     x_invoice_rel = fields.Many2one('account.move', 'account_invoice_payment_rel', 'payment_id', 'invoice_id' , domain=[('id', 'in', invoice_ids.ids)])

    # x_name_rel = fields.Char (related='name',string="Invoice relation")
    # x_rpd_pos = fields.Monetary(compute='_calulate_pos_total', string="Pos")
    # x_rpd_cheque = fields.Monetary(compute='_calulate_cheque_total', string="Cheque")
    # ('x_invoice'), ('payment_method_id', '=', 1)
    # 'x_invoice_lin'
    def _calculate_cash_total(self):
        amountcash = self.env['account.payment'].read_group([('payment_method_id', '=', 1),('partner_type','=','customer'),('state','=','posted')], fields=['amount','communication'], groupby=['communication'])
        for records in amountcash:
            print('.........>>>>>>>', records)
            payrec = records.get('communication')
            print(payrec)
            invoicerec=self.search_read(domain=[('name','=',payrec)] , fields=['id'])
            print('oiioioioi',invoicerec)
            if not invoicerec:
               pass
            else:
               inid= invoicerec[0]['id']
               print("mmmmm",inid)
               invoicerec = self.browse(inid)
               invoicerec.x_rpd_cash = records['amount']
               self -= invoicerec
        self.x_rpd_cash = 0

    def _calculate_pos_total(self):
        amountcash = self.env['account.payment'].read_group([('payment_method_id', '=', 5),('partner_type','=','customer'),('state','=','posted')], fields=['amount','communication'], groupby=['communication'])
        for records in amountcash:
            print('.........>>>>>>>', records)
            payrec = records.get('communication')
            print(payrec)
            invoicerec = self.search_read(domain=[('name', '=', payrec)], fields=['id'])
            print('oiioioioi', invoicerec)
            if not invoicerec:
               pass
            else:
               inid = invoicerec[0]['id']
               print("mmmmm", inid)
               invoicerec = self.browse(inid)
               invoicerec.x_rpd_pos = records['amount']
               self -= invoicerec
        self.x_rpd_pos = 0


    def _calculate_cheque_total(self):
        amountcash = self.env['account.payment'].read_group([('payment_method_id', '=', 3),('partner_type','=','customer'),('state','=','posted')], fields=['amount','communication'], groupby=['communication'])
        for records in amountcash:
            print('.........>>>>>>>', records)
            payrec = records.get('communication')
            print(payrec)
            invoicerec = self.search_read(domain=[('name', '=', payrec)], fields=['id'])
            print('oiioioioi', invoicerec)
            if not invoicerec:
               pass
            else:
               inid = invoicerec[0]['id']
               print("mmmmm", inid)
               invoicerec = self.browse(inid)
               invoicerec.x_rpd_cheque = records['amount']
               self -= invoicerec
        self.x_rpd_cheque = 0



"""class PaymentAccount(models.Model):
    _inherit='account.payment'
    x_invoice_lin= fields.Many2one('account.move' ,string="Invoice Link", copy=False)"""


    # def _calulate_cash_total(self):
    #         # for rec in self:
    #
    #             amountcash = self.env['account.payment'].read_group([('invoice_ids','in',self.id),
    #                                                                  ('payment_method_id','=',1)],fields=[ 'invoice_ids.id' ,'amount', 'payment_method_id'], groupby=['communication'])
    #             if not amountcash:
    #                 print(amountcash)
    #                 self.x_rpd_cash = 0
    #             else:
    #                 for records in amountcash:
    #                     print('.........>>>>>>>', records)
    #                     total = records.get('amount')[0]
    #
    #                     invoice_name = records.get('communication')
    #                     print(invoice_name)
    #                     record = self.search([('name', '=', invoice_name)])
    #                     print(record)
    #                     record.x_rpd_cash = records['amount']
    #                     self -= record
    #                 self.x_rpd_cash= 0







                # invoice_record.x_cash = records['amount']
                # self.x_rpd_cash = total

    # def _calulate_pos_total(self):
    #
    #         amountcash = self.env['account.payment'].read_group([('invoice_ids','in',self.id),
    #                                                              ('payment_method_id','=',2)],
    #                                                             fields=['invoice_ids' ,'amount', 'payment_method_id'], groupby=['communication'])
    #         for records in amountcash:
    #             print('.........>>>>>>>', records)
    #             total = records.get('amount')
    #             invoice_name = records.get('communication')
    #             record = self.browse('name','=' , invoice_name)
    #             record.x_rpd_cash = total
    #             # invoice_record.x_cash = records['amount']
    #             self.x_rpd_pos = total
    #
    #
    #
    # def _calulate_cheque_total(self):
    #
    #         amountcash = self.env['account.payment'].read_group([('invoice_ids','in',self.id),
    #                                                              ('payment_method_id','=',1)],
    #                                                             fields=['invoice_ids' ,'amount', 'payment_method_id'], groupby=['communication'])
    #         for records in amountcash:
    #             print('.........>>>>>>>', records)
    #             total = records.get('amount')
    #             # invoice_name = records.get('communication')
    #             # invoice_record = self.browse(name)
    #             # invoice_record.x_cash = records['amount']
    #             self.x_rpd_cheque = total
    # def _calulate_amount_total(self):
    #     for r in self:
    #         if r.invoice_ids.id

                #
                # @api.depends('num')
                # def _sum_num(self):
                #     for rec in self:
                #
                # rec_sum = sum(self.filtered(
                #     lambda x:(x.amount)).mapped('invoice_ids.id'))
                # rec.sum_num = rec_sum

     # my reference from browsing
    # def onchange_get_value_c(self):
    #     for rec in self:
    #         if rec.get_value_c and rec.o_2_m:
    #             for line in rec.get_value_c:
    #                 find_c = self.env["model.c"].search([('num_c', '=', line.num_c)])
    #                 find_a = self.env["model.a"].search([('num_a', '=', line.num_a)])
    #                 # compare value of num_c with num_a
    #                 if find_c.num_c == find_a.num_a:
    #                     for abc in rec.o_2_m:
    #                         return {'domain': {'o_2_m': [('num_a', '=', abc.find_a.id)]}}
    


