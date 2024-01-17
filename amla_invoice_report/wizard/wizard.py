from odoo import models, fields, api,_
from datetime import datetime
import logging
_logger = logging.getLogger(__name__)

try:
	import xlsxwriter
except ImportError:
	_logger.debug('Cannot `import xlsxwriter`.')
try:
	import base64
except ImportError:
	_logger.debug('Cannot `import base64`.')

class report_wizard(models.TransientModel):
    _name = 'report.wizard'
    start_date=fields.Date(string='Start Date',default=datetime.today().replace(day=1))
    end_date = fields.Date(string='End Date',default=datetime.today())
    old_bill = fields.Boolean(string="Show Old Bills")


    def get_wizard_data(self):
        data = {
            'start_date': self.start_date,
            'end_date': self.end_date,
            'old_bill': self.old_bill,

        }
        return data


    def view(self):

        if self.old_bill == False:

            domain = [('type', '=', 'out_invoice'),('state','=','posted'),
            ('invoice_date', '>=', self.start_date),
            ('invoice_date', '<=', self.end_date),]
        else:

            domain = [('type', '=', 'out_invoice'),('state','=','posted'),
                      ('payment_date', '>=', self.start_date),
                      ('payment_date', '<=', self.end_date),('invoice_date', '<', self.start_date)]

        return {
            'type': 'ir.actions.act_window',
            'name': _('Collection Report'),
            'res_model': 'account.move',
            'view_mode': 'tree',
            'limit': 99999999,
            'search_view_id': self.env.ref('account.view_invoice_tree').id,
            'domain': domain,
            }
            #return self.env.ref('amla_invoice_report.invoice_report_tree_view')

    def excel(self):
        """ Button function for Xlsx """

        data = {
            'start_date': self.start_date,
            'end_date': self.end_date,
            'old_bill': self.old_bill,
        }

        return self.env.ref(
            'amla_invoice_report.excel_report_xlsx').report_action(self,data)

        # self.ensure_one()
        # [data] = self.read()
        # file_path = 'Invoice Report' + '.xlsx'
        # workbook = xlsxwriter.Workbook('/tmp/' + file_path)
        # self.sheet = workbook.add_worksheet('Invoice Report')
        # workbook.close()
        # buf = base64.b64encode(open('/tmp/' + file_path, 'rb+').read())
        # self.document = buf
        # self.file = 'Invoice Report' + '.xlsx'

    def pdf(self):
        """ Button function for PDF """
        data = {
            'start_date': self.start_date,
            'end_date': self.end_date,
            #'old_bill': self.old_bill,
        }
        return self.env.ref(
            'amla_invoice_report.pdf_report_pdf').report_action(self,data)

