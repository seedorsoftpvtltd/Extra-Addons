from odoo import models, fields, api


class ItemMaster(models.Model):
    _inherit = 'item.master'

    company_id = fields.Many2one('res.company', string='Company', readonly=True, default=lambda self: self.env.company)


class MultiContainer(models.Model):
    _inherit = "multiple.container"

    company_id = fields.Many2one('res.company', string='Company', readonly=True, default=lambda self: self.env.company)


class StockKeep(models.Model):
    _inherit = 'stock.keep'

    company_id = fields.Many2one('res.company', string='Company', readonly=True, default=lambda self: self.env.company)


class ContainerPattern(models.Model):
    _inherit = "container.pattern"

    company_id = fields.Many2one('res.company', string='Company', readonly=True, default=lambda self: self.env.company)


class PatternTemplate(models.Model):
    _inherit = "pattern.template"

    company_id = fields.Many2one('res.company', string='Company', readonly=True, default=lambda self: self.env.company)


class JobEstimateProduct(models.Model):
    _inherit = "job.estimate.product"

    company_id = fields.Many2one('res.company', string='Company', readonly=True, default=lambda self: self.env.company)


class WarehousePackages(models.Model):
    _inherit = "warehouse.packages"

    company_id = fields.Many2one('res.company', string='Company', readonly=True, default=lambda self: self.env.company)


class WarehouseTag(models.Model):
    _inherit = "warehouse.tag"

    company_id = fields.Many2one('res.company', string='Company', readonly=True, default=lambda self: self.env.company)

class Product(models.Model):
    _inherit = "product.template"

    x_company=fields.Char(string='Com',compute="_company_defult")


    @api.depends('type')
    def _company_defult(self):
        for rec in self:
            rec['company_id']=self.env.company
            rec['x_company']=1

class ProductProduct(models.Model):
    _inherit = "product.product"

    x_company1=fields.Char(string='Com',compute="_company1_defult")


    @api.depends('type')
    def _company1_defult(self):
        for rec in self:
            rec['company_id']=self.env.company
            rec['x_company1']=1