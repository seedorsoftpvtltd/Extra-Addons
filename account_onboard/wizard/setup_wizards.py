# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from datetime import date

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError

class SetupBarBankConfigWizard(models.TransientModel):
    _inherits = {'res.partner.bank': 'res_partner_bank_id'}
    _name = 'account.setup.bank.manual.config'
    _description = 'Bank setup manual config'

    res_partner_bank_id = fields.Many2one(comodel_name='res.partner.bank', ondelete='cascade', required=True)
    new_journal_name = fields.Char(default=lambda self: self.linked_journal_id.name, inverse='set_linked_journal_id', required=True, help='Will be used to name the Journal related to this bank account')
    linked_journal_id = fields.Many2one(string="Journal", comodel_name='account.journal', inverse='set_linked_journal_id', compute="_compute_linked_journal_id")
    new_journal_code = fields.Char(string="Code", required=True, default=lambda self: self._onchange_new_journal_code())
    num_journals_without_account = fields.Integer(default=lambda self: self._number_unlinked_journal())
    # field computing the type of the res.patrner.bank. It's behaves the same as a related res_part_bank_id.acc_type
    # except we want to display  this information while the record isn't yet saved.
    related_acc_type = fields.Selection(string="Account Type", selection=lambda x: x.env['res.partner.bank'].get_supported_account_types(), compute='_compute_related_acc_type')

    @api.model
    def create(self, vals):
        """ This wizard is only used to setup an account for the current active
        company, so we always inject the corresponding partner when creating
        the model.
        """
        vals['partner_id'] = self.env.company.partner_id.id
        return super(SetupBarBankConfigWizard, self).create(vals)

    @api.depends('acc_number')
    def _compute_related_acc_type(self):
        for record in self:
            record.related_acc_type = self.env['res.partner.bank'].retrieve_acc_type(record.acc_number)

    def _number_unlinked_journal(self):
        return self.env['account.journal'].search([('type', '=', 'bank'), ('bank_account_id', '=', False)], count=True)

    @api.onchange('linked_journal_id')
    def _onchange_new_journal_code(self):
        for record in self:
            if not record.linked_journal_id:
                record.new_journal_code = self.env['account.journal'].get_next_bank_cash_default_code('bank', self.env.company.id)
            else:
                record.new_journal_code = self.linked_journal_id.code

    @api.onchange('linked_journal_id')
    def _onchange_new_journal_related_data(self):
        for record in self:
            if record.linked_journal_id:
                record.new_journal_name = record.linked_journal_id.name

    @api.depends('journal_id')  # Despite its name, journal_id is actually a One2many field
    def _compute_linked_journal_id(self):
        for record in self:
            record.linked_journal_id = record.journal_id and record.journal_id[0] or record.default_linked_journal_id()

    def default_linked_journal_id(self):
        default = self.env['account.journal'].search([('type', '=', 'bank'), ('bank_account_id', '=', False)], limit=1)
        return default and default[0].id


    def set_linked_journal_id(self):
        """ Called when saving the wizard.
        """
        for record in self:
            selected_journal = record.linked_journal_id
            if record.num_journals_without_account == 0:
                company = self.env.company
                selected_journal = self.env['account.journal'].create({
                    'name': record.new_journal_name,
                    'code': record.new_journal_code,
                    'type': 'bank',
                    'company_id': company.id,
                    'bank_account_id': record.res_partner_bank_id.id,
                })
            else:
                selected_journal.bank_account_id = record.res_partner_bank_id.id
                selected_journal.name = record.new_journal_name
                selected_journal.code = record.new_journal_code

    def validate(self):
        """ Called by the validation button of this wizard. Serves as an
        extension hook in account_bank_statement_import.
        """
        self.linked_journal_id.mark_bank_setup_as_done_action()
