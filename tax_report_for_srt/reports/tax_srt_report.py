from odoo import models, fields, _
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


class PartnerXlsx(models.AbstractModel):
    _name = 'report.tax_report_srt_xlsx.tax_xlsx'
    _inherit = ['report.report_xlsx.abstract', 'report.base_accounting_kit.report_tax']

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
            'valign': 'top',
            'border': True,
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

    def _format_float_and_dates(self, currency_id, lang_id):

        self.line_header.num_format = currency_id.excel_format
        self.line_header_light.num_format = currency_id.excel_format
        self.line_header_light_initial.num_format = currency_id.excel_format
        self.line_header_light_ending.num_format = currency_id.excel_format

        self.line_header_light_date.num_format = DATE_DICT.get(lang_id.date_format, 'dd/mm/yyyy')
        self.content_header_date.num_format = DATE_DICT.get(lang_id.date_format, 'dd/mm/yyyy')

    def generate_xlsx_report(self, workbook, data, record):

        # current_time = datetime.datetime.now()

        # Get the current user
        user = self.env.user

        # Get the timezone of the user
        user_tz = user.tz or 'UTC'

        # Convert the user timezone string to a pytz timezone object
        user_timezone = timezone(user_tz)

        # Now you can use the user timezone object to perform datetime operations
        # For example, to get the current time in the user's timezone:
        current_time = timezone('UTC').localize(fields.Datetime.now()).astimezone(user_timezone)

        self._define_formats(workbook)
        self.row_pos = 0

        self.sheet = workbook.add_worksheet('Cost')
        self.sheet.set_column(0, 0, 20)
        self.sheet.set_column(1, 1, 20)
        self.sheet.set_column(2, 2, 20)
        self.sheet.set_column(3, 3, 28)
        self.sheet.set_column(4, 4, 20)
        self.sheet.set_column(5, 5, 20)
        self.sheet.set_column(6, 6, 20)

        # For Formating purpose
        lang = self.env.user.lang
        self.language_id = self.env['res.lang'].search([('code', '=', lang)])[0]
        # self._format_float_and_dates(self.env.user.company_id.currency_id, self.language_id)

        # self.sheet.freeze_panes(5, 0)

        # self.sheet.screen_gridlines = False

        date = current_time.strftime(self.language_id.date_format)
        time = current_time.strftime("%H:%M")

        date_time = date + ' ' + time

        self.sheet.merge_range(2, 0, 2, 1, 'Created on: ' + date_time,
                               self.format_header)

        self.row_pos += 4


        if record:
            self.sheet.merge_range(0, 0, 0, 8, 'Tax Report' + ' - ' + record.company_id.name, self.format_title)
            if record['date_from']:
                self.sheet.write_string(2, 2,
                                        'Date from: ' + record['date_from'].strftime(self.language_id.date_format),
                                        self.format_header)
                self.sheet.write_string(2, 3, 'Date to: ' + record['date_to'].strftime(self.language_id.date_format),
                                        self.format_header)
            data_cost, data_income = record.get_report_datas_for_srt(record)

            self.sheet.write_string(self.row_pos, 0, _('Date'),
                                    self.line_header)
            self.sheet.write_string(self.row_pos, 1, _('Voucher No'),
                                    self.line_header)
            self.sheet.write_string(self.row_pos, 2, _('Client'),
                                    self.line_header)
            self.sheet.write_string(self.row_pos, 3, _('A/C Name'),
                                    self.line_header)
            self.sheet.write_string(self.row_pos, 4, _('Total'),
                                    self.line_header)
            self.sheet.write_string(self.row_pos, 5, _('VAT'),
                                    self.line_header)
            self.sheet.write_string(self.row_pos, 6, _('Total'),
                                    self.line_header)
            if self.env.user.company_id.currency_id.symbol:
                self.currency_format_2 = workbook.add_format({
                    'bold': False,
                    'font_size': 10,
                    'align': 'center',
                    'text_wrap': True,
                    'font': 'Arial',
                    'valign': 'top',
                    'border': True,
                    'num_format': '#,##0.00' + ' ' + self.env.user.company_id.currency_id.symbol})
            i = 0
            if data_cost:
                for key_line in data_cost:
                    self.row_pos += 1
                    formatted_date = key_line["date"].strftime('%Y-%m-%d')
                    self.sheet.write_string(self.row_pos, 0, formatted_date or '', self.line_header_light)
                    self.sheet.write_string(self.row_pos, 1, key_line['move_name'] or '', self.line_header_light)
                    self.sheet.write_string(self.row_pos, 2, key_line['client'], self.line_header_light)
                    self.sheet.write_string(self.row_pos, 3, key_line['taxes_account'], self.line_header_light)
                    self.sheet.write_string(self.row_pos, 4, str(key_line['sub_total']),
                                            self.line_header_light)
                    self.sheet.write_string(self.row_pos, 5, str(key_line['taxes']),
                                            self.line_header_light)
                    self.sheet.write_string(self.row_pos, 6, str(key_line['total']),
                                            self.line_header_light)

        # Income
        self.sheet2 = workbook.add_worksheet('Income')
        self.sheet2.set_column(0, 0, 20)
        self.sheet2.set_column(1, 1, 20)
        self.sheet2.set_column(2, 2, 20)
        self.sheet2.set_column(3, 3, 28)
        self.sheet2.set_column(4, 4, 20)
        self.sheet2.set_column(5, 5, 20)
        self.sheet2.set_column(6, 6, 20)

        self.sheet2.merge_range(2, 0, 2, 1, 'Created on: ' + date_time,
                                self.format_header)
        # Define a format with a specific number format
        # floating_point_bordered = workbook.add_format({'num_format': '#,##0.000', 'border': 1})



        self.row_pos = 0
        self.row_pos += 4
        if record:
            self.sheet2.merge_range(0, 0, 0, 8, 'Tax Report' + ' - ' + record.company_id.name, self.format_title)
            if record['date_from']:
                self.sheet2.write_string(2, 2,
                                         'Date from: ' + record['date_from'].strftime(self.language_id.date_format),
                                         self.format_header)
                self.sheet2.write_string(2, 3, 'Date to: ' + record['date_to'].strftime(self.language_id.date_format),
                                         self.format_header)

            self.sheet2.write_string(self.row_pos, 0, _('Date'),
                                     self.line_header)
            self.sheet2.write_string(self.row_pos, 1, _('Voucher No'),
                                     self.line_header)
            self.sheet2.write_string(self.row_pos, 2, _('Client'),
                                     self.line_header)
            self.sheet2.write_string(self.row_pos, 3, _('A/C Name'),
                                     self.line_header)
            self.sheet2.write_string(self.row_pos, 4, _('Total'),
                                     self.line_header)
            self.sheet2.write_string(self.row_pos, 5, _('VAT'),
                                     self.line_header)
            self.sheet2.write_string(self.row_pos, 6, _('Total'),
                                     self.line_header)
            if self.env.user.company_id.currency_id.symbol:
                self.currency_format_2 = workbook.add_format({
                    'bold': False,
                    'font_size': 10,
                    'align': 'center',
                    'text_wrap': True,
                    'font': 'Arial',
                    'valign': 'top',
                    'border': True,
                    'num_format': '#,##0.00' + ' ' + self.env.user.company_id.currency_id.symbol})
            i = 0
            if data_income:
                for key_line in data_income:
                    self.row_pos += 1
                    formatted_date = key_line["date"].strftime('%Y-%m-%d')

                    self.sheet2.write_string(self.row_pos, 0, formatted_date or '', self.line_header_light)
                    self.sheet2.write_string(self.row_pos, 1, key_line['move_name'] or '', self.line_header_light)
                    self.sheet2.write_string(self.row_pos, 2, key_line['client'], self.line_header_light)
                    self.sheet2.write_string(self.row_pos, 3, key_line['taxes_account'], self.line_header_light)
                    self.sheet2.write_number(self.row_pos, 4, key_line['sub_total'],
                                             self.line_header_light)
                    self.sheet2.write_number(self.row_pos, 5, key_line['taxes'],
                                            self.line_header_light)
                    self.sheet2.write_number(self.row_pos, 6, key_line['total'],
                                             self.line_header_light)


