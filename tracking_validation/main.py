from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class StockMoveLine(models.Model):
    _inherit = "stock.move.line"

    @api.onchange('qty_done')
    def validation_track(self):
        if self.picking_id.picking_type_id.name == 'Pick':
            if self.product_id.tracking == 'lot':
                if self.qty_done > self.lot_id.product_qty:
                    raise ValidationError(_("""On Hand quantity for the Tracking Number is less than the Done quantity.
please select another Tracking Number"""))
