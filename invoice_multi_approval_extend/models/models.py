from odoo import fields, models,api,_
from odoo.exceptions import ValidationError

class InvoiceApproval(models.Model):
    _inherit = 'invoice.approval'

    company_id=fields.Many2one('res.company',string='Company',default=lambda self: self.env.company)


    @api.model
    def search(self, args, offset=0, limit=None, order=None, count=False):
        current_company_id = self.env.company.id
        args.append(('company_id', '=', current_company_id))
        return super(InvoiceApproval, self).search(args, offset, limit, order, count)


    @api.model
    def create(self,vals):
        res = super(InvoiceApproval, self).create(vals)
        total_len = self.env['invoice.approval'].sudo().search_count([])
        if total_len > 1:
            raise ValidationError(_('You can have only one approval configuration per company'))
        return res

class AccountMove(models.Model):
    _inherit = 'account.move'

    document_fully_approved = fields.Boolean(compute='compute_document_fully_approvede_extend')

    @api.onchange('partner_id')
    def _onchange_partner_id(self):
        """This is the onchange function of the partner which loads the
        persons for the approval to the approver table of the account.move"""
        res = super(AccountMove, self)._onchange_partner_id()
        invoice_approval_id = self.env['invoice.approval'].search([('company_id', '=', self.env.company.id)])
        self.approval_ids = None
        if invoice_approval_id.approve_customer_invoice and self.type == 'out_invoice':
            for user in invoice_approval_id.invoice_approver_ids:
                vals = {
                    'approver_id': user.id
                }
                self.approval_ids |= self.approval_ids.new(vals)
        elif invoice_approval_id.approve_vendor_bill and self.type == 'in_invoice':
            for user in invoice_approval_id.bill_approver_ids:
                vals = {
                    'approver_id': user.id
                }
                self.approval_ids |= self.approval_ids.new(vals)
        elif invoice_approval_id.approve_customer_credit and self.type == 'out_refund':
            for user in invoice_approval_id.cust_credit_approver_ids:
                vals = {
                    'approver_id': user.id
                }
                self.approval_ids |= self.approval_ids.new(vals)
        elif invoice_approval_id.approve_vendor_credit and self.type == 'in_refund':
            for user in invoice_approval_id.vend_credit_approver_ids:
                vals = {
                    'approver_id': user.id
                }
                self.approval_ids |= self.approval_ids.new(vals)
        return res


    @api.depends('approval_ids')
    def compute_document_fully_approvede_extend(self):
        """This is the compute function which verifies whether
        the document is completely approved or not"""
        length_approval_ids = len(self.approval_ids)
        approval_ids = self.approval_ids
        approve_lines = approval_ids.filtered(lambda item: item.approval_status)
        length_approve_lines = len(approve_lines)
        print(length_approve_lines)
        if self.type == 'entry':
            self.document_fully_approved = True
        else:
            if not length_approval_ids:
                self.document_fully_approved = True
            else:
                if length_approve_lines > 0:

                    self.document_fully_approved = True
                else:
                    self.document_fully_approved = False




class AccountPayment(models.Model):

    _inherit='account.payment'

    document_fully_approved = fields.Boolean(compute='compute_document_fully_approvede_extend')

    @api.onchange('partner_id')
    def _onchange_partner_id(self):
        """This is the onchange function of the partner which loads the
        persons for the approval to the approver table of the account.move"""
        res = super(AccountPayment, self)._onchange_partner_id()
        payment_approver_ids = self.env['invoice.approval'].search([('company_id', '=', self.env.company.id)])
        self.approval_ids = None
        if payment_approver_ids.approve_customer_payment and self.partner_type == 'customer':
            for user in payment_approver_ids.payment_approver_ids:
                vals = {
                    'approver_id': user.id
                }
                self.approval_ids |= self.approval_ids.new(vals)
        elif payment_approver_ids.approve_vendor_payment and self.partner_type == 'supplier':
            for user in payment_approver_ids.vendor_payment_approver_ids:
                vals = {
                    'approver_id': user.id
                }
                self.approval_ids |= self.approval_ids.new(vals)
        return res

    @api.depends('approval_ids')
    def compute_document_fully_approvede_extend(self):
        """This is the compute function which verifies whether
        the document is completely approved or not"""
        length_approval_ids = len(self.approval_ids)
        approval_ids = self.approval_ids
        approve_lines = approval_ids.filtered(lambda item: item.approval_status)
        length_approve_lines = len(approve_lines)

        if not length_approval_ids:
            self.document_fully_approved = True
        else:
            if length_approve_lines > 0:

                self.document_fully_approved = True
            else:
                self.document_fully_approved = False