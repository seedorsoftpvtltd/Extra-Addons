from odoo import api,models,fields, _
import datetime
from pytz import timezone

DATE_DICT = {
    '%m/%d/%Y': 'mm/dd/yyyy',
    '%Y/%m/%d': 'yyyy/mm/dd',
    '%m/%d/%y': 'mm/dd/yy',
    '%d/%m/%Y': 'dd/mm/yyyy',
    '%d/%m/%y': 'dd/mm/yy',
    '%d-%m-%Y': 'dd-mm-yyyy',
    '%d-%m-%y': 'dd-mm-yy',
    '%m-%d-%Y': 'mm-dd-yyyy',
    '%m-%d-%y': 'mm-dd-yy',
    '%Y-%m-%d': 'yyyy-mm-dd',
    '%f/%e/%Y': 'm/d/yyyy',
    '%f/%e/%y': 'm/d/yy',
    '%e/%f/%Y': 'd/m/yyyy',
    '%e/%f/%y': 'd/m/yy',
    '%f-%e-%Y': 'm-d-yyyy',
    '%f-%e-%y': 'm-d-yy',
    '%e-%f-%Y': 'd-m-yyyy',
    '%e-%f-%y': 'd-m-yy'
}



class InvoiceXlsx(models.AbstractModel):
    _name = 'report.amla_invoice_report.invoice_report_xlsx'
    _inherit = ['report.report_xlsx.abstract']

    def _define_formats(self, workbook):
        """ Add cell formats to current workbook.
        Available formats:
         * format_title
         * format_header
        """
        self.format_title = workbook.add_format({
            'bold': True,
            'align': 'center',
            'font_size': 12,
            'font': 'Arial',
            'border': False
        })
        self.format_header = workbook.add_format({
            'bold': True,
            'font_size': 10,
            'align': 'center',
            'font': 'Arial',
            # 'border': True
        })
        self.content_header = workbook.add_format({
            'bold': False,
            'font_size': 10,
            'align': 'center',
            'border': True,
            'font': 'Arial',
        })
        self.content_header_date = workbook.add_format({
            'bold': False,
            'font_size': 10,
            'border': True,
            'align': 'center',
            'font': 'Arial',
        })
        self.line_header = workbook.add_format({
            'bold': True,
            'font_size': 10,
            'align': 'center',
            'top': True,
            'bottom': True,
            'font': 'Arial',
        })
        self.line_header_light = workbook.add_format({
            'bold': False,
            'font_size': 10,
            'align': 'center',
            'text_wrap': True,
            'font': 'Arial',
            'valign': 'top'
        })
        self.line_header_light_date = workbook.add_format({
            'bold': False,
            'font_size': 10,
            'align': 'center',
            'font': 'Arial',
        })
        self.line_header_light_initial = workbook.add_format({
            'italic': True,
            'font_size': 10,
            'align': 'center',
            'bottom': True,
            'font': 'Arial',
            'valign': 'top'
        })
        self.line_header_light_ending = workbook.add_format({
            'italic': True,
            'font_size': 10,
            'align': 'center',
            'top': True,
            'font': 'Arial',
            'valign': 'top'
        }
        )

    def generate_xlsx_report(self, workbook, data, record):

        self._define_formats(workbook)
        self.row_pos = 5
        self.col_pos = 0
        self.sheet = workbook.add_worksheet('Collection Report')
        self.sheet.set_column(0, 0, 20)
        self.sheet.set_column(1, 1, 20)
        self.sheet.set_column(2, 2, 20)
        self.sheet.set_column(3, 3, 18)
        self.sheet.set_column(5, 5, 18)
        self.sheet.set_column(8, 8, 18)
        # self.sheet.screen_gridlines = False
        title = 'Collection Report'
        self.sheet.merge_range(0, 0, 0, 8, title, self.format_title)
        title = 'Bill Details'
        self.sheet.merge_range(4, 9, 4, 11, title, self.format_title)
        invoice = self._get_payment_detail(data)
        invoice1 = self.env['account.move'].search(
            [('type', '=', 'out_invoice'),('state','=','posted'),('invoice_date', '>=', data['start_date']),
             ('invoice_date', '<=', data['end_date'])])
        # else:
        invoice2 = self.env['account.move'].search(
            [('type', '=', 'out_invoice'),('state','=','posted'),('payment_date', '>=', data['start_date']),
             ('payment_date', '<=', data['end_date']), ('invoice_date', '<', data['start_date'])])
        # self.sheet.write_string(self.row_pos, 0, _(''),
        #                         self.format_header)
        self.sheet.write_string(self.row_pos, 0, _('GST IN'),
                                self.format_header)
        self.sheet.write_string(self.row_pos, 1, _('Party Name'),
                                self.format_header)
        self.sheet.write_string(self.row_pos, 2, _('Bill Number'),
                                self.format_header)
        self.sheet.write_string(self.row_pos, 3, _('Date'),
                                self.format_header)
        self.sheet.write_string(self.row_pos, 4, _('Quantity'),
                                self.format_header)
        self.sheet.write_string(self.row_pos, 5, _('Net Amount'),
                                self.format_header)
        self.sheet.write_string(self.row_pos, 6, _('SGST'),
                                self.format_header)
        self.sheet.write_string(self.row_pos, 7, _('CGST'),
                                self.format_header)
        self.sheet.write_string(self.row_pos, 8, _('Total Amount'),
                                self.format_header)
        self.sheet.write_string(self.row_pos, 9, _('Paid'),
                                self.format_header)
        self.sheet.write_string(self.row_pos, 10, _('Bank'),
                                self.format_header)
        self.sheet.write_string(self.row_pos, 11, _('Credit'),
                                self.format_header)

        if invoice1:
            invoice1_sorted = sorted(invoice1, key=lambda x: x.invoice_date, reverse=False)
            for line in invoice1_sorted:
                self.row_pos += 1

                self.sheet.write_string(self.row_pos, 0, str(line['x_gstin']))
                self.sheet.write_string(self.row_pos, 1, str(line['partner_id'].name))
                self.sheet.write_string(self.row_pos, 2, line['name'] or '', self.line_header_light)
                self.sheet.write_string(self.row_pos, 3, str(line['invoice_date'].strftime('%d/%m/%Y')))
                #self.sheet.write_string(self.row_pos, 4, str(line['tot_qty']))
                self.sheet.write_number(self.row_pos, 4, int(line['tot_qty']))
                self.sheet.write_string(self.row_pos, 5, str(line['amount_untaxed']))
                self.sheet.write_string(self.row_pos, 6, str(line['x_sgst1']))
                self.sheet.write_string(self.row_pos, 7, str(line['x_cgst1']))
                self.sheet.write_string(self.row_pos, 8, str(line['amount_total']))
                self.sheet.write_string(self.row_pos, 9, str(line['paid']))
                self.sheet.write_string(self.row_pos, 10, str(line['bank']))
                self.sheet.write_string(self.row_pos, 11, str(line['amount_residual']))
        if invoice2:
            invoice2_sorted = sorted(invoice2, key=lambda x: x.invoice_date, reverse=False)
            self.sheet.merge_range(self.row_pos + 3, self.col_pos + 1, self.row_pos + 3,
                                   self.col_pos + 6, 'Old Bills Report', self.format_title)

            self.row_pos =self.row_pos + 4
            for line in invoice2_sorted:
                self.row_pos += 1
                self.sheet.write_string(self.row_pos, 0, str(line['x_gstin']))
                self.sheet.write_string(self.row_pos, 1, str(line['partner_id'].name))
                self.sheet.write_string(self.row_pos, 2, line['name'] or '', self.line_header_light)
                self.sheet.write_string(self.row_pos, 3, str(line['invoice_date'].strftime('%d/%m/%Y')))
                self.sheet.write_number(self.row_pos, 4, int(line['tot_qty']))
                #self.sheet.write_string(self.row_pos, 4, str(line['tot_qty']))
                self.sheet.write_string(self.row_pos, 5, str(line['amount_untaxed']))
                self.sheet.write_string(self.row_pos, 6, str(line['x_sgst1']))
                self.sheet.write_string(self.row_pos, 7, str(line['x_cgst1']))
                self.sheet.write_string(self.row_pos, 8, str(line['amount_total']))
                self.sheet.write_string(self.row_pos, 9, str(line['paid']))
                self.sheet.write_string(self.row_pos, 10, str(line['bank']))
                self.sheet.write_string(self.row_pos, 11, str(line['amount_residual']))

    def _get_payment_detail(self,data):
        payments = self.env['account.payment'].search([
            ('partner_type', '=', 'customer'),
            ('state', '=', 'posted'),
        ])
        invoice = self.env['account.move'].search([
            ('type', '=', 'out_invoice'),
            ('state', '=', 'posted'),
        ])
        invoice_names = {inv.name: inv for inv in invoice}

        for payment in payments.filtered(lambda p: p.reconciled_invoice_ids):
            for reconciled_invoice in payment.mapped('reconciled_invoice_ids').filtered(
                    lambda r: r.name in invoice_names):
                inv = invoice_names[reconciled_invoice.name]
                if payment.payment_method_id.name == 'Manual':
                    inv.paid = payment.amount
                    inv.payment_date = payment.payment_date
                else:
                    inv.bank = payment.amount
                    inv.payment_date = payment.payment_date
        #for inv in invoice:
        #    for pay in payments:
        #        for pay1 in pay.reconciled_invoice_ids:
        #            if pay1.name == inv.name:
        #                if pay.payment_method_id.name == 'Manual':
        #                    inv.paid = pay.amount
        #                    inv.payment_date = pay.payment_date
        #                else:
        #                    inv.bank = pay.amount
        #                    inv.payment_date = pay.payment_date




