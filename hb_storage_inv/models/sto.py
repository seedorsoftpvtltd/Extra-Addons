from odoo.http import request
from odoo import api, fields, models, tools, osv, http, _
import odoo.osv.osv
from datetime import datetime, date, timedelta


class storage(models.Model):
    _name = 'storage.type'

    name = fields.Char('Name')


class productstorage(models.Model):
    _inherit = 'product.template'

    storage_type = fields.Many2one('storage.type', string="Storage Type", store=True)


class Addedservice(models.Model):
    _name = 'added.service'

    name = fields.Char('Name')


class warehouseorder(models.Model):
    _inherit = 'stock.picking'

    added_service = fields.Many2one('added.service', string="Added service")


class Warehousemovelineext(models.Model):
    _inherit = 'stock.move.line'

    location_barcode = fields.Char(string="Location Barcode", compute='_locationbarcode', store=True)


class ResPartner(models.Model):
    # _name = 'res.partner'
    _inherit = 'res.partner'

    # final_inv_date = fields.Datetime(string='Final invoice date')
    last_inv_date = fields.Datetime(string='Last invoice date', compute="_inv_gen_date")
    inv_end_date = fields.Datetime(string='Invoice Date', compute="_inv_gen_date")
    # last_inv_date = fields.Datetime(string='Last invoice date', store=True)
    # inv_end_date = fields.Datetime(string='Invoice Date', store=True)
    # sdate = fields.Integer(string='Date')
    # smonth = fields.Integer(string='Month')
    # syear = fields.Integer(string='Year')
    # edate = fields.Integer(string='Date')
    # emonth = fields.Integer(string='Month')op
    # eyear = fields.Integer(string='Year')

    # last_inv_date = fields.Datetime(string='Last invoice date')
    # inv_end_date = fields.Datetime(string='Invoice Date')

    def _inv_gen_date(self):
        for rec in self:
            agr = self.env['agreement'].search([('partner_id','=',rec.id)])
            if agr:
                for ag in agr:
                    if ag.start_date and ag.end_date:
                        rec['last_inv_date'] = ag.start_date
                        rec['inv_end_date'] = ag.end_date
                    else:
                        today = datetime.today().date()
                        first_da = today.replace(day=1)
                        # first_day = datetime.strptime(str(first_da), '%Y-%m-%d').strftime('%Y-%m-%d %H:%M:%S')
                        last_mo = first_da - timedelta(days=1)
                        # last_month = datetime.strptime((last_mo), '%Y-%m-%d').strftime('%Y-%m-%d %H:%M:%S')
                        begin_day = last_mo.replace(day=26)
                        rec['last_inv_date'] = begin_day
                        rec['inv_end_date'] = today.replace(day=25)

            else:
                today = datetime.today().date()
                first_da = today.replace(day=1)
                # first_day = datetime.strptime(str(first_da), '%Y-%m-%d').strftime('%Y-%m-%d %H:%M:%S')
                last_mo = first_da - timedelta(days=1)
                # last_month = datetime.strptime((last_mo), '%Y-%m-%d').strftime('%Y-%m-%d %H:%M:%S')
                begin_day = last_mo.replace(day=26)
                rec['last_inv_date'] = begin_day
                rec['inv_end_date'] = today.replace(day=25)
            print(rec.last_inv_date, rec.inv_end_date)

        # for rec in self:
        #     today = datetime.today().date()
        #     first_da = today.replace(day=1)
        #     # first_day = datetime.strptime(str(first_da), '%Y-%m-%d').strftime('%Y-%m-%d %H:%M:%S')
        #     last_mo = first_da - timedelta(days=1)
        #     # last_month = datetime.strptime((last_mo), '%Y-%m-%d').strftime('%Y-%m-%d %H:%M:%S')
        #     begin_day = last_mo.replace(day=26)
        #     rec['last_inv_date'] = begin_day
        #     rec['inv_end_date'] = today.replace(day=25)
        #     print(rec.last_inv_date, rec.inv_end_date)

    def inv_gen_date(self):
        for rec in self:
            today = datetime.today().date()
            first_da = today.replace(day=1)
            # first_day = datetime.strptime(str(first_da), '%Y-%m-%d').strftime('%Y-%m-%d %H:%M:%S')
            last_mo = first_da - timedelta(days=1)
            # last_month = datetime.strptime((last_mo), '%Y-%m-%d').strftime('%Y-%m-%d %H:%M:%S')
            begin_day = last_mo.replace(day=26)
            rec['last_inv_date'] = begin_day
            rec['inv_end_date'] = today.replace(day=25)
            print(rec.last_inv_date, rec.inv_end_date)





