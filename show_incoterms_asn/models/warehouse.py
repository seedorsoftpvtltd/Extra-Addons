from odoo import api, fields, models, _

class warehouseOrder(models.Model):
    _inherit = "warehouse.order"

    incoterm_id = fields.Many2one('account.incoterms', string='Incoterm',
                                  help='International Commercial Terms are a series of predefined commercial terms used in international transactions.')