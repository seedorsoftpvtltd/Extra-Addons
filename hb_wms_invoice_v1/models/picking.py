from odoo import api, models, fields, http, _
from datetime import datetime, date, timedelta
from odoo.exceptions import AccessError, UserError, ValidationError
import logging


class PickingInvoice(models.Model):
    _inherit = "stock.picking"

    invoice_count = fields.Integer(string='Invoices', compute='_compute_invoice_count')
    operation_code = fields.Selection(related='picking_type_id.code')

    def _compute_invoice_count(self):
        for picking_id in self:
            move_ids = self.env['account.move'].search([('invoice_origin', '=', picking_id.name)])
            if move_ids:
                self.invoice_count = len(move_ids)
            else:
                self.invoice_count = 0

    def create_invoice_in(self):
        for picking_id in self:
            current_user = self.env.uid
            if picking_id.picking_type_id.code == 'incoming':

                invoice_line_list = []
                for pick in picking_id.service_id:
                    vals = (0, 0, {
                        'name': pick.product_id.name,
                        'product_id': pick.product_id.id,
                        'price_unit': pick.qty,
                        'account_id': pick.product_id.property_account_income_id.id if pick.product_id.property_account_income_id
                        else pick.product_id.categ_id.property_account_income_categ_id.id,
                        'tax_ids': [(6, 0, [pick.taxes_id.id])] if pick.taxes_id else False,
                        'quantity': pick.price,

                    })
                    invoice_line_list.append(vals)
                invoice = picking_id.env['account.move'].create({
                    'type': 'out_invoice',
                    'invoice_origin': picking_id.name,
                    'invoice_user_id': current_user,
                    'narration': picking_id.name,
                    'partner_id': picking_id.partner_id.id,
                    'currency_id': picking_id.env.user.company_id.currency_id.id,
                    # 'journal_id': int(UOMer_journal_id),
                    'invoice_payment_ref': picking_id.name,
                    # 'picking_id': picking_id.id,
                    'invoice_line_ids': invoice_line_list
                })
                return invoice

    def create_invoice_out(self):
        for picking_id in self:
            current_user = self.env.uid
            if picking_id.picking_type_id.code == 'outgoing':

                invoice_line_list = []
                for pick in picking_id.service_id:
                    vals = (0, 0, {
                        'name': pick.product_id.name,
                        'product_id': pick.product_id.id,
                        'price_unit': pick.qty,
                        'account_id': pick.product_id.property_account_income_id.id if pick.product_id.property_account_income_id
                        else pick.product_id.categ_id.property_account_income_categ_id.id,
                        'tax_ids': [(6, 0, [pick.taxes_id.id])] if pick.taxes_id else False,
                        'quantity': pick.price,

                    })
                    invoice_line_list.append(vals)
                invoice = picking_id.env['account.move'].create({
                    'type': 'out_invoice',
                    'invoice_origin': picking_id.name,
                    'invoice_user_id': current_user,
                    'narration': picking_id.name,
                    'partner_id': picking_id.partner_id.id,
                    'currency_id': picking_id.env.user.company_id.currency_id.id,
                    # 'journal_id': int(UOMer_journal_id),
                    'invoice_payment_ref': picking_id.name,
                    # 'picking_id': picking_id.id,
                    'invoice_line_ids': invoice_line_list
                })
                return invoice


class TransferServiceTab(models.Model):
    _inherit = "picking.services"

    product_uom = fields.Many2one('uom.uom', 'Unit of Measure', required=False)
