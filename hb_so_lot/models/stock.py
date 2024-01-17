from odoo import models
from odoo.exceptions import ValidationError

class StockPickingautoval(models.Model):
    _inherit = 'stock.picking'




    def ding(self):
        # lot = self.env['stock.picking'].search_count([('id','=',id)])

        print('function start')
        for picking in self:
            print("hello welcome data")
            print(picking.id)
            reserved_qty = sum(
                picking.move_ids_without_package.mapped(
                    'reserved_availability'))
            print(reserved_qty,'reserverd 1')
            product_qty = sum(
                picking.move_ids_without_package.mapped('product_uom_qty'))
            print(product_qty,'product 1')
            if reserved_qty == product_qty:
                print(reserved_qty == product_qty,'.........')
                for move in picking.move_lines:
                    move.quantity_done = move.product_uom_qty
                    print(move.quantity_done)
            # else:
            #     raise ValidationError("reserved_availability and product_uom_qty are not equal")

                print(picking, 'picking')
            if picking.state != 'done' and picking.state == 'assigned':
                print(picking.state,'......................>')
                picking.action_done()


            # else:
            #     raise ValidationError("reserved_availability ")




   

class StockMove(models.Model):
    _inherit = "stock.move"

    def _update_reserved_quantity(
        self,
        need,
        available_quantity,
        location_id,
        lot_id=None,
        package_id=None,
        owner_id=None,
        strict=True,
    ):
        if self._context.get("sol_lot_id"):
            lot_id = self.sale_line_id.lot_id
        return super()._update_reserved_quantity(
            need,
            available_quantity,
            location_id,
            lot_id=lot_id,
            package_id=package_id,
            owner_id=owner_id,
            strict=strict,
        )

    def _prepare_move_line_vals(self, quantity=None, reserved_quant=None):
        vals = super()._prepare_move_line_vals(
            quantity=quantity, reserved_quant=reserved_quant
        )
        if reserved_quant and self.sale_line_id.lot_id:
            vals["lot_id"] = self.sale_line_id.lot_id.id
        return vals
