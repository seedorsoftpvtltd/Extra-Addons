# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    security_leads = fields.Float(related='company_id.security_leads', string="Security Lead Time", readonly=False)
    group_display_incoterms = fields.Boolean("Incoterms", implied_group='gio_stock.group_display_incotermss')
    group_lot_on_invoice = fields.Boolean("Display Lots & Serial Numbers on Invoices",
        implied_group='gio_stock.group_lot_on_invoices')
    use_security_leads = fields.Boolean(
        string="Security Lead Time for Sales",
        config_parameter='gio_stock.use_security_leads',
        help="Margin of error for dates promised to customers. Products will be scheduled for delivery that many days earlier than the actual promised date, to cope with unexpected delays in the supply chain.")
    default_picking_policy = fields.Selection([
        ('direct', 'Ship products as soon as available, with back orders'),
        ('one', 'Ship all products at once')
        ], "Picking Policy", default='direct', default_model="goods.issue.order", required=True)

    @api.onchange('use_security_leads')
    def _onchange_use_security_lead(self):
        if not self.use_security_leads:
            self.security_leads = 0.0
