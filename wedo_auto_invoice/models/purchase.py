# -*- coding: utf-8 -*-
# Copyright 2020 WeDo Technology
# Website: http://wedotech-s.com
# Email: apps@wedotech-s.com
# Phone:00249900034328 - 00249122005009

from odoo import api, models, fields

class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    def create_invoice(self):
        bill = self.env['account.move'].browse()

        bill = bill.new({
            'date': fields.date.today(),
            'partner_id': self.partner_id.id,
            'ref': self.partner_ref,
            'company_id': self.env.company.id,
            'invoice_payment_term_id': self.payment_term_id.id,
            'currency_id': self.currency_id.id,
            'fiscal_position_id': self.fiscal_position_id,
            'type': 'in_invoice',
            'purchase_id': self.id,
        })
        bill._onchange_purchase_auto_complete()
        self.invoice_ids += bill

    def _get_invoiced(self):
        super(PurchaseOrder, self)._get_invoiced()
        if self.invoice_status == 'to invoice' and self.company_id.auto_invoice:
            self.create_invoice()
            super(PurchaseOrder, self)._get_invoiced()


