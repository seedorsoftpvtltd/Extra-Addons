 # -*- coding: utf-8 -*-

from odoo import api, fields, models, tools, _


class ProductProduct(models.Model):
    _inherit = 'product.product'

    pricelist = fields.Char(string='Pricelist')
    price = fields.Float(
        'Public Price', compute='_compute_product_lst_price_axis',
        digits='Product Price', inverse='_set_product_lst_price_axis',
        help="The sale price is managed from the product template. Click on the 'Configure Variants' button to set the extra attribute prices.")

    ax_min_quantity = fields.Integer(string='Min Quantity')
    ax_start_date = fields.Date(string='Start Date')
    end_date = fields.Date(string='End Date')

    @api.depends('list_price', 'standard_price')
    def _compute_product_lst_price_axis(self):
        for product in self:
            if product.standard_price:
                price = product.standard_price
            else:
                price = None
            product.price = price
            product.ax_min_quantity = 1
            product.pricelist = product.standard_price

    def _set_product_lst_price_axis(self):
        for product in self:
            if product.list_price:
                # value = product.lst_price
                value = product.standard_price
                product.write({'price': value})

