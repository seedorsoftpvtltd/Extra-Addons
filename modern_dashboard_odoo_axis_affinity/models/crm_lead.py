# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.http import request
import datetime



class CrmInherit(models.Model):
    _inherit = 'crm.lead'


    @api.model
    def get_crm_value(self):
        crm_lead = self.env['crm.lead']

    @api.model
    def get_crm_list(self):
        uid = request.session.uid 
        user_id=self.env['res.users'].browse(uid)
        today_date = datetime.datetime.now().date()
        calculate_pipeline = self.env['crm.lead'].sudo().search_count([('user_id', '=', uid)])
        calculate_total_won= self.sudo().search_count([('active', '=', True),('probability', '=', 100)])
        calculate_total_lost= self.sudo().search_count([('active', '=', False),('probability', '=', 0)])
        calculate_overdue_opportunities = self.sudo().search_count([('type', '=', 'opportunity'),('date_deadline', '<', today_date), ('date_closed', '=', False)])
        calculate_open_opportunities = self.sudo().search_count([('type', '=', 'opportunity'),('probability', '<', 100)])
        crm_search_view_id = self.env.ref('crm.view_crm_case_opportunities_filter')
        abcd = self.env.ref('crm.view_crm_case_opportunities_filter')
        crm_obj =self.env['crm.lead'].sudo().search([])
        get_lead = self.search([])
        list_lead = get_lead.mapped('name')
        len_list_lead =len(list_lead)
        expected_revenue=0
        for lead in crm_obj:
            expected_revenue=round(expected_revenue + (lead.planned_revenue or 0.0) * (lead.probability or 0) / 100.0, 2)
        return{
            'total_won': calculate_total_won,
            'total_loss': calculate_total_lost,
            'my_pipeline' :calculate_pipeline,
            'overdue_opportunities':calculate_overdue_opportunities,
            'open_opportunities' :calculate_open_opportunities,
            'total_revenue': expected_revenue,
            'total_leads': len_list_lead

        }


    @api.model
    def get_crm_table(self):
        sql_query = """
            SELECT cl.name AS lead_name, cl.planned_revenue AS planned_revenue, cl.probability AS probability
            FROM crm_lead cl   
            ORDER BY lead_name DESC LIMIT 10

        """

        self._cr.execute(sql_query)
        crm_table = self._cr.dictfetchall()

        sql_query = """
           SELECT cl.name AS lead_name,cl.probability AS probability
            FROM crm_lead cl
            WHERE cl.probability = 100 limit 10

        """
        self._cr.execute(sql_query)
        total_won = self._cr.dictfetchall()


        sql_query = """
           SELECT cl.name AS lead_name,cl.probability AS probability
            FROM crm_lead cl
            WHERE cl.probability = 0 limit 10

        """
        self._cr.execute(sql_query)
        total_loss = self._cr.dictfetchall()


        sql_query = """
           SELECT cl.partner_id AS partner_name,cl.probability AS probability,rs.name AS partner_name
            FROM crm_lead cl INNER JOIN res_partner rs ON (cl.partner_id = rs.id)
            WHERE cl.probability = 100 limit 10

        """
        self._cr.execute(sql_query)
        total_won_customer = self._cr.dictfetchall()


        sql_query = """
           SELECT mt.name AS activity_name
            FROM mail_activity_type mt
            

        """
        self._cr.execute(sql_query)
        total_activity_type = self._cr.dictfetchall()
    
        


        return {
            
            'crm_tables': crm_table,
            'calculate_won':total_won,
            'calculate_loss':total_loss,
            'calculate': total_won_customer,
            'calculate_type':total_activity_type

          }


    @api.model
    def get_crm_lead(self):

        cr = self._cr  

        query = """
           select * from (
                select  to_char(now(), 'MON-YYYY') as Month ,sum((planned_revenue*probability)/100) as expected_revenue,1 as sorting
                from crm_lead where date_deadline 
                between (date_trunc('month', now()) + interval '0 month') and ((date_trunc('month', now()) + interval '1 month')- interval '1 day')
                union
                select  to_char((date_trunc('month', now()) + interval '1 month'), 'MON-YYYY') as Month ,sum((planned_revenue*probability)/100) as expecte_revenue, 2 as sorting
                from crm_lead where date_deadline 
                between (date_trunc('month', now()) + interval '1 month') and ((date_trunc('month', now()) + interval '2 month')- interval '1 day')
                union
                select  to_char((date_trunc('month', now()) + interval '2 month'), 'MON-YYYY') as Month ,sum((planned_revenue*probability)/100) as expected_revenue,3 as sorting
                from crm_lead where date_deadline 
                between (date_trunc('month', now()) + interval '2 month') and ((date_trunc('month', now()) + interval '3 month')- interval '1 day')
                union
                select  to_char((date_trunc('month', now()) + interval '3 month'), 'MON-YYYY') as Month ,sum((planned_revenue*probability)/100) as expected_revenue,4 as sorting
                from crm_lead where date_deadline 
                between (date_trunc('month', now()) + interval '3 month') and ((date_trunc('month', now()) + interval '4 month')- interval '1 day')
                union
                select  to_char((date_trunc('month', now()) + interval '4 month'), 'MON-YYYY') as Month ,sum((planned_revenue*probability)/100) as expected_revenue,5 as sorting
                from crm_lead where date_deadline 
                between (date_trunc('month', now()) + interval '4 month') and ((date_trunc('month', now()) + interval '5 month')- interval '1 day')
                union
                select  to_char((date_trunc('month', now()) + interval '5 month'), 'MON-YYYY') as Month ,sum((planned_revenue*probability)/100) as expected_revenue,6 as sorting
                from crm_lead where date_deadline 
                between (date_trunc('month', now()) + interval '5 month') and ((date_trunc('month', now()) + interval '6 month')- interval '1 day')
                ) as t order by sorting
        """  

        cr.execute(query)
        payroll_data = cr.dictfetchall()
        payroll_label = []
        payroll_dataset = []
        data_set = {}
        for data in payroll_data:
            payroll_label.append(data['month'])
            payroll_dataset.append(data['expected_revenue'])
        data_set.update({"payroll_dataset":payroll_dataset})
        data_set.update({"payroll_label":payroll_label})
        return data_set




    @api.model
    def get_probability(self):

        cr = self._cr  

        query = """
          SELECT cl.partner_id AS partner_name,cl.probability AS probability,rs.name AS partner_name
            FROM crm_lead cl INNER JOIN res_partner rs ON (cl.partner_id = rs.id)
            WHERE cl.probability = 100 
            group by cl.partner_id,cl.probability,rs.name
             order by cl.partner_id desc limit 5
                
        """  

        cr.execute(query)
        payroll_data = cr.dictfetchall()
        payroll_label = []
        payroll_dataset = []
        data_set = {}
        for data in payroll_data:
            payroll_label.append(data['partner_name'])
            payroll_dataset.append(data['probability'])
        data_set.update({"payroll_dataset":payroll_dataset})
        data_set.update({"payroll_label":payroll_label})
        return data_set




    @api.model
    def get_probability_loss(self):

        cr = self._cr  

        query = """
          SELECT cl.partner_id AS partner_name,cl.probability AS probability,rs.name AS partner_name
            FROM crm_lead cl INNER JOIN res_partner rs ON (cl.partner_id = rs.id)
            WHERE cl.probability = 0 
            order by cl.partner_id desc limit 5
                
        """  

        cr.execute(query)
        payroll_data = cr.dictfetchall()
        payroll_label = []
        payroll_dataset = []
        data_set = {}
        for data in payroll_data:
            payroll_label.append(data['partner_name'])
            payroll_dataset.append(data['probability'])
        data_set.update({"payroll_dataset":payroll_dataset})
        data_set.update({"payroll_label":payroll_label})
        return data_set


    @api.model
    def get_crm_team_sale(self):
        cr = self._cr

        query = """
            
         SELECT so.team_id as name, cl.name,count(*) 
        from sale_order so left join crm_team cl on so.team_id = cl.id   
        group by cl.name,so.team_id
        order by  so.team_id 
        
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
    def get_loss_list(self):
        cr = self._cr

        query = """
            
      SELECT rs.name as lead_name,count(*),cl.probability
            FROM crm_lead cl join res_partner rs on cl.partner_id =rs.id   
            WHERE cl.probability = 0
             group by rs.name,cl.probability
             order by rs.name desc limit 3
        """   
                
        cr.execute(query)
        payroll_data = cr.dictfetchall()
        payroll_label = []
        payroll_dataset = []
        data_set = {}
        for data in payroll_data:
            payroll_label.append(data['lead_name'])
            payroll_dataset.append(data['count'])
        data_set.update({"payroll_dataset":payroll_dataset})
        data_set.update({"payroll_label":payroll_label})
        return data_set



    @api.model
    def get_won_list(self):
        cr = self._cr

        query = """
            
        SELECT rs.name as lead_name,count(*),cl.probability
            FROM crm_lead cl join res_partner rs on cl.partner_id =rs.id   
            WHERE cl.probability = 100 
             group by rs.name,cl.probability
             order by rs.name desc limit 3
        """  
                
        cr.execute(query)
        payroll_data = cr.dictfetchall()
        payroll_label = []
        payroll_dataset = []
        data_set = {}
        for data in payroll_data:
            payroll_label.append(data['lead_name'])
            payroll_dataset.append(data['count'])
        data_set.update({"payroll_dataset":payroll_dataset})
        data_set.update({"payroll_label":payroll_label})
        return data_set

