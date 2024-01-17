from odoo import models, fields, api, _

class StockMove(models.Model):
    _inherit = "stock.move"

    gross_weight = fields.Float(string="Gross Weight(kg)", related='warehouse_line_id.gross_weight', readonly=False, store=True)
