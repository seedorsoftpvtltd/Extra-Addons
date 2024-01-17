# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
import logging
from odoo.exceptions import UserError
from odoo.tools.float_utils import float_round, float_is_zero

_logger = logging.getLogger(__name__)


class Inventory(models.Model):
    _inherit = 'stock.inventory'

    def action_cancel_draft(self):
        self.mapped('move_ids').with_context(inventory=True)._action_cancel()
        self.write({'line_ids': [(5,)], 'state': 'cancel'})
        for move in self.move_ids:
            if move.product_id.tracking != 'none':
                lot_id = False
                for line in move.move_line_ids:
                    lot_id = line.lot_id.id
                dest_loc_domain = [('product_id', '=', move.product_id.id),
                                   ('location_id', '=', move.location_dest_id.id), ('lot_id', '=', lot_id)]
                src_loc_domain = [('product_id', '=', move.product_id.id), ('location_id', '=', move.location_id.id),
                                  ('lot_id', '=', lot_id)]
                quants_dest_lot_id = self.env['stock.quant'].sudo().search(dest_loc_domain)
                quants_src_lot_id = self.env['stock.quant'].sudo().search(src_loc_domain)

                if quants_dest_lot_id:
                    if quants_dest_lot_id[0].product_id.tracking == 'lot':
                        if quants_dest_lot_id[0].reserved_quantity:
                            old_qty = quants_dest_lot_id[0].quantity
                            quants_dest_lot_id[0].quantity = old_qty - move.product_uom_qty
                            quants_dest_lot_id[0].quantity = quants_dest_lot_id[0].quantity

                            if move.restrict_partner_id.id == quants_dest_lot_id[0].owner_id.id:
                                quants_dest_lot_id[0].owner_id = False

                            if quants_dest_lot_id[0].quantity <= 0:
                                quants_dest_lot_id[0].unlink()


                        else:
                            old_qty = quants_dest_lot_id[0].quantity
                            quants_dest_lot_id[0].quantity = old_qty - move.product_uom_qty

                            if move.restrict_partner_id.id == quants_dest_lot_id[0].owner_id.id:
                                quants_dest_lot_id[0].owner_id = False

                            if quants_dest_lot_id[0].quantity <= 0:
                                quants_dest_lot_id[0].unlink()
                    else:
                        if quants_dest_lot_id[0].reserved_quantity:
                            old_qty = quants_dest_lot_id[0].quantity
                            quants_dest_lot_id[0].quantity = old_qty - move.product_uom_qty
                            quants_dest_lot_id[0].quantity = quants_dest_lot_id[0].quantity

                            if move.restrict_partner_id.id == quants_dest_lot_id[0].owner_id.id:
                                quants_dest_lot_id[0].owner_id = False

                            if quants_dest_lot_id[0].quantity <= 0:
                                quants_dest_lot_id[0].unlink()

                        else:
                            old_qty = quants_dest_lot_id[0].quantity
                            quants_dest_lot_id[0].quantity = old_qty - move.product_uom_qty

                            if move.restrict_partner_id.id == quants_dest_lot_id[0].owner_id.id:
                                quants_dest_lot_id[0].owner_id = False

                            if quants_dest_lot_id[0].quantity <= 0:
                                quants_dest_lot_id[0].unlink()
                if quants_src_lot_id:

                    if quants_src_lot_id[0].product_id.tracking == 'lot':
                        old_qty = quants_src_lot_id[0].quantity
                        quants_src_lot_id[0].quantity = old_qty + move.product_uom_qty

                        if move.restrict_partner_id.id == quants_src_lot_id[0].owner_id.id:
                            quants_src_lot_id[0].owner_id = False

                        if quants_src_lot_id[0].quantity <= 0:
                            quants_src_lot_id[0].unlink()
                    else:

                        if move.restrict_partner_id.id == quants_src_lot_id[0].owner_id.id:
                            quants_src_lot_id[0].owner_id = False
                        if quants_src_lot_id[0].quantity <= 0:
                            quants_src_lot_id[0].unlink()
            else:

                quants_dest_id = self.env['stock.quant'].sudo().search(
                    [('product_id', '=', move.product_id.id), ('location_id', '=', move.location_dest_id.id)])
                quants_src_id = self.env['stock.quant'].sudo().search(
                    [('product_id', '=', move.product_id.id), ('location_id', '=', move.location_id.id)])
                if quants_dest_id:
                    if quants_dest_id[0].reserved_quantity:
                        old_qty = quants_dest_id[0].quantity
                        quants_dest_id[0].quantity = old_qty - move.product_uom_qty
                        quants_dest_id[0].quantity = quants_dest_id[0].quantity

                        if move.restrict_partner_id.id == quants_dest_id[0].owner_id.id:
                            quants_dest_id[0].owner_id = False
                    else:
                        old_qty = quants_dest_id[0].quantity
                        quants_dest_id[0].quantity = old_qty - move.product_uom_qty
                        if move.restrict_partner_id.id == quants_dest_id[0].owner_id.id:
                            quants_dest_id[0].owner_id = False
                if quants_src_id:
                    old_qty = quants_src_id[0].quantity
                    quants_src_id[0].quantity = old_qty + move.product_uom_qty
                    if move.restrict_partner_id.id == quants_src_id[0].owner_id.id:
                        quants_src_id[0].owner_id = False

    def action_reset_draft(self):
        self.write({'line_ids': [(5,)], 'state': 'draft'})

    def action_check(self):
        """ Checks the inventory and computes the stock move to do """
        # tde todo: clean after _generate_moves
        for inventory in self.filtered(lambda x: x.state not in ('done','cancel')):
            inventory.with_context(prefetch_fields=False,inventory=True).mapped('move_ids').unlink()
            inventory.line_ids._generate_moves()


