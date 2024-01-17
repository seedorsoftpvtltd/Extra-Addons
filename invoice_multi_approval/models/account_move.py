# -*- coding: utf-8 -*-
#############################################################################
#
#    Cybrosys Technologies Pvt. Ltd.
#
#    Copyright (C) 2020-TODAY Cybrosys Technologies(<https://www.cybrosys.com>).
#    Author: Sayooj A O(<https://www.cybrosys.com>)
#
#    You can modify it under the terms of the GNU AFFERO
#    GENERAL PUBLIC LICENSE (AGPL v3), Version 3.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU AFFERO GENERAL PUBLIC LICENSE (AGPL v3) for more details.
#
#    You should have received a copy of the GNU AFFERO GENERAL PUBLIC LICENSE
#    (AGPL v3) along with this program.
#    If not, see <http://www.gnu.org/licenses/>.
#
#############################################################################
from odoo import api, fields, models
import itertools
from operator import itemgetter
import operator

class AccountMove(models.Model):
    _inherit = 'account.move'

    approval_ids = fields.One2many('approval.line', 'move_id')
    document_fully_approved = fields.Boolean(compute='_compute_document_fully_approved')
    check_approve_ability = fields.Boolean(compute='_compute_check_approve_ability')
    is_approved = fields.Boolean(compute='_compute_is_approved')
    page_visibility = fields.Boolean(compute='_compute_page_visibility')

    state = fields.Selection(selection=[
        ('draft', 'Draft'),
        ('approve', 'Approved'),
        ('posted', 'Posted'),
        ('cancel', 'Cancelled')
    ], string='Status', required=True, readonly=True, copy=False, tracking=True,
        default='draft')

    @api.depends('approval_ids')
    def _compute_page_visibility(self):
        """Compute function for making the approval page visible/invisible"""
        if self.approval_ids:
            self.page_visibility = True
        else:
            self.page_visibility = False

    @api.onchange('partner_id')
    def _onchange_partner_id(self):
        """This is the onchange function of the partner which loads the
        persons for the approval to the approver table of the account.move"""
        res = super(AccountMove, self)._onchange_partner_id()
        invoice_approval_id = self.env['invoice.approval'].search([])
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

    @api.depends('approval_ids.approver_id')
    def _compute_check_approve_ability(self):
        """This is the compute function which check the current
        logged in user is eligible or not for approving the document"""
        current_user = self.env.uid
        approvers_list = []
        for approver in self.approval_ids:
            approvers_list.append(approver.approver_id.id)
        if current_user in approvers_list:
            self.check_approve_ability = True
        else:
            self.check_approve_ability = False

    def invoice_approve(self):
        """This is the function of the approve button also
        updates the approval table values according to the
        approval of the users"""
        self.ensure_one()
        current_user = self.env.uid
        for approval_id in self.approval_ids:
            if current_user == approval_id.approver_id.id:
                approval_id.update({'approval_status': True})
        for rec in self:
                if self.document_fully_approved == True:
                    rec['state'] = 'approve'

    def _compute_is_approved(self):
        """In this compute function we are verifying whether the document
        is approved/not approved by the current logged in user"""
        current_user = self.env.uid
        if self.invoice_line_ids and self.approval_ids:
            for approval_id in self.approval_ids:
                if current_user == approval_id.approver_id.id:
                    if approval_id.approval_status:
                        self.is_approved = True
                        break
                    else:
                        self.is_approved = False
                else:
                    self.is_approved = False
        else:
            self.is_approved = False

    @api.depends('approval_ids')
    def _compute_document_fully_approved(self):
        """This is the compute function which verifies whether
        the document is completely approved or not"""
        length_approval_ids = len(self.approval_ids)
        approval_ids = self.approval_ids
        approve_lines = approval_ids.filtered(lambda item: item.approval_status)
        length_approve_lines = len(approve_lines)
        if length_approval_ids == length_approve_lines:
            self.document_fully_approved = True
        else:
            self.document_fully_approved = False


class ApprovalLine(models.Model):
    _name = 'approval.line'
    _description = 'Approval line in Move'

    move_id = fields.Many2one('account.move')
    payment_id=fields.Many2one('account.payment')
    # bulk_payment=fields.Many2one('bulk.inv.payment')
    approver_id = fields.Many2one('res.users', string='Approver')
    approval_status = fields.Boolean(string='Status')

