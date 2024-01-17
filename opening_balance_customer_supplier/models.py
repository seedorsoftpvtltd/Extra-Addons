from odoo import models, fields, api


class Partner(models.Model):
    _inherit = 'res.partner'

    opening_balance_customer = fields.Float(string='Opening Balance')
    opening_balance_total_customer = fields.Float(string='Opening Balance Total',compute='_compute_opening_balance_customer')
    opening_balance_vendor = fields.Float(string='Opening Balance')
    opening_balance_total_vendor = fields.Float(string='Opening Balance Total',compute='_compute_opening_balance_vendor')


    def _compute_opening_balance_customer(self):

        for record in self:

            entry=self.env['account.move'].search([('type','=','entry'),('state','!=','cancel')])
            credit=0
            debit=0
            for entry1 in entry:
                if not entry1.invoice_line_ids.payment_id:
                    for entry2 in entry1.line_ids.filtered(lambda rec: rec.partner_id.id == record.id):
                            if entry2.account_id.user_type_id.type == 'receivable':
                                credit=credit+entry2.credit
                                debit=debit+entry2.debit

            total=debit-credit
            record.opening_balance_total_customer=total

    def _compute_opening_balance_vendor(self):
        for record in self:
            entry=self.env['account.move'].search([('type','=','entry'),('state','!=','cancel')])
            credit=0
            debit=0

            for entry1 in entry:
                if not entry1.invoice_line_ids.payment_id:
                    for entry2 in entry1.line_ids.filtered(lambda rec: rec.partner_id.id == record.id):

                            if entry2.account_id.user_type_id.type == 'payable':

                                credit=credit+entry2.credit
                                debit=debit+entry2.debit

            total=credit-debit
            record.opening_balance_total_vendor=total

    @api.onchange('filter_start_date_customer','filter_end_date_customer')

    def onchange_filter_start_date_customer(self):
        entry = self.env['account.move'].search([('type', '=', 'entry'),('state','!=','cancel')])
        credit = 0
        debit = 0

        for entry1 in entry:

                if entry1.date:
                    if self.filter_start_date_customer and self.filter_end_date_customer:
                        if entry1.date >= self.filter_start_date_customer and entry1.date <= self.filter_end_date_customer:

                            if not entry1.invoice_line_ids.payment_id:
                                for entry2 in entry1.line_ids.filtered(lambda rec: rec.partner_id.id == self._origin.id):
                                        if entry2.account_id.user_type_id.type == 'receivable':
                                            credit = credit + entry2.credit
                                            debit = debit + entry2.debit

                    elif self.filter_start_date_customer:
                        if entry1.date >= self.filter_start_date_customer:
                            if not entry1.invoice_line_ids.payment_id:
                                for entry2 in entry1.line_ids.filtered(lambda rec: rec.partner_id.id == self._origin.id):
                                        if entry2.account_id.user_type_id.type == 'receivable':
                                            credit = credit + entry2.credit
                                            debit = debit + entry2.debit
                    elif self.filter_end_date_customer:
                        if entry1.date <= self.filter_end_date_customer:
                            if not entry1.invoice_line_ids.payment_id:
                                for entry2 in entry1.line_ids.filtered(lambda rec: rec.partner_id.id == self._origin.id):
                                        if entry2.account_id.user_type_id.type == 'receivable':

                                            credit = credit + entry2.credit
                                            debit = debit + entry2.debit

        total = debit - credit
        self.opening_balance_customer = total

    @api.onchange('filter_start_date_vendor', 'filter_end_date_vendor')
    def onchange_filter_start_date_vendor(self):
        entry = self.env['account.move'].search([('type', '=', 'entry'),('state','!=','cancel')])
        credit = 0
        debit = 0

        for entry1 in entry:

            if entry1.date:
                if self.filter_start_date_vendor and self.filter_end_date_vendor:
                    if entry1.date >= self.filter_start_date_vendor and entry1.date <= self.filter_end_date_vendor:
                        if not entry1.invoice_line_ids.payment_id:
                            for entry2 in entry1.line_ids.filtered(lambda rec: rec.partner_id.id == self._origin.id):
                                    if entry2.account_id.user_type_id.type == 'payable':
                                        credit = credit + entry2.credit
                                        debit = debit + entry2.debit

                elif self.filter_start_date_vendor:
                    if entry1.date >= self.filter_start_date_vendor:
                        if not entry1.invoice_line_ids.payment_id:
                            for entry2 in entry1.line_ids.filtered(lambda rec: rec.partner_id.id == self._origin.id):
                                    if entry2.account_id.user_type_id.type == 'payable':
                                        credit = credit + entry2.credit
                                        debit = debit + entry2.debit
                elif self.filter_end_date_vendor:
                    if entry1.date <= self.filter_end_date_vendor:
                        if not entry1.invoice_line_ids.payment_id:
                            for entry2 in entry1.line_ids.filtered(lambda rec: rec.partner_id.id == self._origin.id):
                                    if entry2.account_id.user_type_id.type == 'payable':
                                        credit = credit + entry2.credit
                                        debit = debit + entry2.debit

        total = credit-debit
        self.opening_balance_vendor = total



