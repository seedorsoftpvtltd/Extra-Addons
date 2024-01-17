from odoo import models, fields, api, _


# class JobEstimateLine(models.Model):
#     _inherit = 'sale.order.line'
#     product_sale_line_link = fields.Many2one('job.estimate.product')


class SaleEstimateJob(models.Model):
    _inherit = "sale.estimate.job"

    job_estimate_product_id = fields.One2many(
        "job.estimate.product",
        "job_product_id",

        copy=False,
        string="Product Estimation",
        store=True
    )
    x_survey_vol = fields.Float(string="Survey Volume (cbm)", compute='_compute_survey_volume', store=True)
    x_approx_wt = fields.Integer(string="Approx.wt (kgs)",store=True,compute='_compute_approx_wt')
    survey_area = fields.Float(string="Survey Area (sqm)",store=True,compute='_compute_survey_area')


    @api.depends('job_estimate_product_id.total_volume')
    def _compute_survey_volume(self):
        for job in self:
            total_volume = sum(job.job_estimate_product_id.mapped('total_volume'))
            job.x_survey_vol = total_volume

    @api.depends('job_estimate_product_id.total_area')
    def _compute_survey_area(self):
        for job in self:
            total_area = sum(job.job_estimate_product_id.mapped('total_area'))
            job.survey_area = total_area

    @api.depends('job_estimate_product_id.total_weight')
    def _compute_approx_wt(self):
        for job in self:
            total_weight = sum(job.job_estimate_product_id.mapped('total_weight'))
            job.x_approx_wt = total_weight

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    job_estimate_product_ids = fields.One2many(
        "job.estimate.product",
        "job_product_id",
        string="Product Estimation",
        compute="compute_job_estimation_in_sales_order"
    )

    def compute_job_estimation_in_sales_order(self):
        for instance in self:
            print(instance.job_estimate_product_ids)
            print(instance.id)
            sale_estimate = self.env['sale.estimate.job'].search([('quotation_id', '=', instance.id)])
            print(sale_estimate.id)
            job_estimate = self.env['job.estimate.product'].search([('job_product_id.id', '=', sale_estimate.id)])
            print(job_estimate)

            if instance.job_estimate_product_ids:
                print(job_estimate, 'job_estimate 1')
                instance.job_estimate_product_ids += job_estimate
            else:
                print(job_estimate, 'job_estimate')
                instance.job_estimate_product_ids = job_estimate
