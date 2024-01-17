from odoo import models, fields, api


class Partner(models.Model):
    _inherit = 'res.partner'


    ending_balance_customer=fields.Float(string='Ending Balance',compute='_compute_ending_balance')
    ending_balance_filter_customer = fields.Float(string='Ending Balance Filtered')
    ending_balance_vendor=fields.Float(string='Ending Balance',compute='_compute_ending_balance_vendor')
    ending_balance_filter_vendor = fields.Float(string='Ending Balance Filtered')

    def _compute_ending_balance(self):
        for rec in self:
            total1=0
            total2=0
            invoice_bal=0

            for line in self.balance_invoice_ids:
                        invoice_bal=invoice_bal+line.result
            for line in rec.oustanding_invoice_ids:
                        total1=total1+line.amount
            for credit in rec.oustanding_credit_ids:
                        total2=total2+credit.amount
            balance = rec.opening_balance_total_customer+invoice_bal+total2
            ending_bal=balance - total1
            rec.ending_balance_customer=ending_bal


    def _compute_ending_balance_vendor(self):
        for rec in self:
            total1=0
            total2=0
            invoice_bal=0

            for line in self.supplier_invoice_ids:
                        invoice_bal=invoice_bal+line.result
            for line in rec.supplier_paymnet_ids:
                        total1=total1+line.amount
            for credit in rec.supplier_credit_ids:
                        total2=total2+credit.amount

            balance = rec.opening_balance_total_vendor+invoice_bal+total2
            ending_bal=balance - total1
            rec.ending_balance_vendor=ending_bal


    @api.onchange('filter_start_date_customer','filter_end_date_customer')

    def onchange_ending_balance_customer(self):
        entry = self.env['account.move'].search([('type', '=', 'entry')])
        credits_customer = 0
        debit_customer = 0
        total1_customer=0
        total2_customer=0
        balance_cus_ids_total=0
        for entry1 in entry:

            if entry1.date:
                if self.filter_start_date_customer and self.filter_end_date_customer:
                    if entry1.date >= self.filter_start_date_customer and entry1.date <= self.filter_end_date_customer:
                        if not entry1.invoice_line_ids.payment_id:

                            for entry2 in entry1.line_ids.filtered(lambda rec: rec.partner_id.id == self._origin.id):

                                if entry2.account_id.user_type_id.type == 'receivable':
                                    credits_customer = credits_customer + entry2.credit
                                    debit_customer = debit_customer + entry2.debit

                elif self.filter_start_date_customer:
                    if entry1.date >= self.filter_start_date_customer:
                        if not entry1.invoice_line_ids.payment_id:

                            for entry2 in entry1.line_ids.filtered(lambda rec: rec.partner_id.id == self._origin.id):

                                if entry2.account_id.user_type_id.type == 'receivable':
                                    credits_customer = credits_customer + entry2.credit
                                    debit_customer = debit_customer + entry2.debit

                elif self.filter_end_date_customer:
                    if entry1.date <= self.filter_end_date_customer:
                        if not entry1.invoice_line_ids.payment_id:

                            for entry2 in entry1.line_ids.filtered(lambda rec: rec.partner_id.id == self._origin.id):

                                if entry2.account_id.user_type_id.type == 'receivable':
                                    credits_customer = credits_customer + entry2.credit
                                    debit_customer = debit_customer + entry2.debit

        if self.filter_start_date_customer and self.filter_end_date_customer:
            for line in self.balance_invoice_ids.filtered(
                    lambda invoice: invoice.invoice_date >= self.filter_start_date_customer and invoice.invoice_date <= self.filter_end_date_customer):
                balance_cus_ids_total = balance_cus_ids_total + line.result

            for line in self.oustanding_invoice_ids.filtered(
                    lambda payment: payment.payment_date >= self.filter_start_date_customer and payment.payment_date <= self.filter_end_date_customer):
                total1_customer = total1_customer + line.amount
            for credit in self.oustanding_credit_ids.filtered(
                    lambda payment: payment.payment_date >= self.filter_start_date_customer and payment.payment_date <= self.filter_end_date_customer):
                total2_customer = total2_customer + credit.amount
        elif self.filter_start_date_customer:
            for line in self.balance_invoice_ids.filtered(
                    lambda invoice: invoice.invoice_date >= self.filter_start_date_customer):
                balance_cus_ids_total = balance_cus_ids_total + line.result

            for line in self.oustanding_invoice_ids.filtered(
                    lambda payment: payment.payment_date >= self.filter_start_date_customer):
                total1_customer = total1_customer + line.amount
            for credit in self.oustanding_credit_ids.filtered(
                    lambda payment: payment.payment_date >= self.filter_start_date_customer):
                total2_customer = total2_customer + credit.amount
        elif self.filter_end_date_customer:
            for line in self.balance_invoice_ids.filtered(
                    lambda invoice: invoice.invoice_date <= self.filter_end_date_customer):
                balance_cus_ids_total = balance_cus_ids_total + line.result

            for line in self.oustanding_invoice_ids.filtered(
                    lambda payment: payment.payment_date <= self.filter_end_date_customer):
                total1_customer = total1_customer + line.amount
            for credit in self.oustanding_credit_ids.filtered(
                    lambda payment: payment.payment_date <= self.filter_end_date_customer):
                total2_customer = total2_customer + credit.amount


        totals = debit_customer - credits_customer

        balance = totals + balance_cus_ids_total + total2_customer
        ending_bals = balance - total1_customer
        self.ending_balance_filter_customer = ending_bals

    @api.onchange('filter_start_date_vendor', 'filter_end_date_vendor')
    def onchange_ending_balance_vendor(self):
        entry = self.env['account.move'].search([('type', '=', 'entry')])
        credits_vendor = 0
        debit_vendor = 0
        total1_vendor = 0
        total2_vendor = 0
        balance_supp_ids_total = 0
        for entry1 in entry:

            if entry1.date:
                if self.filter_start_date_vendor and self.filter_end_date_vendor:
                    if entry1.date >= self.filter_start_date_vendor and entry1.date <= self.filter_end_date_vendor:
                        if not entry1.invoice_line_ids.payment_id:

                            for entry2 in entry1.line_ids.filtered(lambda rec: rec.partner_id.id == self._origin.id):

                                if entry2.account_id.user_type_id.type == 'payable':
                                    credits_vendor = credits_vendor + entry2.credit
                                    debit_vendor = debit_vendor + entry2.debit

                elif self.filter_start_date_vendor:
                    if entry1.date >= self.filter_start_date_vendor:
                        if not entry1.invoice_line_ids.payment_id:

                            for entry2 in entry1.line_ids.filtered(lambda rec: rec.partner_id.id == self._origin.id):

                                if entry2.account_id.user_type_id.type == 'payable':
                                    credits_vendor = credits_vendor + entry2.credit
                                    debit_vendor = debit_vendor + entry2.debit

                elif self.filter_end_date_vendor:
                    if entry1.date <= self.filter_end_date_vendor:
                        if not entry1.invoice_line_ids.payment_id:

                            for entry2 in entry1.line_ids.filtered(lambda rec: rec.partner_id.id == self._origin.id):

                                if entry2.account_id.user_type_id.type == 'payable':
                                    credits_vendor = credits_vendor + entry2.credit
                                    debit_vendor = debit_vendor + entry2.debit
        if self.filter_start_date_vendor and self.filter_end_date_vendor:
            for line in self.supplier_invoice_ids.filtered(
                    lambda invoice: invoice.invoice_date >= self.filter_start_date_vendor and invoice.invoice_date <= self.filter_end_date_vendor):
                balance_supp_ids_total = balance_supp_ids_total + line.result

            for line in self.supplier_paymnet_ids.filtered(
                    lambda payment: payment.payment_date >= self.filter_start_date_vendor and payment.payment_date <= self.filter_end_date_vendor):
                total1_vendor = total1_vendor + line.amount
            for credit in self.supplier_credit_ids.filtered(
                    lambda payment: payment.payment_date >= self.filter_start_date_vendor and payment.payment_date <= self.filter_end_date_vendor):
                total2_vendor = total2_vendor + credit.amount
        elif self.filter_start_date_vendor:
            for line in self.supplier_invoice_ids.filtered(
                    lambda invoice: invoice.invoice_date >= self.filter_start_date_vendor):
                balance_supp_ids_total = balance_supp_ids_total + line.result

            for line in self.supplier_paymnet_ids.filtered(
                    lambda payment: payment.payment_date >= self.filter_start_date_vendor):
                total1_vendor = total1_vendor + line.amount
            for credit in self.supplier_credit_ids.filtered(
                    lambda payment: payment.payment_date >= self.filter_start_date_vendor):
                total2_vendor = total2_vendor + credit.amount
        elif self.filter_end_date_vendor:
            for line in self.supplier_invoice_ids.filtered(
                    lambda invoice: invoice.invoice_date <= self.filter_end_date_vendor):
                balance_supp_ids_total = balance_supp_ids_total + line.result

            for line in self.supplier_paymnet_ids.filtered(
                    lambda payment: payment.payment_date <= self.filter_end_date_vendor):
                total1_vendor = total1_vendor + line.amount
            for credit in self.supplier_credit_ids.filtered(
                    lambda payment: payment.payment_date <= self.filter_end_date_vendor):
                total2_vendor = total2_vendor + credit.amount


        total = credits_vendor - debit_vendor

        balance = total + balance_supp_ids_total + total2_vendor
        ending_bal = balance - total1_vendor
        self.ending_balance_filter_vendor = ending_bal

