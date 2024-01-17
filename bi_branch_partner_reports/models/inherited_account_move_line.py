# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.

from odoo import api, models
from odoo.tools.safe_eval import safe_eval


class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    @api.model
    def _query_get(self, domain=None):
        self.check_access_rights('read')

        context = dict(self._context or {})
        domain = domain or []

        if context.get('branch_ids'):
            domain += [('branch_id', 'in', context.get('branch_ids'))]

        return super(AccountMoveLine, self)._query_get(domain)



# class AccountMoveLine(models.Model):
#     _inherit = 'account.move.line'
#
#     @api.model
#     def _query_get(self, domain=None):
#         self.check_access_rights('read')
#
#         context = dict(self._context or {})
#         domain = domain or []
#         if not isinstance(domain, (list, tuple)):
#             domain = safe_eval(domain)
#
#         date_field = 'date'
#         if context.get('aged_balance'):
#             date_field = 'date_maturity'
#         if context.get('date_to'):
#             domain += [(date_field, '<=', context['date_to'])]
#         if context.get('date_from'):
#             if not context.get('strict_range'):
#                 domain += ['|', (date_field, '>=', context['date_from']),
#                            ('account_id.user_type_id.include_initial_balance', '=', True)]
#             elif context.get('initial_bal'):
#                 domain += [(date_field, '<', context['date_from'])]
#             else:
#                 domain += [(date_field, '>=', context['date_from'])]
#
#         if context.get('journal_ids'):
#             domain += [('journal_id', 'in', context['journal_ids'])]
#
#         if context.get('branch_ids'):
#             domain += [('branch_id', 'in', context.get('branch_ids'))]
#
#         state = context.get('state')
#         if state and state.lower() != 'all':
#             domain += [('move_id.state', '=', state)]
#
#         if context.get('company_id'):
#             domain += [('company_id', '=', context['company_id'])]
#
#         if 'company_ids' in context:
#             domain += [('company_id', 'in', context['company_ids'])]
#
#         if context.get('reconcile_date'):
#             domain += ['|', ('reconciled', '=', False), '|',
#                        ('matched_debit_ids.max_date', '>', context['reconcile_date']),
#                        ('matched_credit_ids.max_date', '>', context['reconcile_date'])]
#
#         if context.get('account_tag_ids'):
#             domain += [('account_id.tag_ids', 'in', context['account_tag_ids'].ids)]
#
#         if context.get('account_ids'):
#             domain += [('account_id', 'in', context['account_ids'].ids)]
#
#         if context.get('analytic_tag_ids'):
#             domain += [('analytic_tag_ids', 'in', context['analytic_tag_ids'].ids)]
#
#         if context.get('analytic_account_ids'):
#             domain += [('analytic_account_id', 'in', context['analytic_account_ids'].ids)]
#
#         if context.get('partner_ids'):
#             domain += [('partner_id', 'in', context['partner_ids'].ids)]
#
#         if context.get('partner_categories'):
#             domain += [('partner_id.category_id', 'in', context['partner_categories'].ids)]
#
#         where_clause = ""
#         where_clause_params = []
#         tables = ''
#         if domain:
#             query = self._where_calc(domain)
#             # Wrap the query with 'company_id IN (...)' to avoid bypassing company access rights.
#             self._apply_ir_rules(query)
#
#             tables, where_clause, where_clause_params = query.get_sql()
#         return tables, where_clause, where_clause_params