class StockMove(models.Model):
    _inherit = 'stock.move'

    def _action_cancel(self):
        if self._context.get('inventory'):
            # if any(move.state == 'done' and not move.scrapped for move in self):
            #     raise UserError(_('You cannot cancel a stock move that has been set to \'Done\'.'))
            moves_to_cancel = self.filtered(lambda m: m.state != 'cancel')
            # self cannot contain moves that are either cancelled or done, therefore we can safely
            # unlink all associated move_line_ids
            moves_to_cancel.with_context(inventory=True)._do_unreserve()

            for move in moves_to_cancel:
                siblings_states = (move.move_dest_ids.mapped('move_orig_ids') - move).mapped('state')
                if move.propagate_cancel:
                    # only cancel the next move if all my siblings are also cancelled
                    if all(state == 'cancel' for state in siblings_states):
                        move.move_dest_ids.filtered(lambda m: m.state != 'done')._action_cancel()
                else:
                    if all(state in ('done', 'cancel') for state in siblings_states):
                        move.move_dest_ids.write({'procure_method': 'make_to_stock'})
                        move.move_dest_ids.write({'move_orig_ids': [(3, move.id, 0)]})
            self.write({'state': 'cancel', 'move_orig_ids': [(5, 0, 0)]})
            return True
        return super(StockMove, self)._action_cancel()

    def _do_unreserve(self):
        if self._context.get('inventory'):
            moves_to_unreserve = self.env['stock.move']
            for move in self:
                if move.state == 'cancel':
                    # We may have cancelled move in an open picking in a "propagate_cancel" scenario.
                    continue
                if move.state == 'done':
                    if move.scrapped:
                        # We may have done move in an open picking in a scrap scenario.
                        continue
                    # else:
                    #     raise UserError(_('You cannot unreserve a stock move that has been set to \'Done\'.'))
                moves_to_unreserve |= move
            moves_to_unreserve.with_context(prefetch_fields=False).mapped('move_line_ids').with_context(inventory=True).unlink()
            return True
        else:
            return super(StockMove, self)._do_unreserve()


class StockMoveLine(models.Model):
    _inherit = 'stock.move.line'

    def unlink(self):
        if self._context.get('inventory'):
            precision = self.env['decimal.precision'].precision_get('Product Unit of Measure')
            for ml in self:
                if ml.product_id.type == 'product' and not ml._should_bypass_reservation(ml.location_id) and not float_is_zero(ml.product_qty, precision_digits=precision):
                    self.env['stock.quant']._update_reserved_quantity(ml.product_id, ml.location_id, -ml.product_qty, lot_id=ml.lot_id, package_id=ml.package_id, owner_id=ml.owner_id, strict=True)
            moves = self.mapped('move_id')
            if moves:
                moves._recompute_state()
            return models.Model.unlink(self)
        else:
            return super(StockMoveLine, self).unlink()