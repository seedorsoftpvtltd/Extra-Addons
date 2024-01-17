from odoo import models, fields, api, _

class AccountMove(models.Model):
    _inherit='account.move'

    def post(self):
        res = super(AccountMove, self).post()
        if not self.type == 'entry':
            line=self.invoice_line_ids
            for lines in line:
                if lines:
                    lines.partner_id=self.partner_id
            line_ids=self.line_ids
            for rec in line_ids:
                if not rec.partner_id:
                    rec.partner_id=self.partner_id
            return res


