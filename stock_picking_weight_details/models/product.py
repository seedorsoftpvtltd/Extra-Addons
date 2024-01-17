from odoo import api, fields, models


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    value_goods = fields.Float(string="Value of Goods")
