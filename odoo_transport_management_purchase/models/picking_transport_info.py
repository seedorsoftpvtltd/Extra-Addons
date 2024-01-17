# -*- coding: utf-8 -*-

from odoo import models, fields, api

class PickingTransportInfo(models.Model):
    _inherit = 'picking.transport.info'

    purchaseorder_id = fields.Many2one(
        'purchase.order',
        string="Purchase Order",
        copy=True,
    )