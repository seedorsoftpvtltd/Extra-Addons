from odoo import models, _, api, fields


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    @api.model
    def create(self, vals_list):
        return super(SaleOrder, self).create(vals_list)

    def _action_confirm(self):
        res = super(SaleOrder, self)._action_confirm()

        automate_purchase = self.env['ir.config_parameter'].sudo().get_param('automate_sale')
        automate_invoice = self.env['ir.config_parameter'].sudo().get_param('automate_invoice')
        automate_print_invoices = self.env['ir.config_parameter'].sudo().get_param('automate_print_invoices')
        automate_validate_voice = self.env['ir.config_parameter'].sudo().get_param('automate_validate_voice')
        if automate_print_invoices:
            self.automate_print_invoices = True
        if automate_invoice:
            self._create_invoices()
            if automate_validate_voice:
                self.invoice_ids.action_post()

        return res
