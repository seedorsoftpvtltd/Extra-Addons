from odoo import api, fields, models,_
from odoo.exceptions import ValidationError
import logging


_logger = logging.getLogger(__name__)
class AccountMoveLine(models.Model):
    _inherit = "stock.move.line"

    @api.constrains('qty_done')
    def _check_excess_qty(self):
        total=0
        if self.move_id.picking_id.picking_type_id.code == 'incoming':
            for ml in self.move_id.move_line_ids:
                     print(ml)
                     total=total+ml.qty_done
            print(total)
        if total > self.move_id.product_uom_qty:
                            print(self.move_id.product_uom_qty)
                            raise ValidationError(_(
                                "You can't able to set excess quantity for product %s.\n"
                                "Initial Demand: %s.\n"
                                "Done Quantity: %s."
                                % (self.move_id.product_id.name, self.move_id.product_uom_qty, total)
                            ))


    # @api.onchange('qty_done')
    # def _onchange_qty_done(self):
    #     for rec in self:
    #         if rec.move_id.picking_id.picking_type_id.code == 'incoming':
    #
    #
    #
    #             if len(line_item) > 1:
    #                 for i in range(len(line_item) - 1):
    #
    #                         total_qty += line_item[i].qty_done
    #                         print(line_item[i].qty_done)
    #                 print(total_qty)
    #             else:
    #
    #                 total_qty += line_item.qty_done
    #                 print(line_item.qty_done)
    #         if total_qty > rec.move_id.product_uom_qty:
    #
    #             raise ValidationError(_("You can't able to set excess quantity for product %s. "% (rec.move_id.product_id.name)))
    #
    #
