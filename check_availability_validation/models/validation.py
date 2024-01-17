
from odoo import api, fields, models, _, SUPERUSER_ID
from odoo.exceptions import UserError
from odoo.osv import expression
from odoo.tools.float_utils import float_compare, float_round, float_is_zero

class stock_move(models.Model):
    _inherit='stock.move'
    reserved = fields.Float('Reserved Avail', default=0.0)

class Picking(models.Model):
    _inherit='stock.picking'

    def action_assign(self):
        res = super(Picking, self).action_assign()
        for r in self:
            if self.picking_type_id.name == 'Pick':
                for rec in r.move_ids_without_package:
                        if rec.move_line_ids:
                            r = 0.0
                            for rec1 in rec.move_line_ids:
                                r = r + rec1.product_uom_qty
                            rec['reserved'] = r

                            if rec.reserved < rec.product_uom_qty:
                                raise UserError(_('Insufficient on hand stock for the product in inventory : %s.\nProduct has been already reserved for delivery.') % rec.product_id.name)
                        else:

                            raise UserError(_('Insufficient on hand stock for the product in inventory : %s.\nProduct has been already reserved for delivery.')% rec.product_id.name)


        return res
