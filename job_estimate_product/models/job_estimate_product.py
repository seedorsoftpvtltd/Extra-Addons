# from odoo import api, fields, models,

from odoo import models, fields, api, _


class JobEstimateProduct(models.Model):
    _name = "job.estimate.product"

    job_product_id = fields.Many2one('sale.estimate.job', string="Product Estimation")
    sale_order_id = fields.Many2one('sale.order', string="Sale Order")
    # product_name_job = fields.Many2one("product.product", string="Product Name")
    product_name_job = fields.Char(string="Product Name",required=True,)
    product_description = fields.Char(string='Description')
    product_quantity = fields.Integer(string="Quantity",required=True,default=1)
    product_length = fields.Float(string="Length")
    product_width = fields.Float(string='Width')
    product_height = fields.Float(string="Height")
    product_weight = fields.Float(string='Weight (kgs)')
    uom = fields.Selection([
        ('m', 'm'),
        ('cm', 'cm'),
        ('inch', 'inch')], string='UOM',required=True,)

    product_volume = fields.Float(string='Volume', compute='_compute_product_volume', store=True)
    product_area = fields.Float(string='Area', compute='_compute_product_area', store=True)
    total_volume = fields.Float(string='Net Volume', compute='_compute_total_volume', store=True)
    total_area = fields.Float(string='Net Area', compute='_compute_total_area', store=True)
    total_weight = fields.Float(string='Net Weight',compute='_compute_total_weight',store=True)

    @api.depends('product_length', 'product_width', 'product_height', 'uom')
    def _compute_product_volume(self):
        for r in self:
            if r.uom == 'm':
                l = r.product_length
                b = r.product_width
                h = r.product_height
                cbm = l * b * h
                r.product_volume = cbm
                print(cbm,' r.product_volume ')

            if r.uom == 'cm':
                l = r.product_length * 0.01
                b = r.product_width * 0.01
                h = r.product_height * 0.01
                cbm = l * b * h
                r.product_volume = cbm
                print( cbm,' cm')

            if r.uom == 'inch':
                l = r.product_length * 0.0254
                b = r.product_width * 0.0254
                h = r.product_height * 0.0254
                cbm = l * b * h
                r.product_volume = cbm
                print( cbm,' inch')

    @api.depends('product_length', 'product_width','uom')
    def _compute_product_area(self):
        for product in self:
            if product.uom == 'm':
                l = product.product_length
                b = product.product_width
                cbm = l * b
                product.product_area = cbm
                print(cbm, ' r.product_volume11 ')
            if product.uom == 'cm':
                l = product.product_length * 0.01
                b = product.product_width * 0.01

                cbm = l * b
                product.product_area = cbm
                print( cbm,' cm111')

            if product.uom == 'inch':
                l = product.product_length * 0.0254
                b =product.product_width * 0.0254

                cbm = l * b
                product.product_area = cbm
                print( cbm,' inch111')
            # product.product_area = product.product_length * product.product_width
    # @api.depends('product_length', 'product_width')
    # def _compute_product_area(self):
    #     for product in self:
    #         product.product_area = product.product_length * product.product_width

    @api.depends('product_quantity', 'product_volume')
    def _compute_total_volume(self):
        for job in self:
            job.total_volume = job.product_quantity * job.product_volume

    @api.depends('product_quantity', 'product_area')
    def _compute_total_area(self):
        for job in self:
            job.total_area = job.product_quantity * job.product_area

    @api.depends('product_quantity', 'product_weight')
    def _compute_total_weight(self):
        for job in self:
            job.total_weight = job.product_quantity * job.product_weight

# price = fields.Float(string="Price")
# product_uom = fields.Many2one('uom.uom', 'Unit of Measure', required=True, )
# # domain = "[('category_id', '=', product_uom_category_id)]"
# qty_transfer = fields.Integer(string="Quantity")
# # vat_transfer = fields.Integer(string="VAT")
# taxes_id = fields.Many2many('account.tax', string='Taxes')
