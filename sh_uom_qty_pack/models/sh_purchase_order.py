# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import models, fields, api, _
from odoo.tools.float_utils import float_compare


class sh_purchase_order_line(models.Model):
    _inherit = "purchase.order.line"
    
    sh_bag_qty = fields.Integer('Bag Quantity')
    sh_qty_in_bag = fields.Float(
        related="product_id.sh_qty_in_bag", string="Quantity in Bag")

    @api.onchange('sh_bag_qty')
    def onchange_product_uom_qty_sh(self):
        if self and self.sh_bag_qty > 0:
            self.product_qty = self.sh_bag_qty * self.product_id.sh_qty_in_bag
            
    
    def _prepare_account_move_line(self, move):
        self.ensure_one()
        if self.product_id.purchase_method == 'purchase':
            qty = self.product_qty - self.qty_invoiced
        else:
            qty = self.qty_received - self.qty_invoiced
        if float_compare(qty, 0.0, precision_rounding=self.product_uom.rounding) <= 0:
            qty = 0.0

        if self.currency_id == move.company_id.currency_id:
            currency = False
        else:
            currency = move.currency_id

        return {
            'name': '%s: %s' % (self.order_id.name, self.name),
            'move_id': move.id,
            'currency_id': currency and currency.id or False,
            'purchase_line_id': self.id,
            'date_maturity': move.invoice_date_due,
            'product_uom_id': self.product_uom.id,
            'product_id': self.product_id.id,
            'price_unit': self.price_unit,
            'quantity': qty,
            'partner_id': move.partner_id.id,
            'sh_bag_qty':self.sh_bag_qty,
            'analytic_account_id': self.account_analytic_id.id,
            'analytic_tag_ids': [(6, 0, self.analytic_tag_ids.ids)],
            'tax_ids': [(6, 0, self.taxes_id.ids)],
            'display_type': self.display_type,
        }


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    sh_enable_quantity = fields.Boolean(
        "Enable Quantity", related="company_id.sh_show_bag_size_purchase_order_line")
    sh_enable_quantity_in_report = fields.Boolean(
        "Enable Quantity In Report", related="company_id.sh_show_bag_size_in_purchase_report"
    )
