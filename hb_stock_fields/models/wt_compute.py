from odoo import api, fields, models, _
from odoo.exceptions import UserError, AccessError, MissingError, ValidationError


class StockMoveWtComp(models.Model):
    _inherit = 'stock.move'

    freeport_diff = fields.Float(string='Free Port Difference for gw', store=True, digits=(5, 3))
    freeport_diff_nw = fields.Float(string='Free Port Difference for nw', store=True, digits=(5, 3))
    freeport_diff_vol = fields.Float(string='Free Port Difference for vol', store=True, digits=(5, 3))
    apply_free_port_charge = fields.Boolean(string="Apply Free port difference", store=True)
    x_gross_weight = fields.Float(string="Gross Weight / Qty", store=True)
    x_net_weight = fields.Float(string="Net Weight / Qty", store=True)
    net_weightt = fields.Float(string="Net Weight(kg)", store=True, related='warehouse_line_id.net_weight')

    @api.constrains('product_uom_qty', 'gross_weight')
    def divide_number_with_rounding(self):
        for rec in self:
            if rec.picking_id:
                if rec.picking_id.picking_type_id.code == 'incoming':
                    number = rec.gross_weight
                    num_pieces = int(rec.quantity_done if rec.quantity_done > 0 else rec.product_uom_qty)
                    print(num_pieces, '----Quantity')
                    print(number, '----Weight')
                    if num_pieces <= 1:
                        raise ValueError("Number of pieces should be greater than 1")
                    unit_weightt = number / num_pieces
                    unit_weight = round(unit_weightt, 3)
                    u = unit_weight * (num_pieces - 1)
                    v = round((number - u), 3)
                    # pieces = [unit_weight] * (num_pieces - 1)
                    # pieces.append(v)
                    rec['freeport_diff'] = v
                    rec['x_gross_weight'] = unit_weight

    @api.constrains('product_uom_qty', 'net_weightt')
    def divide_number_with_rounding_for_nw(self):
        for rec in self:
            if rec.picking_id:
                if rec.picking_id.picking_type_id.code == 'incoming':
                    number = rec.net_weightt
                    num_pieces = int(rec.quantity_done if rec.quantity_done > 0 else rec.product_uom_qty)
                    print(num_pieces, '----Quantity')
                    print(number, '----Weight')
                    if num_pieces <= 1:
                        raise ValueError("Number of pieces should be greater than 1")
                    unit_weightt = number / num_pieces
                    unit_weight = round(unit_weightt, 3)
                    u = unit_weight * (num_pieces - 1)
                    v = round((number - u), 3)
                    # pieces = [unit_weight] * (num_pieces - 1)
                    # pieces.append(v)
                    rec['freeport_diff_nw'] = v
                    rec['x_net_weight'] = unit_weight

    @api.onchange('qty_done', 'product_uom_qty', 'gross_weight')
    def onchange_divide_number_with_rounding(self):
        if self.picking_id:
            if self.picking_id.picking_type_id.code == 'incoming':
                number = self.gross_weight
                num_pieces = int(self.quantity_done if self.quantity_done > 0 else self.product_uom_qty)
                print(num_pieces, '----Quantity')
                print(number, '----Weight')
                if num_pieces <= 1:
                    raise ValueError("Number of pieces should be greater than 1")
                unit_weightt = number / num_pieces
                unit_weight = round(unit_weightt, 3)
                u = unit_weight * (num_pieces - 1)
                v = round((number - u), 3)
                # pieces = [unit_weight] * (num_pieces - 1)
                # pieces.append(v)
                self['freeport_diff'] = v
                self['x_gross_weight'] = unit_weight

    @api.onchange('qty_done', 'product_uom_qty', 'net_weightt')
    def onchange_divide_number_with_rounding_nw(self):
        if self.picking_id:
            if self.picking_id.picking_type_id.code == 'incoming':
                number = self.net_weightt
                num_pieces = int(self.quantity_done if self.quantity_done > 0 else self.product_uom_qty)
                print(num_pieces, '----Quantity')
                print(number, '----Weight')
                if num_pieces <= 1:
                    raise ValueError("Number of pieces should be greater than 1")
                unit_weightt = number / num_pieces
                unit_weight = round(unit_weightt, 3)
                u = unit_weight * (num_pieces - 1)
                v = round((number - u), 3)
                # pieces = [unit_weight] * (num_pieces - 1)
                # pieces.append(v)
                self['freeport_diff_nw'] = v
                self['x_net_weight'] = unit_weight

    def weight_diff_manage(self):
        for rec in self:
            if rec.freeport_diff != 0 or rec.freeport_diff_nw != 0:
                if rec.move_line_ids and rec.apply_free_port_charge == False:
                    count = 0
                    for ml in rec.move_line_ids:
                        print(ml.id)
                        if count == 0 and rec.apply_free_port_charge == False and ml.qty_done > 1:
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
                            ml._compute_weight()

                        if count == 0 and rec.apply_free_port_charge == False and ml.qty_done == 1:
                            ml['freeport_diff_applied'] = True
                            rec['apply_free_port_charge'] = True
                            # copy._compute_weight()
                            ml._compute_weight()
                        if count == 0 and rec.apply_free_port_charge == False and ml.qty_done == 0:
                            raise ValueError("Enter the done Quantity!")


