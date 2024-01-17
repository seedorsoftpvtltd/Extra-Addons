# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models
from odoo.addons.base.models.res_partner import WARNING_MESSAGE, WARNING_HELP


class res_partner(models.Model):
    _name = 'res.partner'
    _inherit = 'res.partner'

    def _compute_warehouse_order_count(self):
        # retrieve all children partners and prefetch 'parent_id' on them
        all_partners = self.with_context(active_test=False).search([('id', 'child_of', self.ids)])
        all_partners.read(['parent_id'])

        warehouse_order_groups = self.env['warehouse.order'].read_group(
            domain=[('partner_id', 'in', all_partners.ids)],
            fields=['partner_id'], groupby=['partner_id']
        )
        partners = self.browse()
        for group in warehouse_order_groups:
            partner = self.browse(group['partner_id'][0])
            while partner:
                if partner in self:
                    partner.warehouse_order_count += group['partner_id_count']
                    partners |= partner
                partner = partner.parent_id
        (self - partners).warehouse_order_count = 0

    def _compute_supplier_invoice_count(self):
        # retrieve all children partners and prefetch 'parent_id' on them
        all_partners = self.with_context(active_test=False).search([('id', 'child_of', self.ids)])
        all_partners.read(['parent_id'])

        supplier_invoice_groups = self.env['account.move'].read_group(
            domain=[('partner_id', 'in', all_partners.ids),
                    ('type', 'in', ('in_invoice', 'in_refund'))],
            fields=['partner_id'], groupby=['partner_id']
        )
        partners = self.browse()
        for group in supplier_invoice_groups:
            partner = self.browse(group['partner_id'][0])
            while partner:
                if partner in self:
                    partner.supplier_invoice_count += group['partner_id_count']
                    partners |= partner
                partner = partner.parent_id
        (self - partners).supplier_invoice_count = 0

    @api.model
    def _commercial_fields(self):
        return super(res_partner, self)._commercial_fields()

    property_warehouse_currency_id = fields.Many2one(
        'res.currency', string="Supplier Currency", company_dependent=True,
        help="This currency will be used, instead of the default one, for warehouses from the current partner")
    warehouse_order_count = fields.Integer(compute='_compute_warehouse_order_count', string='Warehouse Booking Count')
    supplier_invoice_count = fields.Integer(compute='_compute_supplier_invoice_count', string='# Vendor Bills')
    warehouse_warn = fields.Selection(WARNING_MESSAGE, 'Warehouse Booking', help=WARNING_HELP, default="no-message")
    warehouse_warn_msg = fields.Text('Message for Warehouse Booking')
