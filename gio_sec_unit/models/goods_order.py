from odoo import models, fields, api, _

class GoodsOrderLine(models.Model):
    _inherit = 'goods.order.line'

    sh_sec_qty = fields.Float("Secondary Qty", digits='Product Unit of Measure')
    sh_sec_uom = fields.Many2one("uom.uom", 'Secondary UOM')
    sh_is_secondary_unit = fields.Boolean("Related Sec Uni", related="product_id.sh_is_secondary_unit")
    category_id = fields.Many2one("uom.category", "Category", related="product_uom.category_id")

    @api.onchange('product_uom_qty', 'product_uom')
    def onchange_product_uom_qty_sh(self):
        if self and self.sh_is_secondary_unit == True and self.sh_sec_uom:
            self.sh_sec_qty = self.product_uom._compute_quantity(self.product_uom_qty, self.sh_sec_uom)

    @api.onchange('sh_sec_qty', 'sh_sec_uom')
    def onchange_sh_sec_qty_sh(self):
        if self and self.sh_is_secondary_unit == True and self.product_uom:
            self.product_uom_qty = self.sh_sec_uom._compute_quantity(self.sh_sec_qty, self.product_uom)

    @api.onchange('product_id')
    def onchange_secondary_uom(self):
        if self:
            for rec in self:
                if rec.product_id.sh_is_secondary_unit == True and rec.product_id.uom_id:
                    rec.sh_sec_uom = rec.product_id.sh_secondary_uom.id
                elif rec.product_id.sh_is_secondary_unit == False:
                    rec.sh_sec_uom = False
                    rec.sh_sec_qty = 0.0

class sh_stock_move(models.Model):
    _inherit = "stock.move"

    # sh_sec_done_qty = fields.Float("Secondary Done Qty", digits='Product Unit of Measure', store=True, copy=False,
    #                                compute="compute_product_uom_done_qty_sh")

    @api.model
    def create(self, vals):
        res = super(sh_stock_move, self).create(vals)
        if res.goods_line_id and res.goods_line_id.sh_is_secondary_unit == True and res.goods_line_id.sh_sec_uom:
            res.update({'sh_sec_uom': res.goods_line_id.sh_sec_uom.id, 'sh_sec_qty': res.goods_line_id.sh_sec_qty})
        return res

    @api.depends('quantity_done')
    def compute_product_uom_done_qty_sh(self):
        for rec in self:
            if rec and rec.sh_is_secondary_unit == True and rec.sh_sec_uom:
                rec.sh_sec_done_qty = rec.product_uom._compute_quantity(rec.quantity_done, rec.sh_sec_uom)
            else:
                rec.sh_sec_done_qty = 0