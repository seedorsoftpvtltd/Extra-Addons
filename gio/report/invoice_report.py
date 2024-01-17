# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models


class AccountInvoiceReport(models.Model):
    _inherit = 'account.invoice.report'

    teams_id = fields.Many2one('crm.team', string='GIO Team')

    def _select(self):
        return super(AccountInvoiceReport, self)._select() + ", move.teams_id as teams_id"

    def _group_by(self):
        return super(AccountInvoiceReport, self)._group_by() + ", move.teams_id"
