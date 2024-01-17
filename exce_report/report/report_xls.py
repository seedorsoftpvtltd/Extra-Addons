from odoo import models, fields, api, _



class ReportXlsx(models.AbstractModel):
    _name = 'report.exce_report.report_customer_xls'
    _inherit = 'report.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook,data,lines):
        """ Add cell formats to current workbook.
        Available formats:
         * format_title
         * format_header
        """
        format_title = workbook.add_format({
            'bold': True,
            'align': 'center',
            'font_size': 10,
            'border': False,
            'font': 'Arial',
        })
        bold_format = workbook.add_format({
            'bold': True,
            'font_size': 14,
        })
        # sheet=workbook.add_worksheet('Customer Statement')
        # sheet.set_column(3, 3, 50)
        # sheet.set_column(2, 2, 50)
        # sheet.write(2,2,'Invoice Date',format_title)
        # sheet.write(2, 3, 'Number', format_title)
        # sheet.write(2, 4, 'Company', format_title)
        # sheet.write(2, 5, 'Currency', format_title)
        # sheet.write(2, 6, 'Due Date', format_title)
        # sheet.write(2, 7, 'INV Invoice', format_title)
        # sheet.write(2, 8, 'INV Paymenet', format_title)
        # sheet.write(2, 9, 'INV Balance', format_title)
        # sheet.write(2, 10, 'Base Invoice', format_title)
        # sheet.write(2, 11, 'Base Payment', format_title)
        # sheet.write(2, 12, 'Base Balance', format_title)
        # workbook = xlwt.Workbook()
        worksheet = workbook.add_worksheet('Customer Statement')

        worksheet.set_column(0, 0, 20)
        worksheet.set_column(1, 1, 20)
        worksheet.set_column(2, 2, 20)
        worksheet.set_column(3, 3, 20)
        worksheet.set_column(4, 4, 20)
        worksheet.set_column(5, 5, 20)
        worksheet.set_column(6, 6, 20)
        worksheet.set_column(7, 7, 20)
        worksheet.set_column(8, 8, 20)
        worksheet.set_column(9, 9, 20)
        worksheet.set_column(10, 10, 20)

        # Define column headers
        row_num = 4
        title = 'Customer Statement Report'
        columns = ['Date', 'Invoice Number','Currency','Due Date','INV Invoices / Debits','INV Payments / Credits','INV Balance','Base Invoices / Debits','Base Payments / Credits','Base Balance', 'Narration']
        worksheet.merge_range(1, 7, 1, 14, title,bold_format)
        for col_num, column_title in enumerate(columns):
            worksheet.write(row_num, col_num, column_title,format_title)

        # Write sale order lines to worksheet
        for line in lines.balance_invoice_ids:
         if not lines.filter_start_date_customer and not lines.filter_end_date_customer and not lines.currency_customer:
            row_num += 1
            row = [
                str(line.invoice_date),
                line.name,
                line.currency_id.name,
                str(line.invoice_date_due),
                line.amount_total,
                line.credit_amount_inv,
                line.result_inv,
                line.amount_total_signed,
                line.credit_amount,
                line.result,
                line.narration if line.narration else '',
            ]
            for col_num, cell_value in enumerate(row):
                    worksheet.write(row_num, col_num, cell_value)
         if lines.filter_start_date_customer and lines.filter_end_date_customer and not lines.currency_customer:
            if line.invoice_date >= lines.filter_start_date_customer and line.invoice_date <= lines.filter_end_date_customer:
                row_num += 1
                row = [
                    str(line.invoice_date),
                    line.name,
                    line.currency_id.name,
                    str(line.invoice_date_due),
                    line.amount_total,
                    line.credit_amount_inv,
                    line.result_inv,
                    line.amount_total_signed,
                    line.credit_amount,
                    line.result,
                    line.narration if line.narration else '',
                ]
                for col_num, cell_value in enumerate(row):
                        worksheet.write(row_num, col_num, cell_value)
         if lines.filter_start_date_customer and lines.filter_end_date_customer and lines.currency_customer:
             if line.invoice_date >= lines.filter_start_date_customer and line.invoice_date <= lines.filter_end_date_customer and line.currency_id == lines.currency_customer:
                row_num += 1
                row = [
                    str(line.invoice_date),
                    line.name,
                    line.currency_id.name,
                    str(line.invoice_date_due),
                    line.amount_total,
                    line.credit_amount_inv,
                    line.result_inv,
                    line.amount_total_signed,
                    line.credit_amount,
                    line.result,
                    line.narration if line.narration else '',
                ]
                for col_num, cell_value in enumerate(row):
                        worksheet.write(row_num, col_num, cell_value)
        # worksheet.title = 'Overdue Payments'
        # worksheet.merge_range(1, 1, 1, 7, title, bold_format)
        title1 = 'Outstanding Payments and Credit Note'
        worksheet.merge_range(row_num+2, col_num, row_num+1,col_num-5, title1, bold_format)
        columns = ['Payment Number', 'Payment Date', 'Currency', 'Amount']
        for col_num, column_title in enumerate(columns):
            worksheet.write(row_num+4, col_num, column_title,format_title)
        for line in lines.oustanding_invoice_ids:
            if not lines.filter_start_date_customer and not lines.filter_end_date_customer and not lines.currency_customer:
                row_num += 1
                row1 = [
                    line.name,
                    str(line.payment_date),
                    line.currency_id.name,
                    line.amount,
                ]
                for col_num, cell_value in enumerate(row1):
                    worksheet.write(row_num+5, col_num, cell_value)

        columns = ['Payment Number', 'Payment Date', 'Currency', 'Amount']
        for col_num, column_title in enumerate(columns):
            worksheet.write(row_num+7, col_num, column_title,format_title)
        for line in lines.oustanding_credit_ids:
            if not lines.filter_start_date_customer and not lines.filter_end_date_customer and not lines.currency_customer:
                    row_num += 1
                    row2 = [
                        line.name,
                        str(line.payment_date),
                        line.currency_id.name,
                        line.amount,

                    ]
                    for col_num, cell_value in enumerate(row2):
                        worksheet.write(row_num+8, col_num, cell_value)


        # Save the workbook
        # workbook.save('sale_order_lines.xls')

