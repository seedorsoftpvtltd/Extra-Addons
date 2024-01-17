# -*- coding: utf-8 -*-
##########################################################################
# Author      : Webkul Software Pvt. Ltd. (<https://webkul.com/>)
# Copyright(c): 2017-Present Webkul Software Pvt. Ltd.
# All Rights Reserved.
#
#
#
# This program is copyright property of the author mentioned above.
# You can`t redistribute it and/or modify it.
#
#
# You should have received a copy of the License along with this program.
# If not, see <https://store.webkul.com/license.html/>
##########################################################################

import logging
from dateutil.relativedelta import relativedelta
from re import template
from datetime import datetime, timedelta
from odoo import _, api, fields, models
from odoo.exceptions import UserError, ValidationError

_logger = logging.getLogger(__name__)


class ProductProduct(models.Model):
    _inherit = "product.product"

    activate_subscription = fields.Boolean(string="Is Subscription Type", default=False)
    subscription_plan_id = fields.Many2one(comodel_name="subscription.plan", string="Subscription Plan")

    @api.onchange('subscription_plan_id')
    def on_change_subscription_plan(self):
        for current_rec in self:
            override = current_rec.subscription_plan_id.override_product_price
            if current_rec.subscription_plan_id:
                if override:
                    current_rec.lst_price = current_rec.subscription_plan_id.plan_amount
                current_rec.type = 'service'

    @api.onchange('activate_subscription')
    def on_change_activate_subscription(self):
        for current_rec in self:
            if current_rec.activate_subscription:
                current_rec.invoice_policy = 'delivery'
                current_rec.type = 'service'
            else:
                current_rec.invoice_policy = 'order'

    #@api.multi
    def write(self, vals):
        if vals.get('activate_subscription'):
            vals['type'] = 'service'
        if vals.get('subscription_plan_id'):
            subscription_plan_id = self.env['subscription.plan'].browse(
                vals['subscription_plan_id'])
        return super(ProductProduct, self).write(vals)

    @api.depends('list_price', 'price_extra')
    def _compute_product_lst_price(self):
        res = super(ProductProduct, self)._compute_product_lst_price()
        for product in self:
            override = product.subscription_plan_id.override_product_price
            if override and product.activate_subscription and product.subscription_plan_id:
                product.lst_price = product.subscription_plan_id.plan_amount + product.price_extra
        return res

    #@api.multi
    def price_compute(self, price_type, uom=False, currency=False, company=False):
        res = super(ProductProduct, self).price_compute(price_type=price_type, uom=uom, currency=currency,
                                                        company=company)

        if not uom and self._context.get('uom'):
            uom = self.env['uom.uom'].browse(self._context['uom'])
        if not currency and self._context.get('currency'):
            currency = self.env['res.currency'].browse(self._context['currency'])

        products = self
        if price_type == 'standard_price':
            products = self.with_context(force_company=company and company.id or self._context.get('force_company',
                                                                                                   self.env.user.company_id.id)).sudo()

        prices = dict.fromkeys(self.ids, 0.0)
        for product in products:
            prices[product.id] = product[price_type] or 0.0
            if price_type == 'list_price':
                prices[product.id] += product.price_extra

            if uom:
                prices[product.id] = product.uom_id._compute_price(prices[product.id], uom)

            if currency:
                prices[product.id] = product.currency_id.compute(prices[product.id], currency)

            if product.activate_subscription:
                override = product.subscription_plan_id.override_product_price
                if override and product.activate_subscription and product.subscription_plan_id:
                    prices[product.id] = product.currency_id.compute(
                        product.subscription_plan_id.plan_amount + product.price_extra, currency)
        return prices


class ProductTemplate(models.Model):
    _inherit = "product.template"

    activate_subscription = fields.Boolean(related='product_variant_ids.activate_subscription',
                                           string='Is Subscription Type', readonly=False)
    subscription_plan_id = fields.Many2one(comodel_name="subscription.plan",
                                           related="product_variant_ids.subscription_plan_id",
                                           string="Subscription Plan", readonly=False)

    @api.model
    def create(self, vals):
        if vals.get('activate_subscription'):
            vals['type'] = 'service'
        template_id = super(ProductTemplate, self).create(vals)
        related_vals = {}
        if vals.get('activate_subscription'):
            related_vals['activate_subscription'] = vals['activate_subscription']
        if vals.get('subscription_plan_id'):
            related_vals['subscription_plan_id'] = vals['subscription_plan_id']
            subscription_plan_id = self.env['subscription.plan'].browse(
                vals['subscription_plan_id'])
        if related_vals:
            template_id.write(related_vals)
        return template_id

    #@api.multi
    def write(self, vals):
        if vals.get('activate_subscription'):
            vals['type'] = 'service'
        if vals.get('subscription_plan_id'):
            subscription_plan_id = self.env['subscription.plan'].browse(vals['subscription_plan_id'])
            if not subscription_plan_id.override_product_price:
                vals['list_price'] = subscription_plan_id.plan_amount
        for rec in self:
            res = super(ProductTemplate, self).write(vals)
            if vals.get('subscription_plan_id') and vals.get('list_price'):
                rec.product_variant_ids.write({'subscription_plan_id': vals['subscription_plan_id']})
                rec.product_variant_ids.write({'list_price': vals['list_price']})
            return res

    @api.onchange('activate_subscription')
    def on_change_activate_subscription(self):
        for current_rec in self:
            if current_rec.activate_subscription:
                current_rec.invoice_policy = 'delivery'
                current_rec.type = 'service'
            else:
                current_rec.invoice_policy = 'order'

    @api.onchange('subscription_plan_id')
    def on_change_subscription_plan(self):
        for current_rec in self:
            current_rec.list_price = current_rec.subscription_plan_id.plan_amount


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    #@api.multi
    def invoice_line_create(self, invoice_ids, qty):
        for current_rec in self:
            if current_rec.product_id.activate_subscription:
                pass
            else:
                return super(SaleOrderLine, current_rec).invoice_line_create(invoice_ids, qty)


