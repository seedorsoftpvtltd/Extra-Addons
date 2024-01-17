from odoo import fields, models, api, _

class Main(models.Model):
    _inherit = "stock.picking"

    x_country = fields.Many2one('res.country', readonly=True, store=True, related="warehouse_id.x_country")