# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import models,fields,api,_

class ResCompany(models.Model):
    _inherit='res.company'
    
    sh_free_product_tax = fields.Selection([('yes','Yes'),('no','No')],default='yes',string='Free Sample Product Tax')

class ResConfigSetting(models.TransientModel):
    _inherit='res.config.settings'
    
    sh_free_product_tax = fields.Selection([('yes','Yes'),('no','No')],default='yes',string='Free Sample Product Tax',related='company_id.sh_free_product_tax',readonly=False)