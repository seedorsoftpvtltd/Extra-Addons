# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import models, api, fields, _
from odoo.tools.misc import format_date


class report_account_aged_partner(models.AbstractModel):
    _inherit = ["account.aged.partner", "account.report"]
    _description = "Aged Partner Balances"

    filter_analytic = True