class Accountpayment(models.Model):
    _inherit='account.payment'
    approval_ids = fields.One2many('approval.line', 'payment_id')

    state = fields.Selection([('draft', 'Draft'),('approve', 'Approved'),('posted', 'Validated'),('reconciled','Reconciled'),('cancelled','Cancelled')],
                             required=True, default='draft')

    document_fully_approved = fields.Boolean(compute='_compute_document_fully_approvede')
    check_approve_ability = fields.Boolean(compute='_compute_check_approve_abilitye')
    is_approved = fields.Boolean(compute='_compute_is_approvede')
    page_visibility = fields.Boolean(compute='_compute_page_visibilitye')

    @api.depends('approval_ids')
    def _compute_page_visibilitye(self):
        """Compute function for making the approval page visible/invisible"""
        if self.approval_ids:
            self.page_visibility = True
        else:
            self.page_visibility = False

    @api.depends('approval_ids.approver_id')
    def _compute_check_approve_abilitye(self):
        """This is the compute function which check the current
        logged in user is eligible or not for approving the document"""
        current_user = self.env.uid
        approvers_list = []
        for approver in self.approval_ids:
            approvers_list.append(approver.approver_id.id)
        if current_user in approvers_list:
            self.check_approve_ability = True
        else:
            self.check_approve_ability = False

    def invoice_approve(self):
        #print("fuuuuuuuuuuu")
        """This is the function of the approve button also
        updates the approval table values according to the
        approval of the users"""
        self.ensure_one()
        current_user = self.env.uid
        for approval_id in self.approval_ids:
            if current_user == approval_id.approver_id.id:
                approval_id.update({'approval_status': True})
        for rec in self:
            if self.document_fully_approved == True:
                rec['state']='approve'

    def _compute_is_approvede(self):
        """In this compute function we are verifying whether the document
        is approved/not approved by the current logged in user"""
        current_user = self.env.uid
        if self.approval_ids:
            for approval_id in self.approval_ids:
                if current_user == approval_id.approver_id.id:
                    if approval_id.approval_status:
                        self.is_approved = True
                        break
                    else:
                        self.is_approved = False
                else:
                    self.is_approved = False
        else:
            self.is_approved = False

    @api.onchange('partner_id')
    def _onchange_partner_id(self):
        """This is the onchange function of the partner which loads the
        persons for the approval to the approver table of the account.move"""
        res = super(Accountpayment, self)._onchange_partner_id()
        payment_approver_ids = self.env['invoice.approval'].search([])
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


    @api.depends('approval_ids')
    def _compute_document_fully_approvede(self):
        """This is the compute function which verifies whether
        the document is completely approved or not"""
        length_approval_ids = len(self.approval_ids)
        approval_ids = self.approval_ids
        approve_lines = approval_ids.filtered(lambda item: item.approval_status)
        length_approve_lines = len(approve_lines)
        if length_approval_ids == length_approve_lines:
            self.document_fully_approved = True
        else:
            self.document_fully_approved = False


    def post(self):
        for rec in self:
            print(rec.state)
            print(rec.name)
            rec['state']='draft'
            res=super(Accountpayment, self).post()

    
    #def write(self,values):
        # print("hiii")
        #return super(Accountpayment, self).write(values)
    def writepayment(self):

        #print("hiii")
        # return super(Accountpayment, self).write(vals)
        vals = {
                        'journal_id': self.journal_id.id or False,
                        'amount': self.amount or 0.0,
                        'currency_id': self.currency_id.id,
                        'date': self.payment_date,
                        'bank_reference': self.bank_reference or '',
                        'cheque_reference': self.cheque_reference or '',
                        'payment_method_id': self.payment_method_id,
                        'partner_id': self.partner_id,

                    }
        payment=self.env['account.payment'].write(vals)
        return payment



