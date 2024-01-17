from odoo import models, fields, api, _

class JobEstimate(models.Model):
    _inherit='sale.order'
    estim_sale_link=fields.Many2one('sale.estimate.job')


class JobEstimateLine(models.Model):
    _inherit='sale.order.line'
    estim_sale_line_link=fields.Many2one('sale.estimate.line.job')


class UOM(models.Model):
    _inherit='product.template'
    uom = fields.Selection([
        ('m', 'm'),
        ('cm', 'cm'),
        ('inch', 'inch')], string='UOM')



    def cbm(self):
        for r in self:
            if r.uom == 'm':
                l = r.product_length
                b = r.product_width
                h = r.product_height
                cbm = l * b * h
                r["volume"] = cbm

            if r.uom == 'cm':

                l = r.product_length * 0.01
                b = r.product_width * 0.01
                h = r.product_height * 0.01
                cbm = l * b * h
                r["volume"] = cbm

            if r.uom == 'inch':

                l = r.product_length * 0.0254
                b = r.product_width * 0.0254
                h = r.product_height * 0.0254
                cbm = l * b * h
                r["volume"] = cbm







