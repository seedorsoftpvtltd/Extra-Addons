# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _
from odoo.tools.sql import column_exists, create_column


class StockLocationRoute(models.Model):
    _inherit = "stock.location.route"
    sale_selectable = fields.Boolean("Selectable on Sales Order Line")


class StockMove(models.Model):
    _inherit = "stock.move"
    goods_line_id = fields.Many2one('goods.order.line', 'Goods Line', index=True)

    @api.model
    def _prepare_merge_moves_distinct_fields(self):
        distinct_fields = super(StockMove, self)._prepare_merge_moves_distinct_fields()
        distinct_fields.append('goods_line_id')
        return distinct_fields

    @api.model
    def _prepare_merge_move_sort_method(self, move):
        move.ensure_one()
        keys_sorted = super(StockMove, self)._prepare_merge_move_sort_method(move)
        keys_sorted.append(move.goods_line_id.id)
        return keys_sorted

    def _get_related_invoices(self):
        """ Overridden from stock_account to return the customer invoices
        related to this stock move.
        """
        rslt = super(StockMove, self)._get_related_invoices()
        invoices = self.mapped('picking_id.goods_id.invoice_ids').filtered(lambda x: x.state == 'posted')
        rslt += invoices
        #rslt += invoices.mapped('reverse_entry_ids')
        return rslt

    def _assign_picking_post_process(self, new=False):
        super(StockMove, self)._assign_picking_post_process(new=new)
        if new:
            picking_id = self.mapped('picking_id')
            sale_order_ids = self.mapped('goods_line_id.order_id')
            for sale_order_id in sale_order_ids:
                picking_id.message_post_with_view(
                    'mail.message_origin_link',
                    values={'self': picking_id, 'origin': sale_order_id},
                    subtype_id=self.env.ref('mail.mt_note').id)


class ProcurementGroup(models.Model):
    _inherit = 'procurement.group'

    goods_id = fields.Many2one('goods.issue.order', 'Goods Order')


class StockRule(models.Model):
    _inherit = 'stock.rule'

    def _get_custom_move_fields(self):
        fields = super(StockRule, self)._get_custom_move_fields()
        fields += ['goods_line_id', 'partner_id']
        return fields


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    goods_id = fields.Many2one(related="group_id.goods_id", string="Goods Order", store=True, readonly=False)

    def _auto_init(self):
        """
        Create related field here, too slow
        when computing it afterwards through _compute_related.

        Since group_id.sale_id is created in this module,
        no need for an UPDATE statement.
        """
        if not column_exists(self.env.cr, 'stock_picking', 'goods_id'):
            create_column(self.env.cr, 'stock_picking', 'goods_id', 'int4')
        return super()._auto_init()

    def _log_less_quantities_than_expected(self, moves):
        """ Log an activity on sale order that are linked to moves. The
        note summarize the real proccessed quantity and promote a
        manual action.

        :param dict moves: a dict with a move as key and tuple with
        new and old quantity as value. eg: {move_1 : (4, 5)}
        """

        def _keys_in_sorted(sale_line):
            """ sort by order_id and the sale_person on the order """
            return (sale_line.order_id.id, sale_line.order_id.user_id.id)

        def _keys_in_groupby(sale_line):
            """ group by order_id and the sale_person on the order """
            return (sale_line.order_id, sale_line.order_id.user_id)

        def _render_note_exception_quantity(moves_information):
            """ Generate a note with the picking on which the action
            occurred and a summary on impacted quantity that are
            related to the sale order where the note will be logged.

            :param moves_information dict:
            {'move_id': ['sale_order_line_id', (new_qty, old_qty)], ..}

            :return: an html string with all the information encoded.
            :rtype: str
            """
            origin_moves = self.env['stock.move'].browse([move.id for move_orig in moves_information.values() for move in move_orig[0]])
            origin_picking = origin_moves.mapped('picking_id')
            values = {
                'origin_moves': origin_moves,
                'origin_picking': origin_picking,
                'moves_information': moves_information.values(),
            }
            return self.env.ref('gio_stock.exception_on_picking').render(values=values)

        documents = self._log_activity_get_documents(moves, 'goods_line_id', 'DOWN', _keys_in_sorted, _keys_in_groupby)
        self._log_activity(_render_note_exception_quantity, documents)

        return super(StockPicking, self)._log_less_quantities_than_expected(moves)

class ProductionLot(models.Model):
    _inherit = 'stock.production.lot'

    sale_order_ids = fields.Many2many('goods.issue.order', string="Goods Orders", compute='_compute_sale_order_ids')
    sale_order_count = fields.Integer('Goods order count', compute='_compute_sale_order_ids')

    @api.depends('name')
    def _compute_sale_order_ids(self):
        for lot in self:
            stock_moves = self.env['stock.move.line'].search([
                ('lot_id', '=', lot.id),
                ('state', '=', 'done')
            ]).mapped('move_id')
            stock_moves = stock_moves.search([('id', 'in', stock_moves.ids)]).filtered(
                lambda move: move.picking_id.location_dest_id.usage == 'customer' and move.state == 'done')
            if self.env.user.has_group('stock.group_stock_user'):
                lot.sale_order_ids = stock_moves.sudo().mapped('goods_line_id.order_id')
            else:
                lot.sale_order_ids = stock_moves.mapped('goods_line_id.order_id')
            lot.sale_order_count = len(lot.sale_order_ids)

    def action_view_so(self):
        self.ensure_one()
        action = self.env.ref('gio.action_orders').read()[0]
        action['domain'] = [('id', 'in', self.mapped('sale_order_ids.id'))]
        action['context'] = dict(self._context, create=False)
        return action
