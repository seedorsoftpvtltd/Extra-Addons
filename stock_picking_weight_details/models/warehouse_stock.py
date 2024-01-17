from odoo import models, fields, api, _

class WarehouseOrderLine(models.Model):
    _inherit = "warehouse.order.line"


    net_weight = fields.Float(string="Net Weight(kg)" , compute="compute_net_weight", readonly=False)
    gross_weight = fields.Float(string="Gross Weight(kg)")
    value_goods = fields.Float(string="Value",compute="compute_value_goods", readonly=False)
    volume = fields.Float(string="Volume",compute="compute_volume", readonly=False)
    # hs_code = fields.Char(string='HS Code', related="product_id.default_code", readonly=False)

    @api.depends('product_id','product_qty')
    def compute_net_weight(self):
        self.currency_id = self.order_id.currency_id
        for rec in self:
            rec.net_weight = rec.product_id.weight * rec.product_qty

    @api.depends('product_id','product_qty')
    def compute_value_goods(self):
        for rec in self:
            rec.value_goods =  rec.product_id.value_goods * rec.product_qty

    @api.depends('product_id','product_qty')
    def compute_volume(self):
        for rec in self:
            rec.volume =  rec.product_id.volume * rec.product_qty

class StockMove(models.Model):
    _inherit = "stock.move"

    net_weight = fields.Float(string="Net Weight(kg)", compute="compute_net_weight", readonly=False)
    gross_weight = fields.Float(string="Gross Weight(kg)", related='warehouse_line_id.gross_weight', readonly=False)
    volume = fields.Float(string="Volume",compute="compute_volume", readonly=False)
    value_goods = fields.Float(string="Value", compute="compute_value_goods", readonly=False)

    currency_id = fields.Many2one(related='company_id.currency_id')
    hs_code = fields.Char(string='HS Code', related="product_id.default_code", readonly=False)
    per_boe = fields.Char(string="Item No as per BOE")

    @api.depends('product_id','product_uom_qty','quantity_done')
    def compute_net_weight(self):
        for rec in self:
            if rec.quantity_done > 0:
                rec.net_weight = rec.product_id.weight * rec.quantity_done
                break
            elif rec.product_uom_qty:
                rec.net_weight = rec.product_id.weight * rec.product_uom_qty
            else:
                rec.net_weight = 0

    @api.depends('product_id','product_uom_qty','quantity_done')
    def compute_volume(self):
        for rec in self:
            if rec.quantity_done > 0:
                rec.volume = rec.product_id.volume * rec.quantity_done
                break
            elif rec.product_uom_qty:
                rec.volume = rec.product_id.volume * rec.product_uom_qty
            else:
                rec.volume = 0

    @api.depends('product_id', 'product_uom_qty', 'quantity_done')
    def compute_value_goods(self):
        for rec in self:
            rec.value_goods =  rec.product_id.value_goods * rec.product_qty

class StockMoveLine(models.Model):
    _inherit = "stock.move.line"

    net_weight = fields.Float(string="Net Weight(kg)")
    gross_weight = fields.Float(string="Gross Weight(kg)", related='move_id.gross_weight')
    volume = fields.Float(string="Volume",related='move_id.volume')
    # value_goods = fields.Float(string="Value", related='move_id.value')
