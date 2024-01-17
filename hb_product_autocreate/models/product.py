from odoo import api, fields, models, _
from odoo.http import request
import os
from odoo.exceptions import UserError, AccessError, MissingError, ValidationError


class Productproduct(models.Model):
    _inherit = 'item.master'

    product_id = fields.Many2one('product.product', string="Product", required=False)
    product_created = fields.Boolean(string="product Created")

    @api.model
    def create(self, vals):
        res = super(Productproduct, self).create(vals)
        # self.product_create()
        # if not self.product_id:
        #     raise MissingError(_('Please click the button to Create a Product'))
        return res


    def product_create(self):
        print('mmmmmmm')
        for rec in self:
            if rec['product_created'] == False:
                print('nnnnn')
                vals = {
                    'name': rec.sku_no,
                    'tracking' : 'lot'
                }
                product = self.env['product.product'].create(vals)
                print(product, 'product')
                rec['product_id'] = product.id
                rec['product_created'] = True
                # if rec.product_id:
                #     raise ValidationError(_("Please Enter the Product."))




