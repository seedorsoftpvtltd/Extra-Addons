from odoo import models,fields,api, _
from odoo.exceptions import ValidationError, UserError
from _datetime import datetime

class AccountTaxReport(models.TransientModel):
    _inherit = 'account.tax.report'

    target_move = fields.Selection(
        [("posted", "All Posted Entries"), ("all", "All Entries")],
        string="Target Moves",
        required=True,
        default="posted",
    )

    def action_xlsx(self):
        """ Button function for Xlsx """
        return self.env.ref(
            'tax_report_export_xlsx.action_tax_report_xlsx').report_action(self)

    def _sql_from_amls_one(self):
        sql = """SELECT "account_move_line".tax_line_id, COALESCE(SUM("account_move_line".debit-"account_move_line".credit), 0)
                    FROM %s
                    WHERE %s AND "account_move_line".tax_exigible GROUP BY "account_move_line".tax_line_id"""
        return sql

    def _sql_from_amls_two(self):
        sql = """SELECT r.account_tax_id, COALESCE(SUM("account_move_line".debit-"account_move_line".credit), 0)
                 FROM %s
                 INNER JOIN account_move_line_account_tax_rel r ON ("account_move_line".id = r.account_move_line_id)
                 INNER JOIN account_tax t ON (r.account_tax_id = t.id)
                 WHERE %s AND "account_move_line".tax_exigible GROUP BY r.account_tax_id"""
        return sql

    def _compute_from_amls(self, options, taxes):
        # compute the tax amount
        sql = self._sql_from_amls_one()
        tables, where_clause, where_params = self.env['account.move.line']._query_get()
        if options['target_move'] == 'posted':
            where_clause += " AND parent_state = %s"
            where_params.append('posted')
        query = sql % (tables, where_clause)
        self.env.cr.execute(query, where_params)
        results = self.env.cr.fetchall()
        for result in results:
            if result[0] in taxes:
                taxes[result[0]]['tax'] = abs(result[1])

        # compute the net amount
        sql2 = self._sql_from_amls_two()
        query = sql2 % (tables, where_clause)
        self.env.cr.execute(query, where_params)
        results = self.env.cr.fetchall()
        for result in results:
            if result[0] in taxes:
                taxes[result[0]]['net'] = abs(result[1])

    def get_lines(self, options):
        taxes = {}
        for tax in self.env['account.tax'].search(
                [('type_tax_use', '!=', 'none')]):
            if tax.children_tax_ids:
                for child in tax.children_tax_ids:
                    if child.type_tax_use != 'none':
                        continue
                    taxes[child.id] = {'tax': 0, 'net': 0, 'name': child.name,
                                       'type': tax.type_tax_use}
            else:
                taxes[tax.id] = {'tax': 0, 'net': 0, 'name': tax.name,
                                 'type': tax.type_tax_use}
        if options['date_from'] and not options['date_to']:
            self.with_context(date_from=options['date_from'],
                              strict_range=True)._compute_from_amls(options,
                                                                    taxes)
        elif options['date_to'] and not options['date_from']:
            self.with_context(date_to=options['date_to'],
                              strict_range=True)._compute_from_amls(options,
                                                                    taxes)
        elif options['date_from'] and options['date_to']:
            self.with_context(date_from=options['date_from'],
                              date_to=options['date_to'],
                              strict_range=True)._compute_from_amls(options,
                                                                    taxes)
        else:
            date_to = str(datetime.today().date())
            self.with_context(date_to=date_to,
                              strict_range=True)._compute_from_amls(options,
                                                                    taxes)

        groups = dict((tp, []) for tp in ['sale', 'purchase'])
        for tax in taxes.values():
            if tax['tax'] or tax['net']:
                groups[tax['type']].append(tax)
        return groups

    def get_report_datas(self, data):
        return self.get_lines(data)
