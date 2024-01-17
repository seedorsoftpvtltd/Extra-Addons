# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import models, fields, api


class ShSaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    sh_bag_qty = fields.Integer()
    sh_qty_in_bag = fields.Float(related="product_id.sh_qty_in_bag")

    @api.onchange("sh_bag_qty")
    def onchange_product_uom_qty_sh(self):
        if self and self.sh_bag_qty > 0:
            self.product_uom_qty = self.sh_bag_qty * self.product_id.sh_qty_in_bag

    def _prepare_invoice_line(self, **optional_values):
        self.ensure_one()
        res = super(ShSaleOrderLine, self)._prepare_invoice_line(
            **optional_values)
        res.update({
            "sh_bag_qty": self.sh_bag_qty,
        })
        return res


class ShSaleOrder(models.Model):
    _inherit = 'sale.order'

    sh_enable_quantity = fields.Boolean(
        "Enable Quantity", related="company_id.sh_show_bag_size_order_line")
    sh_enable_quantity_in_report = fields.Boolean(
        "Enable Quantity In Report", related="company_id.sh_show_bag_size_in_report"
    )
