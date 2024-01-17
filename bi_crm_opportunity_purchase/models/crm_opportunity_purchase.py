# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _
from datetime import datetime


class CrmLead(models.Model):
    _inherit = "crm.lead"

    purchase_order_line_ids = fields.One2many('crm.purchase.order.line','line_id',string="Order Lines")
    purchase_order_count = fields.Integer(compute='_compute_purchase_data', string="Number of Purchase Orders")

    # count purchase orders
    @api.depends('purchase_order_line_ids')
    def _compute_purchase_data(self):
        self.purchase_order_count = self.env['purchase.order'].search_count([('opportunity_id','=',self.id)])

    # create purchase order from crm

    def create_crm_purchase(self):
        for po in self.purchase_order_line_ids:
            purchase_order = self.env['purchase.order'].search([('opportunity_id','=',self.id),('partner_id','=',po.partner_id.id)])
            if purchase_order:
                purchase_order.write({ 'order_line': [
                    (0, 0, {
                        'name':po.product_id.name,
                        'product_id': po.product_id.id,
                        'product_qty': po.req_qty,
                        'date_planned':datetime.now(),
                        'product_uom': po.product_uom_id.id,
                        'price_unit': po.product_id.list_price,
                    })
                ]})
                po.order_id=purchase_order.id
                for line in purchase_order.order_line:
                    po.order_line_id = line

            else:
                p_obj = self.env['purchase.order'].sudo().create({
                    'partner_id': po.partner_id.id,
                    'date_order': datetime.now(),
                    'opportunity_id': self.id,
                    'order_line': [
                        (0, 0, {
                            'name':po.product_id.name,
                            'product_id': po.product_id.id,
                            'product_qty': po.req_qty,
                            'date_planned':datetime.now(),
                            'product_uom': po.product_uom_id.id,
                            'price_unit': po.product_id.list_price,
                        })
                    ]
                })
                po.order_id=p_obj.id
                po.order_line_id = p_obj.order_line

        action = self.env.ref('bi_crm_opportunity_purchase.purchase_order_tree').read()[0]
        return action


class CrmPurchaseLines(models.Model):
    _name = 'crm.purchase.order.line'
    _description = "CRM Purchase Order Line"

    line_id = fields.Many2one('crm.lead', string="Opportunity")
    product_id = fields.Many2one('product.product', string="Product", required=True)
    qty_on_hand = fields.Integer('On Hand Quantity')
    req_qty = fields.Integer('Required Quantity', default=1)
    product_uom_id = fields.Many2one('uom.uom', string='Unit of Measure', required=True)
    partner_id = fields.Many2one('res.partner',string="Vendor", readonly=False, required=True)
    order_line_id = fields.Many2one('purchase.order.line', string="Purchase Line", readonly=True)
    order_id = fields.Many2one('purchase.order', string="Purchase Order", required=False, readonly=True)

    # get on hand quantity on product change
    @api.onchange('product_id')
    def onchange_product(self):
        for rec in self:
            if rec.product_id:
                rec.qty_on_hand = rec.product_id.qty_available

class PurchaseOrder(models.Model):
    _name = "purchase.order"
    _inherit = ['purchase.order', 'utm.mixin']

    opportunity_id = fields.Many2one('crm.lead', string='Opportunity', domain="[('type', '=', 'opportunity')]")