class SaleOrder(models.Model):
    _inherit = 'sale.order'

   # @api.multi
    def _get_subscription_count(self):
        sub_obj = self.env['subscription.subscription']
        for current_record in self:
            current_record.subscription_count = sub_obj.search_count([('so_origin', '=', current_record.id)])

    def _get_invoiced(self):
#        res = super(SaleOrder, self)._get_invoiced()
#        invoice_ids_sub = self.env['account.move'].search([('name', '=', self.name)])
#        self.invoice_ids = invoice_ids_sub.union(self.invoice_ids)
#        self.invoice_count = len(self.invoice_ids)
#        res.invoice_ids = invoice_ids_sub.union(res.invoice_ids)
#        res.invoice_count = len(res.invoice_ids) 
#        return res
        res = super(SaleOrder, self)._get_invoiced()
        # invoice_ids_sub = self.env['account.move'].search([('name', '=', self.name)])
        # self.invoice_ids = invoice_ids_sub.union(self.invoice_ids)
        # self.invoice_count = len(self.invoice_ids)
        for order in self:
            invoice_ids_sub = self.env['account.move'].search([('name', '=', order.name)])
            order.invoice_ids = invoice_ids_sub.union(order.invoice_ids)
            order.invoice_count = len(order.invoice_ids)

        return res

    subscription_count = fields.Integer(
        compute=_get_subscription_count, string="#Subscription")
    subscription_ids = fields.One2many(
        "subscription.subscription", 'so_origin', string="Subscription",
        readonly=True, copy=False)

   # @api.multi
    def action_view_subscription(self):
        subscription_ids = self.env['subscription.subscription'].search([('so_origin', '=', self.id)])
        action = self.env.ref('subscription_management.action_subscription').read()[0]
        action['context'] = {}
        if len(subscription_ids) > 1:
            action['domain'] = "[('id','in',%s)]" % subscription_ids.ids
        elif len(subscription_ids) == 1:
            action['views'] = [(self.env.ref('subscription_management.subscription_subscription_form_view').id, 'form')]
            action['res_id'] = subscription_ids.ids[0]
        else:
            action = {'type': 'ir.actions.act_window_close'}
        return action

   # @api.multi
    def action_view_invoice(self):
        invoice_ids_sub = self.env['account.move'].search(
            [('name', '=', self.name)])
        self.invoice_ids = invoice_ids_sub.union(self.invoice_ids)
        return super(SaleOrder, self).action_view_invoice()

   # @api.multi
    def action_confirm(self):
        subscription = self.env['subscription.subscription'].sudo()
        trial_period_setting = self.env['res.config.settings'].sudo().get_values()['trial_period_setting']
        for order in self:
            res = super(SaleOrder, order).action_confirm()
            if res:
                for line in order.order_line:
                    if line.product_id:
                        if line.product_id.activate_subscription:
                            date = datetime.strptime(str(order.date_order), '%Y-%m-%d %H:%M:%S')

                            # import pdb
                            # pdb.set_trace()
                            if line.product_id.subscription_plan_id.trial_period:
                                if line.product_id.subscription_plan_id.trial_duration_unit == 'day':
                                    date = date + relativedelta(
                                        days=line.product_id.subscription_plan_id.trial_duration)
                                if line.product_id.subscription_plan_id.trial_duration_unit == 'month':
                                    date = date + relativedelta(
                                        months=line.product_id.subscription_plan_id.trial_duration)
                                if line.product_id.subscription_plan_id.trial_duration_unit == 'year':
                                    date = date + relativedelta(
                                        years=line.product_id.subscription_plan_id.trial_duration)
                            vals = {'customer_name': order.partner_id.id,
                                    'customer_billing_address': order.partner_invoice_id.id, 'source': 'so',
                                    'so_origin': order.id, 'product_id': line.product_id.id,
                                    'quantity': line.product_uom_qty, 'start_date': date, 'tax_id': [
                                    (6, 0, line.tax_id.ids)], 'sub_plan_id': line.product_id.subscription_plan_id.id,
                                    'unit': line.product_id.subscription_plan_id.unit,
                                    'duration': line.product_id.subscription_plan_id.duration, 'price': line.price_unit,
                                    'currency_id': order.pricelist_id.currency_id.id,
                                    'trial_period': line.product_id.subscription_plan_id.trial_period,
                                    'trial_duration_unit': line.product_id.subscription_plan_id.trial_duration_unit,
                                    'trial_duration': line.product_id.subscription_plan_id.trial_duration,
                                    'num_billing_cycle': -1 if line.product_id.subscription_plan_id.never_expires else line.product_id.subscription_plan_id.num_billing_cycle,
                                    'create_uid': self._uid}
                            if len(self.partner_id.all_subscription) != 0 and trial_period_setting == 'one_time':
                                if vals.get('trial_period'):
                                    vals['trial_period'] = False
                                    vals.pop('trial_duration_unit', None)
                                    vals.pop('trial_duration', None)
                                    vals.update({
                                        'start_date': order.date_order,
                                        # 'next_payment_date':datetime.strptime(order.date_order, '%Y-%m-%d %H:%M:%S') + relativedelta(days=1)
                                    })
                            elif trial_period_setting == 'product_based' and self.partner_id.all_subscription.filtered(
                                    lambda subscription: subscription.product_id == line.product_id):
                                if vals.get('trial_period'):
                                    vals['trial_period'] = False
                                    vals.pop('trial_duration_unit', None)
                                    vals.pop('trial_duration', None)
                                    vals.update({
                                        'start_date': order.date_order,
                                        # 'next_payment_date':datetime.strptime(order.date_order, '%Y-%m-%d %H:%M:%S') + relativedelta(days=1)
                                    })
                            subscription_id = subscription.create(vals)
                            subscription_id.get_confirm_subscription()
        return res

    #@api.multi
    def _cart_update(self, product_id=None, line_id=None, add_qty=0, set_qty=0, **kwargs):
        res = super(SaleOrder, self)._cart_update(product_id=product_id, line_id=line_id, add_qty=add_qty,
                                                  set_qty=set_qty, kwargs=kwargs)

        for product in self.order_line:
            override = product.product_id.subscription_plan_id.override_product_price
            if line_id is not False and override:
                order = self.sudo().browse(self.id)
                order_line = self._cart_find_product_line(product_id, line_id, **kwargs)[:1]
                product = self.env['product.product'].browse(int(product_id))
                if product.activate_subscription:
                    values = {
                        'price_unit': product.product_tmpl_id.currency_id._convert(
                            product.subscription_plan_id.plan_amount + product.price_extra,
                            order.pricelist_id.currency_id,
                            product.product_tmpl_id._get_current_company(pricelist=order.pricelist_id),
                            fields.Date.today()
                        ),
                    }
                    order_line.write(values)
        return res

    @api.onchange('order_line')
    def subscription_product_order_line(self):
        for product in self.order_line:
            override = product.product_id.subscription_plan_id.override_product_price
            if override and product.product_id.activate_subscription:
                product.price_unit = product.product_id.subscription_plan_id.plan_amount + product.product_id.price_extra


