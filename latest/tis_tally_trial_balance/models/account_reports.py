# -*- coding: utf-8 -*-
# This module and its content is copyright of Technaureus Info Solutions Pvt. Ltd.
# - © Technaureus Info Solutions Pvt. Ltd 2019. All rights reserved.

# from odoo import api, models, _
import time
from odoo import api, models, _
from odoo.exceptions import UserError


class AccountChartOfAccountReport(models.AbstractModel):
    _inherit = "account.coa.report"
    # _description = "Chart of Account Report"
    # _inherit = "account.report"


    @api.model
    def _get_lines_new(self, options, line_id=None):
        # Create new options with 'unfold_all' to compute the initial balances.
        # Then, the '_do_query' will compute all sums/unaffected earnings/initial balances for all comparisons.
        new_options = options.copy()
        new_options['unfold_all'] = True
        options_list = self._get_options_periods_list(new_options)
        accounts_results = self.env['account.general.ledger']._do_query_new(options_list, fetch_lines=False)
        return accounts_results


class AccountGeneralLedgerReport(models.AbstractModel):
    _inherit = "account.general.ledger"

    @api.model
    def _get_query_sums_new(self, options_list, expanded_account=None):
        options = options_list[0]
        unfold_all = options.get('unfold_all') or (self._context.get('print_mode') and not options['unfolded_lines'])

        params = []
        queries = """"""

        # Create the currency table.
        # As the currency table is the same whatever the comparisons, create it only once.
        ct_query = self._get_query_currency_table(options)

        # ============================================
        # 1) Get sums for all accounts.
        # ============================================

        domain = [('account_id', '=', expanded_account.id)] if expanded_account else []

        for i, options_period in enumerate(options_list):
            # The period domain is expressed as:
            # [
            #   ('date' <= options['date_to']),
            #   '|',
            #   ('date' >= fiscalyear['date_from']),
            #   ('account_id.user_type_id.include_initial_balance', '=', True),
            # ]
            new_options = options_period.copy()
            if options_period['date']['date_from'] and options_period['date']['date_to']:
                new_options = self._get_options_sum_balance(options_period)
            tables, where_clause, where_params = self._query_get(new_options, domain=domain)
            params += where_params
            queries = '''
                    SELECT
                        account_move_line.account_id                            AS id,
                        'sum'                                                   AS key,
                        MAX(account_move_line.date)                             AS max_date,
                        %s                                                      AS period_number,
                        COALESCE(SUM(account_move_line.amount_currency), 0.0)   AS amount_currency,
                        SUM(ROUND(account_move_line.debit * currency_table.rate, currency_table.precision))   AS debit,
                        SUM(ROUND(account_move_line.credit * currency_table.rate, currency_table.precision))  AS credit,
                        SUM(ROUND(account_move_line.balance * currency_table.rate, currency_table.precision)) AS balance
                    FROM %s
                    LEFT JOIN %s ON currency_table.company_id = account_move_line.company_id
                    WHERE %s
                    GROUP BY account_move_line.account_id
                ''' % (i, tables, ct_query, where_clause)

        return queries, params

    @api.model
    def _do_query_new(self, options_list, expanded_account=None, fetch_lines=True):
        # Execute the queries and dispatch the results.
        context = self.env.context.copy()
        context.update({'state': 'posted'})
        self.env.context = context
        query, params = self._get_query_sums_new(options_list, expanded_account=expanded_account)
        display_account = options_list[0]['display_account']
        accounts = self.env['account.account'].search([])
        # groupby_accounts = {}
        # groupby_companies = {}
        # groupby_taxes = {}
        account_result = {}

        self._cr.execute(query, params)
        for row in self._cr.dictfetchall():
            account_result[row.pop('id')] = row

        account_res = []
        for account in accounts:
            res = dict((fn, 0.0) for fn in ['credit', 'debit', 'balance'])
            currency = account.currency_id and account.currency_id or account.company_id.currency_id
            res['code'] = account.code
            res['name'] = account.name
            if account.id in account_result:
                res['debit'] = account_result[account.id].get('debit')
                res['credit'] = account_result[account.id].get('credit')
                res['balance'] = account_result[account.id].get('balance')
            if display_account == 'all':
                account_res.append(res)
            if display_account == 'not_zero' and not currency.is_zero(res['balance']):
                account_res.append(res)
            if display_account == 'movement' and (
                    not currency.is_zero(res['debit']) or not currency.is_zero(res['credit'])):
                account_res.append(res)
        return account_res


