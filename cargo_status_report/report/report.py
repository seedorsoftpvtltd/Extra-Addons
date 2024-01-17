from odoo import api,models,fields, _

class InvoiceXlsx(models.AbstractModel):
    _name = 'report.cargo_status_report.report_xlsx'
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
            'border': True
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
            'valign': 'top',
            'border': True
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
        print(data)
        # if data['job_date'] and data['client_name']:
        #     print('eeeeeeeeeee')
        #     subjob=self.env['sub.job'].search([('job_date','=',data['job_date']),('partner_id','=',data['client_name'])])
        if data['start_date'] and data['end_date']:
            print('erer')
            subjob=self.env['sub.job'].search([('job_date', '>=', data['start_date']),
                      ('job_date', '<=', data['end_date'])])
        elif data['start_date']:
            subjob=self.env['sub.job'].search([('job_date', '>=', data['start_date'])])
        elif data['end_date']:
            subjob=self.env['sub.job'].search([('job_date', '<=', data['end_date'])])
        # elif data['client_name']:
        #     print('xxxxxx')
        #     subjob=self.env['sub.job'].search([('partner_id','=',data['client_name'])])
        else:
            subjob = self.env['sub.job'].search([])
        print(subjob)
        self._define_formats(workbook)
        self.row_pos = 0
        self.col_pos = 0
        self.sheet = workbook.add_worksheet('Cargo Status Report')
        self.sheet.set_column(0, 0, 20)
        self.sheet.set_column(1, 1, 20)
        self.sheet.set_column(2, 2, 20)
        self.sheet.set_column(3, 3, 18)
        self.sheet.set_column(5, 5, 18)
        self.sheet.set_column(6, 6, 18)
        self.sheet.set_column(7, 7, 18)
        self.sheet.set_column(8, 8, 18)
        self.sheet.set_column(9, 9, 18)
        self.sheet.set_column(10, 10, 18)
        self.sheet.set_column(11, 11, 18)
        self.sheet.set_column(12, 12, 18)
        self.sheet.set_column(13, 13, 18)

        self.sheet.write_string(self.row_pos, 0, _('Job No'),
                                self.format_header)
        self.sheet.write_string(self.row_pos, 1, _('Sub Job'),
                                self.format_header)
        self.sheet.write_string(self.row_pos, 2, _('Job Date'),
                                self.format_header)
        self.sheet.write_string(self.row_pos, 3, _('Mbl No.'),
                                self.format_header)
        self.sheet.write_string(self.row_pos, 4, _('ETA'),
                                self.format_header)
        self.sheet.write_string(self.row_pos, 5, _('Hbl No.'),
                                self.format_header)
        self.sheet.write_string(self.row_pos, 6, _('Client Name'),
                                self.format_header)
        self.sheet.write_string(self.row_pos, 7, _('Origin Agent Name'),
                                self.format_header)
        self.sheet.write_string(self.row_pos, 8, _('Conatiner No.'),
                                self.format_header)
        self.sheet.write_string(self.row_pos, 9, _('No. Of Pcs'),
                                self.format_header)
        self.sheet.write_string(self.row_pos, 10, _('G.Weight'),
                                self.format_header)
        self.sheet.write_string(self.row_pos, 11, _('Volume'),
                                self.format_header)
        self.sheet.write_string(self.row_pos, 12, _('Cargo Delivered Date'),
                                self.format_header)
        self.sheet.write_string(self.row_pos, 13, _('Status'),
                                self.format_header)

        if subjob:

            for line in subjob:
                self.row_pos += 1

                self.sheet.write_string(self.row_pos, 0, str(line['origin']) if line['origin'] else '',self.line_header_light)
                self.sheet.write_string(self.row_pos, 1, str(line['name']) if line['name'] else '',self.line_header_light)
                self.sheet.write_string(self.row_pos, 2, str(line['job_date'].strftime('%d/%m/%Y')) if line['job_date'] else '',self.line_header_light)
                self.sheet.write_string(self.row_pos, 3, str(line['mbl_no']) if line['mbl_no'] else '',self.line_header_light)
                self.sheet.write_string(self.row_pos, 4, str(line['eta'].strftime('%d/%m/%Y')) if line['eta'] else '',self.line_header_light)
                self.sheet.write_string(self.row_pos, 5, str(line['hbl_no']) if line['hbl_no'] else '',self.line_header_light)
                self.sheet.write_string(self.row_pos, 6, str(line['partner_id'].name) if line['partner_id'] else '',self.line_header_light)
                self.sheet.write_string(self.row_pos, 7, str(line['job_id'].agent_id.name) if line['job_id'].agent_id else '',self.line_header_light)
                self.sheet.write_string(self.row_pos, 8, str(line['container_no']) if line['container_no'] else '',self.line_header_light)
                self.sheet.write_string(self.row_pos, 9, str(line['received_qty']) if line['received_qty'] else '',self.line_header_light)
                self.sheet.write_string(self.row_pos, 10, str(line['weight']) if line['weight'] else '',self.line_header_light)
                self.sheet.write_string(self.row_pos, 11, str(line['volume']) if line['volume'] else '',self.line_header_light)
                self.sheet.write_string(self.row_pos, 12, str(line['etd'].strftime('%d/%m/%Y')) if line['etd'] else '',self.line_header_light)
                if line['state'] == 'draft':
                    self.sheet.write_string(self.row_pos, 13, 'Yet to be Collected',self.line_header_light)
                elif line['state'] == 'confirm':
                    self.sheet.write_string(self.row_pos, 13, 'Shipment Colleted',self.line_header_light)
                else:
                    self.sheet.write_string(self.row_pos, 13, 'Cancelled',self.line_header_light)


