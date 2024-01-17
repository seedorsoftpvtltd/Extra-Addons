from odoo import api, fields, models, _
from odoo.http import request
import os
from odoo.exceptions import UserError, AccessError, MissingError, ValidationError


class SKUMaster(models.Model):
    _name = 'item.master'

    name = fields.Char(string="Name", compute='_namee')
    weight = fields.Float(string="Weight")
    length = fields.Float(string="Length")
    height = fields.Float(string="Height")
    width = fields.Float(string="Width")
    product_id = fields.Many2one('product.product', string="Product", required=True)
    partner_id = fields.Many2one('res.partner', string="Customer", required=True)
    description = fields.Char(string="Description")
    sku_no = fields.Char(string="Product Code", required=True)
    company_id = fields.Many2one('res.company', string='Company', default=lambda self: self.env.company.id)
    volume = fields.Float(string="Volume", compute='_volume', readonly=False)

    @api.depends('sku_no')
    def _namee(self):
        for rec in self:
            rec['name'] = rec.sku_no

    @api.depends('length', 'height', 'width')
    def _volume(self):
        for rec in self:
            rec['volume'] = rec.length * rec.height * rec.width







