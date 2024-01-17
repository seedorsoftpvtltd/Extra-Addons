from odoo import api, fields, models, _
from odoo.http import request
import os
from odoo.exceptions import UserError, AccessError, MissingError, ValidationError
import datetime


class GoodsOrderLineextend(models.Model):
    _inherit = 'goods.order.line'

    x_sku_id = fields.Many2one('item.master', string="Product Code", compute='_skucode')
    x_length = fields.Float('Length', related='x_sku_id.length', store=True)
    x_breadth = fields.Float('Breadth', related='x_sku_id.width', store=True)
    x_height = fields.Float('Height', related='x_sku_id.height', store=True)
    x_dimension = fields.Float('Dimension')
    x_weight = fields.Float('Weight', related='x_sku_id.weight', store=True)
    # product_id = fields.Many2one('product.product', string="Product", compute='_product', store=True, required=False, readonly=False)

    @api.depends('product_id')
    def _skucode(self):
        for rec in self:
            if rec.product_id:
                rec['x_sku_id'] = rec.product_id.item
                print(rec.x_sku_id, ']]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]][[[[[[[[[[[[[[[[[[[[[[[[[')
            else:
                rec['x_sku_id'] = ''

    # @api.depends('x_sku_id')
    # def _product(self):
    #     for rec in self:
    #         if rec.x_sku_id:
    #             rec['product_id'] = rec.x_sku_id.product_id.id

    # @api.model
    # def create(self, vals_list):
    #     res = super(GoodsOrderLineextend, self).create(vals_list)
    #     if self.x_sku_id:
    #         self['product_id'] = self.x_sku_id.product_id.id
    #     return res
