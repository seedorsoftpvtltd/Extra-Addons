# -*- coding: utf-8 -*-
# This module and its content is copyright of Technaureus Info Solutions Pvt. Ltd.
# - © Technaureus Info Solutions Pvt. Ltd 2019. All rights reserved.

from odoo import fields, models
from datetime import datetime
from odoo.tools.misc import xlwt
import io
import base64
from xlwt import easyxf


class AccountingReport(models.TransientModel):
    _inherit = "accounting.report"

    report_type = fields.Selection([('normal', 'Normal'), ('tally', 'Tally')], string='Report Type', default='tally')
    bs_pl_summary_file = fields.Binary('Report')

    def print_tally_bs(self):
        self.ensure_one()
        data = {}
        data['ids'] = self.env.context.get('active_ids', [])
        data['model'] = self.env.context.get('active_model', 'ir.ui.menu')
        data['form'] = self.read(['date_from', 'date_to', 'journal_ids', 'target_move', 'company_id'])[0]
        used_context = self._build_contexts(data)
        data['form']['used_context'] = dict(used_context, lang=self.env.context.get('lang') or 'en_US')
        return self.with_context(discard_logo_check=True)._print_bs_report(data)

    def _print_bs_report(self, data):
        data['form'].update(self.read(
            ['date_from_cmp', 'debit_credit', 'date_to_cmp', 'filter_cmp', 'account_report_id', 'enable_filter',
             'label_filter', 'target_move', 'report_type'])[0])
        return self.env.ref('tis_tally_bs_and_pl.action_report_tally_bs').report_action(self, data=data,
                                                                                           config=False)

    def export_tally_bs(self):
        # data = {}
        # data['ids'] = self.env.context.get('active_ids', [])
        # data['model'] = self.env.context.get('active_model', 'ir.ui.menu')
        # data['form'] = self.read()[0]
        # used_context = self._build_contexts(data)
        # data['form']['used_context'] = dict(used_context, lang=self.env.context.get('lang') or 'en_US')
        # account_lines = self.env['report.accounting_pdf_reports.report_financial'].get_account_lines(data['form'])
        # start_date = ''
        # end_date = ''
        # if self.date_from:
        #     start_date = datetime.strptime(str(self.date_from), '%Y-%m-%d').strftime(
        #         "%d-%m-%Y")
        # if self.date_to:
        #     end_date = datetime.strptime(str(self.date_to), '%Y-%m-%d').strftime(
        #         "%d-%m-%Y")
        # workbook = xlwt.Workbook()
        # worksheet = workbook.add_sheet('Report', cell_overwrite_ok=True)
        # format4 = easyxf('font:bold True;font:height 250; borders: left thin;')
        # format0 = easyxf('font:height 200;borders: left thin, right thin;')
        # text = easyxf('font:height 200; borders: left thin;')
        # format3 = easyxf('font:height 200; align: horiz right;')
        # format1 = easyxf('font:height 250; font:bold True; borders: bottom thin, top thin, left thin;')
        # format5 = easyxf('font:height 200; align: horiz right; borders: bottom thin, top thin, right thin;')
        # format5_l = easyxf('font:height 200; align: horiz right;borders: bottom thin, right thin, top thin;')
        # format6 = easyxf('font:height 200; align: horiz right;borders: right thin;')
        # format6_r = easyxf('font:height 200; align: horiz right;borders: right thin;')
        # format_7 = easyxf(
        #     'font:height 250; align: horiz right; font:bold True;borders: left thin, top thin, bottom thin;')
        # format_8 = easyxf(
        #     'font:height 250; align: horiz right; font:bold True;borders: right thin, top thin, bottom thin;')
        # format_8_r = easyxf(
        #     'font:height 250; align: horiz right; font:bold True;borders: right thin, top thin, bottom thin;')
        # format_9 = easyxf(
        #     'font:height 250;borders: top thin, bottom thin;')
        # title = easyxf('font:height 300; font:bold True;borders: left thin, right thin, top thin;')
        # format_10 = easyxf('font:height 200;')
        # format_11 = easyxf('font:height 200; borders: right thin;')
        # format_12 = easyxf('borders: right thin;')
        # format_13 = easyxf('borders: left thin;')
        # worksheet.col(0).width = 8000
        # worksheet.col(1).width = 4000
        # worksheet.col(2).width = 4000
        # worksheet.col(3).width = 8000
        # worksheet.col(4).width = 4000
        # worksheet.col(5).width = 4000
        # worksheet.col(16).width = 10000
        # worksheet.col(17).width = 4000
        # worksheet.col(18).width = 2000
        # worksheet.col(19).width = 2000
        # worksheet.col(20).width = 2000
        # worksheet.col(21).width = 2000
        # worksheet.row(5).height = 400
        # worksheet.row(2).height = 400
        # worksheet.row(4).height = 400
        # worksheet.write_merge(0, 1, 0, 2, data['form']['account_report_id'][1], title)
        # if start_date and end_date:
        #     worksheet.write_merge(2, 2, 0, 2, start_date + ' ' + 'to' + ' ' + end_date,format0)
        # elif start_date:
        #     worksheet.write_merge(2, 2, 0, 2, 'from' + ' ' + start_date, format0)
        # elif end_date:
        #     worksheet.write_merge(2, 2, 0, 2, 'till' + ' ' + end_date, format0)
        # else:
        #     worksheet.write_merge(2, 2, 0, 2, '', format0)
        # worksheet.write(3, 3, '', format_10)
        # worksheet.write(3, 4, '', format_10)
        # worksheet.write(3, 5, '', format_10)
        # worksheet.write(3, 2, '', format_11)
        # worksheet.write(3, 0, '', format_13)
        # row = 4
        # col = 0
        # flag = 0
        # row_n = 4
        # for account in account_lines:
        #     worksheet.row(row).height = 400
        #     if account.get('level') == 1:
        #         flag += 1
        #         if flag < 2:
        #             worksheet.write(row, col, account.get('name'), format1)
        #             if end_date:
        #                 worksheet.write_merge(row, row, col + 1, col + 2, 'as at' + ' ' + end_date, format5_l)
        #             else:
        #                 worksheet.write_merge(row, row, col + 1, col + 2, '', format5_l)
        #             worksheet.write(row + 1, col, account.get('name'), format4)
        #             worksheet.write(row + 1, col + 2, account.get('balance'), format6)
        #             row = row + 1
        #         elif flag == 2:
        #             worksheet.write(row_n, col + 3, account.get('name'), format1)
        #             if end_date:
        #                 worksheet.write_merge(row_n, col + 4, row_n, col + 5, 'as at' + ' ' + end_date, format5)
        #             else:
        #                 worksheet.write_merge(row_n, col + 4, row_n, col + 5, '', format5)
        #             worksheet.write(row_n + 1, col + 3, account.get('name'), format4)
        #             worksheet.write(row_n + 1, col + 5, account.get('balance'), format6_r)
        #             row_n = row_n + 1
        #     worksheet.write(row + 1, col + 2, '', format_11)
        #     print("account.get('level')",account.get('level'))
        #     if int(account.get('level')) >= 2:
        #         if flag < 2:
        #             worksheet.write(row + 1, col, ''.join([i for i in account.get('name') if not i.isdigit()]), text)
        #             worksheet.write(row + 1, col + 1, account.get('balance'), format3)
        #             row = row + 1
        #         elif flag == 2:
        #             worksheet.write(row_n + 1, col + 3, ''.join([i for i in account.get('name') if not i.isdigit()]),
        #                             text)
        #             worksheet.write(row_n + 1, col + 4, account.get('balance'), format3)
        #             worksheet.write(row_n + 1, col + 5, '', format_12)
        #             row_n = row_n + 1
        # flag_t = 0
        # for line in account_lines:
        #     if line.get('level') == 1:
        #         worksheet.row(max(row, row_n) + 1).height = 400
        #         flag_t += 1
        #         if flag_t < 2:
        #             worksheet.write(max(row, row_n) + 1, 0, 'Total', format_7)
        #             worksheet.write(max(row, row_n) + 1, 1, '', format_9)
        #             worksheet.write(max(row, row_n) + 1, 2, abs(line.get('balance')), format_8)
        #         elif flag_t == 2:
        #             worksheet.write(max(row, row_n) + 1, 3, 'Total', format_7)
        #             worksheet.write(max(row, row_n) + 1, 4, '', format_9)
        #             worksheet.write(max(row, row_n) + 1, 5, abs(line.get('balance')), format_8_r)
        #
        # fp = io.BytesIO()
        # workbook.save(fp)
        # excel_file = base64.encodestring(fp.getvalue())
        # self.bs_pl_summary_file = excel_file
        # fp.close()
        data = {}
        data['ids'] = self.env.context.get('active_ids', [])
        data['model'] = self.env.context.get('active_model', 'ir.ui.menu')
        data['form'] = self.read()[0]
        used_context = self._build_contexts(data)
        data['form']['used_context'] = dict(used_context,
                                            lang=self.env.context.get(
                                                'lang') or 'en_US')
        account_lines = self.env[
            'report.tis_tally_bs_and_pl.report_tally_bs'].get_account_lines(
            data['form'])
        start_date = ''
        end_date = ''
        if self.date_from:
            start_date = datetime.strptime(str(self.date_from),
                                           '%Y-%m-%d').strftime(
                "%d-%m-%Y")
        if self.date_to:
            end_date = datetime.strptime(str(self.date_to),
                                         '%Y-%m-%d').strftime(
                "%d-%m-%Y")
        workbook = xlwt.Workbook()
        worksheet = workbook.add_sheet('Report', cell_overwrite_ok=True)
        format0 = easyxf('font:height 200;borders: left thin, right thin;')
        format_1 = easyxf(
            'font:bold True;font:height 250; borders: right thin, bottom thin, top thin, left thin;')
        format_2 = easyxf(
            'font:bold True;font:height 250; borders:  bottom thin, top thin;')
        format_3 = easyxf(
            'font:bold True;font:height 250; borders: right thin, bottom thin, top thin;')
        format_4 = easyxf(
            'font:bold True;font:height 250; borders: left thin, bottom thin, top thin;')
        format_5 = easyxf('font:bold True;font:height 250;')
        format_6 = easyxf(
            'font:bold True;font:height 250;borders: right thin;')
        format_9 = easyxf('font:height 200; borders: left thin;')
        format_10 = easyxf('font:height 200;')
        format_11 = easyxf('font:height 200; borders: right thin;')
        format_13 = easyxf('borders: left thin;')
        format_14 = easyxf(
            'font:height 200;borders: right thin;')
        worksheet.col(0).width = 8000
        worksheet.col(1).width = 4000
        worksheet.col(2).width = 4000
        worksheet.col(3).width = 8000
        worksheet.col(4).width = 4000
        worksheet.col(5).width = 4000
        worksheet.col(16).width = 10000
        worksheet.col(17).width = 4000
        worksheet.col(18).width = 2000
        worksheet.col(19).width = 2000
        worksheet.col(20).width = 2000
        worksheet.col(21).width = 2000
        worksheet.row(5).height = 400
        worksheet.row(2).height = 400
        worksheet.row(4).height = 400
        worksheet.row(6).height = 400
        worksheet.row(7).height = 400
        worksheet.row(8).height = 400
        worksheet.row(9).height = 400
        worksheet.row(10).height = 400
        worksheet.row(11).height = 400
        worksheet.row(12).height = 400
        worksheet.write_merge(0, 1, 0, 2, data['form']['account_report_id'][1],
                              format_1)
        if start_date and end_date:
            worksheet.write_merge(2, 2, 0, 2,
                                  start_date + ' ' + 'to' + ' ' + end_date,
                                  format0)
        elif start_date:
            worksheet.write_merge(2, 2, 0, 2, 'from' + ' ' + start_date,
                                  format0)
        elif end_date:
            worksheet.write_merge(2, 2, 0, 2, 'till' + ' ' + end_date, format0)
        else:
            worksheet.write_merge(2, 2, 0, 2, '', format0)
        worksheet.write(3, 3, '', format_10)
        worksheet.write(3, 4, '', format_10)
        worksheet.write(3, 5, '', format_10)
        worksheet.write(3, 2, '', format_11)
        worksheet.write(3, 0, '', format_13)
        worksheet.write(4, 1, '', format_2)
        worksheet.write(4, 2, '', format_3)
        worksheet.write(4, 4, '', format_2)
        worksheet.write(4, 5, '', format_3)
        row = 4
        col = 0
        row_n = 0
        extist_pofit_and_loss = False
        op_key = 'chart_of_account'
        res = []
        income_sum = 0
        expense_sum = 0
        other_income_sum = 0
        other_expense_sum = 0
        for account in account_lines:
            # print(account)
            if account.get('chart_of_account') == 'Income':
                income_sum += account['balance']
            if account.get('chart_of_account') == 'Expenses':
                expense_sum += account['balance']
            if account.get('chart_of_account') != 'Income' and account.get('parent_type') == 'Income' and account.get('chart_of_account'):
                other_income_sum += account['balance']
            if account.get('chart_of_account') != 'Expenses' and account.get('parent_type') == 'Expense' and account.get('chart_of_account'):
                other_expense_sum += account['balance']
        print('income_sum', income_sum, 'expense_sum', expense_sum, 'other_income_sum', other_income_sum,
              'other_expense_sum', other_expense_sum)
        gp = income_sum - expense_sum
        if gp >= expense_sum:
            gross_profit = gp
        else:
            gross_profit = gp


        for account in account_lines:
                # print(account)
                if account.get('chart_of_account'):



                    res.append(account[op_key])
        res = list(set(res))
        print(res)
        groups = dict((tp, []) for tp in res)
        for acc in account_lines:
                    if acc.get('chart_of_account'):
                        groups[acc['chart_of_account']].append(acc)
        b=[]

        # for account in res:
        #     balance=0
        #     for ac in account_lines:
        #         if ac.get('chart_of_account'):
        #             if account == ac['chart_of_account']:
        #                 balance=balance+ac['balance']
        #     b.append(balance)
        #     print(b)
        # data_dict = dict(zip(res, b))
        # print(data_dict)

        for ac in account_lines:
                balance =0
                if ac.get('chart_of_account'):
                    if ac['chart_of_account'] == 'Income':
                        balance=balance+ac['balance']
                    elif ac['chart_of_account'] == 'Expenses':
                        balance = balance + ac['balance']
                b.append(balance)
        print(b)
        data_dict = dict(zip(res, b))
        print(data_dict)
        # Print the resulting dictionary
        sorted_account_lines = sorted(account_lines, key=lambda x: x.get('chart_of_account', ''))


        for account in sorted_account_lines:
            worksheet.row(row).height = 400
            if account['account_type'] == 'account_type':
                flag = 0
                account_typ = account['name']
                worksheet.write(row, col, account_typ, format_2)

                j=[]
                k=[]
                for parent_type in sorted_account_lines:
                    print(parent_type, '!!!!!!!!!!!!!!!!!!!!!')
                    if parent_type['parent_type'] == 'Profit (Loss) to report':
                        extist_pofit_and_loss = True
                        if account_typ == 'Liability'and float(parent_type['balance']) < 0:
                            row = row + 2
                            worksheet.write(row, col, parent_type['name'],
                                            format_9)
                            worksheet.write(row, col + 1,
                                            parent_type['balance'])

                        if account_typ == 'Assets'and float(parent_type['balance']) >= 0:
                            row = row + 1
                            worksheet.write(row, col, parent_type['name'],
                                            format_9)
                            worksheet.write(row, col + 1,
                                            parent_type['balance'])

                    if parent_type['parent_type'] == account_typ:
                        if parent_type['name'] == parent_type['parent_type']:

                            if flag == 0:

                                # row = row + 1
                                # worksheet.write(row, col, parent_type['name'],
                                #                 format_5)
                                # worksheet.write(row, col + 2,
                                #                 parent_type['balance'],
                                #                 format_6)
                                total_balance = parent_type['balance']
                                flag = 1
                            else:
                                row = row + 1
                                worksheet.write(row, col, parent_type['name'],
                                                format_9)
                                worksheet.write(row, col + 2,
                                                parent_type['balance'],format_14)
                        else:
                            # row = row + 1
                            # worksheet.write(row, col, parent_type['name'],
                            #                 format_9)
                            # worksheet.write(row, col + 1,
                            #                 parent_type['balance'])
                            # for r in res:
                            #     print(res, '-------------------------r------------------')

                            # if r == parent_type['chart_of_account']:

                                if not parent_type['chart_of_account'] in j:

                                        # for key, value in data_dict.items():
                                        #     if key == parent_type['chart_of_account']:
                                         row = row + 1
                                         if parent_type['chart_of_account'] == 'Income':
                                                worksheet.write(row, col, parent_type['chart_of_account'],
                                                                format_5)
                                                worksheet.write(row, col+1, income_sum,
                                                                format_5)
                                                worksheet.write(row+1, col,'Gross profit',
                                                                format_5)
                                         elif parent_type['chart_of_account'] == 'Expenses':

                                                worksheet.write(row, col, parent_type['chart_of_account'],
                                                                format_5)
                                                worksheet.write(row, col + 1, expense_sum,
                                                                format_5)
                                         else:

                                             if not parent_type['parent_type'] in k:
                                                 if parent_type['parent_type'] == 'Expense':
                                                     worksheet.write(row, col, 'Indirect Expenses',
                                                                     format_5)
                                                     worksheet.write(row, col + 1, other_expense_sum,
                                                                     format_5)
                                                 else:
                                                     worksheet.write(row, col, 'Indirect Income',
                                                                     format_5)
                                                     worksheet.write(row, col + 1, other_income_sum,
                                                                     format_5)
                                             k.append(parent_type['parent_type'])

                                j.append(parent_type['chart_of_account'])
                                worksheet.write(row + 1, col, parent_type['name'],
                                            format_9)
                                worksheet.write(row + 1, col + 1,
                                            parent_type['balance'])

                                row = row + 1



                if row_n < row:
                    row_n = row
                    if extist_pofit_and_loss:
                        row_n = row_n + 1
                col = col + 3
                row = 4
                worksheet.write(row_n + 1, col - 3, "Total", format_4)
                worksheet.write(row_n + 1, col - 1, total_balance, format_3)
                worksheet.write(row_n + 1, col - 2, '', format_2)
                for x in range(6, row_n + 1):
                    worksheet.write(x, col - 1, '', format_6)
        fp = io.BytesIO()
        workbook.save(fp)
        excel_file = base64.encodestring(fp.getvalue())
        self.bs_pl_summary_file = excel_file
        fp.close()
        return {
            'type': 'ir.actions.act_url',
            'url': 'web/content/?model=accounting.report&'
                   'field=bs_pl_summary_file&download=true&id=%s&filename=bs_pl_tally.xls' % self.id,
            'target': 'new',
        }

    def account_name(self, name):
        return ''.join([i for i in name if not i.isdigit()])

    def date_format(self, date):
        return datetime.strptime(date, '%Y-%m-%d').strftime(
            "%d-%m-%Y")


