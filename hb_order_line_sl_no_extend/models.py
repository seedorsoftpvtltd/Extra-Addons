# -*- coding: utf-8 -*-

from odoo import models, fields, api
import logging
_logger = logging.getLogger(__name__)


class smove_order_line_number(models.Model):
    _inherit = 'stock.move'

    line_no = fields.Integer(string='Serial Number', readonly=False, default=False, store=True)


class spick_order_line_number(models.Model):
    _inherit = 'stock.picking'

    @api.model
    def create(self, vals):
        res = super(spick_order_line_number, self).create(vals)
        print('fffffffff11111111111111ffffffffff',  self.move_ids_without_package)
        if vals.get('move_ids_without_package'):
            print('if11111111')
            for l in res.move_ids_without_package:
                l._get_line_numbers()
        return res

    def write(self, vals):
        res = super(spick_order_line_number, self).write(vals)
        for r in self:
            print('gggggggg222222222222ggggggggggggg', self.move_ids_without_package)
            for l in r.move_ids_without_package:
                l._get_line_numbers()
            if vals.get('move_ids_without_package'):
                print('if222222222222222222222')
                for l in r.move_ids_without_package:
                    l._get_line_numbers()
        return res