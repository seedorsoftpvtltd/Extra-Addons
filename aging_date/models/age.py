from datetime import datetime

from odoo import models, fields, api, _
import datetime

class AgingDate(models.Model):
    _inherit = "account.move"

    x_agingdate = fields.Date(string='Aging Date', compute='_compute_aging_date_id')
    x_aging = fields.Integer(string='Aging', compute='_compute_aging_id')

    @api.depends('partner_id')
    def _compute_aging_date_id(self):
        for rec in self:
            rec["x_agingdate"] = datetime.datetime.now()

    @api.depends('x_agingdate', 'invoice_date_due')
    def _compute_aging_id(self):
        for rec in self:
            if rec.invoice_date_due:
                rec["x_aging"] = (rec.x_agingdate - rec.invoice_date_due).days
            else:
                rec["x_aging"] = False


