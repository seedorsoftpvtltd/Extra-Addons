# -*- coding: utf-8 -*-
# Part of Kanak Infosystems LLP.
# See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models


class ResCompany(models.Model):
    _inherit = "res.company"

    use_delivery_order_note = fields.Boolean(
        string='Default Terms & Conditions')
    delivery_order_note = fields.Text(
        string='Default Terms and Conditions', translate=True)


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    delivery_order_note = fields.Text(
        related='company_id.delivery_order_note', readonly=False,
        string="Terms & Conditions")
    use_delivery_order_note = fields.Boolean(
        related='company_id.use_delivery_order_note', readonly=False,
        string='Default Terms & Conditions')


class Picking(models.Model):
    _inherit = "stock.picking"

    @api.model
    def _default_note(self):
        if self.env.user.company_id.use_delivery_order_note:
            return self.env.user.company_id.delivery_order_note
        else:
            return ''

    note = fields.Text('Notes', default=_default_note)
