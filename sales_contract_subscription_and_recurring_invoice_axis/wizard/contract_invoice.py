# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, models, fields


class ContractReport(models.TransientModel):
    _name = "account.contract.invoice"
    _description = "Account Contract Invoice"

    date_from = fields.Date(string="Date", store=True)

    def invoice_generate(self):
        get_date = self.env['account.analytic.account'].sudo().search([('date_of_next_invoice','=',self.date_from)])
        for record in get_date:
            invoice = self.env['account.move'].create({
                'partner_id':record.partner_id.id,
                'type': 'out_invoice',
                'invoice_date': fields.Date.today(),
                'company_id':record.company_id.id,
            })
            for data in record.contact_line:
                invoice.write({
                    'invoice_line_ids': [(0, 0, {
                        'product_id': data.product_id.id,
                        'name':data.name,
                        'quantity':data.product_uom_qty,
                        'price_unit':data.price_unit,
                    })],        
                }) 
            record.write({'invoice_ids': invoice.ids})

class ContractBulkReport(models.TransientModel):
    _name = "bulk.contract.report"
    _description = "Account Contract Invoice"

    contract_lines = fields.Many2many('account.analytic.account', string="lines")
       