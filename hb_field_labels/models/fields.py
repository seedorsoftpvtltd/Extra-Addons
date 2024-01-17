import base64  # file encode
import urllib.request  # file download from url

from odoo.http import request
from odoo import api, fields, models, tools, osv, http, _
import odoo.osv.osv


class moveline(models.Model):
    _inherit = "stock.move.line"

    owner_id = fields.Many2one('res.partner', check_company=True, string="Customer")
    location_dest_id = fields.Many2one('stock.location', string="To Location", check_company=True, required=True)
    lot_id = fields.Many2one('stock.production.lot', 'Tracking Number',
                             domain="[('product_id', '=', product_id), ('company_id', '=', company_id)]",
                             check_company=True)


class stockquant(models.Model):
    _inherit = "stock.quant"

    lot_id = fields.Many2one(
        'stock.production.lot', 'Tracking Number', index=True,
        ondelete='restrict', readonly=True, check_company=True,
        domain=lambda self: self._domain_lot_id())
    owner_id = fields.Many2one(
        'res.partner', 'Customer',
        help='This is the owner of the quant', readonly=True, check_company=True)
