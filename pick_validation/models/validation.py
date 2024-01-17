from odoo import api, fields, models, _
from odoo.exceptions import UserError
class Stock_Picking(models.Model):
    _inherit='stock.picking'

    def button_validate(self):
        moves = super(Stock_Picking, self).button_validate()
        if self.picking_type_id.name == 'Delivery Orders' or self.picking_type_id.name == 'Pick':
            for rec in self:
                for move in rec.move_ids_without_package:
                    if move.product_uom_qty< move.quantity_done:
                      raise UserError(_('You Cannot Validate Done Quantity Which Is Greater Than Demand Quantity.'))
        return moves


