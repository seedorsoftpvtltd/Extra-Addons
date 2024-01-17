# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import models, fields, api, _


class sh_stock_move(models.Model):
    _inherit = "stock.move"
    
    sh_bag_qty = fields.Integer('Bag Quantity')
    sh_qty_in_bag = fields.Float(
        related="product_id.sh_qty_in_bag", string="Quantity in Bag")
    
    @api.onchange('sh_bag_qty')
    def onchange_product_uom_qty(self):
        if self and self.sh_bag_qty > 0:
            self.product_uom_qty = self.sh_bag_qty * self.product_id.sh_qty_in_bag
            
    @api.model
    def create(self, vals):
        res = super(sh_stock_move, self).create(vals)
        if res.sale_line_id:
            res.update({'sh_bag_qty':res.sale_line_id.sh_bag_qty})
        elif res.purchase_line_id:
            res.update({'sh_bag_qty':res.purchase_line_id.sh_bag_qty})
        return res


class StockPicking(models.Model):

    _inherit = "stock.picking"

    sh_enable_quantity = fields.Boolean(
        "Enable Quantity", related="company_id.sh_show_bag_size_stock_move_ids")
    sh_enable_quantity_in_report = fields.Boolean(
        "Enable Quantity In Report", related="company_id.sh_show_bag_size_in_stock_report"
    )
