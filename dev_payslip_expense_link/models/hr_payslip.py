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
from datetime import datetime, timedelta

class hr_payslip(models.Model):
    _inherit = 'hr.payslip'
    
    hr_expence_alw= fields.Float(compute='get_hr_expense_alw',string="HR Expense ALW")
    
        
    @api.depends('employee_id','date_from','date_to')
    def get_hr_expense_alw(self):
        total_amount = 0.00
        payslip_domain = []
        for rec in self:
            if rec.date_from and rec.date_to:
                date_from = datetime.strptime(str(rec.date_from), '%Y-%m-%d').date()
                date_to = datetime.strptime(str(rec.date_to), '%Y-%m-%d').date()
                payslip_domain.append(('payslip_date', '>=', date_from))
                payslip_domain.append(('payslip_date', '<=', date_to))
                payslip_domain.append(('state', '=', 'approve'))
                payslip_domain.append(('payment_mode', '=', 'payslip'))
            payslip_domain.append(('employee_id', '=', rec.employee_id.id))
            hr_expens = self.env['hr.expense.sheet'].search(payslip_domain)
            print(payslip_domain)
            print(hr_expens)
            if hr_expens:
                for expense_data in hr_expens:
                    if expense_data.expense_line_ids:
                        for exp_line in expense_data.expense_line_ids:
                            total_amount += exp_line.total_amount
            rec.hr_expence_alw = total_amount
        
    def action_payslip_done(self):
        for data in self:
            payslip_domain = []
            if self.date_from and self.date_to:
                date_from = datetime.strptime(str(self.date_from), '%Y-%m-%d').date()
                date_to = datetime.strptime(str(self.date_to), '%Y-%m-%d').date()
                payslip_domain.append(('payslip_date','>=',date_from))
                payslip_domain.append(('payslip_date', '<=',date_to))
                payslip_domain.append(('state', '=','approve'))
            payslip_domain.append(('employee_id','=',self.employee_id.id))
            hr_expens = self.env['hr.expense.sheet'].search(payslip_domain)
            if hr_expens:
                for expense_data in hr_expens:
                    expense_data.payslip_id = data.id
                    for exp in expense_data.expense_line_ids:
                        exp.payslip_id = data.id
        return super(hr_payslip, self).action_payslip_done()
        


#
#




# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
