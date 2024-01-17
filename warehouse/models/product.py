# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from datetime import timedelta
from odoo import api, fields, models, _
from odoo.addons.base.models.res_partner import WARNING_MESSAGE, WARNING_HELP
from odoo.tools.float_utils import float_round


class ProductTemplate(models.Model):
    _name = 'product.template'
    _inherit = 'product.template'

    property_account_creditor_price_difference = fields.Many2one(
        'account.account', string="Price Difference Account", company_dependent=True,
        help="This account is used in automated inventory valuation to "\
             "record the price difference between a Warehouse Booking and its related vendor bill when validating this vendor bill.")
    warehoused_product_qty = fields.Float(compute='_compute_warehoused_product_qty', string='warehoused')
    warehouse_method = fields.Selection([
        ('warehouse', 'On ordered quantities'),
        ('receive', 'On received quantities'),
    ], string="Control Policy", help="On ordered quantities: Control bills based on ordered quantities.\n"
        "On received quantities: Control bills based on received quantities.", default="receive")
    warehouse_line_warn = fields.Selection(WARNING_MESSAGE, 'Warehouse Booking Line', help=WARNING_HELP, required=True, default="no-message")
    warehouse_line_warn_msg = fields.Text('Message for Warehouse Booking Line')

    def _compute_warehoused_product_qty(self):
        for template in self:
            template.warehoused_product_qty = float_round(sum([p.warehoused_product_qty for p in template.product_variant_ids]), precision_rounding=template.uom_id.rounding)

    @api.model
    def get_import_templates(self):
        res = super(ProductTemplate, self).get_import_templates()
        if self.env.context.get('warehouse_product_template'):
            return [{
                'label': _('Import Template for Products'),
                'template': '/warehouse/static/xls/product_warehouse.xls'
            }]
        return res

    def action_view_po(self):
        action = self.env.ref('warehouse.action_warehouse_order_report_all').read()[0]
        action['domain'] = ['&', ('state', 'in', ['warehouse', 'done']), ('product_tmpl_id', 'in', self.ids)]
        action['context'] = {
            'graph_measure': 'qty_ordered',
            'search_default_orders': 1,
            'time_ranges': {'field': 'date_approve', 'range': 'last_365_days'}
        }
        return action


class ProductProduct(models.Model):
    _name = 'product.product'
    _inherit = 'product.product'

    warehoused_product_qty = fields.Float(compute='_compute_warehoused_product_qty', string='warehoused')

    def _compute_warehoused_product_qty(self):
        date_from = fields.Datetime.to_string(fields.datetime.now() - timedelta(days=365))
        domain = [
            ('state', 'in', ['warehouse', 'done']),
            ('product_id', 'in', self.ids),
            ('date_order', '>', date_from)
        ]
        warehouseOrderLines = self.env['warehouse.order.line'].search(domain)
        order_lines = self.env['warehouse.order.line'].read_group(domain, ['product_id', 'product_uom_qty'], ['product_id'])
        warehoused_data = dict([(data['product_id'][0], data['product_uom_qty']) for data in order_lines])
        for product in self:
            if not product.id:
                product.warehoused_product_qty = 0.0
                continue
            product.warehoused_product_qty = float_round(warehoused_data.get(product.id, 0), precision_rounding=product.uom_id.rounding)

    def action_view_po(self):
        action = self.env.ref('warehouse.action_warehouse_order_report_all').read()[0]
        action['domain'] = ['&', ('state', 'in', ['warehouse', 'done']), ('product_id', 'in', self.ids)]
        action['context'] = {
            'search_default_last_year_warehouse': 1,
            'search_default_status': 1, 'search_default_order_month': 1,
            'graph_measure': 'qty_ordered'
        }
        return action


class ProductCategory(models.Model):
    _inherit = "product.category"

    property_account_creditor_price_difference_categ = fields.Many2one(
        'account.account', string="Price Difference Account",
        company_dependent=True,
        help="This account will be used to value price difference between warehouse price and accounting cost.")


class ProductSupplierinfo(models.Model):
    _inherit = "product.supplierinfo"

    @api.onchange('name')
    def _onchange_name(self):
        self.currency_id = self.name.property_warehouse_currency_id.id or self.env.company.currency_id.id
