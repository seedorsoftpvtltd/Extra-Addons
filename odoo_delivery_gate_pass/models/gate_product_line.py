# -*- coding: utf-8 -*-

from odoo import models, fields, api


class VisitorGateProductLine(models.Model):
    _name = 'visitor.gate.product.line.custom'

    custom_product_id = fields.Many2one(
    	'product.product',
    	string="Product"
    )

    custom_product_uom_id = fields.Many2one(
    	'uom.uom',
    	string="Unit Of Measure"
    )

    custom_product_uom_qty = fields.Float(
    	default=0.0,
        string="Quantity"
    )

    visitor_gate_pass_id = fields.Many2one('visitor.gate.pass.custom',string="Gate Pass")