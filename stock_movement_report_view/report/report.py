from odoo import models, fields, _


class PartnerXlsx(models.AbstractModel):
    _name = 'report.stock_movement_report_view.movement_xlsx'
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
            'border': True,
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
        self.row_pos = 0
        self.sheet = workbook.add_worksheet('Stock Movement Report')
        self.sheet.set_column('A:AG', 20)
        # Headers
        self.sheet.write_string(self.row_pos, 0, _('Warehouse'), self.line_header)
        self.sheet.write_string(self.row_pos, 1, _('Customer Code'), self.line_header)
        self.sheet.write_string(self.row_pos, 2, _('Customer Name'), self.line_header)
        self.sheet.write_string(self.row_pos, 3, _('Product Code'), self.line_header)
        self.sheet.write_string(self.row_pos, 4, _('Product Name'), self.line_header)
        self.sheet.write_string(self.row_pos, 5, _('Bar Code'), self.line_header)
        self.sheet.write_string(self.row_pos, 6, _('HS Code'), self.line_header)
        self.sheet.write_string(self.row_pos, 7, _('Truck-CNTR Code'), self.line_header)
        self.sheet.write_string(self.row_pos, 8, _('TRK Number'), self.line_header)
        self.sheet.write_string(self.row_pos, 9, _('CNTR Number'), self.line_header)
        self.sheet.write_string(self.row_pos, 10, _('Transaction Type'), self.line_header)
        self.sheet.write_string(self.row_pos, 11, _('Transaction ID'), self.line_header)
        self.sheet.write_string(self.row_pos, 12, _('Trans Date'), self.line_header)
        self.sheet.write_string(self.row_pos, 13, _('Trans No'), self.line_header)
        self.sheet.write_string(self.row_pos, 14, _('Location Code'), self.line_header)
        self.sheet.write_string(self.row_pos, 15, _('UOM'), self.line_header)
        self.sheet.write_string(self.row_pos, 16, _('QTY'), self.line_header)
        # self.sheet.write_string(self.row_pos, 17, _('Volume'), self.line_header)
        # self.sheet.write_string(self.row_pos, 18, _('Gross Weight'), self.line_header)
        # self.sheet.write_string(self.row_pos, 19, _('Net Weight'), self.line_header)
        self.sheet.write_string(self.row_pos, 17, _('In Transaction No'), self.line_header)
        self.sheet.write_string(self.row_pos, 18, _('Pallet ID'), self.line_header)
        self.sheet.write_string(self.row_pos, 19, _('In Ref Date'), self.line_header)
        self.sheet.write_string(self.row_pos, 20, _('In Ref No'), self.line_header)
        self.sheet.write_string(self.row_pos, 21, _('In BOE'), self.line_header)
        self.sheet.write_string(self.row_pos, 22, _('Item No as per BOE'), self.line_header)
        self.sheet.write_string(self.row_pos, 23, _('Batch No'), self.line_header)
        self.sheet.write_string(self.row_pos, 24, _('Lot No'), self.line_header)
        self.sheet.write_string(self.row_pos, 25, _('MF Date'), self.line_header)
        self.sheet.write_string(self.row_pos, 26, _('Exp Date'), self.line_header)
        self.sheet.write_string(self.row_pos, 27, _('COO'), self.line_header)

        data = record.get_data(record)
        if data:
            for line in data:
                self.row_pos += 1
                self.sheet.write_string(self.row_pos, 0, line['x_war'] or '')
                self.sheet.write_string(self.row_pos, 1, line['x_ccode'] or '')
                self.sheet.write_string(self.row_pos, 2, line['owner_id'] or '')
                self.sheet.write_string(self.row_pos, 3, line['product_id'] or '')
                self.sheet.write_string(self.row_pos, 4, line['x_name'] or '')
                self.sheet.write_string(self.row_pos, 5, line['barcode'] or '')
                self.sheet.write_string(self.row_pos, 6, line['x_hs'] or '')
                self.sheet.write_string(self.row_pos, 7, line['x_cntr_code'] or '')
                self.sheet.write_string(self.row_pos, 8, line['x_tno'] or '')
                self.sheet.write_string(self.row_pos, 9, line['container_no'] or '')
                self.sheet.write_string(self.row_pos, 10, line['x_trans_type'] or '')
                self.sheet.write_string(self.row_pos, 11, line['origin'] or '')
                self.sheet.write_string(self.row_pos, 12, line['x_trans_date'] or '')
                self.sheet.write_string(self.row_pos, 13, line['x_trans_no'] or '')
                self.sheet.write_string(self.row_pos, 14, line['loc_code'] or '')
                self.sheet.write_string(self.row_pos, 15, line['x_uom'])
                self.sheet.write_number(self.row_pos, 16, line['x_qty'])
                # self.sheet.write_number(self.row_pos, 17, line['x_vol'] )
                # self.sheet.write_number(self.row_pos, 18, line['total_gw'])
                # self.sheet.write_number(self.row_pos, 19, line['net_weight'])
                self.sheet.write_string(self.row_pos, 17, line['x_namee'] or '')
                self.sheet.write_string(self.row_pos, 18, line['pallet'] or '')
                self.sheet.write_string(self.row_pos, 19, line['x_ref_date'] or '')
                self.sheet.write_string(self.row_pos, 20, line['x_ref_no'] or '')
                self.sheet.write_string(self.row_pos, 21, line['x_bill'] or '')
                self.sheet.write_string(self.row_pos, 22, line['item_boe'] or '')
                self.sheet.write_string(self.row_pos, 23, line['batchno'] or '')
                self.sheet.write_string(self.row_pos, 24, line['lot_id'] or '')
                self.sheet.write_string(self.row_pos, 25, line['production_date'] or '')
                self.sheet.write_string(self.row_pos, 26, line['expiry_date'] or '')
                self.sheet.write_string(self.row_pos, 27, line['x_coo'] or '')
