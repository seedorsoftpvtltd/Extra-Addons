from odoo import api, fields, models, _
from datetime import datetime, time, date, timedelta
from dateutil.relativedelta import relativedelta

class Partner(models.Model):
    _inherit = 'res.partner'
    filter_start_date = fields.Date(string='Start Date')
    filter_end_date = fields.Date(string='End Date')
    filter_start_date_customer = fields.Date(string='Start Date')
    filter_end_date_customer = fields.Date(string='End Date')
    filter_start_date_vendor = fields.Date(string='Start Date')
    filter_end_date_vendor = fields.Date(string='End Date')
    currency = fields.Many2one('res.currency', string='Currency',readonly=False)
    currency_customer = fields.Many2one('res.currency', string='Currency', readonly=False)
    currency_vendor = fields.Many2one('res.currency', string='Currency', readonly=False)

    # filter_invoice_ids = fields.One2many('account.move', 'partner_id', 'Filtered Records', readonly='False',
    #                                     domain=[('type', 'in', ['out_invoice','out_refund']),('state', 'in', ['posted']),
    #                                     ('invoice_date','>=',filter_start_date)])

    def apply_filter(self):


        f=self.env['account.move'].search([('partner_id','=',self.id),('type', 'in', ['out_invoice','out_refund']),('state', 'in', ['posted']),
                                           ('invoice_date','>=',self.filter_start_date),('invoice_date','<=',self.filter_end_date)])
        # print(self.filter_invoice_ids)
        # print(self.balance_invoice_ids)
        print(f)

        print(self.filter_start_date)
        print(self.filter_end_date)

        list=[]
        for line in f:
            list.append([0, 0, {
                'name': line.name,
                'currency_id':line.currency_id,
                'invoice_date':line.invoice_date,
            }])
            print("wwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwww")
            print(list)
            self.filter_invoice_ids = [(6, 0, [])]
            inv=self.write({



                'balance_invoice_ids': list,

                    # 'company_id':line.company_id,
                    # 'invoice_date_due':line.invoice_date_due,
                    # 'amount_total':line.amount_total,
                    # 'credit_amount_inv':line.credit_amount_inv,
                    # 'result_inv':line.result_inv,
                    # 'amount_total_signed':line.amount_total_signed,
                    # 'credit_amount':line.credit_amount,
                    # 'result':line.result,

                })
            return inv

    def print_report(self):
        return self.env.ref('filter_date.report_filter_print').report_action(self)
    def print_report_customer(self):
        return self.env.ref('filter_date.report_filter_print_customer').report_action(self)
    def print_report_vendor(self):
        return self.env.ref('filter_date.report_filter_print_vendor').report_action(self)


