# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.

from odoo import models, fields

class StockRule(models.Model):
    _inherit = 'stock.rule'

    def _get_stock_move_values(self, product_id, product_qty, product_uom, location_id, name, origin, company_id,
                               values):
        result = super(StockRule, self)._get_stock_move_values(product_id, product_qty, product_uom, location_id, name, origin, company_id,
                               values)
        result.update({'product_description' : values.get('product_description', "0")})
        return result



class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    #@api.multi
    def _prepare_procurement_values(self,group_id):
        res = super(SaleOrderLine,self)._prepare_procurement_values(group_id=group_id)
        res.update({'product_description' : self.name})
        return res

    product_description = fields.Char(string="Description")


class stock_move(models.Model):
    _inherit = 'stock.move'

    product_description = fields.Char(string="Description")

    def _prepare_procurement_values(self):
        res = super(stock_move,self)._prepare_procurement_values()
        res.update({'product_description' : self.product_description or ''})
        return res


class purchase_order(models.Model):
    _inherit = 'purchase.order.line'

    #@api.multi
    def _create_stock_moves(self, picking):
        moves = self.env['stock.move']
        done = self.env['stock.move'].browse()
        for line in self:
            for val in line._prepare_stock_moves(picking):
                val.update({'product_description':line.name})
                done += moves.create(val)
        return done

