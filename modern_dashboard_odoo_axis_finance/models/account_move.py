# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.http import request
import datetime



class AccountMoveInherit(models.Model):
    _inherit = 'account.move'


    @api.model
    def get_account_list(self):
        account_move = self.env['account.move']


    @api.model
    def get_account_move_list(self):
        calculate_posted = self.search_count([('state', 'in', ['posted'])])
        calculate_cancel = self.search_count([('state', 'in', ['cancel'])])
        account_payment=  self.env['account.payment']
        calculate_customer_payment = account_payment.search_count([('partner_type','=', 'customer')])
        calculate_vendor_payment = account_payment.search_count([('partner_type','=', 'supplier')])
        account_payment_data = self.env['account.payment'].search([])
        calculate_profit = account_payment_data.mapped('amount')


        
        return{
         'total_posted': calculate_posted,
         'total_cancel': calculate_cancel,
         'total_customer_payment':calculate_customer_payment,
         'total_vendor_payment': calculate_vendor_payment,
         'total_profit': calculate_profit
        }

    @api.model
    def get_invoice_order_table(self,option):
        if option == 'today':
            sql_query = """      
                SELECT distinct ap.amount_total AS amount,ap.invoice_origin as origin,
                ap.invoice_date as invoice_date,ap.partner_id as name,rs.name as name,ap.invoice_payment_ref as payment
                FROM account_move ap INNER JOIN res_partner rs ON (ap.partner_id = rs.id)
                WHERE ap.state = 'posted' AND ap.invoice_date >= current_date
            """
        if option == 'monthly':
            sql_query = """      
                SELECT distinct ap.amount_total AS amount,ap.invoice_origin as origin,
                ap.invoice_date as invoice_date,ap.partner_id as name,rs.name as name,ap.invoice_payment_ref as payment
                FROM account_move ap INNER JOIN res_partner rs ON (ap.partner_id = rs.id)
                WHERE ap.state = 'posted' AND EXTRACT(month FROM ap.invoice_date::date) = EXTRACT(month FROM CURRENT_DATE)  
            """
        if option == 'year':
            sql_query = """      
                SELECT distinct ap.amount_total AS amount,ap.invoice_origin as origin,
                ap.invoice_date as invoice_date,ap.partner_id as name,rs.name as name,ap.invoice_payment_ref as payment
                FROM account_move ap INNER JOIN res_partner rs ON (ap.partner_id = rs.id)
                WHERE ap.state = 'posted' AND EXTRACT(year FROM ap.invoice_date::date) = EXTRACT(year FROM CURRENT_DATE)  
            """
        if option == 'all':
            sql_query = """      
                SELECT distinct ap.amount_total AS amount,ap.invoice_origin as origin,
                ap.invoice_date as invoice_date,ap.partner_id as name,rs.name as name,ap.invoice_payment_ref as payment
                FROM account_move ap INNER JOIN res_partner rs ON (ap.partner_id = rs.id)
                WHERE ap.state = 'posted'
            """
        self._cr.execute(sql_query)
        invoice_order = self._cr.dictfetchall()
        return {
            'total_invoice_order':invoice_order
        }

    @api.model
    def get_account_table(self):
        sql_query = """
            SELECT ap.name AS invoice, rs.name AS partner_name, ap.amount As amount,ap.payment_type AS payment_type,ap.communication AS memo,ap.payment_date AS payment_date
            FROM account_payment ap INNER JOIN res_partner rs ON (ap.partner_id = rs.id)
            WHERE ap.state = 'posted' and ap.partner_type = 'customer' 
            order by invoice asc 

        """
        self._cr.execute(sql_query)
        customer_data = self._cr.dictfetchall()


        sql_query = """
            SELECT ap.name AS invoice, rs.name AS partner_name, ap.amount As amount,ap.payment_type AS payment_type,ap.communication AS memo,ap.payment_date AS payment_date
            FROM account_payment ap INNER JOIN res_partner rs ON (ap.partner_id = rs.id)
            WHERE ap.state = 'posted' and ap.partner_type = 'supplier'

        """
        self._cr.execute(sql_query)
        vendor_data = self._cr.dictfetchall()


        sql_query = """
           SELECT rs.name AS customer_name
            FROM  res_partner rs 
            WHERE rs.id IN (14,10);

        """
        self._cr.execute(sql_query)
        customer_list = self._cr.dictfetchall()

        sql_query = """
           SELECT rs.name AS customer_name
            FROM  res_partner rs 
            WHERE rs.id IN (14);

        """
        self._cr.execute(sql_query)
        vendor_list = self._cr.dictfetchall()


        sql_query = """
           SELECT aj.name AS journal_name,aj.type AS types
            FROM  account_journal aj 
            

        """
        self._cr.execute(sql_query)
        journal_list = self._cr.dictfetchall()


        sql_query = """         
        SELECT distinct ap.partner_id AS partner_name, rs.name AS partner_name, ap.amount_total As amount
        FROM account_move ap INNER JOIN res_partner rs ON (ap.partner_id = rs.id)
        WHERE ap.state = 'posted'
            

        """
        self._cr.execute(sql_query)
        revenue_customer = self._cr.dictfetchall()

        return {
            
            'customer_payment_data': customer_data,
            'vendor_payment_data': vendor_data,
            'customer_list_data': customer_list,
            'vendor_list_data': vendor_list,
            'journal_list_data': journal_list,
            'total_revenue_customer': revenue_customer,
          }


    @api.model
    def get_customer_payment(self, option):
        cr = self._cr  
        if option == 'today':
            query = """
              SELECT so.name as name, rs.name,MAX(amount)  as  amount
            from account_payment so join res_partner rs on (so.partner_id =rs.id)  
            WHERE so.payment_date >= current_date
            group by rs.name,so.name
            order by  so.name desc limit 8      
            """  
        if option == 'monthly':
            query = """
              SELECT so.name as name, rs.name,MAX(amount)  as  amount
            from account_payment so join res_partner rs on (so.partner_id =rs.id)  
            WHERE EXTRACT(month FROM so.payment_date::date) = EXTRACT(month FROM CURRENT_DATE)  
            group by rs.name,so.name
            order by  so.name desc limit 8      
            """  
        if option == 'year':
            query = """
              SELECT so.name as name, rs.name,MAX(amount)  as  amount
            from account_payment so join res_partner rs on (so.partner_id =rs.id)  
             WHERE EXTRACT(year FROM so.payment_date::date) = EXTRACT(year FROM CURRENT_DATE)  
            group by rs.name,so.name
            order by  so.name desc limit 8      
            """  
        if option == 'all':
            query = """
              SELECT so.name as name, rs.name,MAX(amount)  as  amount
            from account_payment so join res_partner rs on (so.partner_id =rs.id)  
            group by rs.name,so.name
            order by  so.name desc limit 8      
            """  

        cr.execute(query)
        payroll_data = cr.dictfetchall()
        payroll_label = []
        payroll_dataset = []
        data_set = {}
        for data in payroll_data:
            payroll_label.append(data['name'])
            payroll_dataset.append(data['amount'])
        data_set.update({"payroll_dataset":payroll_dataset})
        data_set.update({"payroll_label":payroll_label})
        return data_set



    @api.model
    def get_customer_invoice(self):

        cr = self._cr  

        query = """
          SELECT cl.partner_id AS partner_name,max(amount_residual) as price,rs.name AS partner_name
            FROM account_move cl INNER JOIN res_partner rs ON (cl.partner_id = rs.id)
            group by cl.partner_id,rs.name
            order by cl.partner_id

        """

                

        cr.execute(query)
        payroll_data = cr.dictfetchall()
        payroll_label = []
        payroll_dataset = []
        data_set = {}
        for data in payroll_data:
            payroll_label.append(data['partner_name'])
            payroll_dataset.append(data['price'])
        data_set.update({"payroll_dataset":payroll_dataset})
        data_set.update({"payroll_label":payroll_label})
        return data_set



    @api.model
    def get_recent_customer(self):
        cr = self._cr

        query = """
            

        SELECT so.name as name, rs.name,count(*) 
        from sale_order so join res_partner rs on so.partner_id =rs.id   
        group by rs.name,so.name
        order by  so.name desc limit 5
        """  
                
        cr.execute(query)
        payroll_data = cr.dictfetchall()
        payroll_label = []
        payroll_dataset = []
        data_set = {}
        for data in payroll_data:
            payroll_label.append(data['name'])
            payroll_dataset.append(data['count'])
        data_set.update({"payroll_dataset":payroll_dataset})
        data_set.update({"payroll_label":payroll_label})
        return data_set



    @api.model
    def get_bank_cash_info(self, option):
        cr = self._cr
        if option == 'today':
            query = """
                SELECT so.partner_id as name, rs.name,sum(debit)  as debit
                from account_move_line so join res_partner rs on so.partner_id =rs.id   
                WHERE so.date >= current_date
                group by rs.name,so.partner_id
                order by  so.partner_id desc limit 5
            """  
        if option == 'monthly':
            query = """
                SELECT so.partner_id as name, rs.name,sum(debit)  as debit
                from account_move_line so join res_partner rs on so.partner_id =rs.id   
                WHERE EXTRACT(month FROM so.date::date) = EXTRACT(month FROM CURRENT_DATE)  
                group by rs.name,so.partner_id
                order by  so.partner_id desc limit 5
            """  
        if option == 'year':
            query = """
                SELECT so.partner_id as name, rs.name,sum(debit)  as debit
                from account_move_line so join res_partner rs on so.partner_id =rs.id   
                WHERE EXTRACT(year FROM so.date::date) = EXTRACT(year FROM CURRENT_DATE)  
                group by rs.name,so.partner_id
                order by  so.partner_id desc limit 5
            """  
        if option == 'all':
            query = """
                SELECT so.partner_id as name, rs.name,sum(debit)  as debit
                from account_move_line so join res_partner rs on so.partner_id =rs.id   
                group by rs.name,so.partner_id
                order by  so.partner_id desc limit 5
            """  
                
        cr.execute(query)
        payroll_data = cr.dictfetchall()
        payroll_label = []
        payroll_dataset = []
        data_set = {}
        for data in payroll_data:
            payroll_label.append(data['name'])
            payroll_dataset.append(data['debit'])
        data_set.update({"payroll_dataset":payroll_dataset})
        data_set.update({"payroll_label":payroll_label})
        return data_set





    @api.model
    def get_supplier_payment(self, option):
        cr = self._cr  
        if option == 'today':
            query = """
              SELECT cl.partner_id AS partner_name,max(amount) as price,rs.name AS partner_name
                FROM account_payment cl left JOIN res_partner rs ON (cl.partner_id = rs.id)
                where cl.partner_type ='supplier' AND cl.payment_date >= current_date
                group by cl.partner_id,rs.name
                order by cl.partner_id
            """
        if option == 'monthly':
            query = """
              SELECT cl.partner_id AS partner_name,max(amount) as price,rs.name AS partner_name
                FROM account_payment cl left JOIN res_partner rs ON (cl.partner_id = rs.id)
                where cl.partner_type ='supplier' AND EXTRACT(month FROM cl.payment_date::date) = EXTRACT(month FROM CURRENT_DATE)  
                group by cl.partner_id,rs.name
                order by cl.partner_id
            """
        if option == 'year':
            query = """
              SELECT cl.partner_id AS partner_name,max(amount) as price,rs.name AS partner_name
                FROM account_payment cl left JOIN res_partner rs ON (cl.partner_id = rs.id)
                where cl.partner_type ='supplier' AND EXTRACT(year FROM cl.payment_date::date) = EXTRACT(year FROM CURRENT_DATE)  
                group by cl.partner_id,rs.name
                order by cl.partner_id
            """
        if option == 'all':
            query = """
              SELECT cl.partner_id AS partner_name,max(amount) as price,rs.name AS partner_name
                FROM account_payment cl left JOIN res_partner rs ON (cl.partner_id = rs.id)
                where cl.partner_type ='supplier'
                group by cl.partner_id,rs.name
                order by cl.partner_id
            """

                

        cr.execute(query)
        payroll_data = cr.dictfetchall()
        payroll_label = []
        payroll_dataset = []
        data_set = {}
        for data in payroll_data:
            payroll_label.append(data['partner_name'])
            payroll_dataset.append(data['price'])
        data_set.update({"payroll_dataset":payroll_dataset})
        data_set.update({"payroll_label":payroll_label})
        return data_set

    # @api.model
    # def get_vendor_bills(self):

    #     cr = self._cr  

    #     query = """
    #       SELECT cl.partner_id AS partner_name,max(amount_total) as price,rs.name AS partner_name
    #         FROM account_move cl INNER JOIN res_partner rs ON (cl.partner_id = rs.id)
    #         where cl.state ='draft'
    #         group by cl.partner_id,rs.name
    #         order by cl.partner_id

    #     """

    #     cr.execute(query)
    #     payroll_data = cr.dictfetchall()
    #     payroll_label = []
    #     payroll_dataset = []
    #     data_set = {}
    #     for data in payroll_data:
    #         payroll_label.append(data['partner_name'])
    #         payroll_dataset.append(data['price'])
    #     data_set.update({"payroll_dataset":payroll_dataset})
    #     data_set.update({"payroll_label":payroll_label})
    #     return data_set




    @api.model
    def get_journal_list(self):

        cr = self._cr  

        query = """
          SELECT aj.name AS journal_name,aj.type AS types
            FROM  account_journal aj 
            group by aj.name,aj.type
            order by aj.name 

                
        """  

        cr.execute(query)
        payroll_data = cr.dictfetchall()
        payroll_label = []
        payroll_dataset = []
        data_set = {}
        for data in payroll_data:
            payroll_label.append(data['journal_name'])
            payroll_dataset.append(data['types'])
        data_set.update({"payroll_dataset":payroll_dataset})
        data_set.update({"payroll_label":payroll_label})
        return data_set


    def get_current_company_value(self):
        current_company = request.httprequest.cookies.get('cids')
        if current_company:
            company_id = current_company[0]
        else:
            company_id = self.env.company.id
        return int(company_id)



    @api.model
    def get_overdues_this_month_and_year(self, *post):
        cr = self._cr  
      
        query =""" 
                               SELECT to_char(account_move.date, 'Month') as month, res_partner.name as due_partner, account_move.partner_id as parent,
                               sum(account_move.amount_total) as amount from account_move, res_partner where account_move.partner_id = res_partner.id
                               AND account_move.type = 'out_invoice'
                              
                               group by parent, due_partner, month
                               order by amount
                               """
       

    
        cr.execute(query)
        payroll_data = cr.dictfetchall()
        payroll_label = []
        payroll_dataset = []
        data_set = {}
        for data in payroll_data:
            payroll_label.append(data['due_partner'])
            payroll_dataset.append(data['amount'])
        data_set.update({"payroll_dataset":payroll_dataset})
        data_set.update({"payroll_label":payroll_label})
        return data_set
