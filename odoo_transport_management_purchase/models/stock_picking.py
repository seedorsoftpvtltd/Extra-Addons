# -*- coding: utf-8 -*-

from odoo import models, fields, api

class StockPicking(models.Model):
    _inherit = 'stock.picking'

    purchaseorder_id = fields.Many2one(
        'purchase.order',
        string="Purchase Order",
        copy=True,
    )

    @api.model
    def _prepare_picking_transport_info_custom(self,rec):
        picking = super(StockPicking, self)._prepare_picking_transport_info_custom(rec)

        if rec.purchase_id:
            picking.update({'purchaseorder_id':rec.purchase_id.id})
        return picking
