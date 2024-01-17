from odoo import models,fields, _
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
    _name = 'report.tax_report_export_xlsx.tax_xlsx'
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

        self.sheet = workbook.add_worksheet('Tax Report')
        self.sheet.set_column(0, 0, 20)
        self.sheet.set_column(1, 1, 20)
        self.sheet.set_column(2, 2, 20)
        self.sheet.set_column(3, 3, 18)


        # For Formating purpose
        lang = self.env.user.lang
        self.language_id = self.env['res.lang'].search([('code', '=', lang)])[0]
        self._format_float_and_dates(self.env.user.company_id.currency_id, self.language_id)

        self.sheet.freeze_panes(5, 0)

        self.sheet.screen_gridlines = False

        date = current_time.strftime(self.language_id.date_format)
        time = current_time.strftime("%H:%M")

        date_time = date + ' ' + time

        self.sheet.merge_range(2, 0,2,1, 'Created on: '+date_time,
                                self.format_header)

        self.row_pos += 4

        # print(self.format_title)
        if record:
            self.sheet.merge_range(0, 0, 0, 8, 'Tax Report' + ' - ' + record.company_id.name, self.format_title)
            if record['date_from']:
                self.sheet.write_string(2, 2, 'Date from: '+record['date_from'].strftime(self.language_id.date_format),
                                        self.format_header)
                self.sheet.write_string(2, 3, 'Date to: '+record['date_to'].strftime(self.language_id.date_format),
                                        self.format_header)
            data_tax = record.get_report_datas(record)

            self.sheet.write_string(self.row_pos, 0, _(''),
                                    self.format_header)
            self.sheet.write_string(self.row_pos, 1, _('Net'),
                                    self.format_header)
            self.sheet.write_string(self.row_pos, 2, _('Tax'),
                                    self.format_header)
            if self.env.user.company_id.currency_id.symbol:
                self.currency_format_2 = workbook.add_format({
                    'bold': False,
                    'font_size': 10,
                    'align': 'center',
                    'text_wrap': True,
                    'font': 'Arial',
                    'valign': 'top',
                    'num_format': '#,##0.00' + ' ' + self.env.user.company_id.currency_id.symbol})

            if data_tax:
                for line in data_tax:
                    self.row_pos += 1
                    self.sheet.write_string(self.row_pos, 0, line, self.line_header)
                    for key_line in data_tax[line]:
                        # print(key_line['name'])
                        self.row_pos += 1
                        self.sheet.write_string(self.row_pos, 0, key_line['name'] or '', self.line_header_light)
                        self.sheet.write_number(self.row_pos, 1, key_line['net'],
                                                self.currency_format_2 or self.line_header_light)
                        self.sheet.write_number(self.row_pos, 2, key_line['tax'],
                                                self.currency_format_2 or self.line_header_light)
