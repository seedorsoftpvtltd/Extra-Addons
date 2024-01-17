# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _


class StockAssignSerialNumbers(models.TransientModel):
    _inherit = ['stock.assign.serial']
    
    move_id = fields.Many2one(change_default=True)
    tracking_sequence = fields.Many2one('ir.sequence', 'SN Sequence', auto_join=True, readonly=True)
    quantity_done = fields.Float('Done', readonly=True)
    next_readonly = fields.Boolean('Lock First SN', default=False)
    
    @api.onchange('move_id')
    def _onchange_move_id(self):
        self.tracking_sequence = self.move_id.product_id.tracking_sequence
        self.quantity_done = self.move_id.quantity_done
        next_serial_number = self.env['stock.production.lot'].get_name_by_sku(self.move_id.product_id)
        if next_serial_number:
            self.next_serial_number = next_serial_number
            self.next_readonly = True
