from odoo import api, fields, models, tools, _

class TiemsheetCount(models.Model):
    _inherit='project.project'
    timesheet_count=fields.Integer(compute='_timesheet_count',String='Timesheet Count')

    def _timesheet_count(self):
        for rec in self:
           cnt=self.env['account.analytic.line'].search_count([('project_id', '=', rec.id)])
           if cnt:
               rec['timesheet_count'] = cnt
           else:
               rec['timesheet_count'] = ''
           #print(rec.timesheet_count)

class ExpenseCount(models.Model):
    _inherit='res.users'
    expense_count = fields.Integer(compute='_expense_count',String='Expense Count')

    def _expense_count(self):
        for rec in self:
            cnt = self.env['hr.expense'].sudo().search_count([('employee_id.user_id.id', '=', rec.id)])
            if cnt:
                rec['expense_count'] = cnt
            else:
                rec['expense_count'] = ''

            #print(rec.expense_count)
