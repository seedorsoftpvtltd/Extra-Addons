# -*- coding: utf-8 -*-
import time
import datetime

from odoo import api, models, fields, _
from odoo.exceptions import UserError


class ProductLowStockReport(models.AbstractModel):
    _name = 'report.product_expiration_alert.report_product_stock_expiration'
    _description = 'Product Stock Expiration Report'

    def get_product_stock_expiration(self, data):
        return_list = {}
        StockProductionObj = self.env['stock.production.lot']
        report_type = data['form']['report_type']
        report_days = data['form']['report_days']
        include_expire_stock = data['form']['include_expire_stock']
        location_ids = data['form']['location_ids']
        return_list['type'] = report_type
        return_list['report_days'] = report_days

        current_date = datetime.date.today() + datetime.timedelta(days=report_days)
        domain = [('use_date', '<', str(current_date))]
        if not include_expire_stock:
            domain += [('use_date', '>', str(fields.Datetime.now()))]
        if report_type == 'location':
            domain += [('quant_ids.location_id', 'in', location_ids)]
        lot_ids = StockProductionObj.search(domain)
        return_list['lot_ids'] = lot_ids
        return return_list

    def get_product_stock_expiration_email(self):
        report_days = self.env.user.company_id.report_days
        include_expire_stock = self.env.user.company_id.include_expire_stock
        location_ids = self.env.user.company_id.location_ids
        report_type = self.env.user.company_id.report_type

        return_list = {}
        StockProductionObj = self.env['stock.production.lot']
        return_list['type'] = report_type
        return_list['report_days'] = report_days

        current_date = datetime.date.today() + datetime.timedelta(days=report_days)
        domain = [('use_date', '<', str(current_date))]
        if not include_expire_stock:
            domain += [('use_date', '>', str(fields.Datetime.now()))]
        if report_type == 'location':
            domain += [('quant_ids.location_id', 'in', location_ids)]
        lot_ids = StockProductionObj.search(domain)
        return_list['lot_ids'] = lot_ids
        return return_list

    @api.model
    def _get_report_values(self, docids, data=None):
        expiry_product = []
        if self.env.context.get('send_email', False):
            self.model = 'stock.production.lot'
            expiry_product = self.get_product_stock_expiration_email()
        else:
            if not data.get('form'):
                raise UserError(_("Content is missing, this report cannot be printed."))
            self.model = self.env.context.get('active_model')
            expiry_product = self.get_product_stock_expiration(data)
        return {
            'doc_ids': self.ids,
            'doc_model': self.model,
            'time': time,
            'expiry_product': expiry_product,
        }
