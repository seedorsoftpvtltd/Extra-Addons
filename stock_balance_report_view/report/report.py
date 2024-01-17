from odoo import fields, models, api, _

class PartnerBalanceXlsx(models.AbstractModel):
    _name = 'report.stock_balance_report_view.balance_xlsx'
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
        self.sheet.set_column('A:AI', 20)
        # Headers
        self.sheet.write_string(self.row_pos, 0, _('Location code'), self.line_header)
        self.sheet.write_string(self.row_pos, 1, _('Warehouse Code'), self.line_header)
        self.sheet.write_string(self.row_pos, 2, _('Warehouse Name'), self.line_header)
        self.sheet.write_string(self.row_pos, 3, _('ASN ID'), self.line_header)
        self.sheet.write_string(self.row_pos, 4, _('Client Code'), self.line_header)
        self.sheet.write_string(self.row_pos, 5, _('Client Name'), self.line_header)
        self.sheet.write_string(self.row_pos, 6, _('SKU Code'), self.line_header)
        self.sheet.write_string(self.row_pos, 7, _('SKU Name'), self.line_header)
        self.sheet.write_string(self.row_pos, 8, _('HS Code'), self.line_header)
        self.sheet.write_string(self.row_pos, 9, _('IN Date'), self.line_header)
        self.sheet.write_string(self.row_pos, 10, _('GRN No'), self.line_header)
        self.sheet.write_string(self.row_pos, 11, _('Bill Of Entry'), self.line_header)
        self.sheet.write_string(self.row_pos, 12, _('Item No as per BOE'), self.line_header)
        self.sheet.write_string(self.row_pos, 13, _('Pallet ID'), self.line_header)
        self.sheet.write_string(self.row_pos, 14, _('Location Name'), self.line_header)
        self.sheet.write_string(self.row_pos, 15, _('Location type'), self.line_header)
        self.sheet.write_string(self.row_pos, 16, _('Tracking No'), self.line_header)
        self.sheet.write_string(self.row_pos, 17, _('Barcode'), self.line_header)
        self.sheet.write_string(self.row_pos, 18, _('UOM'), self.line_header)
        self.sheet.write_string(self.row_pos, 19, _('Currency'), self.line_header)
        self.sheet.write_string(self.row_pos, 20, _('Available Qty'), self.line_header)
        # self.sheet.write_string(self.row_pos, 21, _('Available Volume'), self.line_header)
        # self.sheet.write_string(self.row_pos, 22, _('Gross weight'), self.line_header)
        # self.sheet.write_string(self.row_pos, 23, _('Net weight'), self.line_header)
        # self.sheet.write_string(self.row_pos, 24, _('EX Rate'), self.line_header)
        self.sheet.write_string(self.row_pos, 21, _('Value Of Goods'), self.line_header)
        self.sheet.write_string(self.row_pos, 22, _('Batch No'), self.line_header)
        self.sheet.write_string(self.row_pos, 23, _('Date Of Manufacture'), self.line_header)
        self.sheet.write_string(self.row_pos, 24, _('Date Of Expiry'), self.line_header)
        self.sheet.write_string(self.row_pos, 25, _('COO'), self.line_header)
        self.sheet.write_string(self.row_pos, 26, _('Putaway zone'), self.line_header)
        self.sheet.write_string(self.row_pos, 27, _('Storage area'), self.line_header)
        self.sheet.write_string(self.row_pos, 28, _('Storage type'), self.line_header)
        self.sheet.write_string(self.row_pos, 29, _('Container No'), self.line_header)
        self.sheet.write_string(self.row_pos, 30, _('Truck Number'), self.line_header)

        data = record.get_data(record)
        if data:
            for line in data:
                self.row_pos += 1
                self.sheet.write_string(self.row_pos, 0, line['x_loc_code'] or '')
                self.sheet.write_string(self.row_pos, 1, line['x_war_code'] or '')
                self.sheet.write_string(self.row_pos, 2, line['x_war_name'] or '')
                self.sheet.write_string(self.row_pos, 3, line['x_asn'] or '')
                self.sheet.write_string(self.row_pos, 4, line['x_ccode'] or '')
                self.sheet.write_string(self.row_pos, 5, line['x_cname'] or '')
                self.sheet.write_string(self.row_pos, 6, line['x_sku_code'] or '')
                self.sheet.write_string(self.row_pos, 7, line['x_sku_name'] or '')
                self.sheet.write_string(self.row_pos, 8, line['x_hs'] or '')
                self.sheet.write_string(self.row_pos, 9, line['sche_date'] or '')
                self.sheet.write_string(self.row_pos, 10, line['x_grn'] or '')
                self.sheet.write_string(self.row_pos, 11, line['x_boe'] or '')
                self.sheet.write_string(self.row_pos, 12, line['item_boe'] or '')
                self.sheet.write_string(self.row_pos, 13, line['package_id'] or '')
                self.sheet.write_string(self.row_pos, 14, line['location_id'] or '')
                self.sheet.write_string(self.row_pos, 15, line['x_ltype'] or '')
                self.sheet.write_string(self.row_pos, 16, line['lot_id'] or '')
                self.sheet.write_string(self.row_pos, 17, line['x_barcode'] or '')
                self.sheet.write_string(self.row_pos, 18, line['x_uom'] or '')
                self.sheet.write_string(self.row_pos, 19, line['x_currency'] or '')
                self.sheet.write_number(self.row_pos, 20, line['quantity'])
                # self.sheet.write_number(self.row_pos, 21, line['x_volume'])
                # self.sheet.write_number(self.row_pos, 22, line['x_weight'])
                # self.sheet.write_number(self.row_pos, 23, line['net_weight'])
                # self.sheet.write_number(self.row_pos, 24, line['x_ex'])
                self.sheet.write_number(self.row_pos, 21, line['value_goods'])
                self.sheet.write_string(self.row_pos, 22, line['x_batchno'] or '')
                self.sheet.write_string(self.row_pos, 23, line['x_prod'] or '')
                self.sheet.write_string(self.row_pos, 24, line['x_exp'] or '')
                self.sheet.write_string(self.row_pos, 25, line['x_coo'] or '')
                self.sheet.write_string(self.row_pos, 26, line['putaway_zone'] or '')
                self.sheet.write_string(self.row_pos, 27, line['x_sarea'] or '')
                self.sheet.write_string(self.row_pos, 28, line['x_stype'] or '')
                self.sheet.write_string(self.row_pos, 29, line['x_container_no'] or '')
                self.sheet.write_string(self.row_pos, 30, line['x_tno'] or '')

