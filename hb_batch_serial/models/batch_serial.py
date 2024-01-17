import base64  # file encode
import urllib.request  # file download from url

from odoo.http import request
from odoo import api, fields, models, tools, osv, http, _
import odoo.osv.osv


class batchmaster(models.Model):
    _name = "stock.batch"

    name = fields.Char(string="Name")
    product_id = fields.Many2one('product.product', string="Product")
    lot_id = fields.Many2one('stock.production.lot', string="Tracking Number")
    expiry_date = fields.Date(string="Expiry Date")


class serialmaster(models.Model):
    _name = "stock.serial"

    name = fields.Char(string="Name")
    product_id = fields.Many2one('product.product', string="Product")
    lot_id = fields.Many2one('stock.production.lot', string="Tracking Number")
    expiry_date = fields.Date(string="Expiry Date")











