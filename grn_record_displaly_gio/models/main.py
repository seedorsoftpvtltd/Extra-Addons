from _datetime import datetime

from collections import defaultdict
from datetime import datetime
from dateutil import relativedelta
from itertools import groupby
from operator import itemgetter
from re import findall as regex_findall, split as regex_split

from odoo import api, fields, models, _, SUPERUSER_ID
from odoo.exceptions import UserError
from odoo.osv import expression
from odoo.tools.float_utils import float_compare, float_round, float_is_zero

import logging

_logger = logging.getLogger(__name__)


class GoodsIssueOrder(models.Model):
    _inherit = "goods.issue.order"

    # stock_move_ids = fields.One2many('stock.move', 'partner_id',
    #                                  domain=[('state', '!=', 'done')])
    stock_move_ids = fields.Many2many('stock.picking')

    @api.onchange('partner_id')
    def _compute_stock_moves(self):
        _logger.info(f"{self.partner_id},{self.stock_move_ids} _compute_stock_moves, processing...")
        for order in self:
            move = self.env['stock.picking'].search([('partner_id', '=', order.partner_id.id),
                                                  ('state', 'not in', ['done', 'cancel']),
                                                  ('picking_type_id.name', '=', 'Receipts')])
            order.stock_move_ids = move
        for mov in move:
            for i in self.stock_move_ids:
                i.state = mov.state



class Picking(models.Model):
    _inherit = "stock.picking"

    gio_pend_qty = fields.Float(String="Demand", related="move_lines.product_uom_qty")

