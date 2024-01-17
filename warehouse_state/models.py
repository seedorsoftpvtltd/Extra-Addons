from odoo import api, fields, models


class WarehouseOrder(models.Model):
    _inherit = 'warehouse.order'

    state = fields.Selection([
        ('draft', 'Booking'),
        ('sent', 'Booking Sent'),
        ('to approve', 'To Approve'),
        ('warehouse', 'Warehouse Booking'),
        ('done', 'Locked'),
        ('cancel', 'Cancelled')
    ], string='Status', readonly=False, index=True, copy=False, default='draft', tracking=True)

class GoodsIssueOrder(models.Model):
    _inherit = "goods.issue.order"

    state = fields.Selection([
        ('draft', 'Draft'),
        ('sent', 'Goods Sent'),
        ('sale', 'Goods Order'),
        ('done', 'Locked'),
        ('cancel', 'Cancelled'),
        ], string='Status', readonly=False, copy=False, index=True, tracking=3, default='draft')