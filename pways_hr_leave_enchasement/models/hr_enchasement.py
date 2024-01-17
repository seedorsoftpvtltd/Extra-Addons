from odoo import models, fields, api, _
from datetime import datetime
from odoo.exceptions import ValidationError


class HrEncasement(models.Model):
    _name = "hr.employee.enchasement"
    _description = 'Enchasment'
    _order = 'id desc'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char('Name', required=True, index=True, readonly=True, copy=False, default='New')
    employee_id = fields.Many2one("hr.employee", required=True)
    date_to = fields.Datetime(required=True, string='Date', default=fields.Datetime.now)
    department_id = fields.Many2one('hr.department')
    job_id = fields.Many2one('hr.job')
    leave = fields.Float(default=1.0,compute='_compute_remaining_leave')
    amount = fields.Float()
    description = fields.Text()
    enchase_type = fields.Selection([('day_salary', 'Daily Salary'), ('fixed_amount', 'Fixed Amount')], required=True,
                                    default='fixed_amount')
    contract_id = fields.Many2one("hr.contract", required=True)
    state = fields.Selection([('draft', 'Draft'), ('approve', 'Approve'), ('paid', 'Paid'), ('cancel', 'Cancel')],
                             default='draft')
    total = fields.Float(compute='_get_sum')
    days = fields.Float(string='Working Days', default=22)
    move_count = fields.Integer(compute='_move_count', string='#Moves')
    journal_id = fields.Many2one('account.journal', string='Journal', required=True)
    currency_id = fields.Many2one('res.currency', string='Currency', default=lambda self: self.env.company.currency_id)


    @api.depends('employee_id')
    def _compute_remaining_leave(self):
         for rec in self:
            rec['leave'] = rec.employee_id.remaining_leaves
    @api.onchange('contract_id.wage', 'days', 'enchase_type')
    def onchange_type(self):
        total_amount = 0.0
        for record in self:
            if record.contract_id and record.contract_id.wage and record.days and record.enchase_type == 'day_salary':
                total_amount = record.contract_id.wage / record.days
            record.amount = total_amount

    @api.depends('leave', 'amount')
    def _get_sum(self):
        for rec in self:
            rec.total = rec.leave * rec.amount

    def button_approve(self):
        self.state = 'approve'

    def button_set_to_draft(self):
        self.state = 'draft'

    def button_cancel(self):
        self.state = 'cancel'

    @api.onchange('employee_id')
    def _onChangeEmployee(self):
        if self.employee_id:
            self.department_id = self.employee_id.department_id and self.employee_id.department_id.id
            self.job_id = self.employee_id.job_id and self.employee_id.job_id.id

    @api.model
    def create(self, vals):
        if vals.get('name', 'New') == 'New':
            vals['name'] = self.env['ir.sequence'].next_by_code('hr.employee.enchasement') or ('New')
        return super(HrEncasement, self).create(vals)

    def _prepare_move_line(self):
        move_line_dict = []
        company_id = self.env.user.company_id
        account_payable_id = company_id.account_payable_id
        partner_id = self.employee_id.address_home_id
        account_id = self.journal_id.default_credit_account_id and self.journal_id.default_debit_account_id
        if not account_payable_id:
            raise ValidationError(_('Please set encash account in company'))
        if not account_id:
            raise ValidationError(_('Please set bank account in journal'))
        if not partner_id:
            raise ValidationError(_('Please set employee home address'))
        curr = self.currency_id.id
        move_line_dict.append(
            {
                'account_id': account_payable_id and account_payable_id.id or False,
                'partner_id': partner_id and partner_id.id or False,
                # 'currency_id': self.currency_id and self.currency_id.id,
                'currency_id': curr if self.env.company.currency_id.id != curr else '',
                'name': self.name,
                'debit': self.total,
                'date_maturity': self.date_to,
                'ref': self.name,
                'date': self.date_to,
            })

        move_line_dict.append({
            'account_id': account_id and account_id.id or False,
            'partner_id': partner_id and partner_id.id or False,
            'name': self.name,
            # 'currency_id': self.currency_id and self.currency_id.id,
            'currency_id': curr if self.env.company.currency_id.id != curr else '',
            'credit': self.total,
            'date_maturity': self.date_to,
            'ref': self.name,
            'date': self.date_to,
        })
        print(move_line_dict,'move_line_dict')
        return move_line_dict

    def button_post(self):
        move_line_dict = self._prepare_move_line()
        vals = {
            'type': 'entry',
            'currency_id': self.currency_id and self.currency_id.id or False,
            'date': self.date_to,
            'journal_id': self.journal_id and self.journal_id.id or False,
            'encash_id': self.id,
            'narration': self.description,
            'line_ids': [(0, 0, line_data) for line_data in move_line_dict]
        }
        print(vals, 'valssss')
        move_id = self.env['account.move'].create(vals)
        move_id.ref = self.name
        self.write({'state': 'paid'})

    def _move_count(self):
        for rec in self:
            move_ids = self.env['account.move'].search([('encash_id', '=', rec.id)])
            rec.move_count = len(move_ids.ids)

    def view_journal_entry(self):
        move_ids = self.env['account.move'].search([('encash_id', '=', self.id)])
        return {
            'name': _('Journal Entries'),
            'view_type': 'form',
            'view_mode': 'tree,form',
            'res_model': 'account.move',
            'view_id': False,
            'type': 'ir.actions.act_window',
            'domain': [('id', 'in', move_ids.ids)],
        }


class HrContract(models.Model):
    _inherit = 'hr.contract'

    enchasement_ids = fields.One2many('hr.employee.enchasement', 'contract_id')


class AccountMove(models.Model):
    _inherit = 'account.move'

    encash_id = fields.Many2one('hr.employee.enchasement', string="Transfer")


class Company(models.Model):
    _inherit = "res.company"

    account_payable_id = fields.Many2one('account.account', string=" Encash Account")

