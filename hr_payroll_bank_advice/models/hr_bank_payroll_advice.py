# -*- coding:utf-8 -*-

from datetime import date
from datetime import datetime

# from openerp import api, fields, models, _
# import openerp.addons.decimal_precision as dp
# from openerp.exceptions import UserError
from odoo import api, fields, models, _
import odoo.addons.decimal_precision as dp
from odoo.exceptions import UserError


class HrBankPayrollAdvice(models.Model):
    _name = 'custom.hr.bank.payroll.advice'
    #_inherit = ['mail.thread']
    # _inherit = ['mail.thread', 'mail.activity.mixin', 'portal.mixin']      # odoo11
    _inherit = ['mail.thread', 'mail.activity.mixin']

    _order = "id desc"

    today = date.today()

    name = fields.Char(
        string="Name",
        readonly=True,
        required=True,
        states={'draft': [('readonly', False)]}
    )
    date = fields.Date(
        string="Date",
        readonly=True,
        required=True,
        states={'draft': [('readonly', False)]},
        default=today,
        help='Advice Date is used to search Payslips',
    )
    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirm', 'Confirmed'),
        ('cancel', 'Cancelled'),
        ], string='Status', default='draft', index=True, readonly=True)
    
    number = fields.Char(
        readonly=True
    )
    line_ids = fields.One2many(
        'custom.hr.bank.payroll.advice.line',
        'advice_id',
        string='Employee Salary',
        states={'draft': [('readonly', False)]},
        readonly=True,
        copy=True
    )
    company_id = fields.Many2one(
        'res.company',
        string='Company',
        required=True,
        readonly=True,
        states={'draft': [('readonly', False)]},
        default=lambda self: self.env.user.company_id
    )
    bank_id = fields.Many2one(
        'res.bank',
        string='Bank',
        readonly=True,
        states={'draft': [('readonly', False)]},
        help='Select the Bank from which the salary is going to be paid'
    )
    batch_id = fields.Many2one(
        'hr.payslip.run',
        string='Batch',
        readonly=True
    )
    partner_id = fields.Many2one(
        related='company_id.partner_id',
    )
    custom_partner_bank_id = fields.Many2one(
        'res.partner.bank',
        required=True,
        string='Bank Account'
    )

    # @api.multi
    def payment_advice_lines(self):
        for advice in self:
            old_lines = self.env['custom.hr.bank.payroll.advice.line'].search([('advice_id', '=', advice.id)])
            if old_lines:
                old_lines.unlink()
            payslips = self.env['hr.payslip'].search([('date_from', '<=', advice.date), ('date_to', '>=', advice.date), ('state', '=', 'done')])
            for slip in payslips:
                if not slip.employee_id.bank_account_id and not slip.employee_id.bank_account_id.acc_number:
                    raise UserError(_('Please define bank account for the %s employee') % (slip.employee_id.name,))
                payslip_line = self.env['hr.payslip.line'].search([('slip_id', '=', slip.id), ('code', 'in', ('NET','NETSNET00'))], limit=1)
                if payslip_line:
                    self.env['custom.hr.bank.payroll.advice.line'].create({
                        'advice_id': advice.id,
                        'employee_bank': slip.employee_id.bank_account_id.bank_id.name,
                        'ifsc_code': slip.employee_id.bank_account_id.bank_id.bic,
                        'name': slip.employee_id.bank_account_id.acc_number,
                        'employee_id': slip.employee_id.id,
                        'bysal': payslip_line.total
                    })
                slip.advice_id = advice.id

    # @api.multi
    def confirm_advice_sheet(self):
        for advice in self:
            if not advice.line_ids:
                raise UserError(_('You can not confirm Payment advice without advice lines.'))
            date = fields.Date.from_string(fields.Date.today())
            advice_date = str(date.month).zfill(2) + '-' + str(date.year)
            advice_number = self.env['ir.sequence'].next_by_code('payment.advice')
            advice.write({
                'number': 'PAY' + '/' + advice_date + '/' + advice_number,
                'state': 'confirm',
            })

    def get_advice_month(self, input_date):
        res = {
               'from_name': '', 'to_name': ''
               }
        slip = self.env['hr.payslip'].search([('date_from', '<=', input_date), ('date_to', '>=', input_date)], limit=1)
        if slip:
            start_date = datetime.strptime(str(slip.date_from), '%Y-%m-%d')
            end_date = datetime.strptime(str(slip.date_to), '%Y-%m-%d')
            res['from_name'] = start_date.strftime('%d') + '-' + start_date.strftime('%B') + '-' + start_date.strftime('%Y')
            res['to_name'] = end_date.strftime('%d') + '-' + end_date.strftime('%B') + '-' + end_date.strftime('%Y')
        return res

    # @api.multi
    def action_bank_payroll_send(self):
        self.ensure_one()
        ir_model_data = self.env['ir.model.data']
        try:
            template_id = ir_model_data.get_object_reference('hr_payroll_bank_advice', 'email_template_bank_payroll_send')[1]
        except ValueError:
            template_id = False
        try:
            compose_form_id = ir_model_data.get_object_reference('mail', 'email_compose_message_wizard_form')[1]
        except ValueError:
            compose_form_id = False
        ctx = dict()
        ctx.update({
            'default_model': 'custom.hr.bank.payroll.advice',
            'default_res_id': self.ids[0],
            'default_use_template': bool(template_id),
            'default_template_id': template_id,
            'default_composition_mode': 'comment',
            'mark_so_as_sent': True,
        })
        return {
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'mail.compose.message',
            'views': [(compose_form_id, 'form')],
            'view_id': compose_form_id,
            'target': 'new',
            'context': ctx,
        }

    # @api.multi
    def set_to_draft(self):
        """Resets Advice as draft.
        """
        self.write({'state': 'draft'})

    # @api.multi
    def cancel_advice_sheet(self):
        self.write({'state': 'cancel'})

    @api.onchange('company_id')
    def _onchange_company_id(self):
        self.bank_id = self.custom_partner_bank_id.bank_id

