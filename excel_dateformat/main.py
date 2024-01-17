from odoo import models, fields, api, _
import io
from odoo.tools.misc import xlsxwriter
from odoo.exceptions import UserError
from odoo.addons.web.controllers.main import ExportXlsxWriter

class ExportXlsxWriter:
    def __myinit__(self, field_names, row_count=0):
        self.field_names = field_names
        self.output = io.BytesIO()
        self.workbook = xlsxwriter.Workbook(self.output, {'in_memory': True})
        self.base_style = self.workbook.add_format({'text_wrap': True})
        self.header_style = self.workbook.add_format({'bold': True})
        self.header_bold_style = self.workbook.add_format({'text_wrap': True, 'bold': True, 'bg_color': '#e9ecef'})
        self.date_style = self.workbook.add_format({'text_wrap': True, 'num_format': 'dd-mm-yyyy'})
        self.datetime_style = self.workbook.add_format({'text_wrap': True, 'num_format': 'dd-mm-yyyy'})
        self.worksheet = self.workbook.add_worksheet()
        self.value = False

        if row_count > self.worksheet.xls_rowmax:
            raise UserError(
                _('There are too many rows (%s rows, limit: %s) to export as Excel 2007-2013 (.xlsx) format. Consider splitting the export.') % (
                row_count, self.worksheet.xls_rowmax))

    ExportXlsxWriter.__init__ = __myinit__
