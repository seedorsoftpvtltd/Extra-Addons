# -*- coding: utf-8 -*-

from odoo import models, fields, api

class IrActionsReport(models.Model):
    _inherit = 'ir.actions.report'

    @api.model
    def get_html_report(self, id, report_name):
        document = report.render_qweb_html([id], data={})
        if document:
            return document
        return False