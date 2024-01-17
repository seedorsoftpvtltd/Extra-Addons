from odoo import api, fields, models, _
from odoo.exceptions import UserError, AccessError, MissingError, ValidationError


class StockMoveWtComp(models.Model):
    _inherit = 'stock.move'

    freeport_diff = fields.Float(string='Free Port Difference', store=True, digits=(5, 3))
    apply_free_port_charge = fields.Boolean(string="Apply Free port difference", store=True)

    @api.onchange('qty_done', 'product_uom_qty', 'gross_weight')
    def divide_number_with_rounding(self):
        number = self.gross_weight
        num_pieces = int(self.quantity_done if self.quantity_done > 0 else self.product_uom_qty)
        print(num_pieces, '----Quantity')
        print(number, '----Weight')
        if num_pieces <= 1:
            raise ValueError("Number of pieces should be greater than 1")
        integer_part = int(number)
        decimal_part = number - integer_part
        quotient = decimal_part / (num_pieces - 1)
        rounded_quotient = round(quotient, 3)
        print(quotient, rounded_quotient)
        total_rounding_error = round(decimal_part - (rounded_quotient * (num_pieces - 1)), 3)
        print(total_rounding_error, '----Difference')
        pieces = [rounded_quotient] * (num_pieces - 1)
        pieces.append(rounded_quotient + total_rounding_error)
        pieces = [round(x + integer_part, 3) for x in pieces]
        print(pieces)
        unit_weight = number / num_pieces
        print(unit_weight, '----Unit Weight')
        self['freeport_diff'] = total_rounding_error
        self['x_weight'] = unit_weight

    def weight_diff_manage(self):
        for rec in self:
            if rec.move_line_ids and rec.apply_free_port_charge == False:
                count = 0
                for ml in rec.move_line_ids:
                    print(ml.id)
                    if count == 0 and rec.apply_free_port_charge == False:
                        print(ml, 'before copy')
                        copy = ml.copy()
                        print(copy, 'after copy')
                        qty = ml.qty_done
                        new_qty = qty - 1
                        ml['qty_done'] = new_qty
                        copy['qty_done'] = 1
                        copy['freeport_diff_applied'] = True
                        rec['apply_free_port_charge'] = True
                        copy._compute_weight()


class StockMoveLineWtComp(models.Model):
    _inherit = 'stock.move.line'

    freeport_diff_applied = fields.Boolean(string="Free Port Difference Applied", store=True)
    x_weight = fields.Float(string="Weight", store=True)

    @api.model
    def create(self, vals):
        res = super(StockMoveLineWtComp, self).create(vals)
        self._weight_to_lot()
        return res

    def write(self, vals):
        res = super(StockMoveLineWtComp, self).write(vals)
        self._weight_to_lot()
        return res

    def _weight_to_lot(self):
        for rec in self:
            if rec.lot_id:
                if rec.picking_code == 'incoming':
                    vals = {'x_weight': rec.x_weight}
                    rec.lot_id.write(vals)
                else:
                    rec['x_weight'] = rec.lot_id.x_weight

    @api.constrains('move_id', 'freeport_diff_applied', 'lot_id', 'product_id')
    def _compute_weight(self):
        print('--------------------------------------------------------------------')
        if self.picking_code == 'incoming':
            if self.move_id:
                print(self.freeport_diff_applied)
                if self.freeport_diff_applied == True:
                    self['x_weight'] = self.move_id.x_weight + self.move_id.freeport_diff
                else:
                    self['x_weight'] = self.product_id.weight
        else:
            print(self.lot_id)
            if self.lot_id.x_weight:
                self['x_weight'] = self.lot_id.x_weight
            else:
                self['x_weight'] = self.product_id.weight


class StockProductionLotwt(models.Model):
    _inherit = "stock.production.lot"

    x_weight = fields.Float(string="Weight", store=True)
