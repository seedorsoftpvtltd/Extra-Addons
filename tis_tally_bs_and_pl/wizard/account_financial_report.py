# -*- coding: utf-8 -*-
# This module and its content is copyright of Technaureus Info Solutions Pvt. Ltd.
# - © Technaureus Info Solutions Pvt. Ltd 2019. All rights reserved.

from odoo import fields, models
from datetime import datetime,date
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
        company_id = self.env.user.company_id.name
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
        bold = easyxf('font:bold True;font:height 280; align: horiz center;')
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
        # worksheet.write_merge(0, 1, 0, 2, data['form']['account_report_id'][1],
        #                       format_1)
        worksheet.write_merge(0, 0, 0, 2, company_id,bold)

        worksheet.write_merge(1, 1, 0, 2, data['form']['account_report_id'][1], bold)
        if start_date and end_date:
            worksheet.write_merge(2, 2, 0, 2,
                                  start_date + ' ' + 'to' + ' ' + end_date,
                                  bold)
        elif start_date:
            worksheet.write_merge(2, 2, 0, 2, 'from' + ' ' + start_date,
                                  bold)
        elif end_date:
            worksheet.write_merge(2, 2, 0, 2, 'till' + ' ' + end_date, bold)
        else:
            today = date.today()
            date_obj = datetime.strptime(str(today), "%Y-%m-%d")

            # Convert the datetime object to a string in "dd-mm-yyyy" format
            output_date = date_obj.strftime("%d-%m-%Y")
            worksheet.write_merge(2, 2, 0, 2, 'As on:'+ ' ' + str(output_date), bold)
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
        entry=[]
        income_sum = 0
        expense_sum = 0
        other_income_sum = 0
        other_expense_sum = 0
        income=[]
        indirect_income=[]
        expense=[]
        indirect_expense=[]
        for account in account_lines:
            # print(account)
            if account.get('chart_of_account') == 'Direct Expenses':  # direct expense data stores in income field
                income_sum += account['balance']
                income.append(account)

            if account.get('chart_of_account') == 'Direct Income':  # direct income data stores in expense field
                expense_sum += account['balance']
                expense.append(account)
            if account.get('chart_of_account') != 'Direct Expenses' and account.get('parent_type') == 'Expense' and account.get('chart_of_account'):
                other_income_sum += account['balance']
                indirect_income.append(account)
            if account.get('chart_of_account') != 'Direct Income' and account.get('parent_type') == 'Income' and account.get('chart_of_account'):
                other_expense_sum += abs(account['balance'])
                indirect_expense.append(account)



        for account in account_lines:
                if account.get('chart_of_account'):


                    res.append(account[op_key])
        res = list(set(res))

        groups = dict((tp, []) for tp in res)
        for acc in account_lines:
                    if acc.get('chart_of_account'):
                        groups[acc['chart_of_account']].append(acc)
        b=[]

        for ac in account_lines:
                balance =0
                if self.account_report_id.name == 'Profit and Loss':
                    if ac.get('chart_of_account'):
                        if ac['chart_of_account'] == 'Income':
                            balance=balance+ac['balance']
                        elif ac['chart_of_account'] == 'Expenses':
                            balance = balance + ac['balance']
                    b.append(balance)
        for account in res:

            balance=0
            if self.account_report_id.name == 'Balance Sheet':
                for ac in account_lines:
                    if ac.get('chart_of_account'):
                        if account == ac['chart_of_account']:

                            balance=balance+ac['balance']
                b.append(balance)

        data_dict = dict(zip(res, b))

        sorted_account_lines = sorted(account_lines, key=lambda x: x.get('chart_of_account', ''))




        for account in sorted_account_lines:
         if self.account_report_id.name == "Balance Sheet":


            worksheet.row(row).height = 400
            if account['account_type'] == 'account_type':
                flag = 0
                account_typ = account['name']

                worksheet.write(row, col, account_typ, format_2)

                j=[]
                k=[]
                for parent_type in sorted_account_lines:
                    if parent_type['parent_type'] == 'Profit (Loss) to report':

                        extist_pofit_and_loss = True
                        if account_typ == 'Liability'and float(parent_type['balance']) < 0:
                            row = row + 2
                            worksheet.write(row, col, 'Profit and Loss Account',
                                            format_9)
                            worksheet.write(row, col + 2,
                                            -(parent_type['balance']), format_6)

                        if account_typ == 'Assets'and float(parent_type['balance']) >= 0:

                            row = row + 1
                            worksheet.write(row, col, 'Profit and Loss Account',
                                            format_9)
                            worksheet.write(row, col + 2,
                                            parent_type['balance'], format_6)

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
                                print("wwwww")
                                # row = row + 1
                                # worksheet.write(row, col, parent_type['name'],
                                #                 format_9)
                                # worksheet.write(row, col + 2,
                                #                 parent_type['balance'],format_14)
                        else:
                                if self.account_report_id.name == "Balance Sheet":

                                    i = 0
                                    for r in res:

                                        if r == parent_type['chart_of_account']:

                                            if not parent_type['chart_of_account'] in j:

                                                for key, value in data_dict.items():
                                                    if key == parent_type['chart_of_account']:
                                                        row = row + 1
                                                        worksheet.write(row, col, parent_type['chart_of_account'],
                                                                        format_5)

                                                        if parent_type['parent_type'] == 'Liability':

                                                            worksheet.write(row, col + 2,
                                                                            -(value),
                                                                            format_6)
                                                        else:
                                                            worksheet.write(row, col + 2,
                                                                            value,
                                                                            format_6)
                                                        j.append(parent_type['chart_of_account'])
                                            if parent_type['parent_type'] == 'Liability':
                                                worksheet.write(row + 1, col, parent_type['name'],
                                                                format_9)
                                                worksheet.write(row + 1, col + 1,
                                                                -(parent_type['balance']))
                                            else:
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
                worksheet.write(row_n + 1, col - 1, abs(total_balance), format_3)
                worksheet.write(row_n + 1, col - 2, '', format_2)


                # for x in range(6, row_n + 1):
                #     worksheet.write(x, col - 1, '', format_6)
        coll=0
        for account in sorted_account_lines:

            if self.account_report_id.name == "Profit and Loss":
                worksheet.row(row).height = 400
                if account['account_type'] == 'account_type':
                    flag = 0
                    account_typ = account['name']


                    if account['name'] == 'Expense':              #label expense need to be write first
                        worksheet.write(row, coll, account_typ, format_2)
                        coll = 3
                    else:
                        # For other account types like 'Income', write them in the next column
                        worksheet.write(row, coll +3, account_typ, format_2)

        if self.account_report_id.name == "Profit and Loss":
            expense_row=0
            bal=0
            netinc=0
            netexp=0
            inc_bal = 0
            inc_other_bal=0
            exp_bal=0
            exp_other_bal=0
            row = row + 1
            worksheet.write(row, col, 'Direct Expense',
                            format_5)
            worksheet.write(row, col + 2, abs(income_sum), format_5)
            expense_row = row
            for i  in range(len(income)):


                        worksheet.write(row + 1, col, income[i]['name'],
                                        format_9)
                        worksheet.write(row + 1, col + 1,
                                        abs(income[i]['balance']))
                        bal=abs(bal)+abs(income[i]['balance'])
                        row = row + 1
            row = row + 2
            tally=0
            tally1=0

            worksheet.write(expense_row, coll, 'Direct Income',
                            format_5)
            worksheet.write(expense_row, coll + 2, abs(expense_sum), format_5)
            for i in range(len(expense)):

                worksheet.write(expense_row + 1, coll, expense[i]['name'],
                                format_9)
                worksheet.write(expense_row + 1, coll + 1,
                                abs(expense[i]['balance']))
                exp_bal = abs(exp_bal) + abs(expense[i]['balance'])

                expense_row = expense_row + 1
            expense_row = expense_row + 1


            if row > expense_row:
                new_row =row
            else:
                new_row=expense_row

            if income_sum < expense_sum:
                tally1 = abs(expense_sum) - abs(income_sum)
                worksheet.write(row, col, 'Gross Profit c/o',format_9)
                worksheet.write(row, col + 2, tally1, format_5)
            else:
                tally = abs(income_sum) - abs(expense_sum)
                worksheet.write(expense_row, coll, 'Gross Loss c/o',format_9)
                worksheet.write(expense_row, coll + 2, tally, format_5)
            new_row = new_row + 1
            a = bal + tally1
            b = exp_bal + tally
            worksheet.write(new_row, col + 2, a, format_2)
            worksheet.write(new_row, coll + 2, b, format_2)
            new_row = new_row + 1

            if income_sum > expense_sum:
                netinc = tally
                new_row = new_row + 1
                worksheet.write(new_row, col, 'Gross Loss b/f', format_9)
                worksheet.write(new_row, col + 2,tally, format_5)
            else:
                netexp=tally1
                new_row = new_row + 1
                worksheet.write(new_row, coll, 'Gross Profit b/f', format_9)
                worksheet.write(new_row, coll + 2, tally1, format_5)
            new_row = new_row + 1
            row = new_row + 1
            worksheet.write(row, col, 'Indirect Expense',
                            format_5)

            worksheet.write(row, col + 2, abs(other_income_sum), format_5)
            for i in range(len(indirect_income)):
                        worksheet.write(row + 1, col, indirect_income[i]['name'],
                                        format_9)
                        worksheet.write(row + 1, col + 1,
                                        abs(indirect_income[i]['balance']))
                        inc_other_bal = inc_other_bal + abs(indirect_income[i]['balance'])
                        row = row + 1
            row = row + 2


            ind_expense_row = new_row + 1
            worksheet.write(ind_expense_row, coll, 'Indirect Income',
                            format_5)
            worksheet.write(ind_expense_row, coll + 2, abs(other_expense_sum), format_5)
            for i in range(len(indirect_expense)):


                worksheet.write(ind_expense_row + 1, coll, indirect_expense[i]['name'],
                                format_9)
                worksheet.write(ind_expense_row + 1, coll + 1,
                                abs(indirect_expense[i]['balance']))
                exp_other_bal = exp_other_bal + abs(indirect_expense[i]['balance'])

                ind_expense_row = ind_expense_row + 1
            ind_expense_row = ind_expense_row + 2

            if row > ind_expense_row:
                new_row1 =row
            else:
                new_row1=ind_expense_row

            net2=tally1+exp_other_bal
            net1 = tally + inc_other_bal
            tally2=0
            tally3=0
            if net1 < net2:
                tally2 = net2 - net1
                worksheet.write(new_row1, col, 'Net Profit',format_9)
                worksheet.write(new_row1, col + 2, tally2, format_5)
            else:
                tally3 = net1 - net2

                worksheet.write(new_row1, coll, 'Net Loss',format_9)
                worksheet.write(new_row1, coll + 2, tally3, format_5)
            new_row1 = new_row1 + 1
            worksheet.write(new_row1, col,'Total', format_2)
            worksheet.write(new_row1, col + 1,'', format_2)
            worksheet.write(new_row1, col + 2, inc_other_bal+netinc+tally2, format_2)
            worksheet.write(new_row1, coll, 'Total', format_2)
            worksheet.write(new_row1, coll + 1, '', format_2)
            worksheet.write(new_row1, coll + 2, exp_other_bal+netexp+tally3, format_2)
            new_row1 = new_row1 + 1
            new_row1 = new_row1 + 1


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