class StockMoveLineWtComp(models.Model):
    _inherit = 'stock.move.line'

    freeport_diff_applied = fields.Boolean(string="Free Port Difference Applied", store=True)
    x_weight = fields.Float(string="Weight", store=True)
    net_weight = fields.Float(string="Net Weight(kg)", store=True)
    total_nw = fields.Float(string="Net Weight", store=True)
    total_gw = fields.Float(string="Gross Weight", store=True)

    @api.onchange('x_weight', 'qty_done')
    def compute_total_gw(self):
        self['total_gw'] = self.x_weight * self.qty_done

    @api.onchange('net_weight', 'qty_done')
    def compute_total_nw(self):
        self['total_nw'] = self.net_weight * self.qty_done

    @api.constrains('x_weight', 'qty_done')
    def compute_total_gww(self):
        for rec in self:
            rec['total_gw'] = rec.x_weight * rec.qty_done

    @api.constrains('net_weight', 'qty_done')
    def compute_total_nww(self):
        for rec in self:
            rec['total_nw'] = rec.net_weight * rec.qty_done

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
                    vals = {'x_weight': rec.x_weight,
                            'gross_weight': rec.x_weight,
                            }
                    rec.lot_id.write(vals)
                # else:
                #     rec['x_weight'] = rec.lot_id.x_weight

    @api.constrains('move_id', 'freeport_diff_applied', 'lot_id', 'product_id', 'qty_done')
    def _compute_weight(self):
        print('--------------------------------------------------------------------')
        if self.picking_code == 'incoming':
            if self.move_id:
                print(self.freeport_diff_applied)
                if self.freeport_diff_applied == True:
                    self['x_weight'] = self.move_id.freeport_diff
                    self['net_weight'] = self.move_id.freeport_diff_nw
                else:
                    self['x_weight'] = self.move_id.x_gross_weight
                    self['net_weight'] = self.move_id.x_net_weight
        else:
            print(self.lot_id)
            if self.lot_id.x_weight:
                self['x_weight'] = self.lot_id.x_weight
                self['net_weight'] = self.lot_id.net_weight
            else:
                self['x_weight'] = self.product_id.weight
                self['net_weight'] = self.product_id.weight

    # def button_confirm(self):
    #     res = super(StockMoveLineWtComp, self).button_confirm()
    #     self._compute_weight()
    #     return res


class StockProductionLotwt(models.Model):
    _inherit = "stock.production.lot"

    x_weight = fields.Float(string="Weight", store=True)


class WarehouseOrderLine(models.Model):
    _inherit = "warehouse.order.line"

    net_weight = fields.Float(string="Net Weight(kg)", store=True)

    @api.onchange('product_id', 'product_qty')
    def compute_net_weight(self):
        self.currency_id = self.order_id.currency_id
        for rec in self:
            if rec.product_id.weight > 0:
                rec.net_weight = rec.product_id.weight * rec.product_qty
