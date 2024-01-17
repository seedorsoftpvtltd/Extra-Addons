from odoo.http import request
from odoo import api, fields, models, tools, osv, http, _


class goodsissueorder(models.Model):
    _inherit = 'goods.order.line'

    serialno = fields.Many2many('stock.serial', string="Serial No")
    batchno = fields.Many2many('stock.batch', string="Batch No")
    lot_ids = fields.Many2many('stock.production.lot',string='Lot', copy=False)



class StockMoveLgio(models.Model):
    _inherit = 'stock.move.line'

    @api.model_create_multi
    def create(self, vals):
        res = super(StockMoveLgio, self).create(vals)
        print('//////////sl,bt////////')
        for rec in self.move_id.goods_line_id.serialno:
            vals['serialno'] = rec.id
        for rec in self.move_id.goods_line_id.batchno:
            vals['batchno'] = rec.id

        return res

    def write(self, vals):
        print('//////////sl,bt////////')

        for rec in self.move_id.goods_line_id.serialno:
            vals['serialno'] = rec.id
        for rec in self.move_id.goods_line_id.batchno:
            vals['batchno'] = rec.id

        return super(StockMoveLgio, self).write(vals)

    @api.onchange('serialno','batchno')
    def _onchange(self):
        if self.picking_code == 'internal':
            if self.serialno:
                self['lot_id'] = self.serialno.lot_id.id
            else:
                self['lot_id'] = self.batchno.lot_id.id


    # def move_line(self):
    #     for move in self:
    #         if move.sale_line_id.lot_ids:
    #             # move.move_line_ids.unlink()
    #             for lot in move.sale_line_id.lot_ids:
    #                 vals = {
    #                     'move_id': move.id,
    #                     'product_id': move.product_id.id,
    #                     'product_uom_id': move.product_uom.id,
    #                     'location_id': move.location_id.id,
    #                     'location_dest_id': move.location_dest_id.id,
    #                     'picking_id': move.picking_id.id,
    #                     'lot_id': lot.id,
    #                 }
    #                 self.env['stock.move.line'].create(vals)




