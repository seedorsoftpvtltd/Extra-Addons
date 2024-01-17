# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.http import request
import datetime


class StockPickinfInherit(models.Model):
    _inherit = 'stock.picking'

    @api.model
    def get_stock_list(self):
        obj_stock_picking = self.env['stock.picking']


    @api.model
    def get_stock_picking_list(self):
        calculate_assigned = self.search_count([('state', 'in', ['assigned'])])
        calculate_done = self.search_count([('state', 'in', ['done'])])
        calculate_waiting = self.search_count([('state', 'in', ['confirmed','waiting'])])
        stock_lot_serial = self.env['stock.production.lot'].search([])
        count_lot_serial = len(stock_lot_serial)
        stock_reordering_rules = self.env['stock.warehouse.orderpoint'].search([])
        count_reordering_rules = len(stock_reordering_rules)
        get_internal_transfer = self.search([])
        list_transfer = get_internal_transfer.mapped('name')
        len_list_transfer =len(list_transfer)


        return{
        'total_assigned': calculate_assigned,
        'total_done':calculate_done,
        'total_waiting':calculate_waiting,
        'total_lot_serial' :count_lot_serial,
        'total_reordering_rules':count_reordering_rules,
        'total_internal_transfer':len_list_transfer,
        }




    @api.model
    def get_inventory_table(self):

        sql_query = """
            SELECT sp.name AS stock_name,sp.scheduled_date As origin
            FROM stock_picking sp
            WHERE sp.state = 'done' limit 10

        """
        self._cr.execute(sql_query)
        delivery_data = self._cr.dictfetchall()



        sql_query = """
            SELECT pp.name AS product_name,pp.list_price As list_price
            FROM product_template pp
            ORDER BY product_name DESC LIMIT 10
             

        """
        self._cr.execute(sql_query)
        product_price = self._cr.dictfetchall()


        sql_query = """
            SELECT spl.name AS lot_number
            FROM stock_production_lot spl limit 10
         

        """
        self._cr.execute(sql_query)
        lot_data = self._cr.dictfetchall()

        return {
            
            'abcd': delivery_data,
            'calculate_price':product_price,
            'calculate_lot':lot_data
          }

    @api.model
    def get_product_moves(self, option):
        cr = self._cr
        if option == 'today':
            query = """
              SELECT cl.product_id AS partner_name,max(qty_done)as price,rs.name AS partner_name
                FROM stock_move_line cl INNER JOIN product_template rs ON (cl.product_id = rs.id)
                WHERE cl.date >= current_date
                group by cl.product_id,rs.name
                order by cl.product_id limit 10
            """
        if option == 'monthly':
            query = """
              SELECT cl.product_id AS partner_name,max(qty_done)as price,rs.name AS partner_name
                FROM stock_move_line cl INNER JOIN product_template rs ON (cl.product_id = rs.id)
                WHERE EXTRACT(month FROM cl.date::date) = EXTRACT(month FROM CURRENT_DATE)  
                group by cl.product_id,rs.name
                order by cl.product_id limit 10
            """
        if option == 'year':
            query = """
              SELECT cl.product_id AS partner_name,max(qty_done)as price,rs.name AS partner_name
                FROM stock_move_line cl INNER JOIN product_template rs ON (cl.product_id = rs.id)
                WHERE EXTRACT(year FROM cl.date::date) = EXTRACT(year FROM CURRENT_DATE)  
                group by cl.product_id,rs.name
                order by cl.product_id limit 10
            """
        if option == 'all':
            query = """
              SELECT cl.product_id AS partner_name,max(qty_done)as price,rs.name AS partner_name
                FROM stock_move_line cl INNER JOIN product_template rs ON (cl.product_id = rs.id)
                group by cl.product_id,rs.name
                order by cl.product_id limit 10
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
    def get_selling_product(self):
        cr = self._cr

        query = """
         SELECT pp.name AS product_name,pp.list_price As list_price
            FROM product_template pp
            ORDER BY product_name DESC LIMIT 10

        """
        cr.execute(query)
        payroll_data = cr.dictfetchall()
        payroll_label = []
        payroll_dataset = []
        data_set = {}
        for data in payroll_data:
            payroll_label.append(data['product_name'])
            payroll_dataset.append(data['list_price'])
        data_set.update({"payroll_dataset":payroll_dataset})
        data_set.update({"payroll_label":payroll_label})
        return data_set

    @api.model
    def get_internal_transfer(self, option):
        cr = self._cr
        if option == 'today':
            query = """
             SELECT sp.name AS product_name,count(*) as price
                FROM stock_picking sp
                WHERE sp.scheduled_date >= current_date
                group by sp.name
                ORDER BY product_name DESC LIMIT 10
            """
        if option == 'monthly':
            query = """
             SELECT sp.name AS product_name,count(*) as price
                FROM stock_picking sp
                WHERE EXTRACT(month FROM sp.scheduled_date::date) = EXTRACT(month FROM CURRENT_DATE)  
                group by sp.name
                ORDER BY product_name DESC LIMIT 10
            """
        if option == 'year':
            query = """
             SELECT sp.name AS product_name,count(*) as price
                FROM stock_picking sp
                WHERE EXTRACT(year FROM sp.scheduled_date::date) = EXTRACT(year FROM CURRENT_DATE)  
                group by sp.name
                ORDER BY product_name DESC LIMIT 10
            """ 
        if option == 'all':
            query = """
             SELECT sp.name AS product_name,count(*) as price
                FROM stock_picking sp
                group by sp.name
                ORDER BY product_name DESC LIMIT 10
            """  
    
        cr.execute(query)
        payroll_data = cr.dictfetchall()
        payroll_label = []
        payroll_dataset = []
        data_set = {}
        for data in payroll_data:
            payroll_label.append(data['product_name'])
            payroll_dataset.append(data['price'])
        data_set.update({"payroll_dataset":payroll_dataset})
        data_set.update({"payroll_label":payroll_label})
        return data_set







    @api.model
    def get_inventory_report(self):
        cr = self._cr

        query = """
         SELECT sq.product_id AS product_name,count(*) as price, rs.name as product_name
            FROM stock_quant sq inner JOIN product_template rs ON (sq.product_id = rs.id)
            group by sq.product_id,rs.name
            order by sq.product_id limit 10


        """
                
    
        cr.execute(query)
        payroll_data = cr.dictfetchall()
        payroll_label = []
        payroll_dataset = []
        data_set = {}
        for data in payroll_data:
            payroll_label.append(data['product_name'])
            payroll_dataset.append(data['price'])
        data_set.update({"payroll_dataset":payroll_dataset})
        data_set.update({"payroll_label":payroll_label})
        return data_set



    @api.model
    def get_operations_type(self):
        cr = self._cr

        query = """
         SELECT sq.name AS product_name,count(*) as price
            FROM stock_picking_type sq 
            group by sq.name
            order by sq.name limit 10


        """
        cr.execute(query)
        payroll_data = cr.dictfetchall()
        payroll_label = []
        payroll_dataset = []
        data_set = {}
        for data in payroll_data:
            payroll_label.append(data['product_name'])
            payroll_dataset.append(data['price'])
        data_set.update({"payroll_dataset":payroll_dataset})
        data_set.update({"payroll_label":payroll_label})
        return data_set


    @api.model
    def get_delivery_order(self, option):
        cr = self._cr
        if option == 'today':
            query = """
                SELECT sq.name AS product_name,count(*) as price
                FROM stock_picking sq 
                WHERE sq.scheduled_date >= current_date
                group by sq.name
                order by sq.name desc limit 5 
            """
        if option == 'monthly':
            query = """
                SELECT sq.name AS product_name,count(*) as price
                FROM stock_picking sq 
                WHERE EXTRACT(month FROM sq.scheduled_date::date) = EXTRACT(month FROM CURRENT_DATE)  
                group by sq.name
                order by sq.name desc limit 5 
            """
        if option == 'year':
            query = """
                SELECT sq.name AS product_name,count(*) as price
                FROM stock_picking sq 
                WHERE EXTRACT(year FROM sq.scheduled_date::date) = EXTRACT(year FROM CURRENT_DATE)  
                group by sq.name
                order by sq.name desc limit 5 
            """
        if option == 'all':
            query = """
             SELECT sq.name AS product_name,count(*) as price
                FROM stock_picking sq 
                group by sq.name
                order by sq.name desc limit 5 
            """
        cr.execute(query)
        payroll_data = cr.dictfetchall()
        payroll_label = []
        payroll_dataset = []
        data_set = {}
        for data in payroll_data:
            payroll_label.append(data['product_name'])
            payroll_dataset.append(data['price'])
        data_set.update({"payroll_dataset":payroll_dataset})
        data_set.update({"payroll_label":payroll_label})
        return data_set


    @api.model
    def get_open_outwards(self):
        cr = self._cr

        query = """
          SELECT sq.product_id AS product_name,sq.reference as reference,count(*),rs.name AS product_name
            FROM stock_move sq join  product_template rs on sq.product_id =rs.id 
           WHERE sq.reference LIKE 'WH/OUT/%'
            group by sq.product_id,sq.reference,rs.name
            order by sq.product_id desc limit 5 

        """

                
    
        cr.execute(query)
        payroll_data = cr.dictfetchall()
        payroll_label = []
        payroll_dataset = []
        data_set = {}
        for data in payroll_data:
            payroll_label.append(data['product_name'])
            payroll_dataset.append(data['count'])
        data_set.update({"payroll_dataset":payroll_dataset})
        data_set.update({"payroll_label":payroll_label})
        return data_set


    @api.model
    def get_open_inwards(self):
        cr = self._cr

        query = """
         SELECT sq.product_id AS product_name,sq.reference as reference,count(*),rs.name AS product_name
            FROM stock_move sq join  product_template rs on sq.product_id =rs.id 
           WHERE sq.reference LIKE 'WH/IN/%'
            group by sq.product_id,sq.reference,rs.name
            order by sq.product_id desc limit 5 

        """

                
    
        cr.execute(query)
        payroll_data = cr.dictfetchall()
        payroll_label = []
        payroll_dataset = []
        data_set = {}
        for data in payroll_data:
            payroll_label.append(data['product_name'])
            payroll_dataset.append(data['count'])
        data_set.update({"payroll_dataset":payroll_dataset})
        data_set.update({"payroll_label":payroll_label})
        return data_set

    @api.model
    def get_stock_moves(self, option):
        cr = self._cr
        if option == 'today':
            query = """
             SELECT sq.product_id AS product_name,sq.reference as reference,count(*),rs.name AS product_name
                FROM stock_move sq join  product_template rs on sq.product_id =rs.id 
                WHERE SQ.date >= current_date
                group by sq.product_id,sq.reference,rs.name
                order by sq.product_id desc limit 10
            """
        if option == 'monthly':
            query = """
             SELECT sq.product_id AS product_name,sq.reference as reference,count(*),rs.name AS product_name
                FROM stock_move sq join  product_template rs on sq.product_id =rs.id 
                WHERE EXTRACT(month FROM sq.date::date) = EXTRACT(month FROM CURRENT_DATE)  
                group by sq.product_id,sq.reference,rs.name
                order by sq.product_id desc limit 10
            """
        if option == 'year':
            query = """
             SELECT sq.product_id AS product_name,sq.reference as reference,count(*),rs.name AS product_name
                FROM stock_move sq join  product_template rs on sq.product_id =rs.id 
                WHERE EXTRACT(year FROM sq.date::date) = EXTRACT(year FROM CURRENT_DATE)  
                group by sq.product_id,sq.reference,rs.name
                order by sq.product_id desc limit 10
            """ 
        if option == 'all':
            query = """
             SELECT sq.product_id AS product_name,sq.reference as reference,count(*),rs.name AS product_name
                FROM stock_move sq join  product_template rs on sq.product_id =rs.id 
                group by sq.product_id,sq.reference,rs.name
                order by sq.product_id desc limit 10
            """    
    
        cr.execute(query)
        payroll_data = cr.dictfetchall()
        payroll_label = []
        payroll_dataset = []
        data_set = {}
        for data in payroll_data:
            payroll_label.append(data['product_name'])
            payroll_dataset.append(data['count'])
        data_set.update({"payroll_dataset":payroll_dataset})
        data_set.update({"payroll_label":payroll_label})
        return data_set


    @api.model
    def get_reserved_stock(self):
        cr = self._cr

        query = """
         SELECT sq.product_id AS product_name,sq.qty_done as reference,count(*),rs.name AS product_name
            FROM stock_move_line sq join  product_template rs on sq.product_id =rs.id 
            group by sq.product_id,sq.qty_done,rs.name
            order by sq.product_id desc limit 10

        """
            
        cr.execute(query)
        payroll_data = cr.dictfetchall()
        payroll_label = []
        payroll_dataset = []
        data_set = {}
        for data in payroll_data:
            payroll_label.append(data['product_name'])
            payroll_dataset.append(data['count'])
        data_set.update({"payroll_dataset":payroll_dataset})
        data_set.update({"payroll_label":payroll_label})
        return data_set