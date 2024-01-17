from odoo.http import request
from odoo import api, fields, models, tools, osv, http, _


class batchserialLot(models.Model):
    _inherit = 'stock.production.lot'

    serialno = fields.Many2one('stock.serial', string="Serial No")
    batchno = fields.Many2one('stock.batch', string="Batch No")


class batchserial(models.Model):
    _inherit = 'stock.move.line'

    serialno = fields.Many2one('stock.serial', string="Serial No")
    batchno = fields.Many2one('stock.batch', string="Batch No")

    @api.model_create_multi
    def create(self, vals_list):
        print('oooooooooooooooooooo')
        res = super(batchserial, self).create(vals_list)
        if self.picking_code == 'incoming':
            if self.batchno:
                if self.lot_id:
                    self.lot_id.batchno = self.batchno.id
                    self.batchno.product_id = self.product_id.id
                    self.batchno.lot_id = self.lot_id.id

            if self.serialno:
                if self.lot_id:
                    self.lot_id.serialno = self.serialno.id
                    self.serialno.product_id = self.product_id.id
                    self.serialno.lot_id = self.lot_id.id

        return res

    def write(self, vals):
        print('qqqqqqqqqqqqqqqqqq')
        res = super(batchserial, self).write(vals)
        for rec in self:
            if rec.picking_code == 'incoming':
                if vals.get('serialno'):
                    if rec.lot_id:
                        rec.lot_id.serialno = rec.serialno.id
                        rec.serialno.product_id = rec.product_id.id
                        rec.serialno.lot_id = rec.lot_id.id
                if vals.get('batchno'):
                    if rec.lot_id:
                        rec.lot_id.batchno = rec.batchno.id
                        rec.batchno.product_id = rec.product_id.id
                        rec.batchno.lot_id = rec.lot_id.id

        return res


class StockMoveL(models.Model):
    _inherit = 'stock.move.line'
    # for rec in self.move_line_ids_without_package:
    #     rec['lot_id'] = rec.move_id.goods_line_id.lot_ids.id
    @api.model_create_multi
    def create(self, vals):
        res = super(StockMoveL, self).create(vals)
        for rec in self.move_id.goods_line_id.lot_ids:
            vals['lot_id'] = rec.id
            # print(vals)
            lot = self.env['stock.production.lot'].browse(vals['lot_id'])
            # print(lot)

            lot.quant_ids.reserved_quantity = 0

        # print(res.lot_id)
        return res

    def write(self, vals):
        vals['product_uom_qty'] = 0
        for rec in  self.move_id.goods_line_id.lot_ids:
            vals['lot_id'] = rec.id
            # print(vals)
            lot = self.env['stock.production.lot'].browse(vals['lot_id'])
            # print(lot)

            lot.quant_ids.reserved_quantity = 0

        # print(self.lot_id)
        # print('lotttttttttttttttttttttttttt')
        return super(StockMoveL, self).write(vals)



class StockMove(models.Model):
    _inherit = 'stock.move'

    lot_ids = fields.Many2many('stock.production.lot', string="Crate", copy=False)
    assign_lot = fields.Boolean(string='Assign Lot')

    def _action_assign(self):
        res = super(StockMove, self)._action_assign()
        for move in self:
            if not move.assign_lot:
                move.move_line()
                move.assign_lot = True

        return True

    def move_line(self):
        for move in self:
            if move.goods_line_id.lot_ids:
                # move.move_line_ids.unlink()
                for lot in move.goods_line_id.lot_ids:
                    vals = {
                        'move_id': move.id,
                        'product_id': move.product_id.id,
                        'product_uom_id': move.product_uom.id,
                        'location_id': move.location_id.id,
                        'location_dest_id': move.location_dest_id.id,
                        'picking_id': move.picking_id.id,
                        'lot_id': lot.id,
                    }
                    self.env['stock.move.line'].create(vals)
