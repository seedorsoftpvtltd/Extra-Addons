# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, models, fields

class ContractBulkReport(models.AbstractModel):
    _name = 'report.contract.custom_contarct_report_template'
    _description = 'Contract Bulk Report'

    @api.model
    def _get_report_values(self, docids, data=None):
        docs = self.env['account.analytic.account'].browse(docids[0])
        for doc in docs:
            data = {
                'doc_ids': doc.id,
                'doc_model': 'account.analytic.account',
                'docs': doc,
            }
            return data

