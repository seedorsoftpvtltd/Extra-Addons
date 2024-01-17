from odoo import models, fields, api, _


class SaleEstimateLine(models.Model):
    _inherit = 'sale.estimate.line.job'

    @api.onchange('product_id')
    def onch(self):
        self.product_id.x_medium = self.env['utm.medium'].browse(14)
        self.product_id.type = 'product'
        self.product_id.tracking = 'none'


class ProductProduct(models.Model):
    _inherit = 'product.product'


    @api.onchange('x_medium')
    def onchange_medium(self):
        if self.x_medium.name == 'Relocation':
            self.tracking = 'none'
        else:
            self.tracking = 'lot'

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    @api.onchange('x_medium')
    def onchange_medium(self):
        if self.x_medium.name == 'Relocation':
            self.tracking = 'none'
        else:
            self.tracking = 'lot'

class JobEstimateProduct(models.Model):
    _inherit = "job.estimate.product"

    product_name_job = fields.Char(string="Product Name", related="product_id.name")
    product_id = fields.Many2one('product.product', string='Product Name')

    @api.onchange('product_id')
    def onch(self):
        self.product_id.x_medium = self.env['utm.medium'].browse(14)
        self.product_id.type = 'product'
        self.product_id.tracking = 'none'



