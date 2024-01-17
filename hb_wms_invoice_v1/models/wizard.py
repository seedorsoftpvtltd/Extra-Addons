from dateutil import parser
from odoo import api, models, fields, http, _
from datetime import datetime, date, timedelta
from odoo.exceptions import AccessError, UserError, ValidationError
import logging
from odoo.exceptions import AccessError, UserError, ValidationError

logger = logging.getLogger(__name__)


class ReportWizard(models.TransientModel):
    _name = 'generate.invoice'

    partner_id = fields.Many2one('res.partner', string="Customer", required=True)
    start_date = fields.Date('Start Date', required=True)
    end_date = fields.Date('End Date', required=True)
    overall_report = fields.Boolean('View All Records')
    company_id = fields.Many2one('res.company', string='Company', default=lambda self: self.env.company)

    def generate_invoice(self):
        if self.partner_id:
            agreement = self.env['agreement'].search([('partner_id','=',self.partner_id.id)])
            if not agreement:
                raise ValidationError(_('The chosen customer is not sync with the Agreement !'))

            # agreement.write({'start_date': self.start_date, 'end_date': self.end_date})
            for ag in agreement:
                print(self.start_date, 'self.start_date', self.end_date, 'self.end_date')
                if self.start_date and self.end_date:
                    ag.write({'start_date':self.start_date, 'end_date': self.end_date})
                    existing_invoices = self.env['account.move'].search([('sto_type', '=' ,'warehouse'),
                                                             ('start_date_sto', '<=', self.start_date), ('state', '!=', 'cancel')])
                    existing_invoices1 = self.env['account.move'].search([('sto_type', '=', 'warehouse'),
                                                                         ('end_date_sto', '>=', self.end_date),
                                                                         ('state', '!=', 'cancel')])
                    # if existing_invoices:
                    #     raise ValidationError(_('Invoice already generated for this customer !'))
                    # if existing_invoices1:
                    #     raise ValidationError(_('Invoice already generated for this customer !'))

                    # ag['start_date'] = self.start_date
                    # ag['end_date'] = self.end_date
            invoices = self.partner_id.create_inv_invoice_coree()


            search_view_ref = self.env.ref('account.view_account_invoice_filter', False)
            form_view_ref = self.env.ref('account.view_move_form', False)
            tree_view_ref = self.env.ref('account.view_move_tree', False)
            print('invoices', invoices)
            return {
                'domain': [('partner_id', '=', self.partner_id.id), ('id','in',invoices)],
                'name': 'Invoices',
                'res_model': 'account.move',
                'type': 'ir.actions.act_window',
                'views': [(tree_view_ref.id, 'tree'), (form_view_ref.id, 'form')],
                # 'search_view_id': search_view_ref and search_view_ref.id,
            }
