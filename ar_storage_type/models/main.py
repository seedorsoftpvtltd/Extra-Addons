from odoo import models, fields, api, _

class WarehouseOrder(models.Model):
    _inherit = 'warehouse.order'

    storage_type = fields.Many2one('storage.type', string="Storage Type")


class StockPicking(models.Model):
    _inherit = 'stock.picking'


class ServiceCharge(models.Model):
    _inherit = "agree.charges"

    storage_type = fields.Many2one('storage.type', string="Storage Type")