class AccountInvoice(models.Model):
    _inherit = "account.move"

    is_subscription = fields.Boolean(string="Is Subscription", copy=False)
    startsubs_date = fields.Datetime(string="Start Date of Subscription")
    endsubs_date = fields.Datetime(string="End Date of Subscription")

    def make_payment(self, invoice_generated):
        journal_id = self.env["ir.default"].get('res.config.settings', 'journal_id')
        if not journal_id:
            raise UserError(_("Default Journal not found."))
        journal = self.env['account.journal'].browse(journal_id)

        for invoice_ids in self:
            #invoice_ids.action_invoice_open()
            if invoice_generated == 'paid':
                res = invoice_ids.pay_and_reconcile(pay_journal=journal, pay_amount=invoice_ids.amount_total)

        return True


class SaleAdvancePaymentInv(models.TransientModel):
    _inherit = "sale.advance.payment.inv"

   # @api.multi
    def create_invoices(self):
        res = super(SaleAdvancePaymentInv, self).create_invoices()
        sale_orders = self.env['sale.order'].browse(self._context.get('active_ids', []))
        for subsc in sale_orders.subscription_ids:
            subsc.invoice_ids = subsc.invoice_ids.union(sale_orders.invoice_ids)
            if subsc.num_billing_cycle > 0:
                start_date = datetime.strptime(str(subsc.start_date), '%Y-%m-%d %H:%M:%S')

                end_date = datetime.strptime(str(subsc.end_date), '%Y-%m-%d %H:%M:%S')
                date_intervals = subsc.cal_date_period(start_date, end_date, subsc.num_billing_cycle)
                subsc.write({
                    'next_payment_date': datetime.strptime(date_intervals[subsc.invoice_count - 2], "%d/%m/%Y %H:%M:%S")
                })
        return res
