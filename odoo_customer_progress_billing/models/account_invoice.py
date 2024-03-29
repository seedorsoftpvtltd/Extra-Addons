# -*- coding: utf-8 -*-

from odoo import models, fields, api, _

class AccountInvoice(models.Model):
#    _inherit = 'account.invoice'
    _inherit = 'account.move'

    #@api.multi
    @api.depends('project_id')
    def _set_total_progress_bill(self):
        for rec in self:
            rec.total_progress_billing = rec.project_id.total_progress_account
            
    #@api.multi
#    @api.depends('amount_total')
    @api.depends('project_id', 'amount_total')#13 Add project due to calculate invoice_to_date amount if project change
    def _set_invoiceto_date(self):
        for rec in self:
            rec.invoice_to_date = 0.0
#            cus_inv = self.search([('state', 'in', ['open', 'paid']), ('partner_id', '=', rec.partner_id.id), ('project_id', '=', rec.project_id.id)])
            if rec.project_id:#odoo13
                cus_inv = self.search(['|', ('state', 'in', ['posted']), ('invoice_payment_state', 'in', ['paid']), ('partner_id', '=', rec.partner_id.id), ('project_id', '=', rec.project_id.id), ('type', '=', 'out_invoice')])
                for inv in cus_inv:
                    rec.invoice_to_date += inv.amount_total
            
    #@api.multi
    @api.depends('total_progress_billing', 'invoice_to_date')
    def _set_remaining_progress_billing(self):
        for rec in self:
            rec.remaining_progress_billing = rec.total_progress_billing - rec.invoice_to_date
            
    #@api.multi
#    @api.depends('amount_total','residual')
    @api.depends('project_id', 'amount_total', 'amount_residual')#13 Add project due to calculate previously_invoice
    def _set_previously_invoiced(self):
        for rec in self:
#            pre_inv = self.search([('state', 'in', ['open', 'paid']), ('partner_id', '=', rec.partner_id.id), ('project_id', '=', rec.project_id.id)])
            rec.previously_invoice = 0.0
            rec.previously_invoice_due = 0.0
            if rec.project_id:#Search projects if project on invoice
                pre_inv = self.search(['|', ('state', 'in', ['posted']), ('invoice_payment_state', 'in', ['paid']), ('partner_id', '=', rec.partner_id.id), ('project_id', '=', rec.project_id.id), ('type', '=', 'out_invoice')])
                print ("pre_inv:---------------------",pre_inv)
                if len(pre_inv) == 1:
                    rec.previously_invoice = 0.0
                if len(pre_inv) > 1:
                    rec.previously_invoice = 0.0
                    for pre in pre_inv:
                        if pre.id != rec.id:
                            rec.previously_invoice += pre.amount_total
    #                        rec.previously_invoice_due += pre.residual
                            rec.previously_invoice_due += pre.amount_residual
                            print ("residual:-------------------",pre.amount_residual)
                #rec.previously_invoice = rec.previously_invoice - rec.amount_total
                #rec.previously_invoice_due = rec.previously_invoice_due - rec.residual
    
    #@api.multi
    @api.depends('amount_total')
    def _set_current_invoiced(self):
        for rec in self:
            rec.current_invoice = rec.amount_total
            
    #@api.multi
#    @api.depends('residual')
    @api.depends('amount_residual')
    def _set_less_paid_amount(self):
        for rec in self:
#            rec.less_paid_amount = rec.residual
            rec.less_paid_amount = rec.amount_residual
            
    #@api.multi
    @api.depends('less_paid_amount','previously_invoice','current_invoice')
    def _set_total_due(self):
        for rec in self:
            rec.total_due = rec.previously_invoice_due + rec.less_paid_amount
    
    progress_bill_title = fields.Char(
        string='Progress Billing Title',
    )
    project_id = fields.Many2one(
        'account.analytic.account',
        string='Project',
        copy=False,
    )
    total_progress_billing = fields.Float(
        string="Total Progress Billing",
        compute='_set_total_progress_bill',
        copy=False,
        store=True,
    )
    invoice_to_date = fields.Float(
        string="Invoice To Date",
        compute='_set_invoiceto_date',
        copy=False,
        store=True,
    )
    remaining_progress_billing = fields.Float(
        string="Remaining Progress Billing",
        compute='_set_remaining_progress_billing',
        copy=False,
        store=True,
    )
    previously_invoice = fields.Float(
        string="Previously Invoiced",
        compute='_set_previously_invoiced',
        copy=False,
#         store=True,
        store=True,
    )
    previously_invoice_due = fields.Float(
        string="Previously Invoiced Due",
        compute='_set_previously_invoiced',
        copy=False,
#         store=True,
        store=True,
    )
    current_invoice = fields.Float(
        string="Current Invoiced",
        compute='_set_current_invoiced',
        copy=False,
        store=True,
    )
    less_paid_amount = fields.Float(
        string="Less Paid Amount",
        compute='_set_less_paid_amount',
        copy=False,
        store=True,
    )
    total_due = fields.Float(
        string="Total Due Now",
        compute='_set_total_due',
        copy=False,
        store=True,
    )
    
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
