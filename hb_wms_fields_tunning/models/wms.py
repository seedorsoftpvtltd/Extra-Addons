from odoo.http import request
from odoo import api, fields, models, tools, osv, http, _


class lotInh(models.Model):
    _inherit = "stock.production.lot"

    warehouse_order_ids = fields.Many2many('warehouse.order', string="warehouse Orders",
                                           compute='_compute_warehouse_order_ids', readonly=True, store=True)


class SaleorderInh(models.Model):
    _inherit = "sale.order"

    # pickings_ids = fields.Many2many('stock.picking','Pickings',
    #                                 domain=[('state', '!=', 'done')], store=True)
    picking_ids = fields.One2many('stock.picking', 'sale_id', string='Transfers', store=True)


class PickingInh(models.Model):
    _inherit = "stock.picking"

    returnpick = fields.Char(string="Return", compute='_returnpick', store=True)


class StockmovEInh(models.Model):
    _inherit = "stock.move"

    returnpick = fields.Char(string="Return", related='picking_id.returnpick', store=True)


class StockKeep(models.Model):
    _inherit = 'stock.keep'

    # warehouse_line_id = fields.Many2one('warehouse.order.line', store=True, string="Warehouse Order Line")
    partner_id = fields.Many2one('res.partner', 'Customer')


class Getsaleorderdataext(models.TransientModel):
    _inherit = 'getsale.orderdata'

    product_uom = fields.Many2one('uom.uom', string='Product Unit of Measure')


class SaleEstimateJobext(models.Model):
    _inherit = "sale.estimate.job"

    payment_term_id = fields.Many2one(
        'account.payment.term',
        string='Payment Terms',
    )


class WarehouseorderInh(models.Model):
    _inherit = 'warehouse.order.line'

    x_sku_id = fields.Many2one('item.master', 'Product Code', compute='_skucode', store=True)


class GoodsOrderLineextend(models.Model):
    _inherit = 'goods.order.line'

    x_sku_id = fields.Many2one('item.master', string="Product Code", compute='_skucode', store=True)