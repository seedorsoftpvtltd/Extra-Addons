import xlwt
import base64
import io
from odoo import api, models, fields, _
import xlwt


class SalesXLReport(models.TransientModel):
    _name = 'sales.xl.report'

    data = fields.Binary(string="Data")
    state = fields.Selection([('choose', 'Choose'), ('get', 'Get')], string="State", default='choose')
    name = fields.Char(string='File Name', readonly=True)
    invoice_no = fields.Many2many('account.move', string='Invoice No')
    partner_id = fields.Many2many('res.partner', string='Customer')
    include_vat = fields.Boolean(string='Include VAT')
    department = fields.Many2many('utm.medium', string='Department')

    def generate_report(self):
        # Get the sales data
        if self.include_vat != True:
            if self.invoice_no and not self.partner_id and not self.department:
                sales_data = self.env['operation.service'].search([('invoice_id', 'in', self.invoice_no.ids)])
                jv_data = self.env['account.move.line'].search([('move_id', 'in', self.invoice_no.ids)])

            elif not self.invoice_no and self.partner_id and not self.department:
                sales_data = self.env['operation.service'].search([('operation_id.customer_id', 'in', self.partner_id.ids)])
                jv_data = self.env['account.move.line'].search([('partner_id', 'in', self.partner_id.ids)])

            elif not self.invoice_no and not self.partner_id and self.department:
                sales_data = self.env['operation.service'].search([('operation_id.customer_id', 'in', self.partner_id.ids)])
                jv_data = self.env['account.move.line'].search([('partner_id', 'in', self.partner_id.ids)])

            elif self.invoice_no and self.partner_id and not self.department:
                sales_data = self.env['operation.service'].search(
                    [('operation_id.customer_id', 'in', self.partner_id.ids), ('invoice_id', 'in', self.invoice_no.ids)])
                jv_data = self.env['account.move.line'].search(
                    [('partner_id', 'in', self.partner_id.ids), ('move_id', 'in', self.invoice_no.ids)])
            elif self.invoice_no and not self.partner_id and self.department:
                sales_data = self.env['operation.service'].search(
                    [('operation_id.x_job_type', 'in', self.department.ids),
                     ('invoice_id', 'in', self.invoice_no.ids)])
                jv_data = self.env['account.move.line'].search(
                    [('move_id.operation_id.x_job_type', 'in', self.department.ids),
                     ('move_id', 'in', self.invoice_no.ids)])
            elif not self.invoice_no and self.partner_id and self.department:
                sales_data = self.env['operation.service'].search(
                    [('operation_id.x_job_type', 'in', self.department.ids),
                     ('operation_id.customer_id', 'in', self.partner_id.ids)])
                jv_data = self.env['account.move.line'].search(
                    [('move_id.operation_id.x_job_type', 'in', self.department.ids),
                     ('partner_id', 'in', self.partner_id.ids)])
            elif not self.invoice_no and self.partner_id and self.department:
                sales_data = self.env['operation.service'].search(
                    [('operation_id.x_job_type', 'in', self.department.ids),
                     ('operation_id.customer_id', 'in', self.partner_id.ids), ('invoice_id', 'in', self.invoice_no.ids)])
                jv_data = self.env['account.move.line'].search(
                    [('move_id.operation_id.x_job_type', 'in', self.department.ids),
                     ('partner_id', 'in', self.partner_id.ids), ('move_id', 'in', self.invoice_no.ids)])
            else:
                sales_data = self.env['operation.service'].search([('invoice_id','!=', False)])
                jv_data = self.env['account.move.line'].search([])

            print(sales_data, 'sales_data')

            # Get the payment data
            payment_data = self.env['account.payment'].search([
                ('payment_type', 'in', ['inbound', 'outbound']),
                ('state', '=', 'posted')
            ])

            # Create the XL workbook and worksheet
            workbook = xlwt.Workbook(encoding='utf-8')
            worksheet = workbook.add_sheet('Sales Report')
            date_format = xlwt.XFStyle()
            date_format.num_format_str = 'yyyy-mm-dd'

            # Write the headers
            default_widths = [
                ('GL Date', 4000), ('Month', 3000), ('Voucher No.', 4000), ('Voucher Type', 4000),
                ('Party', 6000), ('Ref. No.', 5000), ('Job No', 4000), ('Shipment No.', 4000),
                ('COA/AC Name', 6000), ('Department', 4000), ('Sale Amount (OMR)', 5000),
                ('Sales with Vat', 5000), ('Cost Amount (OMR)', 5000), ('Cost with Vat', 5000),
                ('GP', 4000), ('Salesperson', 5000)
            ]

            for index, (header, width) in enumerate(default_widths):
                worksheet.col(index).width = width
                worksheet.write(0, index, header)
            list = []
            row = 0
            # Write the sales data

            for roww, data in enumerate(sales_data):
                name = data.invoice_id.name
                account = data.inv_line_id.account_id.name
                b = str(name) + str(account)
                if b in list:
                    continue
                else:

                    row += 1

                    tax_amount = 0
                    account_name = data.inv_line_id.account_id.name
                    bla = data.search(
                        [('invoice_id.name', '=', data.invoice_id.name),
                         ('inv_line_id.account_id.name', '=', account_name)])
                    credit = 0
                    debit = 0
                    for b in bla:
                        credit += b.x_untaxed_amount_sale
                        debit += b.x_untaxed_amount_cost

                    date = data.invoice_id.invoice_date or data.invoice_id.create_date
                    worksheet.write(row, 0, date, date_format or '')
                    worksheet.write(row, 1, date.strftime("%B") or '')
                    worksheet.write(row, 2, data.invoice_id.name or '')
                    worksheet.write(row, 3, 'Invoices')
                    worksheet.write(row, 4, data.operation_id.customer_id.name or '')
                    worksheet.write(row, 5, data.invoice_id.ref or '')
                    worksheet.write(row, 6, data.operation_id.name or '')
                    # worksheet.write(row, 7, data.invoice_id.shipment_no or '')
                    worksheet.write(row, 8, data.inv_line_id.account_id.name or '')
                    worksheet.write(row, 9, data.operation_id.x_job_type.name or '')
                    worksheet.write(row, 10, data.x_untaxed_amount_sale or '')
                    worksheet.write(row, 11, 0 or '')
                    worksheet.write(row, 12, data.x_untaxed_amount_cost or '')
                    worksheet.write(row, 13, 0 or '')
                    worksheet.write(row, 14, (data.x_untaxed_amount_sale - data.x_untaxed_amount_cost) or '')
                    worksheet.write(row, 15, data.operation_id.operator_id.name or '')


                a = str(data.invoice_id.name) + str(data.inv_line_id.account_id.name)
                list.append(a)

            for roww, data in enumerate(jv_data):
                name = data.move_id.name
                account = data.account_id.name
                b = str(name) + str(account)
                if b in list:
                    continue
                else:
                    # print(data.move_id, 'data.move_id', data.payment_id, 'data.payment_id', data.move_id.type,
                    #       'data.move_id.type', data.account_internal_type, 'data.account_internal_type')
                    # print(data.move_id.type,'data.move_id.type', data.account_internal_type, 'data.account_internal_type', '...............')
                    print(data.tax_ids, 'data.tax_ids', data.move_id.type, 'data.move_id.type',
                          data.account_internal_type,
                          'data.account_internal_type')

                    if data.move_id.type == 'entry' and data.account_internal_type != 'receivable' and data.account_internal_type != 'payable' and not data.tax_line_id:

                        print('11111111111111', data.move_id, 'data.move_id', data.payment_id, 'data.payment_id',
                              data.move_id.type,
                              'data.move_id.type', data.account_internal_type, 'data.account_internal_type')
                        tax_amount = 0
                        bla = data.search(
                            [('move_id.name', '=', data.move_id.name), ('account_id.name', '=', data.account_id.name)])
                        credit = 0
                        debit = 0
                        for b in bla:
                            credit += b.credit
                            debit += b.debit
                        ctax_amount = 0
                        dtax_amount = 0
                        if data.tax_ids:
                            for tax in data.tax_ids:
                                tt = []
                                ttt = data.search(
                                    [('move_id.name', '=', data.move_id.name), ('tax_line_id', '=', tax.id)])
                                if ttt:
                                    tt.append(ttt[0])
                                for t in tt:
                                    ctax_amount += t.credit
                                    dtax_amount += t.debit
                        if credit > 0:
                            row += 1
                            date = data.date
                            worksheet.write(row, 0, date, date_format or '')
                            worksheet.write(row, 1, data.date.strftime("%B") or '')
                            worksheet.write(row, 2, data.move_id.name or '')
                            worksheet.write(row, 3, 'JV')
                            worksheet.write(row, 4, data.partner_id.name or '')
                            worksheet.write(row, 5, data.move_id.ref or '')
                            worksheet.write(row, 6, data.move_id.operation_id.name or '')
                            # worksheet.write(row, 7, data.move_id.shipment_no)
                            worksheet.write(row, 8, data.account_id.name or '')
                            worksheet.write(row, 9, data.move_id.operation_id.x_job_type.name or '')
                            worksheet.write(row, 10, credit or '')
                            worksheet.write(row, 11, 0 or '')
                            worksheet.write(row, 12, debit or '')
                            worksheet.write(row, 13, 0 or '')
                            worksheet.write(row, 14, ((credit) - (debit)) or '')
                            worksheet.write(row, 15, data.move_id.user_id.name or '')


                a = str(data.move_id.name) + str(data.account_id.name)
                list.append(a)

            # Save the XL file
            file_data = io.BytesIO()
            workbook.save(file_data)
            file_data.seek(0)

            # Prepare the file for download
            file_name = 'sales_report.xls'
            file_size = len(file_data.getvalue())
            self.write({
                'state': 'get',
                'data': base64.encodebytes(file_data.getvalue()),
                'name': file_name
            })

            return {
                'name': 'Sales Report',
                'type': 'ir.actions.act_url',
                'url': f"/web/content/{self.id}?model=sales.xl.report&field=data&download=true&filename={file_name}",
                'target': 'self'
            }
        else:
            if self.invoice_no and not self.partner_id and not self.department:
                sales_data = self.env['operation.service'].search([('invoice_id', 'in', self.invoice_no.ids)])
                jv_data = self.env['account.move.line'].search([('move_id', 'in', self.invoice_no.ids)])

            elif not self.invoice_no and self.partner_id and not self.department:
                sales_data = self.env['operation.service'].search(
                    [('operation_id.customer_id', 'in', self.partner_id.ids)])
                jv_data = self.env['account.move.line'].search([('partner_id', 'in', self.partner_id.ids)])

            elif not self.invoice_no and not self.partner_id and self.department:
                sales_data = self.env['operation.service'].search(
                    [('operation_id.customer_id', 'in', self.partner_id.ids)])
                jv_data = self.env['account.move.line'].search([('partner_id', 'in', self.partner_id.ids)])

            elif self.invoice_no and self.partner_id and not self.department:
                sales_data = self.env['operation.service'].search(
                    [('operation_id.customer_id', 'in', self.partner_id.ids),
                     ('invoice_id', 'in', self.invoice_no.ids)])
                jv_data = self.env['account.move.line'].search(
                    [('partner_id', 'in', self.partner_id.ids), ('move_id', 'in', self.invoice_no.ids)])
            elif self.invoice_no and not self.partner_id and self.department:
                sales_data = self.env['operation.service'].search(
                    [('operation_id.x_job_type', 'in', self.department.ids),
                     ('invoice_id', 'in', self.invoice_no.ids)])
                jv_data = self.env['account.move.line'].search(
                    [('move_id.operation_id.x_job_type', 'in', self.department.ids),
                     ('move_id', 'in', self.invoice_no.ids)])
            elif not self.invoice_no and self.partner_id and self.department:
                sales_data = self.env['operation.service'].search(
                    [('operation_id.x_job_type', 'in', self.department.ids),
                     ('operation_id.customer_id', 'in', self.partner_id.ids)])
                jv_data = self.env['account.move.line'].search(
                    [('move_id.operation_id.x_job_type', 'in', self.department.ids),
                     ('partner_id', 'in', self.partner_id.ids)])
            elif not self.invoice_no and self.partner_id and self.department:
                sales_data = self.env['operation.service'].search(
                    [('operation_id.x_job_type', 'in', self.department.ids),
                     ('operation_id.customer_id', 'in', self.partner_id.ids),
                     ('invoice_id', 'in', self.invoice_no.ids)])
                jv_data = self.env['account.move.line'].search(
                    [('move_id.operation_id.x_job_type', 'in', self.department.ids),
                     ('partner_id', 'in', self.partner_id.ids), ('move_id', 'in', self.invoice_no.ids)])
            else:
                sales_data = self.env['operation.service'].search([('invoice_id', '!=', False)])
                jv_data = self.env['account.move.line'].search([])
            print(sales_data, 'sales_data')

            # Get the payment data
            payment_data = self.env['account.payment'].search([
                ('payment_type', 'in', ['inbound', 'outbound']),
                ('state', '=', 'posted')
            ])

            # Create the XL workbook and worksheet
            workbook = xlwt.Workbook(encoding='utf-8')
            worksheet = workbook.add_sheet('Sales Report')
            date_format = xlwt.XFStyle()
            date_format.num_format_str = 'yyyy-mm-dd'

            # Write the headers
            default_widths = [
                ('GL Date', 4000), ('Month', 3000), ('Voucher No.', 4000), ('Voucher Type', 4000),
                ('Party', 6000), ('Ref. No.', 5000), ('Job No', 4000), ('Shipment No.', 4000),
                ('COA/AC Name', 6000), ('Department', 4000), ('Sale Amount (OMR)', 5000),
                ('Sales with Vat', 5000), ('Cost Amount (OMR)', 5000), ('Cost with Vat', 5000),
                ('GP', 4000), ('Salesperson', 5000)
            ]

            for index, (header, width) in enumerate(default_widths):
                worksheet.col(index).width = width
                worksheet.write(0, index, header)
            list = []
            row = 0

            # Write the sales data
            for roww, data in enumerate(sales_data):
                name = data.invoice_id.name
                account = data.inv_line_id.account_id.name
                b = str(name) + str(account)
                if b in list:
                    continue
                else:

                    tax_amount = 0
                    account_name = data.inv_line_id.account_id.name

                    bla = data.search(
                        [('invoice_id.name', '=', data.invoice_id.name),
                         ('inv_line_id.account_id.name', '=', account_name)])
                    credit = 0
                    debit = 0
                    for b in bla:
                        credit += b.x_sale_total
                        debit += b.x_cost_total
                    ctax_amount = 0
                    dtax_amount = 0
                    tax = data.search(
                        [('invoice_id.name', '=', data.invoice_id.name),
                         ('inv_line_id.account_id.name', '=', account_name)])

                    for t in tax:
                        if t.x_sale_total:
                            ctax_amount += b.x_sale_tax.amount
                            dtax_amount += b.x_tax_ids.amount

                    if credit > 0:
                        row += 1
                        date = data.invoice_id.invoice_date or data.invoice_id.create_date
                        worksheet.write(row, 0, date, date_format or '')
                        worksheet.write(row, 1, date.strftime("%B") or '')
                        worksheet.write(row, 2, data.invoice_id.name or '')
                        worksheet.write(row, 3, 'Invoices')
                        worksheet.write(row, 4, data.operation_id.customer_id.name or '')
                        worksheet.write(row, 5, data.invoice_id.ref or '')
                        worksheet.write(row, 6, data.operation_id.name or '')
                        # worksheet.write(row, 7, data.invoice_id.shipment_no or '')
                        worksheet.write(row, 8, data.inv_line_id.account_id.name or '')
                        worksheet.write(row, 9, data.operation_id.x_job_type.name or '')
                        worksheet.write(row, 10, data.x_sale_total or '')
                        worksheet.write(row, 11, data.x_sale_tax.amount or '')
                        worksheet.write(row, 12, data.x_cost_total or '')
                        worksheet.write(row, 13, data.x_tax_ids.amount or '')
                        worksheet.write(row, 14, (data.x_sale_total - data.x_cost_total) or '')
                        worksheet.write(row, 15, data.operation_id.operator_id.name or '')




                a = str(data.invoice_id.name) + str(data.inv_line_id.account_id.name)
                list.append(a)

            for roww, data in enumerate(jv_data):
                name = data.move_id.name
                account = data.account_id.name
                b = str(name) + str(account)
                if b in list:
                    continue
                else:
                    # print(data.move_id, 'data.move_id', data.payment_id, 'data.payment_id', data.move_id.type,
                    #       'data.move_id.type', data.account_internal_type, 'data.account_internal_type')
                    # print(data.move_id.type,'data.move_id.type', data.account_internal_type, 'data.account_internal_type', '...............')
                    print(data.tax_ids, 'data.tax_ids', data.move_id.type, 'data.move_id.type',
                          data.account_internal_type,
                          'data.account_internal_type')

                    if data.move_id.type == 'entry' and data.account_internal_type != 'receivable' and data.account_internal_type != 'payable' and not data.tax_line_id:
                        row += 1
                        print('11111111111111', data.move_id, 'data.move_id', data.payment_id, 'data.payment_id',
                              data.move_id.type,
                              'data.move_id.type', data.account_internal_type, 'data.account_internal_type')
                        tax_amount = 0
                        bla = data.search(
                            [('move_id.name', '=', data.move_id.name), ('account_id.name', '=', data.account_id.name)])
                        credit = 0
                        debit = 0
                        for b in bla:
                            credit += b.credit
                            debit += b.debit
                        ctax_amount = 0
                        dtax_amount = 0
                        if data.tax_ids:
                            for tax in data.tax_ids:
                                tt = []
                                ttt = data.search(
                                    [('move_id.name', '=', data.move_id.name), ('tax_line_id', '=', tax.id)])
                                if ttt:
                                    tt.append(ttt[0])
                                for t in tt:
                                    ctax_amount += t.credit
                                    dtax_amount += t.debit
                        date = data.date
                        worksheet.write(row, 0, date, date_format or '')
                        worksheet.write(row, 1, data.date.strftime("%B") or '')
                        worksheet.write(row, 2, data.move_id.name or '')
                        worksheet.write(row, 3, 'JV')
                        worksheet.write(row, 4, data.partner_id.name or '')
                        worksheet.write(row, 5, data.move_id.ref or '')
                        worksheet.write(row, 6, data.move_id.operation_id.name or '')
                        # worksheet.write(row, 7, data.move_id.shipment_no)
                        worksheet.write(row, 8, data.account_id.name or '')
                        worksheet.write(row, 9, data.move_id.operation_id.x_job_type.name or '')
                        worksheet.write(row, 10, credit or '')
                        worksheet.write(row, 11, 0 or '')
                        worksheet.write(row, 12, debit or '')
                        worksheet.write(row, 13, 0 or '')
                        worksheet.write(row, 14, ((credit) - (debit)) or '')
                        worksheet.write(row, 15, data.move_id.user_id.name or '')

                a = str(data.move_id.name) + str(data.account_id.name)
                list.append(a)
            # Save the XL file
            file_data = io.BytesIO()
            workbook.save(file_data)
            file_data.seek(0)

            # Prepare the file for download
            file_name = 'sales_report.xls'
            file_size = len(file_data.getvalue())
            self.write({
                'state': 'get',
                'data': base64.encodebytes(file_data.getvalue()),
                'name': file_name
            })

            return {
                'name': 'Sales Report',
                'type': 'ir.actions.act_url',
                'url': f"/web/content/{self.id}?model=sales.xl.report&field=data&download=true&filename={file_name}",
                'target': 'self'
            }







    def generate_reportt(self):
        # Get the sales data
        if self.include_vat != True:
            if self.invoice_no and not self.partner_id and not self.department:
                sales_data = self.env['account.move.line'].search([('move_id', 'in', self.invoice_no.ids)])
            elif not self.invoice_no and self.partner_id and not self.department:
                sales_data = self.env['account.move.line'].search([('partner_id', 'in', self.partner_id.ids)])
            elif not self.invoice_no and not self.partner_id and self.department:
                sales_data = self.env['account.move.line'].search([('partner_id', 'in', self.partner_id.ids)])
            elif self.invoice_no and self.partner_id and not self.department:
                sales_data = self.env['account.move.line'].search(
                    [('partner_id', 'in', self.partner_id.ids), ('move_id', 'in', self.invoice_no.ids)])
            elif self.invoice_no and not self.partner_id and self.department:
                sales_data = self.env['account.move.line'].search(
                    [('move_id.operation_id.x_job_type', 'in', self.department.ids),
                     ('move_id', 'in', self.invoice_no.ids)])
            elif not self.invoice_no and self.partner_id and self.department:
                sales_data = self.env['account.move.line'].search(
                    [('move_id.operation_id.x_job_type', 'in', self.department.ids),
                     ('partner_id', 'in', self.partner_id.ids)])
            elif not self.invoice_no and self.partner_id and self.department:
                sales_data = self.env['account.move.line'].search(
                    [('move_id.operation_id.x_job_type', 'in', self.department.ids),
                     ('partner_id', 'in', self.partner_id.ids), ('move_id', 'in', self.invoice_no.ids)])
            else:
                sales_data = self.env['account.move.line'].search([])
            print(sales_data, 'sales_data')

            # Get the payment data
            payment_data = self.env['account.payment'].search([
                ('payment_type', 'in', ['inbound', 'outbound']),
                ('state', '=', 'posted')
            ])

            # Create the XL workbook and worksheet
            workbook = xlwt.Workbook(encoding='utf-8')
            worksheet = workbook.add_sheet('Sales Report')
            date_format = xlwt.XFStyle()
            date_format.num_format_str = 'yyyy-mm-dd'
            

            # Write the headers
            default_widths = [
                ('GL Date', 4000), ('Month', 3000), ('Voucher No.', 4000), ('Voucher Type', 4000),
                ('Party', 6000), ('Ref. No.', 5000), ('Job No', 4000), ('Shipment No.', 4000),
                ('COA/AC Name', 6000), ('Department', 4000), ('Sale Amount (OMR)', 5000),
                ('Sales with Vat', 5000), ('Cost Amount (OMR)', 5000), ('Cost with Vat', 5000),
                ('GP', 4000), ('Salesperson', 5000)
            ]

            for index, (header, width) in enumerate(default_widths):
                worksheet.col(index).width = width
                worksheet.write(0, index, header)
            list = []
            row = 0
            # Write the sales data
            for roww, data in enumerate(sales_data):
                name = data.move_id.name
                account = data.account_id.name
                b = str(name) + str(account)
                if b in list:
                    continue
                else:
                    # print(data.move_id, 'data.move_id', data.payment_id, 'data.payment_id', data.move_id.type,
                    #       'data.move_id.type', data.account_internal_type, 'data.account_internal_type')
                    # print(data.move_id.type,'data.move_id.type', data.account_internal_type, 'data.account_internal_type', '...............')
                    print(data.tax_ids, 'data.tax_ids', data.move_id.type, 'data.move_id.type',
                          data.account_internal_type,
                          'data.account_internal_type')
                    if data.move_id.type == 'out_invoice' and data.account_internal_type != 'receivable' and not data.tax_line_id:
                        row += 1
                        print('11111111111111', data.move_id, 'data.move_id', data.payment_id, 'data.payment_id',
                              data.move_id.type,
                              'data.move_id.type', data.account_internal_type, 'data.account_internal_type')
                        sales = 0
                        cost = 0


                        bla = data.search(
                            [('move_id.name', '=', data.move_id.name), ('account_id.name', '=', data.account_id.name)])
                        credit = 0
                        debit = 0
                        for b in bla:
                            print(b, b.account_id, data.account_id, b.move_id, data.move_id, '---------')
                            credit += b.credit
                            debit += b.debit
                        ctax_amount = 0
                        dtax_amount = 0
                        if data.tax_ids:
                            for tax in data.tax_ids:
                                tt = []
                                ttt = data.search(
                                    [('move_id.name', '=', data.move_id.name), ('tax_line_id', '=', tax.id)])
                                if ttt:
                                    tt.append(ttt[0])
                                for t in tt:
                                    ctax_amount += t.credit
                                    dtax_amount += t.debit
                        date = data.date
                        worksheet.write(row, 0, date, date_format or '')
                        worksheet.write(row, 1, data.date.strftime("%B") or '')
                        worksheet.write(row, 2, data.move_id.name or '')
                        worksheet.write(row, 3, 'Invoice')
                        worksheet.write(row, 4, data.partner_id.name or '')
                        worksheet.write(row, 5, data.move_id.ref or '')
                        worksheet.write(row, 6, data.move_id.operation_id.name or '')
                        # worksheet.write(row, 7, data.move_id.shipment_no or '')
                        worksheet.write(row, 8, data.account_id.name or '')
                        worksheet.write(row, 9, data.move_id.operation_id.x_job_type.name or '')
                        worksheet.write(row, 10, credit or '')
                        worksheet.write(row, 11, 0 or '')
                        worksheet.write(row, 12, debit or '')
                        worksheet.write(row, 13, 0 or '')
                        worksheet.write(row, 14, ((credit) - (debit)) or '')
                        worksheet.write(row, 15, data.move_id.user_id.name or '')
                    elif data.move_id.type == 'out_refund' and data.account_internal_type != 'receivable' and not data.tax_line_id:
                        row += 1
                        print('2222222222', data.move_id, 'data.move_id', data.payment_id, 'data.payment_id',
                              data.move_id.type,
                              'data.move_id.type', data.account_internal_type, 'data.account_internal_type')
                        tax_amount = 0
                        bla = data.search(
                            [('move_id.name', '=', data.move_id.name), ('account_id.name', '=', data.account_id.name)])
                        credit = 0
                        debit = 0
                        for b in bla:
                            credit += b.credit
                            debit += b.debit
                        ctax_amount = 0
                        dtax_amount = 0
                        if data.tax_ids:
                            for tax in data.tax_ids:
                                tt = []
                                ttt = data.search(
                                    [('move_id.name', '=', data.move_id.name), ('tax_line_id', '=', tax.id)])
                                if ttt:
                                    tt.append(ttt[0])
                                for t in tt:
                                    ctax_amount += t.credit
                                    dtax_amount += t.debit
                        date = data.date
                        worksheet.write(row, 0, date, date_format or '')
                        worksheet.write(row, 1, data.date.strftime("%B") or '')
                        worksheet.write(row, 2, data.move_id.name or '')
                        worksheet.write(row, 3, 'Credit Note')
                        worksheet.write(row, 4, data.partner_id.name or '')
                        worksheet.write(row, 5, data.move_id.ref or '')
                        worksheet.write(row, 6, data.move_id.operation_id.name or '')
                        # worksheet.write(row, 7, data.move_id.shipment_no or '')
                        worksheet.write(row, 8, data.account_id.name or '')
                        worksheet.write(row, 9, data.move_id.operation_id.x_job_type.name or '')
                        worksheet.write(row, 10, credit or '')
                        worksheet.write(row, 11, 0 or '')
                        worksheet.write(row, 12, debit or '')
                        worksheet.write(row, 13, 0 or '')
                        worksheet.write(row, 14, ((credit) - (debit)) or '')
                        worksheet.write(row, 15, data.move_id.user_id.name or '')
                    # elif data.move_id.type == 'in_invoice' and data.account_internal_type != 'payable' and not data.tax_line_id:
                    #     row += 1
                    #     print('33333333333', data.move_id, 'data.move_id', data.payment_id, 'data.payment_id',
                    #           data.move_id.type,
                    #           'data.move_id.type', data.account_internal_type, 'data.account_internal_type')
                    #     tax_amount = 0
                    #     bla = data.search(
                    #         [('move_id.name', '=', data.move_id.name), ('account_id.name', '=', data.account_id.name)])
                    #     credit = 0
                    #     debit = 0
                    #     for b in bla:
                    #         credit += b.credit
                    #         debit += b.debit
                    #     ctax_amount = 0
                    #     dtax_amount = 0
                    #     if data.tax_ids:
                    #         for tax in data.tax_ids:
                    #             tt = data.search(
                    #                 [('move_id.name', '=', data.move_id.name), ('tax_line_id', '=', tax.id)])[0]
                    #             for t in tt:
                    #                 ctax_amount += tt.credit
                    #                 dtax_amount += tt.debit
                    #     date = data.date
                    #     worksheet.write(row, 0, date, date_format or '')
                    #     worksheet.write(row, 1, data.date.strftime("%B") or '')
                    #     worksheet.write(row, 2, data.move_id.name or '')
                    #     worksheet.write(row, 3, 'Bill')
                    #     worksheet.write(row, 4, data.partner_id.name or '')
                    #     worksheet.write(row, 5, data.move_id.ref or '')
                    #     worksheet.write(row, 6, data.move_id.operation_id.name or '')
                    #     # worksheet.write(row, 7, data.move_id.shipment_no or '')
                    #     worksheet.write(row, 8, data.account_id.name or '')
                    #     worksheet.write(row, 9, data.move_id.operation_id.x_job_type.name or '')
                    #     worksheet.write(row, 10, credit or '')
                    #     worksheet.write(row, 11, 0 or '')
                    #     worksheet.write(row, 12, debit or '')
                    #     worksheet.write(row, 13, 0 or '')
                    #     worksheet.write(row, 14, ((credit) - (debit)) or '')
                    #     worksheet.write(row, 15, data.move_id.user_id.name or '')
                    # elif data.move_id.type == 'in_refund' and data.account_internal_type != 'payable' and not data.tax_line_id:
                    #     row += 1
                    #     print('44444444444444', data.move_id, 'data.move_id', data.payment_id, 'data.payment_id',
                    #           data.move_id.type,
                    #           'data.move_id.type', data.account_internal_type, 'data.account_internal_type')
                    #     tax_amount = 0
                    #     bla = data.search(
                    #         [('move_id.name', '=', data.move_id.name), ('account_id.name', '=', data.account_id.name)])
                    #     credit = 0
                    #     debit = 0
                    #     for b in bla:
                    #         credit += b.credit
                    #         debit += b.debit
                    #     ctax_amount = 0
                    #     dtax_amount = 0
                    #     if data.tax_ids:
                    #         for tax in data.tax_ids:
                    #             tt = data.search(
                    #                 [('move_id.name', '=', data.move_id.name), ('tax_line_id', '=', tax.id)])[0]
                    #             for t in tt:
                    #                 ctax_amount += tt.credit
                    #                 dtax_amount += tt.debit
                    #     date = data.date
                    #     worksheet.write(row, 0, date, date_format or '')
                    #     worksheet.write(row, 1, data.date.strftime("%B") or '')
                    #     worksheet.write(row, 2, data.move_id.name or '')
                    #     worksheet.write(row, 3, 'Debit Note')
                    #     worksheet.write(row, 4, data.partner_id.name or '')
                    #     worksheet.write(row, 5, data.move_id.ref or '')
                    #     worksheet.write(row, 6, data.move_id.operation_id.name or '')
                    #     # worksheet.write(row, 7, data.move_id.shipment_no or '')
                    #     worksheet.write(row, 8, data.account_id.name or '')
                    #     worksheet.write(row, 9, data.move_id.operation_id.x_job_type.name or '')
                    #     worksheet.write(row, 10, credit or '')
                    #     worksheet.write(row, 11, 0 or '')
                    #     worksheet.write(row, 12, debit or '')
                    #     worksheet.write(row, 13, 0 or '')
                    #     worksheet.write(row, 14, ((credit) - (debit)) or '')
                    #     worksheet.write(row, 15, data.move_id.user_id.name or '')
                    #                elif data.payment_id and data.account_internal_type != 'receivable' and not data.tax_line_id:
                    #                    print('555555555555555', data.move_id, 'data.move_id', data.payment_id, 'data.payment_id',
                    #                          data.move_id.type,
                    #                          'data.move_id.type', data.account_internal_type, 'data.account_internal_type')
                    #                    tax_amount = 0
                    #                    bla = data.search(
                    #                        [('move_id.name', '=', data.move_id.name), ('account_id.name', '=', data.account_id.name)])
                    #                    credit = 0
                    #                    debit = 0
                    #                    for b in bla:
                    #                        credit += data.credit
                    #                        debit += data.debit
                    #                    if data.tax_ids:
                    #                        for tax in data.tax_ids:
                    #                            tax_amount += tax.amount
                    #                    date = data.date
                    #     worksheet.write(row, 0, date, date_format)
                    #                    worksheet.write(row, 1, data.date.strftime("%B"))
                    #                    worksheet.write(row, 2, data.move_id.name)
                    #                    worksheet.write(row, 3, 'Payment')
                    #                    worksheet.write(row, 4, data.partner_id.name)
                    #                    worksheet.write(row, 5, data.move_id.ref)
                    #                    worksheet.write(row, 6, data.move_id.operation_id.name)
                    #                    # worksheet.write(row, 7, data.move_id.shipment_no)
                    #                    worksheet.write(row, 8, data.account_id.name)
                    #                    worksheet.write(row, 9, data.move_id.operation_id.x_job_type.name)
                    #                    worksheet.write(row, 10, credit + tax_amount)
                    #                    worksheet.write(row, 11, tax_amount)
                    #                    worksheet.write(row, 12, debit + tax_amount)
                    #                    worksheet.write(row, 13, tax_amount)
                    #                    worksheet.write(row, 14, ((credit + tax_amount) - (debit + tax_amount)))
                    #                    worksheet.write(row, 15, data.move_id.user_id.name)
                    #                elif data.payment_id and data.account_internal_type != 'payable' and not data.tax_line_id:
                    #                    print('66666666666666', data.move_id, 'data.move_id', data.payment_id, 'data.payment_id',
                    #                          data.move_id.type,
                    #                          'data.move_id.type', data.account_internal_type, 'data.account_internal_type')
                    #                    tax_amount = 0
                    #                    bla = data.search(
                    #                       [('move_id.name', '=', data.move_id.name), ('account_id.name', '=', data.account_id.name)])
                    #                    credit = 0
                    #                    debit = 0
                    #                    for b in bla:
                    #                        credit += data.credit
                    #                        debit += data.debit
                    #                    if data.tax_ids:
                    #                        for tax in data.tax_ids:
                    #                            tax_amount += tax.amount
                    #                    date = data.date
                    #     worksheet.write(row, 0, date, date_format)
                    #                    worksheet.write(row, 1, data.date.strftime("%B"))
                    #                    worksheet.write(row, 2, data.move_id.name)
                    #                    worksheet.write(row, 3, 'Receipt')
                    #                    worksheet.write(row, 4, data.partner_id.name)
                    #                    worksheet.write(row, 5, data.move_id.ref)
                    #                    worksheet.write(row, 6, data.move_id.operation_id.name)
                    #                    # worksheet.write(row, 7, data.move_id.shipment_no)
                    #                    worksheet.write(row, 8, data.account_id.name)
                    #                    worksheet.write(row, 9, data.move_id.operation_id.x_job_type.name)
                    #                    worksheet.write(row, 10, credit + tax_amount)
                    #                    worksheet.write(row, 11, tax_amount)
                    #                    worksheet.write(row, 12, debit + tax_amount)
                    #                    worksheet.write(row, 13, tax_amount)
                    #                    worksheet.write(row, 14, ((credit + tax_amount) - (debit + tax_amount)))
                    #                    worksheet.write(row, 15, data.move_id.user_id.name)
                    elif data.move_id.type == 'entry' and data.account_internal_type != 'receivable' and data.account_internal_type != 'payable' and not data.tax_line_id:
                        row += 1
                        print('11111111111111', data.move_id, 'data.move_id', data.payment_id, 'data.payment_id',
                              data.move_id.type,
                              'data.move_id.type', data.account_internal_type, 'data.account_internal_type')
                        tax_amount = 0
                        bla = data.search(
                            [('move_id.name', '=', data.move_id.name), ('account_id.name', '=', data.account_id.name)])
                        credit = 0
                        debit = 0
                        for b in bla:
                            credit += b.credit
                            debit += b.debit
                        ctax_amount = 0
                        dtax_amount = 0
                        if data.tax_ids:
                            for tax in data.tax_ids:
                                tt = []
                                ttt = data.search(
                                    [('move_id.name', '=', data.move_id.name), ('tax_line_id', '=', tax.id)])
                                if ttt:
                                    tt.append(ttt[0])
                                for t in tt:
                                    ctax_amount += t.credit
                                    dtax_amount += t.debit
                        date = data.date
                        worksheet.write(row, 0, date, date_format or '')
                        worksheet.write(row, 1, data.date.strftime("%B") or '')
                        worksheet.write(row, 2, data.move_id.name or '')
                        worksheet.write(row, 3, 'JV')
                        worksheet.write(row, 4, data.partner_id.name or '')
                        worksheet.write(row, 5, data.move_id.ref or '')
                        worksheet.write(row, 6, data.move_id.operation_id.name or '')
                        # worksheet.write(row, 7, data.move_id.shipment_no)
                        worksheet.write(row, 8, data.account_id.name or '')
                        worksheet.write(row, 9, data.move_id.operation_id.x_job_type.name or '')
                        worksheet.write(row, 10, credit or '')
                        worksheet.write(row, 11, 0 or '')
                        worksheet.write(row, 12, debit or '')
                        worksheet.write(row, 13, 0 or '')
                        worksheet.write(row, 14, ((credit) - (debit)) or '')
                        worksheet.write(row, 15, data.move_id.user_id.name or '')

                a = str(data.move_id.name) + str(data.account_id.name)
                list.append(a)
            # Save the XL file
            file_data = io.BytesIO()
            workbook.save(file_data)
            file_data.seek(0)

            # Prepare the file for download
            file_name = 'sales_report.xls'
            file_size = len(file_data.getvalue())
            self.write({
                'state': 'get',
                'data': base64.encodebytes(file_data.getvalue()),
                'name': file_name
            })

            return {
                'name': 'Sales Report',
                'type': 'ir.actions.act_url',
                'url': f"/web/content/{self.id}?model=sales.xl.report&field=data&download=true&filename={file_name}",
                'target': 'self'
            }
        else:
            if self.invoice_no and not self.partner_id and not self.department:
                sales_data = self.env['account.move.line'].search([('move_id', 'in', self.invoice_no.ids)])
            elif not self.invoice_no and self.partner_id and not self.department:
                sales_data = self.env['account.move.line'].search([('partner_id', 'in', self.partner_id.ids)])
            elif not self.invoice_no and not self.partner_id and self.department:
                sales_data = self.env['account.move.line'].search([('partner_id', 'in', self.partner_id.ids)])
            elif self.invoice_no and self.partner_id and not self.department:
                sales_data = self.env['account.move.line'].search(
                    [('partner_id', 'in', self.partner_id.ids), ('move_id', 'in', self.invoice_no.ids)])
            elif self.invoice_no and not self.partner_id and self.department:
                sales_data = self.env['account.move.line'].search(
                    [('move_id.operation_id.x_job_type', 'in', self.department.ids),
                     ('move_id', 'in', self.invoice_no.ids)])
            elif not self.invoice_no and self.partner_id and self.department:
                sales_data = self.env['account.move.line'].search(
                    [('move_id.operation_id.x_job_type', 'in', self.department.ids),
                     ('partner_id', 'in', self.partner_id.ids)])
            elif not self.invoice_no and self.partner_id and self.department:
                sales_data = self.env['account.move.line'].search(
                    [('move_id.operation_id.x_job_type', 'in', self.department.ids),
                     ('partner_id', 'in', self.partner_id.ids), ('move_id', 'in', self.invoice_no.ids)])
            else:
                sales_data = self.env['account.move.line'].search([])
            print(sales_data, 'sales_data')

            # Get the payment data
            payment_data = self.env['account.payment'].search([
                ('payment_type', 'in', ['inbound', 'outbound']),
                ('state', '=', 'posted')
            ])

            # Create the XL workbook and worksheet
            workbook = xlwt.Workbook(encoding='utf-8')
            worksheet = workbook.add_sheet('Sales Report')
            date_format = xlwt.XFStyle()
            date_format.num_format_str = 'yyyy-mm-dd'

            # Write the headers
            default_widths = [
                ('GL Date', 4000), ('Month', 3000), ('Voucher No.', 4000), ('Voucher Type', 4000),
                ('Party', 6000), ('Ref. No.', 5000), ('Job No', 4000), ('Shipment No.', 4000),
                ('COA/AC Name', 6000), ('Department', 4000), ('Sale Amount (OMR)', 5000),
                ('Sales with Vat', 5000), ('Cost Amount (OMR)', 5000), ('Cost with Vat', 5000),
                ('GP', 4000), ('Salesperson', 5000)
            ]

            for index, (header, width) in enumerate(default_widths):
                worksheet.col(index).width = width
                worksheet.write(0, index, header)
            list = []
            row = 0
            # Write the sales data
            for roww, data in enumerate(sales_data):
                name = data.move_id.name
                account = data.account_id.name
                b = str(name) + str(account)
                if b in list:
                    continue
                else:
                    # print(data.move_id, 'data.move_id', data.payment_id, 'data.payment_id', data.move_id.type,
                    #       'data.move_id.type', data.account_internal_type, 'data.account_internal_type')
                    # print(data.move_id.type,'data.move_id.type', data.account_internal_type, 'data.account_internal_type', '...............')
                    print(data.tax_ids, 'data.tax_ids', data.move_id.type, 'data.move_id.type',
                          data.account_internal_type,
                          'data.account_internal_type')
                    if data.move_id.type == 'out_invoice' and data.account_internal_type != 'receivable' and not data.tax_line_id:
                        row += 1
                        print('11111111111111', data.move_id, 'data.move_id', data.payment_id, 'data.payment_id',
                              data.move_id.type,
                              'data.move_id.type', data.account_internal_type, 'data.account_internal_type')
                        sales = 0
                        cost = 0

                        ctax_amount = 0
                        dtax_amount = 0
                        bla = data.search(
                            [('move_id.name', '=', data.move_id.name), ('account_id.name', '=', data.account_id.name)])
                        credit = 0
                        debit = 0
                        for b in bla:
                            credit += b.credit
                            debit += b.debit

                        if data.tax_ids:
                            for tax in data.tax_ids:
                                tt = []
                                ttt = data.search(
                                    [('move_id.name', '=', data.move_id.name), ('tax_line_id', '=', tax.id)])
                                if ttt:
                                    tt.append(ttt[0])
                                for t in tt:
                                    ctax_amount += t.credit
                                    dtax_amount += t.debit
                        date = data.date
                        worksheet.write(row, 0, date, date_format or '')
                        worksheet.write(row, 1, data.date.strftime("%B") or '')
                        worksheet.write(row, 2, data.move_id.name or '')
                        worksheet.write(row, 3, 'Invoice')
                        worksheet.write(row, 4, data.partner_id.name or '')
                        worksheet.write(row, 5, data.move_id.ref or '')
                        worksheet.write(row, 6, data.move_id.operation_id.name or '')
                        # worksheet.write(row, 7, data.move_id.shipment_no or '')
                        worksheet.write(row, 8, data.account_id.name or '')
                        worksheet.write(row, 9, data.move_id.operation_id.x_job_type.name or '')
                        worksheet.write(row, 10, credit + ctax_amount or '')
                        worksheet.write(row, 11, ctax_amount or '')
                        worksheet.write(row, 12, debit + dtax_amount or '')
                        worksheet.write(row, 13, dtax_amount or '')
                        worksheet.write(row, 14, ((credit + ctax_amount) - (debit + dtax_amount)) or '')
                        worksheet.write(row, 15, data.move_id.user_id.name or '')
                    elif data.move_id.type == 'out_refund' and data.account_internal_type != 'receivable' and not data.tax_line_id:
                        row += 1
                        print('2222222222', data.move_id, 'data.move_id', data.payment_id, 'data.payment_id',
                              data.move_id.type,
                              'data.move_id.type', data.account_internal_type, 'data.account_internal_type')
                        ctax_amount = 0
                        dtax_amount = 0
                        bla = data.search(
                            [('move_id.name', '=', data.move_id.name), ('account_id.name', '=', data.account_id.name)])
                        credit = 0
                        debit = 0
                        for b in bla:
                            credit += b.credit
                            debit += b.debit

                        if data.tax_ids:
                            for tax in data.tax_ids:
                                tt = []
                                ttt = data.search(
                                    [('move_id.name', '=', data.move_id.name), ('tax_line_id', '=', tax.id)])
                                if ttt:
                                    tt.append(ttt[0])
                                for t in tt:
                                    ctax_amount += t.credit
                                    dtax_amount += t.debit
                        date = data.date
                        worksheet.write(row, 0, date, date_format or '')
                        worksheet.write(row, 1, data.date.strftime("%B") or '')
                        worksheet.write(row, 2, data.move_id.name or '')
                        worksheet.write(row, 3, 'Credit Note')
                        worksheet.write(row, 4, data.partner_id.name or '')
                        worksheet.write(row, 5, data.move_id.ref or '')
                        worksheet.write(row, 6, data.move_id.operation_id.name or '')
                        # worksheet.write(row, 7, data.move_id.shipment_no)
                        worksheet.write(row, 8, data.account_id.name or '')
                        worksheet.write(row, 9, data.move_id.operation_id.x_job_type.name or '')
                        worksheet.write(row, 10, credit + ctax_amount or '')
                        worksheet.write(row, 11, ctax_amount or '')
                        worksheet.write(row, 12, debit + dtax_amount or '')
                        worksheet.write(row, 13, dtax_amount or '')
                        worksheet.write(row, 14, ((credit + ctax_amount) - (debit + dtax_amount)) or '')
                        worksheet.write(row, 15, data.move_id.user_id.name or '')
                    # elif data.move_id.type == 'in_invoice' and data.account_internal_type != 'payable' and not data.tax_line_id:
                    #     row += 1
                    #     print('33333333333', data.move_id, 'data.move_id', data.payment_id, 'data.payment_id',
                    #           data.move_id.type,
                    #           'data.move_id.type', data.account_internal_type, 'data.account_internal_type')
                    #     ctax_amount = 0
                    #     dtax_amount = 0
                    #     bla = data.search(
                    #         [('move_id.name', '=', data.move_id.name), ('account_id.name', '=', data.account_id.name)])
                    #     credit = 0
                    #     debit = 0
                    #     for b in bla:
                    #         credit += b.credit
                    #         debit += b.debit
                    #
                    #     if data.tax_ids:
                    #         for tax in data.tax_ids:
                    #             tt = data.search(
                    #                 [('move_id.name', '=', data.move_id.name), ('tax_line_id', '=', tax.id)])[0]
                    #             for t in tt:
                    #                 ctax_amount += tt.credit
                    #                 dtax_amount += tt.debit
                    #     date = data.date
                    #     worksheet.write(row, 0, date, date_format or '')
                    #     worksheet.write(row, 1, data.date.strftime("%B") or '')
                    #     worksheet.write(row, 2, data.move_id.name or '')
                    #     worksheet.write(row, 3, 'Bill')
                    #     worksheet.write(row, 4, data.partner_id.name or '')
                    #     worksheet.write(row, 5, data.move_id.ref or '')
                    #     worksheet.write(row, 6, data.move_id.operation_id.name or '')
                    #     # worksheet.write(row, 7, data.move_id.shipment_no or '')
                    #     worksheet.write(row, 8, data.account_id.name or '')
                    #     worksheet.write(row, 9, data.move_id.operation_id.x_job_type.name or '')
                    #     worksheet.write(row, 10, credit + ctax_amount or '')
                    #     worksheet.write(row, 11, ctax_amount or '')
                    #     worksheet.write(row, 12, debit + dtax_amount or '')
                    #     worksheet.write(row, 13, dtax_amount or '')
                    #     worksheet.write(row, 14, ((credit + ctax_amount) - (debit + dtax_amount)) or '')
                    #     worksheet.write(row, 15, data.move_id.user_id.name or '')
                    # elif data.move_id.type == 'in_refund' and data.account_internal_type != 'payable' and not data.tax_line_id:
                    #     row += 1
                    #     print('44444444444444', data.move_id, 'data.move_id', data.payment_id, 'data.payment_id',
                    #           data.move_id.type,
                    #           'data.move_id.type', data.account_internal_type, 'data.account_internal_type')
                    #     ctax_amount = 0
                    #     dtax_amount = 0
                    #     bla = data.search(
                    #         [('move_id.name', '=', data.move_id.name), ('account_id.name', '=', data.account_id.name)])
                    #     credit = 0
                    #     debit = 0
                    #     for b in bla:
                    #         credit += b.credit
                    #         debit += b.debit
                    #
                    #     if data.tax_ids:
                    #         for tax in data.tax_ids:
                    #             tt = data.search(
                    #                 [('move_id.name', '=', data.move_id.name), ('tax_line_id', '=', tax.id)])[0]
                    #             for t in tt:
                    #                 ctax_amount += tt.credit
                    #                 dtax_amount += tt.debit
                    #     date = data.date
                    #     worksheet.write(row, 0, date, date_format or '')
                    #     worksheet.write(row, 1, data.date.strftime("%B") or '')
                    #     worksheet.write(row, 2, data.move_id.name or '')
                    #     worksheet.write(row, 3, 'Credit Note')
                    #     worksheet.write(row, 4, data.partner_id.name or '')
                    #     worksheet.write(row, 5, data.move_id.ref or '')
                    #     worksheet.write(row, 6, data.move_id.operation_id.name or '')
                    #     # worksheet.write(row, 7, data.move_id.shipment_no or '')
                    #     worksheet.write(row, 8, data.account_id.name or '')
                    #     worksheet.write(row, 9, data.move_id.operation_id.x_job_type.name or '')
                    #     worksheet.write(row, 10, credit + ctax_amount or '')
                    #     worksheet.write(row, 11, ctax_amount or '')
                    #     worksheet.write(row, 12, debit + dtax_amount or '')
                    #     worksheet.write(row, 13, dtax_amount or '')
                    #     worksheet.write(row, 14, ((credit + ctax_amount) - (debit + dtax_amount)) or '')
                    #     worksheet.write(row, 15, data.move_id.user_id.name or '')
                    #                elif data.payment_id and data.account_internal_type != 'receivable' and not data.tax_line_id:
                    #                    print('555555555555555', data.move_id, 'data.move_id', data.payment_id, 'data.payment_id',
                    #                          data.move_id.type,
                    #                          'data.move_id.type', data.account_internal_type, 'data.account_internal_type')
                    #                    tax_amount = 0
                    #                    bla = data.search(
                    #                        [('move_id.name', '=', data.move_id.name), ('account_id.name', '=', data.account_id.name)])
                    #                    credit = 0
                    #                    debit = 0
                    #                    for b in bla:
                    #                        credit += data.credit
                    #                        debit += data.debit
                    #                    if data.tax_ids:
                    #                        for tax in data.tax_ids:
                    #                            tax_amount += tax.amount
                    #                    date = data.date
                    #     worksheet.write(row, 0, date, date_format)
                    #                    worksheet.write(row, 1, data.date.strftime("%B"))
                    #                    worksheet.write(row, 2, data.move_id.name)
                    #                    worksheet.write(row, 3, 'Payment')
                    #                    worksheet.write(row, 4, data.partner_id.name)
                    #                    worksheet.write(row, 5, data.move_id.ref)
                    #                    worksheet.write(row, 6, data.move_id.operation_id.name)
                    #                    # worksheet.write(row, 7, data.move_id.shipment_no)
                    #                    worksheet.write(row, 8, data.account_id.name)
                    #                    worksheet.write(row, 9, data.move_id.operation_id.x_job_type.name)
                    #                    worksheet.write(row, 10, credit + tax_amount)
                    #                    worksheet.write(row, 11, tax_amount)
                    #                    worksheet.write(row, 12, debit + tax_amount)
                    #                    worksheet.write(row, 13, tax_amount)
                    #                    worksheet.write(row, 14, ((credit + tax_amount) - (debit + tax_amount)))
                    #                    worksheet.write(row, 15, data.move_id.user_id.name)
                    #                elif data.payment_id and data.account_internal_type != 'payable' and not data.tax_line_id:
                    #                    print('66666666666666', data.move_id, 'data.move_id', data.payment_id, 'data.payment_id',
                    #                          data.move_id.type,
                    #                          'data.move_id.type', data.account_internal_type, 'data.account_internal_type')
                    #                    tax_amount = 0
                    #                    bla = data.search(
                    #                       [('move_id.name', '=', data.move_id.name), ('account_id.name', '=', data.account_id.name)])
                    #                    credit = 0
                    #                    debit = 0
                    #                    for b in bla:
                    #                        credit += data.credit
                    #                        debit += data.debit
                    #                    if data.tax_ids:
                    #                        for tax in data.tax_ids:
                    #                            tax_amount += tax.amount
                    #                    date = data.date
                    #     worksheet.write(row, 0, date, date_format)
                    #                    worksheet.write(row, 1, data.date.strftime("%B"))
                    #                    worksheet.write(row, 2, data.move_id.name)
                    #                    worksheet.write(row, 3, 'Receipt')
                    #                    worksheet.write(row, 4, data.partner_id.name)
                    #                    worksheet.write(row, 5, data.move_id.ref)
                    #                    worksheet.write(row, 6, data.move_id.operation_id.name)
                    #                    # worksheet.write(row, 7, data.move_id.shipment_no)
                    #                    worksheet.write(row, 8, data.account_id.name)
                    #                    worksheet.write(row, 9, data.move_id.operation_id.x_job_type.name)
                    #                    worksheet.write(row, 10, credit + tax_amount)
                    #                    worksheet.write(row, 11, tax_amount)
                    #                    worksheet.write(row, 12, debit + tax_amount)
                    #                    worksheet.write(row, 13, tax_amount)
                    #                    worksheet.write(row, 14, ((credit + tax_amount) - (debit + tax_amount)))
                    #                    worksheet.write(row, 15, data.move_id.user_id.name)
                    elif data.move_id.type == 'entry' and data.account_internal_type != 'receivable' and data.account_internal_type != 'payable' and not data.tax_line_id:
                        row += 1
                        print('11111111111111', data.move_id, 'data.move_id', data.payment_id, 'data.payment_id',
                              data.move_id.type,
                              'data.move_id.type', data.account_internal_type, 'data.account_internal_type')
                        ctax_amount = 0
                        dtax_amount = 0
                        bla = data.search(
                            [('move_id.name', '=', data.move_id.name), ('account_id.name', '=', data.account_id.name)])
                        credit = 0
                        debit = 0
                        for b in bla:
                            credit += b.credit
                            debit += b.debit

                        if data.tax_ids:
                            for tax in data.tax_ids:
                                tt = []
                                ttt = data.search(
                                    [('move_id.name', '=', data.move_id.name), ('tax_line_id', '=', tax.id)])
                                if ttt:
                                    tt.append(ttt[0])
                                for t in tt:
                                    ctax_amount += t.credit
                                    dtax_amount += t.debit
                        date = data.date
                        worksheet.write(row, 0, date, date_format or '')
                        worksheet.write(row, 1, data.date.strftime("%B") or '')
                        worksheet.write(row, 2, data.move_id.name or '')
                        worksheet.write(row, 3, 'JV')
                        worksheet.write(row, 4, data.partner_id.name or '')
                        worksheet.write(row, 5, data.move_id.ref or '')
                        worksheet.write(row, 6, data.move_id.operation_id.name or '')
                        # worksheet.write(row, 7, data.move_id.shipment_no or '')
                        worksheet.write(row, 8, data.account_id.name or '')
                        worksheet.write(row, 9, data.move_id.operation_id.x_job_type.name or '')
                        worksheet.write(row, 10, credit + ctax_amount or '')
                        worksheet.write(row, 11, ctax_amount or '')
                        worksheet.write(row, 12, debit + dtax_amount or '')
                        worksheet.write(row, 13, dtax_amount or '')
                        worksheet.write(row, 14, ((credit + ctax_amount) - (debit + dtax_amount)) or '')
                        worksheet.write(row, 15, data.move_id.user_id.name or '')

                a = str(data.move_id.name) + str(data.account_id.name)
                list.append(a)
            # Save the XL file
            file_data = io.BytesIO()
            workbook.save(file_data)
            file_data.seek(0)

            # Prepare the file for download
            file_name = 'sales_report.xls'
            file_size = len(file_data.getvalue())
            self.write({
                'state': 'get',
                'data': base64.encodebytes(file_data.getvalue()),
                'name': file_name
            })

            return {
                'name': 'Sales Report',
                'type': 'ir.actions.act_url',
                'url': f"/web/content/{self.id}?model=sales.xl.report&field=data&download=true&filename={file_name}",
                'target': 'self'
            }




        # # Save the XL file
        # file_data = io.BytesIO()
        # workbook.save(file_data)
        # file_data.seek(0)
        #
        # # Prepare the file for download
        # file_name = 'sales_report.xls'
        # file_size = len(file_data.getvalue())
        #
        # return {
        #     'name': 'Sales Report',
        #     'type': 'ir.actions.act_url',
        #     'url': '/web/content/{0}?download=true'.format(self.id),
        #     'target': 'self',
        # }

        # Create the file download response
        # response = {
        #     'name': file_name,
        #     'type': 'binary',
        #     'data': base64.b64encode(file_data.getvalue()),
        #     'file_size': file_size,
        #     'file_type': 'application/vnd.ms-excel'
        # }
        # return response

    # @api.model
    # def generate_report(self):
    #     # Get the sales data
    #     # sales_data = self.env['account.move.line'].search([
    #     #     ('move_id.type', 'in', ['out_invoice', 'in_invoice', 'out_refund', 'in_refund']),
    #     #     ('move_id.state', '=', 'posted')
    #     # ])
    #     sales_data = self.env['account.move.line'].search([])
    #
    #     # Get the payment data
    #     payment_data = self.env['account.payment'].search([
    #         ('payment_type', 'in', ['inbound', 'outbound']),
    #         ('state', '=', 'posted')
    #     ])
    #
    #     # Get the receipt data
    #     # receipt_data = self.env['account.bank.statement.line'].search([
    #     #     ('payment_id', '!=', False),
    #     #     ('statement_id.journal_id.type', '=', 'bank'),
    #     #     ('state', '=', 'posted')
    #     # ])
    #
    #     # Create the XL workbook and worksheet
    #     workbook = xlwt.Workbook(encoding='utf-8')
    #     worksheet = workbook.add_sheet('Sales Report')
    #
    #     # Write the headers
    #     headers = [
    #         'GL Date', 'strftime("%B")', 'Voucher No.', 'Voucher Type', 'Party', 'Ref. No.', 'Job No',
    #         'Shipment No.', 'COA/AC Name', 'Department', 'Sale Amount (OMR)', 'Sales with Vat',
    #         'Cost Amount (OMR)', 'Cost with Vat', 'GP', 'Salesperson'
    #     ]
    #
    #     for index, header in enumerate(headers):
    #         worksheet.write(0, index, header)
    #
    #     # Write the sales data
    #     for row, data in enumerate(sales_data, start=1):
    #         # print(data.move_id, 'data.move_id', data.payment_id, 'data.payment_id', data.move_id.type,
    #         #       'data.move_id.type', data.account_internal_type, 'data.account_internal_type')
    #         # print(data.move_id.type,'data.move_id.type', data.account_internal_type, 'data.account_internal_type', '...............')
    #         if data.move_id.type == 'out_invoice' and data.account_internal_type == 'receivable':
    #             print('11111111111111',data.move_id, 'data.move_id', data.payment_id, 'data.payment_id', data.move_id.type,
    #                   'data.move_id.type', data.account_internal_type, 'data.account_internal_type')
    #             date = data.date
    #             worksheet.write(row, 0, date, date_format)
    #             worksheet.write(row, 1, data.date.strftime("%B"))
    #             worksheet.write(row, 2, data.move_id.name)
    #             worksheet.write(row, 3, 'Invoice')
    #             worksheet.write(row, 4, data.partner_id.name)
    #             worksheet.write(row, 5, data.move_id.ref)
    #             # worksheet.write(row, 6, data.move_id.job_no)
    #             # worksheet.write(row, 7, data.move_id.shipment_no)
    #             # worksheet.write(row, 8, data.move_id.coa_ac_name)
    #             worksheet.write(row, 9, data.move_id.operation_id.x_job_type.name)
    #             # worksheet.write(row, 10, data.move_id.sale_amount)
    #             # worksheet.write(row, 11, data.move_id.sale_amount_with_vat)
    #             # worksheet.write(row, 12, data.move_id.cost_amount)
    #             # worksheet.write(row, 13, data.move_id.cost_amount_with_vat)
    #             # worksheet.write(row, 14, data.move_id.gross_profit)
    #             # worksheet.write(row, 15, data.move_id.salesperson)
    #         elif data.move_id.type == 'out_refund' and data.account_internal_type == 'receivable':
    #             print('2222222222', data.move_id, 'data.move_id', data.payment_id, 'data.payment_id', data.move_id.type,
    #                   'data.move_id.type', data.account_internal_type, 'data.account_internal_type')
    #             date = data.date
    #             worksheet.write(row, 0, date, date_format)
    #             worksheet.write(row, 1, data.date.strftime("%B"))
    #             worksheet.write(row, 2, data.move_id.name)
    #             worksheet.write(row, 3, 'Invoice')
    #             worksheet.write(row, 4, data.partner_id.name)
    #             worksheet.write(row, 5, data.move_id.ref)
    #             # worksheet.write(row, 6, data.move_id.job_no)
    #             # worksheet.write(row, 7, data.move_id.shipment_no)
    #             # worksheet.write(row, 8, data.move_id.coa_ac_name)
    #             worksheet.write(row, 9, data.move_id.operation_id.x_job_type.name)
    #             # worksheet.write(row, 10, data.move_id.sale_amount)
    #             # worksheet.write(row, 11, data.move_id.sale_amount_with_vat)
    #             # worksheet.write(row, 12, data.move_id.cost_amount)
    #             # worksheet.write(row, 13, data.move_id.cost_amount_with_vat)
    #             # worksheet.write(row, 14, data.move_id.gross_profit)
    #             # worksheet.write(row, 15, data.move_id.salesperson)
    #         elif data.move_id.type == 'in_invoice' and data.account_internal_type == 'payable':
    #             print('33333333333',data.move_id, 'data.move_id', data.payment_id, 'data.payment_id', data.move_id.type,
    #                   'data.move_id.type', data.account_internal_type, 'data.account_internal_type')
    #             date = data.date
    #             worksheet.write(row, 0, date, date_format)
    #             worksheet.write(row, 1, data.date.strftime("%B"))
    #             worksheet.write(row, 2, data.move_id.name)
    #             worksheet.write(row, 3, 'Bill')
    #             worksheet.write(row, 4, data.partner_id.name)
    #             worksheet.write(row, 5, data.move_id.ref)
    #             # worksheet.write(row, 6, data.move_id.job_no)
    #             # worksheet.write(row, 7, data.move_id.shipment_no)
    #             # worksheet.write(row, 8, data.move_id.coa_ac_name)
    #             worksheet.write(row, 9, data.move_id.operation_id.x_job_type.name)
    #             # worksheet.write(row, 10, data.move_id.sale_amount)
    #             # worksheet.write(row, 11, data.move_id.sale_amount_with_vat)
    #             # worksheet.write(row, 12, data.move_id.cost_amount)
    #             # worksheet.write(row, 13, data.move_id.cost_amount_with_vat)
    #             # worksheet.write(row, 14, data.move_id.gross_profit)
    #             # worksheet.write(row, 15, data.move_id.salesperson)
    #         elif data.move_id.type == 'in_refund' and data.account_internal_type == 'payable':
    #             print('44444444444444',data.move_id, 'data.move_id', data.payment_id, 'data.payment_id', data.move_id.type,
    #                   'data.move_id.type', data.account_internal_type, 'data.account_internal_type')
    #             date = data.date
    #             worksheet.write(row, 0, date, date_format)
    #             worksheet.write(row, 1, data.date.strftime("%B"))
    #             worksheet.write(row, 2, data.move_id.name)
    #             worksheet.write(row, 3, 'Bill')
    #             worksheet.write(row, 4, data.partner_id.name)
    #             worksheet.write(row, 5, data.move_id.ref)
    #             # worksheet.write(row, 6, data.move_id.job_no)
    #             # worksheet.write(row, 7, data.move_id.shipment_no)
    #             # worksheet.write(row, 8, data.move_id.coa_ac_name)
    #             worksheet.write(row, 9, data.move_id.operation_id.x_job_type.name)
    #             # worksheet.write(row, 10, data.move_id.sale_amount)
    #             # worksheet.write(row, 11, data.move_id.sale_amount_with_vat)
    #             # worksheet.write(row, 12, data.move_id.cost_amount)
    #             # worksheet.write(row, 13, data.move_id.cost_amount_with_vat)
    #             # worksheet.write(row, 14, data.move_id.gross_profit)
    #             # worksheet.write(row, 15, data.move_id.salesperson)
    #         elif data.payment_id and data.account_internal_type == 'receivable':
    #             print('555555555555555',data.move_id, 'data.move_id', data.payment_id, 'data.payment_id', data.move_id.type,
    #                   'data.move_id.type', data.account_internal_type, 'data.account_internal_type')
    #             date = data.date
    #             worksheet.write(row, 0, date, date_format)
    #             worksheet.write(row, 1, data.date.strftime("%B"))
    #             worksheet.write(row, 2, data.move_id.name)
    #             worksheet.write(row, 3, 'payment')
    #             worksheet.write(row, 4, data.partner_id.name)
    #             worksheet.write(row, 5, data.move_id.ref)
    #             # worksheet.write(row, 6, data.move_id.job_no)
    #             # worksheet.write(row, 7, data.move_id.shipment_no)
    #             # worksheet.write(row, 8, data.move_id.coa_ac_name)
    #             worksheet.write(row, 9, data.move_id.operation_id.x_job_type.name)
    #             # worksheet.write(row, 10, data.move_id.sale_amount)
    #             # worksheet.write(row, 11, data.move_id.sale_amount_with_vat)
    #             # worksheet.write(row, 12, data.move_id.cost_amount)
    #             # worksheet.write(row, 13, data.move_id.cost_amount_with_vat)
    #             # worksheet.write(row, 14, data.move_id.gross_profit)
    #             # worksheet.write(row, 15, data.move_id.salesperson)
    #         elif data.payment_id and data.account_internal_type == 'payable':
    #             print('66666666666666',data.move_id, 'data.move_id', data.payment_id, 'data.payment_id', data.move_id.type,
    #                   'data.move_id.type', data.account_internal_type, 'data.account_internal_type')
    #             date = data.date
    #             worksheet.write(row, 0, date, date_format)
    #             worksheet.write(row, 1, data.date.strftime("%B"))
    #             worksheet.write(row, 2, data.move_id.name)
    #             worksheet.write(row, 3, 'Receipt')
    #             worksheet.write(row, 4, data.partner_id.name)
    #             worksheet.write(row, 5, data.move_id.ref)
    #             # worksheet.write(row, 6, data.move_id.job_no)
    #             # worksheet.write(row, 7, data.move_id.shipment_no)
    #             # worksheet.write(row, 8, data.move_id.coa_ac_name)
    #             worksheet.write(row, 9, data.move_id.operation_id.x_job_type.name)
    #             # worksheet.write(row, 10, data.move_id.sale_amount)
    #             # worksheet.write(row, 11, data.move_id.sale_amount_with_vat)
    #             # worksheet.write(row, 12, data.move_id.cost_amount)
    #             # worksheet.write(row, 13, data.move_id.cost_amount_with_vat)
    #             # worksheet.write(row, 14, data.move_id.gross_profit)
    #             # worksheet.write(row, 15, data.move_id.salesperson)
    #
    #
    #
    #     # Write the payment data
    #     for row, data in enumerate(payment_data, start=len(sales_data) + 1):
    #         worksheet.write(row, 0, data.payment_date)
    #         worksheet.write(row, 1, data.payment_date.strftime("%B"))
    #         worksheet.write(row, 2, data.name)
    #         worksheet.write(row, 3, 'Payment')
    #         worksheet.write(row, 4, data.partner_id.name)
    #         worksheet.write(row, 5, '')
    #         worksheet.write(row, 6, '')
    #         worksheet.write(row, 7, '')
    #         worksheet.write(row, 8, '')
    #         worksheet.write(row, 9, '')
    #         worksheet.write(row, 10, data.amount)
    #         worksheet.write(row, 11, '')
    #         worksheet.write(row, 12, '')
    #         worksheet.write(row, 13, '')
    #         worksheet.write(row, 14, '')
    #         worksheet.write(row, 15, '')
    #
    #     # Write the receipt data
    #     # for row, data in enumerate(receipt_data, start=len(sales_data) + len(payment_data) + 1):
    #     #     date = data.date
    #           worksheet.write(row, 0, date, date_format)
    #     #     worksheet.write(row, 1, data.date.strftime("%B"))
    #     #     worksheet.write(row, 2, data.name)
    #     #     worksheet.write(row, 3, 'Receipt')
    #     #     worksheet.write(row, 4, data.partner_id.name)
    #     #     worksheet.write(row, 5, '')
    #     #     worksheet.write(row, 6, '')
    #     #     worksheet.write(row, 7, '')
    #     #     worksheet.write(row, 8, '')
    #     #     worksheet.write(row, 9, '')
    #     #     worksheet.write(row, 10, '')
    #     #     worksheet.write(row, 11, '')
    #     #     worksheet.write(row, 12, '')
    #     #     worksheet.write(row, 13, '')
    #     #     worksheet.write(row, 14, '')
    #     #     worksheet.write(row, 15, '')
    #
    #     # Save the XL file
    #     file_data = io.BytesIO()
    #     workbook.save(file_data)
    #     self.write({
    #         'state': 'get',
    #         'data': base64.encodestring(file_data.getvalue()),
    #         'name': 'sales_report.xls'
    #     })
    #     return {
    #         'name': 'Sales Report',
    #         'type': 'ir.actions.act_window',
    #         'res_model': 'sales.xl.report',
    #         'view_mode': 'form',
    #         'res_id': self.id,
    #         'target': 'new'
    #     }
