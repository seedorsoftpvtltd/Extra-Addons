# -*- coding: utf-8 -*-

from odoo import api, fields, models, _

class ProductProductInherit(models.Model):
    _inherit = "product.product"

    package_pro_id = fields.Many2one('product.packaging', string='Product packaging')
    packaging_relation = fields.Many2one('product.packaging.line', string='Product packaging line')
    prod_qty = fields.Float('Quantity')

class StockPickingInherit(models.Model):
    _inherit = "stock.picking"

    @api.model
    def create(self, vals):
        res = super(StockPickingInherit, self).create(vals)
        sale_ord_obj = self.env['sale.order']
        sale_ord = sale_ord_obj.search([('name','=',vals.get('origin'))])
        prod_list = []
        for line in sale_ord.order_line:
            if line.product_packaging:
                if line.product_packaging.product_ids:
                    for i in line.product_packaging.product_ids:
                        procu_group_id = self.env['procurement.group'].search([('name','=',vals.get('origin'))])
                        move = self.env['stock.move'].create({
                            'name': res.name,
                            'reference': res.name,
                            'location_id': vals.get('location_id'),
                            'location_dest_id': vals.get('location_dest_id'),
                            'product_id': i.product_id.id,
                            # 'lot_id':i.product_lot.id,
                            'product_uom': i.product_uom.id,
                            'product_uom_qty': i.product_qty,
                            'picking_id': res.id,
                            'origin': vals.get('origin'),
                            'group_id': procu_group_id.id,
                        })
                        move._action_assign()
                        # move1._action_confirm()
                        move.move_line_ids.qty_done = i.product_qty
                        move._action_done()
        return res

class ProductPackagingInherit(models.Model):
    _inherit = "product.packaging"

    product_ids = fields.One2many('product.packaging.line','packaging_id',string="Product")



class ProductPackagingLine(models.Model):

    _name = "product.packaging.line"


    @api.onchange('product_id')
    def compute_ids(self):
        print(self.product_id.id)
        print(self.product_id.product_tmpl_id.id)
        m = self.env['stock.production.lot'].search([('product_id', '=', self.product_id.id)]).ids
        print('m',m)
        self.lot_ids = m

    packaging_id = fields.Many2one('product.packaging')
    product_id = fields.Many2one('product.product', string='Product',required=1)
    product_desc = fields.Text('Description', related='product_id.description')
    product_qty = fields.Float('Quantity')
    product_uom = fields.Many2one('uom.uom', 'Unit of Measure',related='product_id.uom_id')
    product_lot = fields.Many2one('stock.production.lot',domain="[('id', 'in', lot_ids)]")
    tracking = fields.Selection(related="product_id.tracking")
    lot_ids = fields.Many2many("stock.production.lot", string="Ids")



