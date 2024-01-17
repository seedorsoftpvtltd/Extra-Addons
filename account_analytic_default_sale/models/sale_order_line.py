# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing
# details.

from odoo import api, fields, models


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    account_analytic_id = fields.Many2one(
        'account.analytic.account',
        string='Analytic Account'
    )
    analytic_tag_ids = fields.Many2many(
        'account.analytic.tag',
        string='Analytic Tags'
    )

    @api.onchange('product_id', 'order_id.date_order')
    def _onchange_product_id_date(self):
        default_analytic_account = self.env[
            'account.analytic.default'].account_get(
            product_id=self.product_id.id,
            partner_id=self.order_id.partner_id.id,
            user_id=self.env.uid, date=self.order_id.date_order)
        if default_analytic_account:
            self.account_analytic_id = \
                default_analytic_account.analytic_id.id
            self.analytic_tag_ids = [
                (6, 0, default_analytic_account.analytic_tag_ids.ids)]