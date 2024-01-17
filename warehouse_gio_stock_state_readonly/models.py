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

class Picking(models.Model):
    _inherit = "stock.picking"

    state = fields.Selection([
        ('draft', 'Draft'),
        ('waiting', 'Waiting Another Operation'),
        ('confirmed', 'Waiting'),
        ('assigned', 'Ready'),
        ('done', 'Done'),
        ('cancel', 'Cancelled'),
    ], string='Status', compute='_compute_state',
        copy=False, index=True, readonly=False, store=True, tracking=True,
        help=" * Draft: The transfer is not confirmed yet. Reservation doesn't apply.\n"
             " * Waiting another operation: This transfer is waiting for another operation before being ready.\n"
             " * Waiting: The transfer is waiting for the availability of some products.\n(a) The shipping policy is \"As soon as possible\": no product could be reserved.\n(b) The shipping policy is \"When all products are ready\": not all the products could be reserved.\n"
             " * Ready: The transfer is ready to be processed.\n(a) The shipping policy is \"As soon as possible\": at least one product has been reserved.\n(b) The shipping policy is \"When all products are ready\": all product have been reserved.\n"
             " * Done: The transfer has been processed.\n"
             " * Cancelled: The transfer has been cancelled.")