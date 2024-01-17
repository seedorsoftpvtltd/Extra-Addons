# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _
from odoo.exceptions import UserError


class StockMoveLine(models.Model):
    _inherit = ['stock.move.line']
    
    def action_get_lot_name_auto(self):
        ids = self.filtered(lambda r: not r.lot_name and r.product_id.tracking == 'lot')
        for rec in ids:
            sku = rec.product_id
            if sku.tracking_sequence:
                name = sku.tracking_sequence.next_by_id()
            else:
                name = self.env['ir.sequence'].with_context(force_company=sku.company_id.id).next_by_code('stock.lot.serial') or ''
            rec.write({'lot_name': name})
