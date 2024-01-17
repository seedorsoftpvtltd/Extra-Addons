from odoo import models, fields, api, _
from datetime import datetime


class Productproduct(models.Model):
    _inherit = 'product.template'

    prod_volume = fields.Float(string='Product Volume', compute='_prod_dimens')
    prod_sqm = fields.Float(string='Product SQM', compute='_prod_dimens')
    uom = fields.Selection([
        ('m', 'm'),
        ('cm', 'cm'),
        ('inch', 'inch')], string='UOM')

    @api.depends('product_length', 'product_height', 'product_width')
    def _prod_dimens(self):
        for r in self:
            try:
                if r.uom == 'm':
                    l = r.product_length
                    b = r.product_width
                    h = r.product_height
                    cbm = l * b * h
                    sqm = l * b
                    r['prod_volume'] = cbm
                    r['prod_sqm'] = sqm
                if r.uom == 'cm':
                    l = r.product_length * 0.01
                    b = r.product_width * 0.01
                    h = r.product_height * 0.01
                    cbm = l * b * h
                    sqm = l * b
                    r['prod_volume'] = cbm
                    r['prod_sqm'] = sqm
                if r.uom == 'inch':
                    l = r.product_length * 0.0254
                    b = r.product_width * 0.0254
                    h = r.product_height * 0.0254
                    cbm = l * b * h
                    sqm = l * b
                    r['prod_volume'] = cbm
                    r['prod_sqm'] = sqm
                if r.uom == False:
                    l = r.product_length
                    b = r.product_width
                    h = r.product_height
                    cbm = l * b * h
                    sqm = l * b
                    r['prod_volume'] = cbm
                    r['prod_sqm'] = sqm

            except:
                r['prod_volume'] = 0
                r['prod_sqm'] = 0
