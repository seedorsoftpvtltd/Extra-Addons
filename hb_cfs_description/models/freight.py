from odoo import models, fields, api, _


class FreightOperationLine(models.Model):
    _inherit = 'freight.operation.line'

    description = fields.Char(string='Description', store=True, readonly=False)
    product_id = fields.Many2one("product.product", string="Goods", compute='_consignment_description', store=True)

    @api.depends('description')
    def _consignment_description(self):
        uom = self.env['uom.uom'].search([], limit=1)[0]
        for rec in self:
            if rec.description:
                vals = {
                    'name': rec.description,
                    'x_medium': 16,
                    'type': 'product',
                    'uom_id': uom.id,
                    'uom_po_id': uom.id,
                }
                product = self.env['product.product'].create(vals)
                rec['product_id'] = product.id

    @api.onchange('description')
    def onchange_consignment_description(self):
        uom = self.env['uom.uom'].search([], limit=1)[0]
        if self.description:
            vals = {
                'name': self.description,
                'x_medium': 16,
                'type': 'product',
                'uom_id': uom.id,
                'uom_po_id': uom.id,
            }
            product = self.env['product.product'].create(vals)
            self.product_id = product.id
