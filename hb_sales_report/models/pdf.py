import io
from odoo import api, models, fields, _
import base64
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, landscape
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
import logging

_logger = logging.getLogger(__name__)


class SalesXLReportextend(models.TransientModel):
    _inherit = 'sales.xl.report'

    def generate_pdf(self):
        buffer = io.BytesIO()
        page_width = 20 * inch  # Set the width to 11 inches
        page_height = 10 * inch  # Set the height to 8.5 inches
        page_size = (page_width, page_height)
        doc = SimpleDocTemplate(buffer, pagesize=page_size)
        doc.pagesize = landscape(doc.pagesize)  # Set landscape orientation
        styles = getSampleStyleSheet()

        # page_width = 8.5 * inch  # Set the width to 8.5 inches
        # page_height = 11 * inch  # Set the height to 11 inches
        # page_size = (page_width, page_height)
        # doc = SimpleDocTemplate(buffer, pagesize=landscape(letter))
        # # doc = SimpleDocTemplate(buffer, pagesize=page_size)
        # styles = getSampleStyleSheet()
        column_widths = [0.8 * inch, 0.8 * inch, 1.2 * inch, 1.2 * inch, 1.5 * inch, 1.2 * inch, 1.2 * inch,
                             1.2 * inch,
                             1.5 * inch, 1.2 * inch, 1.2 * inch, 1.2 * inch, 1.2 * inch, 1.2 * inch, 0.8 * inch,
                             1.2 * inch]

        # Define table headers and data
        table_data = [
            ['GL Date', 'Month', 'Voucher No.', 'Voucher Type', 'Party', 'Ref. No.', 'Job No', 'Shipment No.',
             'COA/AC Name', 'Department', 'Sale Amount (OMR)', 'Sales with Vat', 'Cost Amount (OMR)', 'Cost with Vat',
             'GP', 'Salesperson']
        ]
        # Get the sales data
        if self.include_vat != True:
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


            # Write the headers
            default_widths = [
                ('GL Date', 4000), ('Month', 3000), ('Voucher No.', 4000), ('Voucher Type', 4000),
                ('Party', 6000), ('Ref. No.', 5000), ('Job No', 4000), ('Shipment No.', 4000),
                ('COA/AC Name', 6000), ('Department', 4000), ('Sale Amount (OMR)', 5000),
                ('Sales with Vat', 5000), ('Cost Amount (OMR)', 5000), ('Cost with Vat', 5000),
                ('GP', 4000), ('Salesperson', 5000)
            ]

            list = []
            row = 0
            # Write the sales data
            for data in jv_data:

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
                        if credit == 0:
                            table_data.append([
                                Paragraph(data.date.strftime("%Y-%m-%d"), styles['Normal']),
                                Paragraph(data.date.strftime("%B"), styles['Normal']),
                                Paragraph(data.move_id.name or '', styles['Normal']),
                                'JV',
                                Paragraph(data.partner_id.name or '', styles['Normal']),
                                Paragraph(data.move_id.ref or '', styles['Normal']),
                                Paragraph(data.move_id.operation_id.name or '', styles['Normal']),
                                '',  # Shipment No. - Add the appropriate field if available
                                Paragraph(data.account_id.name or '', styles['Normal']),
                                Paragraph(data.move_id.operation_id.x_job_type.name or '', styles['Normal']),
                                Paragraph(str(credit or ''), styles['Normal']),
                                '0',
                                Paragraph(str(debit or ''), styles['Normal']),
                                '0',
                                Paragraph(str((credit or 0) - (debit or 0)), styles['Normal']),
                                Paragraph(data.move_id.user_id.name or '', styles['Normal']),
                            ])

                a = str(data.move_id.name) + str(data.account_id.name)
                list.append(a)
            for data in sales_data:

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
                    _logger.debug(credit, debit,
                                  '--------------------------------------------b------------------------------------')

                    for b in bla:
                        credit += b.x_untaxed_amount_sale
                        debit += b.x_untaxed_amount_cost
                        _logger.debug(credit, debit, '--------------------------------------------b------------------------------------')
                    date = data.invoice_id.invoice_date or data.invoice_id.create_date
                    table_data.append([
                        Paragraph(date.strftime("%Y-%m-%d"), styles['Normal']),
                        Paragraph(date.strftime("%B"), styles['Normal']),
                        Paragraph(data.invoice_id.name or '', styles['Normal']),
                        'Invoices',
                        Paragraph(data.operation_id.customer_id.name or '', styles['Normal']),
                        Paragraph(data.invoice_id.ref or '', styles['Normal']),
                        Paragraph(data.operation_id.name or '', styles['Normal']),
                        '',  # Shipment No. - Add the appropriate field if available
                        Paragraph(data.inv_line_id.account_id.name or '', styles['Normal']),
                        Paragraph(data.operation_id.x_job_type.name or '', styles['Normal']),
                        Paragraph(str(credit or ''), styles['Normal']),
                        '0',
                        Paragraph(str(debit or ''), styles['Normal']),
                        '0',
                        Paragraph(str((credit or 0) - (debit or 0)), styles['Normal']),
                        Paragraph(data.operation_id.operator_id.name or '', styles['Normal']),
                    ])

                a = str(data.invoice_id.name) + str(data.inv_line_id.account_id.name)
                list.append(a)


            # Create the table
            table = Table(table_data)
            table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.gray),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 12),
            #     ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            #     ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
                ('ALIGN', (0, 1), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
                ('FONTSIZE', (0, 1), (-1, -1), 10),
                ('TOPPADDING', (0, 1), (-1, -1), 10),
                ('BOTTOMPADDING', (0, -1), (-1, -1), 12),
                ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
                ('BOX', (0, 0), (-1, -1), 0.25, colors.black)
            ]))

            # Build the PDF document
            elements = []
            elements.append(table)
            doc.build(elements)

            # Prepare the file for download
            file_data = buffer.getvalue()
            file_name = 'sales_report.pdf'

            # Save the PDF file
            self.write({
                'state': 'get',
                'data': base64.encodebytes(file_data),
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


            # Write the headers
            default_widths = [
                ('GL Date', 4000), ('Month', 3000), ('Voucher No.', 4000), ('Voucher Type', 4000),
                ('Party', 6000), ('Ref. No.', 5000), ('Job No', 4000), ('Shipment No.', 4000),
                ('COA/AC Name', 6000), ('Department', 4000), ('Sale Amount (OMR)', 5000),
                ('Sales with Vat', 5000), ('Cost Amount (OMR)', 5000), ('Cost with Vat', 5000),
                ('GP', 4000), ('Salesperson', 5000)
            ]


            list = []
            row = 0
            # Write the sales data
            for data in jv_data:
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
                        if credit == 0:
                            table_data.append([
                                Paragraph(data.date.strftime("%Y-%m-%d"), styles['Normal']),
                                Paragraph(data.date.strftime("%B"), styles['Normal']),
                                Paragraph(data.move_id.name or '', styles['Normal']),
                                'Invoice',
                                Paragraph(data.partner_id.name or '', styles['Normal']),
                                Paragraph(data.move_id.ref or '', styles['Normal']),
                                Paragraph(data.move_id.operation_id.name or '', styles['Normal']),
                                '',  # Shipment No. - Add the appropriate field if available
                                Paragraph(data.account_id.name or '', styles['Normal']),
                                Paragraph(data.move_id.operation_id.x_job_type.name or '', styles['Normal']),
                                Paragraph(str(credit or ''), styles['Normal']),
                                '0',
                                Paragraph(str(debit or ''), styles['Normal']),
                                '0',
                                Paragraph(str((credit or 0) - (debit or 0)), styles['Normal']),
                                Paragraph(data.move_id.user_id.name or '', styles['Normal']),
                            ])

                a = str(data.move_id.name) + str(data.account_id.name)
                list.append(a)
            for data in sales_data:

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
                    _logger.debug(credit, debit,
                                  '--------------------------------------------b------------------------------------')

                    for b in bla:
                        credit += b.x_untaxed_amount_sale
                        debit += b.x_untaxed_amount_cost
                        _logger.debug(credit, debit, '--------------------------------------------b------------------------------------')

                    ctax_amount = 0
                    dtax_amount = 0
                    tax = data.search(
                        [('invoice_id.name', '=', data.invoice_id.name),
                         ('inv_line_id.account_id.name', '=', account_name)])

                    for t in tax:
                        if t.x_sale_total:
                            ctax_amount += b.x_sale_tax.amount
                            dtax_amount += b.x_tax_ids.amount
                    date = data.invoice_id.invoice_date or data.invoice_id.create_date
                    table_data.append([
                        Paragraph(date.strftime("%Y-%m-%d"), styles['Normal']),
                        Paragraph(date.strftime("%B"), styles['Normal']),
                        Paragraph(data.invoice_id.name or '', styles['Normal']),
                        'Invoices',
                        Paragraph(data.operation_id.customer_id.name or '', styles['Normal']),
                        Paragraph(data.invoice_id.ref or '', styles['Normal']),
                        Paragraph(data.operation_id.name or '', styles['Normal']),
                        '',  # Shipment No. - Add the appropriate field if available
                        Paragraph(data.inv_line_id.account_id.name or '', styles['Normal']),
                        Paragraph(data.operation_id.x_job_type.name or '', styles['Normal']),
                        Paragraph(str(credit or ''), styles['Normal']),
                        Paragraph(str(ctax_amount or ''), styles['Normal']),
                        Paragraph(str(debit or ''), styles['Normal']),
                        Paragraph(str(dtax_amount or ''), styles['Normal']),
                        Paragraph(str((credit or 0) - (debit or 0)), styles['Normal']),
                        Paragraph(data.operation_id.operator_id.name or '', styles['Normal']),
                    ])

                a = str(data.invoice_id.name) + str(data.inv_line_id.account_id.name)
                list.append(a)

            # Create the table
            table = Table(table_data)
            table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.gray),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 12),
                # ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                # ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
                ('ALIGN', (0, 1), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
                ('FONTSIZE', (0, 1), (-1, -1), 10),
                ('TOPPADDING', (0, 1), (-1, -1), 10),
                ('BOTTOMPADDING', (0, -1), (-1, -1), 12),
                ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
                ('BOX', (0, 0), (-1, -1), 0.25, colors.black)
            ]))

            # Build the PDF document
            elements = []
            elements.append(table)
            doc.build(elements)

            # Prepare the file for download
            file_data = buffer.getvalue()
            file_name = 'sales_report.pdf'

            # Save the PDF file
            self.write({
                'state': 'get',
                'data': base64.encodebytes(file_data),
                'name': file_name
            })

            return {
                'name': 'Sales Report',
                'type': 'ir.actions.act_url',
                'url': f"/web/content/{self.id}?model=sales.xl.report&field=data&download=true&filename={file_name}",
                'target': 'self'
            }

    def generate_pdff(self):
        # Get the sales data
        sales_data = self.env['account.move.line'].search([])

        # Create the PDF document
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=letter)
        styles = getSampleStyleSheet()

        # Define table headers and data
        table_data = [
            ['GL Date', 'Month', 'Voucher No.', 'Voucher Type', 'Party', 'Ref. No.', 'Job No', 'Shipment No.',
             'COA/AC Name', 'Department', 'Sale Amount (OMR)', 'Sales with Vat', 'Cost Amount (OMR)', 'Cost with Vat',
             'GP', 'Salesperson']
        ]

        # Populate the table with sales data
        for data in sales_data:
            table_data.append([
                data.date.strftime("%Y-%m-%d"),
                data.date.strftime("%B"),
                data.move_id.name or '',
                'Invoice',
                data.partner_id.name or '',
                data.move_id.ref or '',
                data.move_id.operation_id.name or '',
                '',  # Shipment No. - Add the appropriate field if available
                data.account_id.name or '',
                data.move_id.operation_id.x_job_type.name or '',
                str(data.credit or ''),
                '0',
                str(data.debit or ''),
                '0',
                str((data.credit or 0) - (data.debit or 0)),
                data.move_id.user_id.name or ''
            ])
        column_widths = [1.5 * inch, 1 * inch, 1.5 * inch, 1.5 * inch, 2 * inch, 1.5 * inch]

        # Create the table
        table = Table(table_data, colWidths=column_widths)
        # Create the table and apply styles
        # table = Table(table_data)
        # table.setStyle(TableStyle([
        #     ('BACKGROUND', (0, 0), (-1, 0), colors.gray),
        #     ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        #     ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        #     ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        #     ('FONTSIZE', (0, 0), (-1, 0), 12),
        #     ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        #     ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        #     ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
        #     ('ALIGN', (0, 1), (-1, -1), 'LEFT'),
        #     ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        #     ('FONTSIZE', (0, 1), (-1, -1), 10),
        #     ('TOPPADDING', (0, 1), (-1, -1), 10),
        #     ('BOTTOMPADDING', (0, -1), (-1, -1), 12),
        # ]))

        # Build the PDF document
        elements = []
        elements.append(table)
        doc.build(elements)

        # Prepare the file for download
        file_data = buffer.getvalue()
        file_name = 'sales_report.pdf'

        # Save the PDF file
        self.write({
            'state': 'get',
            'data': base64.encodebytes(file_data),
            'name': file_name
        })

        return {
            'name': 'Sales Report',
            'type': 'ir.actions.act_url',
            'url': f"/web/content/{self.id}?model=sales.xl.report&field=data&download=true&filename={file_name}",
            'target': 'self'
        }

