# -*- coding: utf-8 -*-
from odoo import models, fields, api, exceptions, _
from odoo.exceptions import UserError, ValidationError
from datetime import datetime, date


class PeriodLock(models.Model):
    _name = 'sh.period.lock'
    _description = 'Period Lock'
    _order = 'id desc'

    def unlink(self):
        for rec in self:
            if rec.state == 'locked':
                raise UserError("You can not delete locked period lock")

        return super(PeriodLock, self).unlink()

    name = fields.Char(readonly=True)
    sequence = fields.Integer(string="Sequence")
    state = fields.Selection(
        [('draft', 'Draft'), ('locked', 'Locked'), ('unlocked', 'Unlocked')], default='draft',)
    journal_ids = fields.Many2many(
        'account.journal', string="Journal", required=True)
    company_ids = fields.Many2many(
        'res.company', string="Company", default=lambda self: self.env.company, required=True)
    from_date = fields.Date('From Date', required=True)
    to_date = fields.Date('To Date', required=True)
    
    @api.model
    def create(self, vals):
        vals.update(
            {'name': self.env['ir.sequence'].next_by_code('period.lock.entry')})
        res = super(PeriodLock, self).create(vals)
        return res

    @api.constrains('from_date')
    def validation_for_date(self):
        if self.from_date > self.to_date:
            raise UserError(
                "To Date is lesser than From Date.Kindly Update To Date")


    def action_lock(self):
        
        if self.search([('from_date', '>=', self.from_date), ('to_date',
                                                              '<=', self.to_date), ('id', '!=', self.id), ('journal_ids.id', 'in', self.journal_ids.ids)]):
            raise UserError('Already Period Lock is created for this journal')

        self.write({
            'state': 'locked'
        })

    def action_unlock(self):
        self.write({
            'state': 'unlocked'
        })

    def action_reset_to_draft(self):
        if self.from_date > date.today():
            raise UserError(
                'Current date Can Not be less than From Date.So period lock Can Not be reset to draft')
        if self.to_date < date.today():
            raise UserError(
                'To date Can Not be less than current Date.So period lock Can Not be reset to draft')

        self.write({
            'state': 'draft'
        })


class AccountMove(models.Model):
    _inherit = 'account.move'

    @api.model
    def _get_default_invoice_date(self):
        return fields.Date.context_today(self) if self._context.get('default_type', 'entry') in self.get_purchase_types(include_receipts=True) else date.today()

    invoice_date = fields.Date(string='Invoice/Bill Date', readonly=True, index=True, copy=False,
        states={'draft': [('readonly', False)]},required=False,
        default=_get_default_invoice_date)


    def action_post(self):

        for rec in self:

            period_locks = self.env['sh.period.lock'].search(
                    [('journal_ids.id', 'in', rec.journal_id.ids), ('company_ids.id', 'in', [self.env.company.id])])

            if not self.env.user.has_group('sh_period_lock.group_special_permission_for_period_lock'):
                if period_locks:
                    locked_period_locks = period_locks.filtered(
                        lambda x: x.state == 'locked')
                    if rec.type != 'entry':
                        if locked_period_locks and str(rec.invoice_date) >= str(locked_period_locks[-1].from_date) and str(rec.invoice_date) <= str(locked_period_locks[-1].to_date):
                            raise UserError(
                                "Accounting Journal Can Not be posted from %s to %s for %s" % (locked_period_locks[-1].from_date, locked_period_locks[-1].to_date, rec.journal_id.name))
                        else:
                            super(AccountMove, self).action_post()
                    else:
                        if locked_period_locks and str(rec.date) >= str(locked_period_locks[-1].from_date) and str(rec.date) <= str(locked_period_locks[-1].to_date):
                            raise UserError(
                                "Accounting Journal Can Not be posted from %s to %s for %s" % (locked_period_locks[-1].from_date, locked_period_locks[-1].to_date, rec.journal_id.name))
                        else:
                            super(AccountMove, self).action_post()
                else:
                    super(AccountMove, self).action_post()
            else:
                super(AccountMove, self).action_post()

    @api.constrains('invoice_date')
    def validation_for_invoice_date(self):

        period_locks = self.env['sh.period.lock'].search(
                [('journal_ids.id', 'in', self.journal_id.ids), ('company_ids.id', 'in', [self.env.company.id])])

        if not self.env.user.has_group('sh_period_lock.group_special_permission_for_period_lock'):
            if period_locks:

                locked_period_locks = period_locks.filtered(
                    lambda x: x.state == 'locked')

                if self.type != 'entry':
                    if locked_period_locks and str(self.invoice_date) >= str(locked_period_locks[-1].from_date) and str(self.invoice_date) <= str(locked_period_locks[-1].to_date):
                        raise UserError(
                            "Accounting Journal Can Not be posted from %s to %s for %s" % (locked_period_locks[-1].from_date, locked_period_locks[-1].to_date, self.journal_id.name))
                
                else:
                    if locked_period_locks and str(self.date) >= str(locked_period_locks[-1].from_date) and str(self.date) <= str(locked_period_locks[-1].to_date):
                        raise UserError(
                            "Accounting Journal Can Not be posted from %s to %s for %s" % (locked_period_locks[-1].from_date, locked_period_locks[-1].to_date, self.journal_id.name))
        
