from odoo import models, fields, api, _

class FreightOperationLine(models.Model):
    _inherit = 'freight.operation.line'

    description = fields.Char(string='Description', store=True, readonly=False)
