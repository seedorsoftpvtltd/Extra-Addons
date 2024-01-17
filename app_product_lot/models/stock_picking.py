# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _
from odoo.exceptions import UserError


class StockPicking(models.Model):
    _inherit = ['stock.picking']
    
    def ml_get_lot_name_auto(self):
        # 自动生成批次/序列号
        # 当
        self = self.filtered(lambda r: r.state in ['waiting', 'confirmed', 'assigned'])
        # ids = self.filtered(lambda r: not r.lot_name and r.product_id.tracking != 'none')
        for rec in self:
            # 注意，此处只处理没装箱的
            for m in rec.move_ids_without_package:
                sku = m.product_id
                if sku.tracking == 'lot':
                    # 处理批次的
                    pass
                elif sku.tracking == 'serial':
                    # 处理序列号的，暂时只1对1
                    pass
                if sku.tracking_sequence:
                    name = sku.tracking_sequence.next_by_id()
                else:
                    name = self.env['ir.sequence'].with_context(force_company=sku.company_id.id).next_by_code('stock.lot.serial') or ''
                rec.write({'lot_name': name})
