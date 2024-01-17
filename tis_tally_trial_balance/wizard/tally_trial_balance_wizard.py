# -*- coding: utf-8 -*-
# This module and its content is copyright of Technaureus Info Solutions Pvt. Ltd.
# - © Technaureus Info Solutions Pvt. Ltd 2020. All rights reserved.

from odoo import fields, models, _
from datetime import datetime,date
from odoo.tools.misc import xlwt
import io
import base64
from xlwt import easyxf


class AccountBalanceReport(models.TransientModel):
    _inherit = "account.balance.report"

    report_type = fields.Selection([('normal', 'Normal'), ('tally', 'Tally')], string="Report Type",
                                   default='tally')
    trial_balance_file = fields.Binary('Report')

    def check_report_tally_trial_balance(self):
        self.ensure_one()
        data = {}
        data['ids'] = self.env.context.get('active_ids', [])
        data['model'] = self.env.context.get('active_model', 'ir.ui.menu')
        data['form'] = self.read(['date_from', 'date_to', 'journal_ids', 'target_move', 'company_id'])[0]
        used_context = self._build_contexts(data)
        data['form']['used_context'] = dict(used_context, lang=self.env.context.get('lang') or 'en_US')
        return self.with_context(discard_logo_check=True)._print_report_tally_trial_balance(data)

    def _print_report_tally_trial_balance(self, data):
        data = self.pre_print_report(data)
        records = self.env[data['model']].browse(data.get('ids', []))
        return self.env.ref('tis_tally_trial_balance.action_tally_trial_balance').report_action(records, data=data)

    def print_tally_trial_balance_xls_report(self):
        from datetime import datetime, date
        datas = {}
        datas['model'] = 'account.balance.report'
        datas['form'] = self.read()[0]
        today=date.today()
        print_time = datetime.strptime(str(today.today()), '%Y-%m-%d').strftime('%d-%m-%Y')

        display_account = datas['form'].get('display_account')
        target_move = datas['form'].get('target_move')
        date_from = datas['form'].get('date_from')
        date_to = datas['form'].get('date_to')
        accounts = self.env['account.account'].search([])
        account_res = self.env['report.accounting_pdf_reports.report_trialbalance']._get_accounts(accounts,
                                                                                                  display_account,
                                                                                                  target_move,
                                                                                                  date_from, date_to)

        company_id = self.env.user.company_id.name
        workbook = xlwt.Workbook()
        worksheet = workbook.add_sheet('trial_balance', cell_overwrite_ok=True)
        bold = easyxf('font:bold True;font:height 280; align: horiz center;')
        bold_left = easyxf('font:bold True;font:height 250;')
        bold_right = easyxf('font:bold True; align: horiz right;font:height 250;')
        text_left = easyxf('font:height 250;')
        text_right = easyxf('font:height 250; align: horiz right;')
        time = easyxf('font:height 250; align: horiz right;')
        time_left = easyxf('font:height 250; align: horiz left;')
        bg_color = easyxf('font:bold True; align: horiz center; pattern: pattern solid,'
                          ' fore_colour gray25;font:height 250;')
        worksheet.col(0).width = 7000
        worksheet.col(1).width = 5000
        worksheet.col(2).width = 5000
        worksheet.col(3).width = 7000
        worksheet.col(4).width = 7000
        worksheet.col(5).width = 5000
        worksheet.col(6).width = 5000
        worksheet.col(7).width = 5000
        worksheet.row(2).height = 400
        worksheet.row(3).height = 400
        worksheet.row(4).height = 400
        worksheet.row(5).height = 400
        worksheet.row(6).height = 400
        worksheet.row(7).height = 400
        worksheet.write(2, 3, 'Printed At :', time)

        worksheet.write(2, 4, print_time, time_left)
        worksheet.write_merge(3, 3, 4, 4, '')
        worksheet.write_merge(3, 5, 0, 2, 'Particulars', bold)
        worksheet.write_merge(3, 3, 3, 4, company_id, bold)
        if self.date_from and self.date_to:
            date = datetime.strptime(str(self.date_from), '%Y-%m-%d').strftime(
                '%d-%m-%Y') + ' to ' + datetime.strptime(str(self.date_to), '%Y-%m-%d').strftime(
                '%d-%m-%Y')
            worksheet.write_merge(4, 4, 3, 4, date, bold)
        else:
                worksheet.write_merge(4, 4, 3, 4, 'As on:'+ ''+print_time, bold)

        worksheet.write_merge(5, 5, 3, 4, 'Trial Balance', bold)
        worksheet.write_merge(6, 6, 0, 4, '', bg_color)
        worksheet.write_merge(7, 7, 0, 2, '', bg_color)
        worksheet.write(7, 3, 'Debit Balance', bg_color)
        worksheet.write(7, 4, 'Credit Balance', bg_color)
        row = 8
        col = 0
        op_key = 'chart_of_account'
        res = ['equity','liability','asset','income','expense']
        income=[]

        expense=[]

        indirect_income=[]
        indirect_expense=[]
        equity=[]
        liability=[]
        asset=[]
        off_balance = []
        income_sum = 0
        expense_sum = 0
        other_income_sum=0
        other_expense_sum=0
        equity1=0
        liability1=0
        asset1=0

        off_balance1=0



        for account in account_res:

                # print(account)
                if account.get('chart_of_account') == 'Direct Income':  # direct expense data stores in income field
                    income_sum += account['balance']
                    income.append(account)

                if account.get('chart_of_account') == 'Direct Expenses':  # direct income data stores in expense field
                    expense_sum += account['balance']
                    expense.append(account)
                if account.get('chart_of_account') != 'Direct Income' and account.get('internal_group') == 'income':
                    other_income_sum += account['balance']
                    indirect_income.append(account)
                if account.get('chart_of_account') != 'Direct Expenses' and account.get('internal_group') == 'expense':
                    other_expense_sum += abs(account['balance'])
                    indirect_expense.append(account)
                if account.get('internal_group') == 'equity':
                    equity1 += account['balance']
                    equity.append(account)
                if account.get('internal_group') == 'liability':
                    liability1 += account['balance']
                    liability.append(account)
                if account.get('internal_group') == 'asset':
                    asset1 += account['balance']
                    asset.append(account)
                if account.get('internal_group') == 'off_balance':
                    off_balance1 += account['balance']
                    off_balance.append(account)
        chh=0
        chh1=0
        t=0
        t1=0
        liab=0
        liab1=0
        asse=0
        asse1=0
        inc=0
        inc1=0
        exp=0
        exp1=0
        in_inc=0
        in_inc1=0
        in_exp=0
        in_exp1=0
        off=0
        off1=0

        if equity:
            worksheet.row(row).height = 400
            worksheet.write(row, col, 'Equity', bold_left)
            e_r=row
            # if equity1 > 0:
            #     worksheet.write(row, col + 3, equity1, bold_left)
            #     chh+=equity1
            #
            # else:
            #     worksheet.write(row, col + 4, abs(equity1), bold_left)
            #     chh1+=equity1
            row = row + 1
            for account in equity:

                        if display_account:

                            worksheet.write(row, col, account['name'], text_left)

                        if account['balance'] == 0:
                            worksheet.write(row, col + 3, account['balance'], text_right)
                            worksheet.write(row, col + 4, abs(account['balance']), text_right)


                        if account['balance'] > 0:
                            worksheet.write(row, col + 3, account['balance'], text_right)
                            t=t+account['balance']


                        if account['balance'] < 0:
                            worksheet.write(row, col + 4, abs(account['balance']), text_right)
                            t1=t1+account['balance']

                        row = row + 1
            if t !=0:
                worksheet.write(e_r, col + 3, t, bold_left)
            if t1 !=0:
                worksheet.write(e_r, col + 4, abs(t1), bold_left)

        row = row + 1
        if liability:
            worksheet.row(row).height = 400
            worksheet.write(row, col, 'Liability', bold_left)
            l_r=row
            # if liability1 > 0:
            #     worksheet.write(row, col + 3, liability1, bold_left)
            #     chh += liability1
            # else:
            #     worksheet.write(row, col + 4, abs(liability1), bold_left)
            #     chh1 += liability1
            row = row + 1

            for account in liability:

                if display_account:
                    worksheet.write(row, col, account['name'], text_left)

                if account['balance'] == 0:
                    worksheet.write(row, col + 3, account['balance'], text_right)
                    worksheet.write(row, col + 4, abs(account['balance']), text_right)

                if account['balance'] > 0:
                    worksheet.write(row, col + 3, account['balance'], text_right)
                    liab = liab + account['balance']

                if account['balance'] < 0:
                    worksheet.write(row, col + 4, abs(account['balance']), text_right)
                    liab1 = liab1 + account['balance']

                row = row + 1
            if liab !=0:
                    worksheet.write(l_r, col + 3, liab, bold_left)
            if liab1 != 0:
                    worksheet.write(l_r, col + 4, abs(liab1), bold_left)
        row = row + 1
        if asset:
            worksheet.row(row).height = 400
            worksheet.write(row, col, 'Assets', bold_left)
            a_r=row
            # if asset1 > 0:
            #     worksheet.write(row, col + 3, asset1, bold_left)
            #     chh += asset1
            # else:
            #     worksheet.write(row, col + 4, abs(asset1), bold_left)
            #     chh1 += asset1
            row = row + 1
            for account in asset:


                        if display_account:

                            worksheet.write(row, col, account['name'], text_left)

                        if account['balance'] == 0:
                            worksheet.write(row, col + 3, account['balance'], text_right)
                            worksheet.write(row, col + 4, abs(account['balance']), text_right)

                        if account['balance'] > 0:
                            worksheet.write(row, col + 3, account['balance'], text_right)
                            asse = asse + account['balance']

                        if account['balance'] < 0:
                            worksheet.write(row, col + 4, abs(account['balance']), text_right)
                            asse1 = asse1 + account['balance']

                        row = row + 1
            if asse !=0:
                worksheet.write(a_r, col + 3, asse, bold_left)
            if asse1 !=0:
                worksheet.write(a_r, col + 4, abs(asse1), bold_left)
        row = row + 1
        if income:
            worksheet.row(row).height = 400
            worksheet.write(row, col, 'Direct Income', bold_left)
            in_r=row
            # if income_sum > 0:
            #     worksheet.write(row, col + 3, income_sum, bold_left)
            #     chh += income_sum
            # else:
            #     worksheet.write(row, col + 4, abs(income_sum), bold_left)
            #     chh1 += income_sum
            row = row + 1
            for account in income:


                        if display_account:

                            worksheet.write(row, col, account['name'], text_left)

                        if account['balance'] == 0:
                            worksheet.write(row, col + 3, account['balance'], text_right)
                            worksheet.write(row, col + 4, abs(account['balance']), text_right)

                        if account['balance'] > 0:
                            worksheet.write(row, col + 3, account['balance'], text_right)
                            inc = inc + account['balance']

                        if account['balance'] < 0:
                            worksheet.write(row, col + 4, abs(account['balance']), text_right)
                            inc1 = inc1 + account['balance']

                        row = row + 1
            if inc !=0:
                worksheet.write(in_r, col + 3, inc, bold_left)
            if inc1 !=0:
                worksheet.write(in_r, col + 4, abs(inc1), bold_left)
        row = row + 1
        if expense:
            worksheet.row(row).height = 400
            worksheet.write(row, col, 'Direct Expense', bold_left)
            exp_r=row
            # if expense_sum > 0:
            #     worksheet.write(row, col + 3, expense_sum, bold_left)
            #     chh += expense_sum
            # else:
            #     worksheet.write(row, col + 4, abs(expense_sum), bold_left)
            #     chh1 += expense_sum

            row = row + 1
            for account in expense:


                        if display_account:

                            worksheet.write(row, col, account['name'], text_left)

                        if account['balance'] == 0:
                            worksheet.write(row, col + 3, account['balance'], text_right)
                            worksheet.write(row, col + 4, abs(account['balance']), text_right)

                        if account['balance'] > 0:
                            worksheet.write(row, col + 3, account['balance'], text_right)
                            exp = exp + account['balance']

                        if account['balance'] < 0:
                            worksheet.write(row, col + 4, abs(account['balance']), text_right)
                            exp1 = exp1 + account['balance']

                        row = row + 1
            if exp !=0:
                worksheet.write(exp_r, col + 3, exp, bold_left)
            if exp1 !=0:
                worksheet.write(exp_r, col + 4, abs(exp1), bold_left)
        row = row + 1
        if indirect_income:
            in_inc_r=row
            worksheet.row(row).height = 400
            worksheet.write(row, col, 'Indirect Income', bold_left)
            # if other_income_sum > 0:
            #     worksheet.write(row, col + 3, other_income_sum, bold_left)
            #     chh += other_income_sum
            # else:
            #     worksheet.write(row, col + 4, abs(other_income_sum), bold_left)
            #     chh1 += other_income_sum
            row = row + 1
            for account in indirect_income:


                        if display_account:

                            worksheet.write(row, col, account['name'], text_left)

                        if account['balance'] == 0:
                            worksheet.write(row, col + 3, account['balance'], text_right)
                            worksheet.write(row, col + 4, abs(account['balance']), text_right)

                        if account['balance'] > 0:
                            worksheet.write(row, col + 3, account['balance'], text_right)
                            in_inc = in_inc + account['balance']

                        if account['balance'] < 0:
                            worksheet.write(row, col + 4, abs(account['balance']), text_right)
                            in_inc1 = in_inc1 + account['balance']

                        row = row + 1
            if in_inc != 0:
                worksheet.write(in_inc_r, col + 3, in_inc, bold_left)
            if in_inc1 != 0:
                worksheet.write(in_inc_r, col + 4, abs(in_inc1), bold_left)
        row = row + 1
        if indirect_expense:
            in_exp_r=row

            worksheet.row(row).height = 400
            worksheet.write(row, col, 'Indirect Expense', bold_left)
            # if other_expense_sum > 0:
            #     worksheet.write(row, col + 3, other_expense_sum, bold_left)
            #     chh += other_expense_sum
            # else:
            #     worksheet.write(row, col + 4, abs(other_expense_sum), bold_left)
            #     chh1 += other_expense_sum

            row = row + 1
            for account in indirect_expense:


                        if display_account:

                            worksheet.write(row, col, account['name'], text_left)

                        if account['balance'] == 0:
                            worksheet.write(row, col + 3, account['balance'], text_right)
                            worksheet.write(row, col + 4, abs(account['balance']), text_right)

                        if account['balance'] > 0:
                            worksheet.write(row, col + 3, account['balance'], text_right)
                            in_exp = in_exp + account['balance']

                        if account['balance'] < 0:
                            worksheet.write(row, col + 4, abs(account['balance']), text_right)
                            in_exp1 = in_exp1 + account['balance']

                        row = row + 1
            if in_exp !=0:
                worksheet.write(in_exp_r, col + 3, in_exp, bold_left)
            if in_exp1 !=0:
                worksheet.write(in_exp_r, col + 4, abs(in_exp1), bold_left)
        row = row + 1
        if off_balance:
            off_r=row
            worksheet.row(row).height = 400
            worksheet.write(row, col, 'Off Balance', bold_left)
            # if equity1 > 0:
            #     worksheet.write(row, col + 3, off_balance1, bold_left)
            #     chh+=off_balance1
            #
            # else:
            #     worksheet.write(row, col + 4, abs(equity1), bold_left)
            #     chh1+=off_balance1
            row = row + 1
            for account in off_balance:

                        if display_account:

                            worksheet.write(row, col, account['name'], text_left)

                        if account['balance'] == 0:
                            worksheet.write(row, col + 3, account['balance'], text_right)
                            worksheet.write(row, col + 4, abs(account['balance']), text_right)

                        if account['balance'] > 0:
                            worksheet.write(row, col + 3, account['balance'], text_right)
                            off = off + account['balance']

                        if account['balance'] < 0:
                            worksheet.write(row, col + 4, abs(account['balance']), text_right)
                            off1 = off1 + account['balance']

                        row = row + 1
            if off !=0:
                worksheet.write(off_r, col + 3, off, bold_left)
            if off1 !=0:
                worksheet.write(off_r, col + 4, abs(off1), bold_left)

        row = row + 1
        worksheet.row(row).height = 400
        row = row + 1
        worksheet.write(row, col, 'Grand Total', bold_left)
        worksheet.write(row, col + 3,t+liab+asse+inc+exp+in_inc+in_exp+off , bold_right)
        worksheet.write(row, col + 4, abs(t1+liab1+asse1+inc1+exp1+in_inc1+in_exp1+off1), bold_right)
        fp = io.BytesIO()
        workbook.save(fp)
        excel_file = base64.encodestring(fp.getvalue())
        self.trial_balance_file = excel_file
        fp.close()
        return {
            'type': 'ir.actions.act_url',
            'url': 'web/content/?model=account.balance.report&'
                   'field=trial_balance_file&download=true&id=%s&filename=bs_pl_tally.xls' % self.id,
            'target': 'new',
        }
