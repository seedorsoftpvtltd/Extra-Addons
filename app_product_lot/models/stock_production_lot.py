# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _
from odoo.exceptions import UserError


class ProductionLot(models.Model):
    _inherit = ['stock.production.lot']
    _order = 'name desc'

    name = fields.Char(index=True, copy=False)
    product_id = fields.Many2one(change_default=True)
    company_id = fields.Many2one(default=lambda self: self.env.company)
    
    @api.onchange('product_id')
    def _onchange_product_id(self):
        if self.product_id and self.product_id.tracking_sequence:
            self.name = _("Auto")
    
    @api.model
    def create(self, vals):
        if not vals.get('name', False) or vals.get('name') == _("Auto"):
            if vals.get('product_id'):
                sku = self.product_id.browse(vals.get('product_id'))
                vals['name'] = self.get_name_by_sku(sku)
        return super(ProductionLot, self).create(vals)

    def get_name_by_sku(self, sku):
        name = ''
        if sku and sku.tracking != 'none':
            if sku.tracking_sequence:
                name = sku.tracking_sequence.next_by_id()
            else:
                name = self.env['ir.sequence'].with_context(force_company=sku.company_id.id).next_by_code('stock.lot.serial') or ''
        return name

    def generate_name(self):
        for rec in self:
            rec.name = self.get_name_by_sku(rec.product_id)