# class bulk_inv_payment(models.TransientModel):
#     _inherit='bulk.inv.payment'
#
#     # approval_ids = fields.One2many('approval.line', 'bulk_payment')
#
#     # @api.model
#     def write_post(self):
#         # print("hiiisdffffffffffd")
#         # for res in self:
#         #     ress= self.env['account.payment'].write({
#         #         'payment_type': res.payment_type,
#         #         # 'payment_date': payment_date,
#         #         'partner_type': res.partner_type,
#         #         'payment_for': 'multi_payment',
#         #         'partner_id': res.invoice_ids.partner_id,
#         #         'journal_id': res.journal_id and self.journal_id.id or False,
#         #         'communication': res.communication,
#         #         # 'payment_method_id': payment_method_id and payment_method_id.id or False,
#         #         'state': 'draft',
#         #         # 'currency_id': res.get('values')[0].get('currency_id'),
#         #         'amount': 0.0}
#         #     )
#         #
#         #     print(ress)
#         # return ress
#         vals = []
#         for line in self.invoice_ids:
#             if line.paid_amount > 0.0:
#                 vals.append({
#                     'invoice_id': line.invoice_id or False,
#                     'partner_id': line.partner_id and line.partner_id.id or False,
#                     'amount': line.amount or 0.0,
#                     'paid_amount': line.paid_amount or 0.0,
#                     'currency_id': line.invoice_id.currency_id.id or False,
#                 })
#         new_vals = sorted(vals, key=itemgetter('partner_id'))
#         groups = itertools.groupby(new_vals, key=operator.itemgetter('partner_id'))
#         result = [{'partner_id': k, 'values': [x for x in v]} for k, v in groups]
#         new_payment_ids = []
#         for res in result:
#             payment_method_id = self.env['account.payment.method'].search([('name', '=', 'Manual')], limit=1)
#             if not payment_method_id:
#                 payment_method_id = self.env['account.payment.method'].search([], limit=1)
#             payment_date = False
#             if self.payment_date:
#                 payment_date = self.payment_date.strftime("%Y-%m-%d")
#             pay_val = {
#                 'payment_type': self.payment_type,
#                 'payment_date': payment_date,
#                 'partner_type': self.partner_type,
#                 'payment_for': 'multi_payment',
#                 'partner_id': res.get('partner_id'),
#                 'journal_id': self.journal_id and self.journal_id.id or False,
#                 'communication': self.communication,
#                 'payment_method_id': payment_method_id and payment_method_id.id or False,
#                 'state': 'draft',
#                 'currency_id': res.get('values')[0].get('currency_id'),
#                 'amount': 0.0,
#             }
#             payment_id = self.env['account.payment'].create(pay_val)
#
#             line_list = []
#             paid_amt = 0
#             inv_ids = []
#             vals=[]
#             for inv_line in res.get('values'):
#                 invoice = inv_line.get('invoice_id')
#                 inv_ids.append(invoice.id)
#                 full_reco = False
#                 if invoice.amount_residual == inv_line.get('paid_amount'):
#                     full_reco = True
#                 line_list.append((0, 0, {
#                     'invoice_id': invoice.id,
#                     'date': invoice.invoice_date,
#                     'due_date': invoice.invoice_date_due,
#                     'original_amount': invoice.amount_total,
#                     'balance_amount': invoice.amount_residual,
#                     'allocation': inv_line.get('paid_amount'),
#                     'full_reconclle': full_reco,
#                     'account_payment_id': payment_id and payment_id.id or False
#                 }))
#                 paid_amt += inv_line.get('paid_amount')
#             payment_approver_ids = self.env['invoice.approval'].search([])
#             # self.approval_ids = None
#             if payment_approver_ids.approve_customer_payment and self.partner_type == 'customer':
#                 for user in payment_approver_ids.payment_approver_ids:
#                     vals.append((0, 0, {
#                         'approver_id': user.id,
#
#                     }))
#             elif payment_approver_ids.approve_vendor_payment and self.partner_type == 'supplier':
#                 for user in payment_approver_ids.vendor_payment_approver_ids:
#                     vals.append((0, 0, {
#                         'approver_id': user.id,
#
#                     }))
#
#             payment_id.write({
#                 'line_ids': line_list,
#                 'amount': paid_amt,
#                 'invoice_ids': [(6, 0, inv_ids)],
#                 'approval_ids':vals,
#             })
#             new_payment_ids.append(payment_id)
#
#
#
#
#         return True
