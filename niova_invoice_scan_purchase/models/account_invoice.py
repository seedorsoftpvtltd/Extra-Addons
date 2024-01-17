# -*- coding: utf-8 -*-
#################################################################################
# Author      : Niova IT ApS (<https://niova.dk/>)
# Copyright(c): 2018-Present Niova IT ApS
# License URL : https://invoice-scan.com/license/
# All Rights Reserved.
#################################################################################
import sys
from odoo import models, api, fields
import logging

_logger = logging.getLogger(__name__)

class AccountInvoice(models.Model):
    _inherit = 'account.move'
    
    # -------------------------------------------------------------------------
    # ACTIONS
    # -------------------------------------------------------------------------        
    def action_add_purchase_lines(self):
        self._add_invoice_lines('purchase')

    # -------------------------------------------------------------------------
    # ATTACHMENTS
    # -------------------------------------------------------------------------
    def _auto_attach_invoice_lines(self):
        res = False
        if self.partner_id and not self.invoice_line_ids:
            # First do purchase order line attachment
            if self.partner_id.property_invoice_automation_purchase:
                try:
                    res = self._attach_invoice_lines('purchase')
                    self.env.cr.commit()
                except:
                    self.env.cr.rollback()
                    _logger.exception('Invoice (invoice id: {invoice_id}) did not add invoice lines due to an unexpected error: {error_content}'.format(error_content=sys.exc_info()[1], invoice_id=self.id))
            
            # If non was found then do normal flow
            if not res and not self.partner_id.property_invoice_automation_purchase:
                res = super(AccountInvoice, self)._auto_attach_invoice_lines()
        return res

    def _attach_invoice_lines(self, attach_type):
        res = False
        if attach_type == 'purchase':
            res = self._add_purchase_orders()
        return super(AccountInvoice, self)._attach_invoice_lines(attach_type) if not res else res

    def _add_purchase_orders(self):
        self.ensure_one()
        if not self.voucher_id:
            return False
        try:
            new_lines = self.env['account.move.line']
            PurchaseOrder = self.env['purchase.order']
            for purchase_order in self.voucher_id.get_purchase_references():
                po = PurchaseOrder.search([('name', '=', purchase_order),
                                           ('company_id', '=', self.company_id.id)], limit=1)
                if po:
                    new_lines = self._add_purchase_order_line(po, new_lines)
            if new_lines:
                self.line_ids += new_lines
                self.payment_term_id = self.purchase_id.payment_term_id

                # Apply the taxes
                new_lines._onchange_mark_recompute_taxes()
                return True
        except:
            _logger.exception("Purchases was not added to vendor bill: %s", sys.exc_info()[1])
        return False

    def _add_purchase_order_line(self, purchase, new_lines):
        # Add missing partner if it exist in the purchase
        if not self.partner_id:
            self.partner_id = purchase.partner_id.id

        for line in purchase.order_line - self.line_ids.mapped('purchase_line_id'):
            data = line._prepare_account_move_line(self)
            
            # Cash the lines if it is an user action
            new_line = new_lines.new(data)
            new_line.account_id = new_line._get_computed_account()
            new_line._onchange_price_subtotal()
            new_lines += new_line
        return new_lines