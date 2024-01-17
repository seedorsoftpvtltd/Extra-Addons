# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2015 DevIntelle Consulting Service Pvt.Ltd (<http://www.devintellecs.com>).
#
#    For Module Support : devintelle@gmail.com  or Skype : devintelle
#
##############################################################################

from odoo import fields, models, api


class hr_expense(models.Model):
    _inherit = 'hr.expense'

    payment_mode = fields.Selection(selection_add=[('payslip', 'Payslip(to reimburse)')])
    payslip_date = fields.Date(string="Payslip Date")
    payslip_id = fields.Many2one('hr.payslip', string="Payslips")

    def action_submit_expenses(self):
        res = super(hr_expense, self).action_submit_expenses()
        if res.get('context'):
            res.get('context').update({'default_payment_mode': self.payment_mode,
                                       'default_payslip_date': self.payslip_date})
        return res

class hr_expense_sheet(models.Model):
    _inherit = 'hr.expense.sheet'

    payslip_date = fields.Date(string="Payslip Date")
    payslip_id = fields.Many2one('hr.payslip',string="Payslip")


# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
