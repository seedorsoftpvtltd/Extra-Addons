# -*- coding: utf-8 -*-
# See LICENSE-DOC file for full copyright and licensing details

from odoo import models, fields, api, _


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    margin_percentage = fields.Float(string='Margin (%)')

    def action_update_margin(self):
        for line in self:
            sale_margin_percentage = line.margin_percentage
            for rec in line.order_line:
#                 rec.margin_percentage = sale_margin_percentage
                rec.update({
                'margin_percentage': sale_margin_percentage,
                })
                rec.price_unit = (
                rec.product_id.standard_price
                + ((rec.margin_percentage * rec.product_id.standard_price) / 100)
            )


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    margin_percentage = fields.Float(string='Margin (%)')

    @api.onchange('margin_percentage', 'product_id')
    def onchange_margin_percentage(self):
        if self.margin_percentage and self.product_id.standard_price:
            self.price_unit = (
                self.product_id.standard_price
                + ((self.margin_percentage * self.product_id.standard_price) / 100)
            )

