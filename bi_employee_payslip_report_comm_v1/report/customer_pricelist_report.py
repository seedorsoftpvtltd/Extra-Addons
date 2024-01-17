# -*- coding: utf-8 -*-


from datetime import datetime
from odoo import models, api, fields


class PayslipInh(models.Model):
    _inherit = 'hr.payslip'

    supervisor = fields.Many2one('hr.employee','Supervisor')
    bank_name = fields.Many2one('res.bank',string="Bank Name", related='bank_no.bank_id')
    bank_no = fields.Many2one('res.partner.bank',string="Bank Acc No", related='employee_id.bank_account_id')


class ExportCustomerPricelistReport(models.AbstractModel):
    _name = 'report.bi_employee_payslip_report_comm_v1.report_emp_payslip'
    _description = 'Employee Payslip Report'

    def _get_payslip_details(self, payslip_ids):
        main = []
        final = []
        new = {}
        no = 1

        b_lst = []
        a_lst = []
        g_lst = []
        d_lst = []
        n_lst = []
        all_seq = []
        all_rules = self.env['hr.payslip.line'].search([]).salary_rule_id
        for rule in all_rules:
            all_seq.append(rule.name)
        lable = self._get_payslip_lable(payslip_ids)[0]
        for payslip in payslip_ids:
            values = {}
            category = []
            not_category = []
            if lable.get('no'):
                values['NO'] = no,
            if lable.get('payslip_ref'):
                values['Payslip_Ref'] = payslip.number or '',

            if lable.get('supervisor'):
                values['Supervisor'] = payslip.supervisor.name or '',
            if lable.get('bank_name'):
                values['Bank_Name'] = payslip.bank_name.name or '',
            if lable.get('work_days'):
                for rec in payslip.worked_days_line_ids:
                 values['Work_Days'] = rec.number_of_days or '',
                 # values['Work_Days'] = payslip.worked_days_line_ids.number_of_days or '',
            if lable.get('employee'):
                values['Employee'] = payslip.employee_id.name or '',
            if lable.get('designation'):
                values['Designation'] = payslip.employee_id.job_id.name or '',
            if lable.get('period'):
                values['Period'] = str(payslip.date_from) + '  to  ' + str(payslip.date_to),
            lines = self.env['hr.payslip.line'].search([('slip_id', '=', payslip.id)])
            all_category = lines.mapped('salary_rule_id.name')
            sub_categ = lines.mapped('name')
            temp = []
            for i in all_seq:
                if i not in ['no', 'payslip_ref', 'employee', 'designation', 'period', 'supervisor', 'bank_name',
                             'work_days']:
                    if i in all_category:
                        for line in lines:
                            if line.salary_rule_id.name == i:
                                values[i] = [line.total]
                    else:
                        values[i] = [0.0]
            main.append(values)
        return main

    # def _get_payslip_details(self, payslip_ids):
    #
    #     return True

    def get_sum_of_values(self, name_test=False, a=[], mn={}):
        val = mn.get(name_test)
        if len(a) == len(val):
            return [sum(x) for x in zip(a, val)]
        else:
            return val

    def _get_payslip_lable(self, payslip_ids):
        dict = {}
        lines = [dict]
        category = []
        main_sub = []
        for payslip in payslip_ids:
            for line in payslip.line_ids:
                subcategory = []
                dict['no'] = 'NO #'
                dict['payslip_ref'] = 'Payslip Ref'
                dict['supervisor'] = 'Supervisor'
                dict['bank_name'] = 'Bank Name'
                dict['work_days'] = 'Work Days'
                dict['employee'] = 'Employee'
                dict['designation'] = 'Designation'
                dict['period'] = 'Period'
                category_id = line.category_id
                all_subcategory = self.env['hr.payslip.line'].search(
                    [('category_id', '=', category_id.id), ('slip_id', '=', payslip.id)])
                if line.category_id.name not in category:
                    category.append(line.category_id.name)
                    if all_subcategory:
                        for i in all_subcategory:
                            subcategory.append(i.name)
                            main_sub.append(i.name)
                    dict[line.category_id.name] = subcategory
                else:
                    remaining = []
                    if all_subcategory:
                        for i in all_subcategory:
                            if i.name not in main_sub:
                                remaining.append(i.name)
                    if remaining:
                        for i, j in dict.items():
                            if i == line.category_id.name:
                                for r in remaining:
                                    main_sub.append(r)
                                    dict[i].append(r)
        return lines

    def _get_feature(self):
        all_rules = self.env['hr.payslip.line'].search([]).salary_rule_id
        all_seq = []
        for rule in all_rules:
            all_seq.append(rule.name)

        list = ['NO', 'Payslip_Ref', 'Employee', 'Designation', 'Period', 'Supervisor', 'Bank_Name',
                'Work_Days'] + all_seq
        return list

    def _get_total(self,payslip_ids):
        list = ['NO', 'Payslip_Ref', 'Employee', 'Designation', 'Period', 'Supervisor', 'Bank_Name',
                'Work_Days']
        all_rules = self.env['hr.payslip.line'].search([]).salary_rule_id
        all_rule = [rule.name for rule in all_rules]
        main = self._get_payslip_details(payslip_ids)
        total_dict = {}
        for i,j in main[0].items():
            if i not in list:
                if i in all_rule:
                    total_salaries = sum([employee[i][0] for employee in main if i in employee])
                    total_dict[i] = total_salaries
            else:
                total_dict[i] = ''

        total = [total_dict]
        return total


    @api.model
    def _get_report_values(self, docids, data=None):
        payslip_ids = self.env['hr.payslip'].browse(data['ids'])
        docargs = {
            'doc_model': 'export.customer.pricelist',
            'data': data,
            'docs': payslip_ids,
            'get_payslip_details': self._get_payslip_details(payslip_ids),
            'get_payslip_lable': self._get_payslip_lable(payslip_ids),
            'get_features': self._get_feature(),
            'get_total': self._get_total(payslip_ids)
        }
        return docargs

