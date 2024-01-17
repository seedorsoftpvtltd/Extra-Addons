# -*- coding: utf-8 -*-

from odoo import models, fields, api

class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    custom_transporter_id = fields.Many2one(
        'res.partner',
        string="Transporter",
        copy=True,
    )

    @api.model
    def _prepare_picking(self):
        picking = super(PurchaseOrder, self)._prepare_picking()
        if self.custom_transporter_id:
            picking.update({
            'transporter_id': self.custom_transporter_id.id
            })
        return picking