class ReportSupplierXlsx(models.AbstractModel):
        _name = 'report.exce_report.report_supplier_xls'
        _inherit = 'report.report_xlsx.abstract'

        def generate_xlsx_report(self, workbook, data, lines):
            """ Add cell formats to current workbook.
            Available formats:
             * format_title
             * format_header
            """
            format_title = workbook.add_format({
                'bold': True,
                'align': 'center',
                'font_size': 10,
                'border': False,
                'font': 'Arial',
            })
            worksheet = workbook.add_worksheet('Supplier Statement')

            worksheet.set_column(0, 0, 20)
            worksheet.set_column(1, 1, 20)
            worksheet.set_column(2, 2, 20)
            worksheet.set_column(3, 3, 20)
            worksheet.set_column(4, 4, 20)
            worksheet.set_column(5, 5, 20)
            worksheet.set_column(6, 6, 20)
            worksheet.set_column(7, 7, 20)
            worksheet.set_column(8, 8, 20)
            worksheet.set_column(9, 9, 20)
            worksheet.set_column(10, 10, 20)
            # Define column headers
            row_num = 5
            bold_format = workbook.add_format({
                'bold': True,
                'font_size': 14,
            })
            title='Supplier Statement Report'
            worksheet.merge_range(1, 7, 1, 14, title, bold_format)
            columns = ['Date', 'Invoice Number','Currency','Due Date','INV Invoices / Credits','INV Payments / Debits','INV Balance','Base Invoices / Credits','Base Payments / Debits','Base Balance', 'Narration']
            for col_num, column_title in enumerate(columns):
                worksheet.write(row_num, col_num, column_title, format_title)

            # Write sale order lines to worksheet
            for line in lines.supplier_invoice_ids:
                if not lines.filter_start_date_vendor and not lines.filter_end_date_vendor and not lines.currency_vendor:
                    row_num += 1
                    row = [
                        str(line.invoice_date),
                        line.name,
                        line.currency_id.name,
                        str(line.invoice_date_due),
                        line.amount_total,
                        line.credit_amount_inv,
                        line.result_inv,
                        line.amount_total_signed,
                        line.credit_amount,
                        line.result,
                        line.narration if line.narration else '',
                    ]
                    for col_num, cell_value in enumerate(row):
                        worksheet.write(row_num, col_num, cell_value)

                if lines.filter_start_date_vendor and lines.filter_end_date_vendor and not lines.currency_vendor:
                        if line.invoice_date >= lines.filter_start_date_vendor and line.invoice_date <= lines.filter_end_date_vendor:
                            row_num += 1
                            row = [
                                str(line.invoice_date),
                                line.name,
                                line.currency_id.name,
                                str(line.invoice_date_due),
                                line.amount_total,
                                line.credit_amount_inv,
                                line.result_inv,
                                line.amount_total_signed,
                                line.credit_amount,
                                line.result,
                                line.narration if line.narration else '',
                            ]
                            for col_num, cell_value in enumerate(row):
                                worksheet.write(row_num, col_num, cell_value)
                if lines.filter_start_date_vendor and lines.filter_end_date_vendor and lines.currency_vendor:
                        if line.invoice_date >= lines.filter_start_date_vendor and line.invoice_date <= lines.filter_end_date_vendor and line.currency_id == lines.currency_vendor:
                            row_num += 1
                            row = [
                                str(line.invoice_date),
                                line.name,
                                line.currency_id.name,
                                str(line.invoice_date_due),
                                line.amount_total,
                                line.credit_amount_inv,
                                line.result_inv,
                                line.amount_total_signed,
                                line.credit_amount,
                                line.result,
                                line.narration if line.narration else '', 
                            ]
                            for col_num, cell_value in enumerate(row):
                                worksheet.write(row_num, col_num, cell_value)
            title1 = 'Outstanding Payments and Debit Note'
            worksheet.merge_range(row_num+2, col_num, row_num+1,col_num-5, title1, bold_format)
            columns = ['Invoice Number', 'Payment Date', 'Currency', 'Amount']
            for col_num, column_title in enumerate(columns):
                worksheet.write(row_num+4, col_num, column_title,format_title)
            for line in lines.supplier_paymnet_ids:
             if not lines.filter_start_date_vendor and not lines.filter_end_date_vendor and not lines.currency_vendor:
                row_num += 1
                row1 = [
                    line.name,
                    str(line.payment_date),
                    line.currency_id.name,
                    line.amount,
                ]
                for col_num, cell_value in enumerate(row1):
                    worksheet.write(row_num+5, col_num, cell_value)

            columns = ['Invoice Number', 'Payment Date', 'Currency', 'Amount']
            for col_num, column_title in enumerate(columns):
                worksheet.write(row_num+7, col_num, column_title,format_title)
            for line in lines.supplier_credit_ids:
                if not lines.filter_start_date_vendor and not lines.filter_end_date_vendor and not lines.currency_vendor:
                        row_num += 1
                        row2 = [
                            line.name,
                            str(line.payment_date),
                            line.currency_id.name,
                            line.amount,

                        ]
                        for col_num, cell_value in enumerate(row2):
                            worksheet.write(row_num+8, col_num, cell_value)



