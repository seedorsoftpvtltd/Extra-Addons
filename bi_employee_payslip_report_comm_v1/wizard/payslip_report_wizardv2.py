# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models, api, _
from datetime import datetime
import xlsxwriter
import base64
import io
from io import BytesIO
import tempfile
import csv
from io import StringIO


class EmpPayslipReport(models.TransientModel):
    _name = "emp.payslip.report"

    file = fields.Binary("Download File")
    file_name = fields.Char(string="File Name")
    file_type = fields.Selection([('pdf', 'PDF'), ('xls', 'XLS')
                                  ], 'File Type', default="xls")

    def get_sum_of_values(self, name_test=False, a=[], mn={}):
        val = mn.get(name_test)
        if len(a) == len(val):
            return [sum(x) for x in zip(a, val)]
        else:
            return val

    def employee_payslip_xls(self):
        if self.file_type == 'pdf':
            self.ensure_one()
            [data] = self.read()
            active_ids = self.env.context.get('active_ids', [])
            payslip = self.env['hr.payslip'].browse(active_ids)
            datas = {
                'ids': active_ids,
                'model': 'emp.payslip.report ',
                'form': data
            }
            return self.env.ref('bi_employee_payslip_report_comm_v1.action_report_export_emp_payslip').report_action(self,
                                                                                                                  data=datas)
        elif self.file_type == 'xls':
            # name_of_file = 'Export Payslip Report.xls'
            # file_path = 'Export Payslip Report' + '.xls'
            # workbook = xlsxwriter.Workbook('./tmp/' + file_path)
            # worksheet = workbook.add_worksheet('Export Payslip Report')

            name_of_file = 'Export Payslip Report.xls'
            file_path = tempfile.gettempdir() + '/' + name_of_file

            workbook = xlsxwriter.Workbook(file_path)
            worksheet = workbook.add_worksheet('Export Payslip Report')

            header_format = workbook.add_format(
                {'bold': True, 'valign': 'vcenter', 'font_size': 16, 'align': 'center'})
            title_format = workbook.add_format(
                {'border': 1, 'bold': True, 'valign': 'vcenter', 'align': 'center', 'font_size': 14,
                 'bg_color': '#D8D8D8'})
            cell_wrap_format_bold = workbook.add_format(
                {'border': 1, 'bold': True, 'valign': 'vjustify', 'valign': 'vcenter', 'align': 'center',
                 'font_size': 12})  ##E6E6E6
            cell_wrap_format = workbook.add_format(
                {'border': 1, 'valign': 'vjustify', 'valign': 'vcenter', 'align': 'left', 'font_size': 12,
                 'align': 'center', 'text_wrap': True})  ##E6E6E6

            sub_cell_wrap_format_bold = workbook.add_format(
                {'border': 1, 'valign': 'vjustify', 'valign': 'vcenter', 'align': 'center',
                 'font_size': 12, 'text_wrap': True})

            worksheet.set_row(1, 30)  # Set row height
            worksheet.set_row(4, 50)

            # Merge Row Columns
            TITLEHEDER = 'Payslip Report'

            worksheet.set_column(0, 0, 3)
            worksheet.set_column(1, 1, 15)
            worksheet.set_column(2, 3, 25)
            worksheet.set_column(4, 4, 25)
            worksheet.set_column(5, 15, 20)

            worksheet.merge_range(1, 1, 1, 7, TITLEHEDER, header_format)
            rowscol = 1

            active_ids = self.env.context.get('active_ids', [])
            payslip_ids = self.env['hr.payslip'].browse(active_ids)

            worksheet.merge_range(3, 0, 4, 0, 'NO', cell_wrap_format_bold)
            worksheet.merge_range(3, 1, 4, 1, 'Payslip Ref', cell_wrap_format_bold)
            worksheet.merge_range(3, 2, 4, 2, 'Employee', cell_wrap_format_bold)
            worksheet.merge_range(3, 3, 4, 3, 'Designation', cell_wrap_format_bold)
            worksheet.merge_range(3, 4, 4, 4, 'Period', cell_wrap_format_bold)
            worksheet.merge_range(3, 5, 4, 5, 'Supervisor', cell_wrap_format_bold)
            worksheet.merge_range(3, 6, 4, 6, 'Bank Name', cell_wrap_format_bold)
            worksheet.merge_range(3, 7, 4, 7, 'Work Days', cell_wrap_format_bold)

            # For the get Lables
            dict = {}
            lines = [dict]
            category = []
            main_sub = []
            all_seq = []
            for payslip in payslip_ids:
                for line in payslip.line_ids:
                    subcategory = []
                    category_id = line.category_id
                    all_subcategory = self.env['hr.payslip.line'].search(
                        [('category_id', '=', category_id.id), ('slip_id', '=', payslip.id)])
                    if line.category_id.name not in category:
                        # category.append(line.category_id.name)
                        category.append(line.name)
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

            all_rules = self.env['hr.payslip.line'].search([]).salary_rule_id
            for rule in all_rules:
                all_seq.append(rule.name)

            seq_col = 7
            for seq in all_seq:
                seq_col += 1
                padding = len(seq)*1.5
                worksheet.set_column(seq_col, seq_col, padding)
                worksheet.merge_range(3, seq_col, 4, seq_col, seq, cell_wrap_format_bold)


            # For Print the values
            # For the get Values of lable
            main = []
            final = []
            new = {}
            no = 1

            lable = lines[0]
            for payslip in payslip_ids:
                values = {}
                category = []
                not_category = []
                values['NO'] = no,
                values['Payslip_Ref'] = payslip.number or '',
                values['Employee'] = payslip.employee_id.name or '',
                values['Designation'] = payslip.employee_id.job_id.name or '',
                values['Period'] = str(payslip.date_from) + '  to  ' + str(payslip.date_to),
                values['Supervisor'] = payslip.supervisor.name or '',
                values['Bank_Name'] = payslip.bank_name.name or '',
                for rec in payslip.worked_days_line_ids:
                    values['Work_Days'] = rec.number_of_days or '',
                lines = self.env['hr.payslip.line'].search([('slip_id', '=', payslip.id)])
                all_category = lines.mapped('category_id.name')
                sub_categ = lines.mapped('name')
                temp = []
                for i, j in lable.items():
                    if i not in ['no', 'payslip_ref', 'employee', 'designation', 'period', 'supervisor', 'bank_name',
                                 'work_days']:
                        if i in all_category:
                            present_categ = []
                            for sub in j:
                                if sub in sub_categ:
                                    for line in lines:
                                        if sub == line.name:
                                            present_categ.append(line.total)
                                            temp.append(line.total)
                                else:
                                    present_categ.append(0.0)
                                    temp.append(0.0)
                            print(sub)
                            values[sub] = present_categ
                        else:
                            not_present_categ = []
                            for k in j:
                                not_present_categ.append(0.0)
                                temp.append(0.0)
                            values[i] = not_present_categ
                no = no + 1
                main.append(values)

            # For get the values
            # end_row = row
            row = 5
            for value in main:
                col = 0
                row = row
                list = ['NO', 'Payslip_Ref', 'Employee', 'Designation', 'Period', 'Supervisor', 'Bank_Name',
                        'Work_Days'] + all_seq
                for l in list:
                    if l in value.keys():
                        data = value.get(l)
                        for r in data:
                            worksheet.write(row, col, r, cell_wrap_format)
                            col += 1
                    else:
                        worksheet.write(row, col, 0, cell_wrap_format)
                        col += 1

                row += 1
                end_row = row

            # For Get the Total
            total_row = end_row
            list = all_seq
            coln = 8
            for l in list:
                lst = []
                for mn in main:
                    if l in mn.keys():
                        lst = self.get_sum_of_values(l, lst, mn)

                for r in lst:
                    worksheet.write(total_row, coln, r, cell_wrap_format_bold)
                    coln += 1
            worksheet.merge_range(total_row, 7, total_row, 7, 'Total', cell_wrap_format_bold)

            # workbook.close()
            # export_id = base64.b64encode(open('/tmp/' + file_path, 'rb+').read())
            # result_id = self.env['emp.payslip.report'].create({'file': export_id, 'file_name': name_of_file})

            workbook.close()
            with open(file_path, 'rb') as file:
                export_id = base64.b64encode(file.read())
            result_id = self.env['emp.payslip.report'].create({'file': export_id, 'file_name': name_of_file})
            return {
                'name': 'Export Payslip Report',
                'view_mode': 'form',
                'res_id': result_id.id,
                'res_model': 'emp.payslip.report',
                'view_type': 'form',
                'type': 'ir.actions.act_window',
                'target': 'new',
            }
