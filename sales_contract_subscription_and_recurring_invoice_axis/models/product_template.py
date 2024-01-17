# -*- coding: utf-8 -*-

from odoo import http, models, fields, api, tools
from odoo.tools import float_is_zero, float_compare


class ProductTemplate (models.Model):
    _inherit = "product.template"

    contract_warranty = fields.Boolean('Contract/Warranty Product')
    recuring_period=fields.Char(string='Recuring Period')
