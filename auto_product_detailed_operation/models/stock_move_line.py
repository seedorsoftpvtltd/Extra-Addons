from odoo import models, fields, api, _
import xml.etree.ElementTree as ET


class StockMoveLine(models.Model):
    _inherit = "stock.move.line"

    @api.model
    def default_get(self, vals):
        res = super(StockMoveLine, self).default_get(vals)
        self.product_id = self.move_id.product_id
        return res


# class StockMove(models.Model):
#     _inherit = "stock.move"
#
#     def action_show_details(self):
#         res = super(StockMove, self).action_show_details()
#         return res