class ReportOverdueXlsx(models.AbstractModel):
    _name = 'report.exce_report.report_overdue_xls'
    _inherit = 'report.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, lines):
        """ Add cell formats to current workbook.
        Available formats:
         * format_title
         * format_header
        """
        format_title = workbook.add_format({
            'bold': True,
            'align': 'center',
            'font_size': 12,
            'border': False,
            'font': 'Arial',
        })

        if lines.report_type == 'fcy':

            format_title = workbook.add_format({
                'bold': True,
                'align': 'center',
                'font_size': 10,
                'border': False,
                'font': 'Arial',
            })
            bold_format = workbook.add_format({
                'bold': True,
                'font_size': 14,
            })
            worksheet = workbook.add_worksheet('FCY Report')
            row_num = 4
            title = 'FCY Report'
            columns = ['Date', 'Voucher Number', 'Salesperson','Narration','Currency','Amount',
                       'O/S Amount']
            worksheet.merge_range(1, 1, 1, 7, title,bold_format)
            for col_num, column_title in enumerate(columns):
                worksheet.write(row_num, col_num, column_title, format_title)

            # Write sale order lines to worksheet
            print(lines)
            for line in lines.balance_invoice_over_ids:
                print(line.name)
                print(line.currency_id)
                print(self.env.company.currency_id)
                print(line.currency_id)
                if not lines.filter_start_date and not lines.filter_end_date and line.currency_id != self.env.company.currency_id:

                    row_num += 1
                    row = [
                        str(line.invoice_date),
                        line.name,
                        lines.balance_invoice_over_ids.invoice_user_id.name,
                        line.narration,
                        line.currency_id.name,
                        line.amount_total,
                        line.result_over,

                    ]
                    for col_num, cell_value in enumerate(row):
                        worksheet.write(row_num, col_num, cell_value)
                if lines.filter_start_date and lines.filter_end_date and line.currency_id != self.env.company.currency_id:

                    if line.invoice_date >= lines.filter_start_date and line.invoice_date <= lines.filter_end_date:
                        row_num += 1
                        row = [
                            str(line.invoice_date),
                            line.name,
                            lines.balance_invoice_over_ids.invoice_user_id.name,
                            line.narration,
                            line.currency_id.name,
                            line.amount_total,
                            line.result_over,
                        ]
                        for col_num, cell_value in enumerate(row):
                            worksheet.write(row_num, col_num, cell_value)

        elif lines.report_type == 'overdue':
            format_title = workbook.add_format({
                'bold': True,
                'align': 'center',
                'font_size': 10,
                'border': False,
                'font': 'Arial',
            })
            bold_format = workbook.add_format({
                'bold': True,
                'font_size': 14,
            })
            worksheet = workbook.add_worksheet('Overdue Payments')
            row_num = 4
            title = 'Overdue Payments'
            columns = ['Date', 'Voucher Number', 'Salesperson', 'Narration','Amount',
                       'O/S Amount','Running Total']
            worksheet.merge_range(1, 1, 1, 7, title,bold_format)
            for col_num, column_title in enumerate(columns):
                worksheet.write(row_num, col_num, column_title, format_title)

            # Write sale order lines to worksheet
            print(lines)
            running = 0
            for line in lines.balance_invoice_over_ids:
                print(line.name)
                print(line.currency_id)
                print(self.env.company.currency_id)
                print(line.currency_id)

                if not lines.filter_start_date and not lines.filter_end_date and line.currency_id == self.env.company.currency_id:

                    running=running+line.amount_total
                    print(running)
                    row_num += 1
                    row = [
                        str(line.invoice_date),
                        line.name,
                        lines.balance_invoice_over_ids.invoice_user_id.name,
                        line.narration,
                        line.amount_total,
                        line.result_over,
                        running,

                    ]
                    for col_num, cell_value in enumerate(row):
                        worksheet.write(row_num, col_num, cell_value)
                if lines.filter_start_date and lines.filter_end_date and line.currency_id == self.env.company.currency_id:

                    if line.invoice_date >= lines.filter_start_date and line.invoice_date <= lines.filter_end_date:

                        running = running + line.amount_total
                        row_num += 1
                        row = [
                            str(line.invoice_date),
                            line.name,
                            lines.balance_invoice_over_ids.invoice_user_id.name,
                            line.narration,
                            line.amount_total,
                            line.result_over,
                            running,
                        ]
                        for col_num, cell_value in enumerate(row):
                            worksheet.write(row_num, col_num, cell_value)
        elif lines.report_type == 'bl':
            format_title = workbook.add_format({
                'bold': True,
                'align': 'center',
                'font_size': 10,
                'border': False,
                'font': 'Arial',
            })
            bold_format = workbook.add_format({
                'bold': True,
                'font_size': 14,
            })
            worksheet = workbook.add_worksheet('BL Details Report')
            row_num = 4
            title = 'BL Details Report'
            columns = ['Date', 'Voucher Number','POL','POD','MBL / MAWB','HBL / HAWB','PO No',
                       'Amount',
                       'O/S Amount','Running Total']
            worksheet.merge_range(1, 1, 1, 7, title,bold_format)
            for col_num, column_title in enumerate(columns):
                worksheet.write(row_num, col_num, column_title, format_title)

            # Write sale order lines to worksheet
            print(lines)
            running = 0
            for line in lines.balance_invoice_over_ids:
                print(line.name)
                print(line.currency_id)
                print(self.env.company.currency_id)
                print(line.currency_id)
                if not lines.filter_start_date and not lines.filter_end_date and line.currency_id == self.env.company.currency_id:
                    running = running + line.amount_total
                    row_num += 1
                    row = [
                        str(line.invoice_date),
                        line.name,
                        line.x_port.name,
                        line.x_final.name,
                        line.x_master,
                        line.x_hn,
                        lines.x_pono,
                        line.amount_total,
                        line.result_over,
                        running,

                    ]
                    for col_num, cell_value in enumerate(row):
                        worksheet.write(row_num, col_num, cell_value)
                if lines.filter_start_date and lines.filter_end_date and line.currency_id == self.env.company.currency_id:

                    if line.invoice_date >= lines.filter_start_date and line.invoice_date <= lines.filter_end_date:
                        running = running + line.amount_total
                        row_num += 1
                        row = [
                            str(line.invoice_date),
                            line.name,
                            line.x_port.name,
                            line.x_final.name,
                            line.x_master,
                            line.x_hn,
                            lines.x_pono,
                            line.amount_total,
                            line.result_over,
                            running,
                        ]
                        for col_num, cell_value in enumerate(row):
                            worksheet.write(row_num, col_num, cell_value)
