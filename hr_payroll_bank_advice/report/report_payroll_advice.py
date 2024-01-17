# -*- coding:utf-8 -*-

import time
from datetime import datetime
#from openerp.tools import amount_to_text_en
from odoo.tools.misc import formatLang
# from openerp import api, models
from odoo import api, models


class bank_payroll_advice_report(models.AbstractModel):
    _name = 'report.hr_payroll_bank_advice.report_back_payroll_advice'

    def get_advice_month(self, input_date):
        res = {
               'from_name': '', 'to_name': ''
               }
        slip = self.env['hr.payslip'].search([('date_from', '<=', input_date), ('date_to', '>=', input_date)], limit=1)
        if slip:
            start_date = datetime.strptime(str(slip.date_from), '%Y-%m-%d')
            end_date = datetime.strptime(str(slip.date_to), '%Y-%m-%d')
            res['from_name'] = start_date.strftime('%d') + '-' + start_date.strftime('%b') + '-' + start_date.strftime('%Y')
            res['to_name'] = end_date.strftime('%d') + '-' + end_date.strftime('%b') + '-' + end_date.strftime('%Y')
        return res

    def convert(self, amount, cur):
        return amount_to_text_en.amount_to_text(amount, 'en', cur)

    def get_bysal_total(self):
        return self.total_bysal

    def get_advice_line_detail(self, line_ids):
        result = []
        self.total_bysal = 0.00
        for l in line_ids:
            res = {}
            res.update({
                    'name': l.employee_id.name,
                    'employee_bank':l.employee_bank,
                    'acc_no': l.name,
                    'ifsc_code': l.ifsc_code,
                    'bysal': l.bysal,
                    })
            self.total_bysal += l.bysal
            result.append(res)
        return result

    @api.model
    #def render_html(self, docids, data=None):
    def _get_report_values(self, docids, data=None):
        report = self.env['ir.actions.report']._get_report_from_name('hr_payroll_bank_advice.report_back_payroll_advice')
        advice = self.env['custom.hr.bank.payroll.advice'].browse(docids)
        account_number = advice.custom_partner_bank_id.acc_number
        advice_date = datetime.strftime(datetime.strptime(str(advice.date), '%Y-%m-%d'), '%d-%m-%Y')
        #docargs = {
        return {
            'doc_ids': docids,
            #'doc_model': 'hr.bank.payroll.advice',
            'doc_model': report.model,
            'data': data,
            'docs': advice,
            'time': time,
            'advice_date':advice_date,
            'account_number':account_number,
            'get_month': self.get_advice_month(advice.date),
            'convert': self.convert,
            'get_detail': self.get_advice_line_detail(advice.line_ids),
            'get_bysal_total': self.get_bysal_total,
        }
        #return self.env['report'].render('hr_payroll_bank_advice.report_back_payroll_advice', docargs)
