from odoo import api, fields, models, _
from odoo.http import request
import os
from odoo.exceptions import UserError, AccessError, MissingError, ValidationError
import datetime


class Stockmove(models.Model):
    _inherit = 'stock.move.line'

    @api.onchange("result_package_id")
    def _onchange_result_package_id(self):
        for rec in self:
            if rec.serial == False:
                pallet = self.env['stock.move.line'].search([('picking_code', '=', 'incoming')])
                for pal in pallet:
                    if pal.result_package_id:
                        if pal.result_package_id == rec.result_package_id:
                            raise UserError('Pallet Id must be Unique!')