from odoo import models, tools,api


class ProductionLot(models.Model):
    _inherit = 'stock.production.lot'

    _sql_constraints = [
        ('name_ref_uniq', 'unique ()',
         'The combination of serial number and product must be unique across a company !'),
    ]
