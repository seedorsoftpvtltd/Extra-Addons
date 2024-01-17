from dateutil import parser
from odoo import api, models, fields, _
from datetime import datetime, date, timedelta
from odoo.exceptions import AccessError, UserError, ValidationError


class AccountMove(models.Model):
    _inherit = 'account.move'

    supp_id = fields.Many2one('summary.sheet', compute='_summary_sheet', string='Summary Sheet')

    def _summary_sheet(self):
        for rec in self:
            summ = self.env['summary.sheet'].search([('invoice_id', '=', rec.id)])
            if summ:
                for sum in summ:
                    rec['supp_id'] = sum.id
            else:
                rec['supp_id'] = False


class respartner(models.Model):
    _inherit = 'res.partner'

    def view_wms_invoices(self):
        domain = [('partner_id', '=', self.id), ('supp_id', '!=',False)]
        return {
            'type': 'ir.actions.act_window',
            'name': _('Invoices'),
            'res_model': 'account.move',
            'view_mode': 'tree,form',
            'limit': 80,
            'order': 'desc',
            # 'search_view_id': self.env.ref('account.view_invoice_tree').id,
            # 'views': ['list'],
            'domain': domain,
        }

