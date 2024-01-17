# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _
from odoo.exceptions import UserError

class StockMove(models.Model):
    _inherit = ['stock.move']

    tracking_sequence = fields.Many2one('ir.sequence', 'SN Sequence', related='product_id.tracking_sequence', auto_join=True, readonly=True)
    
    def _generate_serial_numbers(self, next_serial_count=False):
        # 特殊处理，用序号规则
        self.ensure_one()

        if not self.next_serial:
            self.next_serial = self.env['stock.production.lot'].get_name_by_sku(self.product_id)
        
        if not next_serial_count:
            next_serial_count = self.next_serial_count
        
        lot_names = [self.next_serial]
        
        for i in range(1, next_serial_count):
            lot_names.append(self.env['stock.production.lot'].get_name_by_sku(self.product_id))
        move_lines_commands = self._app_generate_serial_move_line_commands(lot_names)
        self.write({
            'move_line_ids': move_lines_commands,
            'next_serial': False,
        })
        return True

    def action_assign_serial_show_details(self):
        self.ensure_one()
        if not self.next_serial:
            self.write({
                'next_serial': self.env['stock.production.lot'].get_name_by_sku(self.product_id)
            })
        return super(StockMove, self).action_assign_serial_show_details()
    
    def _app_generate_serial_move_line_commands(self, lot_names, origin_move_line=None):
        # odoo旧版本没有 _generate_serial_move_line_commands 方法
        self.ensure_one()

        # Select the right move lines depending of the picking type configuration.
        move_lines = self.env['stock.move.line']
        if self.picking_type_id.show_reserved:
            move_lines = self.move_line_ids.filtered(lambda ml: not ml.lot_id and not ml.lot_name)
        else:
            move_lines = self.move_line_nosuggest_ids.filtered(lambda ml: not ml.lot_id and not ml.lot_name)

        if origin_move_line:
            location_dest = origin_move_line.location_dest_id
        else:
            location_dest = self.location_dest_id._get_putaway_strategy(self.product_id)
        move_line_vals = {
            'picking_id': self.picking_id.id,
            'location_dest_id': location_dest.id or self.location_dest_id.id,
            'location_id': self.location_id.id,
            'product_id': self.product_id.id,
            'product_uom_id': self.product_id.uom_id.id,
            'qty_done': 1,
        }
        if origin_move_line:
            # `owner_id` and `package_id` are taken only in the case we create
            # new move lines from an existing move line. Also, updates the
            # `qty_done` because it could be usefull for products tracked by lot.
            move_line_vals.update({
                'owner_id': origin_move_line.owner_id.id,
                'package_id': origin_move_line.package_id.id,
                'qty_done': origin_move_line.qty_done or 1,
            })

        move_lines_commands = []
        for lot_name in lot_names:
            # We write the lot name on an existing move line (if we have still one)...
            if move_lines:
                move_lines_commands.append((1, move_lines[0].id, {
                    'lot_name': lot_name,
                    'qty_done': 1,
                }))
                move_lines = move_lines[1:]
            # ... or create a new move line with the serial name.
            else:
                move_line_cmd = dict(move_line_vals, lot_name=lot_name)
                move_lines_commands.append((0, 0, move_line_cmd))
        return move_lines_commands
