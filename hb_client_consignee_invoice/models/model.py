from dateutil import parser
from odoo import api, models, fields, http, _
from datetime import datetime, date, timedelta
from odoo.exceptions import AccessError, UserError, ValidationError
import logging


class wovalidation(models.Model):
    _inherit = "warehouse.order"

    @api.onchange('partner_id')
    def _partner_onchange(self):
        for rec in self.order_line:
            print(rec, 'rec')
            rec.write({'order_id': False})
            # rec.unlink()

    def button_confirm(self):
        print('button confirm')
        for rec in self:
            for r in rec.order_line:
                if r.product_id.item:
                    if r.product_id.customer_id not in [rec.partner_id, rec.x_consignee]:
                    # if rec.partner_id != r.product_id.customer_id or rec.x_consignee != r.product_id.customer_id:
                        raise UserError(_('Make sure the product is under the selected the customer!'))
        return super(wovalidation, self).button_confirm()


class giovalidation(models.Model):
    _inherit = "goods.issue.order"

    @api.onchange('partner_id')
    def _partner_onchange(self):
        for rec in self.order_line:
            print(rec, 'rec')
            rec.write({'order_id': False})
            # rec.unlink()

    def action_confirm(self):
        print('button confirm')
        for rec in self:
            for r in rec.order_line:
                if r.product_id.item:
                    if r.product_id.customer_id not in [rec.partner_id, rec.consignee]:
                    # if rec.partner_id != r.product_id.customer_id or rec.consignee != r.product_id.customer_id:
                        raise UserError(_('Make sure the product is under the selected the customer!'))
        return super(giovalidation, self).action_confirm()
