# Copyright 2020 WeDo Technology
# Website: http://wedotech-s.com
# Email: apps@wedotech-s.com
# Phone:00249900034328 - 00249122005009

from odoo import fields, models

class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    auto_invoice = fields.Boolean(string='Auto Invoice', related="company_id.auto_invoice", readonly=False,
                                  help="Create bill automatic wwhen confirm purchase order or receive stock picking based on bill Control Policy in the products")

class ResCompany(models.Model):
    _inherit = 'res.company'

    auto_invoice = fields.Boolean(string='Auto Invoice')
