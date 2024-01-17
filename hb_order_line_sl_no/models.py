# -*- coding: utf-8 -*-

from odoo import models, fields, api


class gio_order_line_number(models.Model):
    _inherit = 'goods.order.line'

    def _get_line_numbers(self):
        line_num = 1
        if self.ids:
            first_line_rec = self.browse(self.ids[0])

            for line_rec in first_line_rec.order_id.order_line:
                line_rec.line_no = line_num
                line_num += 1

    line_no = fields.Integer(string='Serial Number', readonly=False, default=False)


class gio_order_number(models.Model):
    _inherit = 'goods.issue.order'

    @api.model
    def create(self, vals):
        res = super(gio_order_number, self).create(vals)
        if vals.get('order_line'):
            for l in res.order_line:
                l._get_line_numbers()
        return res

    def write(self, vals):
        res = super(gio_order_number, self).write(vals)
        for r in self:
            if 'order_line' in vals:
                for l in r.order_line:
                    l._get_line_numbers()
        return res


class wms_order_line_number(models.Model):
    _inherit = 'warehouse.order.line'

    def _get_line_numbers(self):
        line_num = 1
        if self.ids:
            first_line_rec = self.browse(self.ids[0])

            for line_rec in first_line_rec.order_id.order_line:
                line_rec.line_no = line_num
                line_num += 1

    line_no = fields.Integer(string='Serial Number', readonly=False, default=False)


class wms_order_linenumber(models.Model):
    _inherit = 'warehouse.order'

    @api.model
    def create(self, vals):
        res = super(wms_order_linenumber, self).create(vals)
        if vals.get('order_line'):
            for l in res.order_line:
                l._get_line_numbers()
        return res

    def write(self, vals):
        res = super(wms_order_linenumber, self).write(vals)
        for r in self:
            if 'order_line' in vals:
                for l in r.order_line:
                    l._get_line_numbers()
        return res


class smove_order_line_number(models.Model):
    _inherit = 'stock.move'

    def _get_line_numbers(self):
        line_num = 1
        if self.ids:
            first_line_rec = self.browse(self.ids[0])

            for line_rec in first_line_rec.picking_id.move_ids_without_package:
                line_rec.line_no = line_num
                line_num += 1

    line_no = fields.Integer(compute='_get_line_numbers', string='Serial Number', readonly=False, default=False)


# class spick_order_line_number(models.Model):
#     _inherit = 'stock.picking'
#
#     @api.model
#     def create(self, vals):
#         res = super(spick_order_line_number, self).create(vals)
#         print('fffffffffffffffffff',  self.move_ids_without_package)
#         if vals.get('move_ids_without_package'):
#             print('fffffffffffffffffff')
#
#             for l in res.move_ids_without_package:
#                 l._get_line_numbers()
#         return res
#
#     def write(self, vals):
#         res = super(spick_order_line_number, self).write(vals)
#         for r in self:
#             print('ggggggggggggggggggggg', self.move_ids_without_package)
#             if 'move_ids_without_package' in vals:
#                 for l in r.move_ids_without_package:
#                     l._get_line_numbers()
#         return res