from _datetime import datetime

from odoo import api, models, _
from odoo.exceptions import UserError


class ReportTax(models.AbstractModel):
    _inherit = 'report.base_accounting_kit.report_tax'
    _description = 'Tax Report'

    def _compute_from_amls(self, options, taxes):
        # compute the tax amount
        sql = self._sql_from_amls_one()
        tables, where_clause, where_params = self.env[
            'account.move.line']._query_get()
        where_clause += " AND parent_state = 'posted'"
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