class HrBankPayslipRun(models.Model):
    _inherit = 'hr.payslip.run'
    _description = 'Payslip Batches'

    custom_payment_advice = fields.Many2one(
        'custom.hr.bank.payroll.advice',
        string='Payment Advice'
    )
    custom_partner_bank_id = fields.Many2one(
        'res.partner.bank',
        string='Bank Account'
    )

    # @api.multi
    def draft_payslip_run(self):
        res = super(HrBankPayslipRun, self).draft_payslip_run()
        self.write({'custom_payment_advice': False})
        return res

    # @api.multi
    def create_bank_advice(self):
        for run in self:
            if run.custom_payment_advice:
                raise UserError("Payment advice already created.")
            if not run.custom_partner_bank_id:
                raise UserError(_("Please select your company bank account."))
            company = self.env.user.company_id
            advice = self.env['custom.hr.bank.payroll.advice'].create({
                        'batch_id': run.id,
                        'company_id': company.id,
                        'name': run.name,
                        'date': run.date_end,
                        'custom_partner_bank_id':run.custom_partner_bank_id.id,
                        'bank_id': run.custom_partner_bank_id.bank_id and run.custom_partner_bank_id.bank_id.id or False
                    })
            for slip in run.slip_ids:
                if not slip.employee_id.bank_account_id or not slip.employee_id.bank_account_id.acc_number:
                    raise UserError(_('Please define bank account for the %s employee') % (slip.employee_id.name))
                payslip_line = self.env['hr.payslip.line'].search([('slip_id', '=', slip.id), ('code', 'in',( 'NET','NETSNET00'))], limit=1)
                if payslip_line:
                    self.env['custom.hr.bank.payroll.advice.line'].create({
                        'advice_id': advice.id,
                        'employee_bank': slip.employee_id.bank_account_id.bank_id.name,
                        'ifsc_code': slip.employee_id.bank_account_id.bank_id.bic,
                        'name': slip.employee_id.bank_account_id.acc_number,
                        'employee_id': slip.employee_id.id,
                        'bysal': payslip_line.total
                    })
        self.custom_payment_advice = advice

class HrBankPayrollAdviceLine(models.Model):
    _name = 'custom.hr.bank.payroll.advice.line'
    _description = 'Bank Advice Lines'

    advice_id = fields.Many2one('custom.hr.bank.payroll.advice', string='Bank Advice')
    name = fields.Char('Bank Account No.', required=True)
    employee_bank = fields.Char('Bank', required=True)
    ifsc_code = fields.Char(string='IFSC Code')
    employee_id = fields.Many2one('hr.employee', string='Employee', required=True)
    bysal = fields.Float(string='By Salary', digits=dp.get_precision('Payroll'))
    debit_credit = fields.Char(string='C/D', default='C')
    company_id = fields.Many2one('res.company', related='advice_id.company_id', string='Company', store=True)

    @api.onchange('employee_id')
    def onchange_employee_id(self):
        self.name = self.employee_id.bank_account_id.acc_number
        self.employee_bank = self.employee_id.bank_account_id.bank_id.name
        self.ifsc_code = self.employee_id.bank_account_id.bank_id.bic or ''

class HrBankPayslip(models.Model):
    _inherit = 'hr.payslip'
    _description = 'Pay Slips'

    advice_id = fields.Many2one('custom.hr.bank.payroll.advice', string='Bank Advice', copy=False)
