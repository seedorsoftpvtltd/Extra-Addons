# -*- coding: utf-8 -*-

from odoo import api, models, fields


class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    @api.depends('order_line.price_total', 'date_order')
    def _amount_all(self):
        res = super(PurchaseOrder, self)._amount_all()
        for order in self:
            amount_untaxed_signed = 0.0
            currency = order.currency_id
            company = order.company_id
            date = order.date_order or fields.Date.today()

            amount_untaxed_signed = currency._convert(
                order.amount_untaxed, company.currency_id, company,
                date
            )

            order.update(
                {
                    'amount_untaxed_signed':amount_untaxed_signed,
                    'diff':abs(
                        order.amount_untaxed -
                        amount_untaxed_signed)
                }
            )

        return res

    company_currency_id = fields.Many2one(
        'res.currency',
        string="Company Currency",
        related='company_id.currency_id',
        readonly=True
    )
    amount_untaxed_signed = fields.Monetary(
        compute='_amount_all',
        string='Untaxed Amount',
        readonly=True,
        store=True,
        currency_field='company_currency_id',
        compute_sudo=True
    )
    diff = fields.Monetary(
        compute='_amount_all',
        string='diff',
    )


class PurchaseOrderLine(models.Model):
    _inherit = "purchase.order.line"

    @api.depends('price_subtotal', 'order_id.date_order',
                 'qty_invoiced')
    def _compute_amount_signed(self):
        price_subtotal = 0.0
        product_qty_invoiced_signed = 0.0
        for line in self:
            currency = line.order_id.currency_id
            company = line.order_id.company_id
            date = line.order_id.date_order or fields.Date.today()

            price_subtotal = currency._convert(
                line.price_subtotal, company.currency_id, company,
                date)

            price = line.qty_invoiced * line.price_unit
            product_qty_invoiced_signed = \
                currency._convert(
                    price, company.currency_id, company, date
                )

            line.update(
                {
                    'price_subtotal_signed':price_subtotal,
                    'product_qty_invoiced_signed':product_qty_invoiced_signed,
                }
            )

    company_currency_id = fields.Many2one(
        'res.currency',
        related='order_id.company_currency_id',
        readonly=True,
        help='Utility field to express amount currency'
    )
    price_subtotal_signed = fields.Monetary(
        compute='_compute_amount_signed',
        string='Subtotal',
        store=True,
        currency_field='company_currency_id',
        compute_sudo=True
    )
    product_qty_invoiced_signed = fields.Monetary(
        compute='_compute_amount_signed',
        string='Billed',
        store=True,
        currency_field='company_currency_id',
        compute_sudo=True
    )