class productt_static(models.AbstractModel):
    _name = "report.amla_invoice_report.report_pdf"

    def _get_payment_detail(self,data):
        payments = self.env['account.payment'].search([
            ('partner_type', '=', 'customer'),
            ('state', '=', 'posted'),
        ])
        invoice = self.env['account.move'].search([
            ('type', '=', 'out_invoice'),
            ('state', '=', 'posted'),
        ])
        invoice_names = {inv.name: inv for inv in invoice}

        for payment in payments.filtered(lambda p: p.reconciled_invoice_ids):
            for reconciled_invoice in payment.mapped('reconciled_invoice_ids').filtered(
                    lambda r: r.name in invoice_names):
                inv = invoice_names[reconciled_invoice.name]
                if payment.payment_method_id.name == 'Manual':
                    inv.paid = payment.amount
                    inv.payment_date = payment.payment_date
                else:
                    inv.bank = payment.amount
                    inv.payment_date = payment.payment_date
        #for inv in invoice:
        #    for pay in payments:
        #        for pay1 in pay.reconciled_invoice_ids:
        #            if pay1.name == inv.name:
        #                if pay.payment_method_id.name == 'Manual':
        #                    inv.paid = pay.amount
        #                    inv.payment_date = pay.payment_date
        #                else:
        #                    inv.bank = pay.amount
        #                    inv.payment_date = pay.payment_date

    @api.model
    def _get_report_values(self, docids,data):

        ids=[]
        ids1=[]
        payment_detail = self._get_payment_detail(data)
        invoice1 = self.env['account.move'].search(
                [('type', '=', 'out_invoice'),('state','=','posted'),('invoice_date', '>=', data['start_date']),
                 ('invoice_date', '<=', data['end_date'])])

        invoice2 = self.env['account.move'].search(
                [('type', '=', 'out_invoice'),('state','=','posted'),('payment_date', '>=', data['start_date']),
                 ('payment_date', '<=', data['end_date']),('invoice_date', '<', data['start_date'])])

        for rec in invoice1:
            ids.append(rec)
        for rec1 in invoice2:
            ids1.append(rec1)

        return  {
           'invoice':ids,
            'invoice1':ids1,


         }
