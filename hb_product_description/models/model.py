from odoo import models, fields, api


class ProductTemplateext(models.Model):
    _inherit = 'product.template'

    product_description = fields.Many2one('product.description', 'Product Description', store=True)
    description = fields.Char('Description', related='product_description.name', store=True)


class ProductDescription(models.Model):
    _name = 'product.description'

    name = fields.Char('Name', store=True)

