from odoo import api, models, fields, _
import collections
from collections import Counter
from datetime import datetime


class productt_static(models.AbstractModel):
    _name = "report.odoo_mo_monthlysales.monthly_sales_report"

    @api.model
    def _get_report_values(self, docids, data):

        ids=[]
        current_date=datetime.today().date().strftime('%m/%d/%Y')

        product_ids = self.env['sale.order'].search([])
        for rec in product_ids:
          # print(rec.date_order)
          if rec.date_order.strftime('%m/%d/%Y') == current_date and rec.state == 'sale':

            ids.append(rec.order_line)

        # print(product_ids)
        # print(product_ids.date_order)
        return  {
           'product':ids,


         }