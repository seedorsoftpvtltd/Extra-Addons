# -*- coding: utf-8 -*-
#################################################################################
# Author      : Acespritech Solutions Pvt. Ltd. (<www.acespritech.com>)
# Copyright(c): 2012-Present Acespritech Solutions Pvt. Ltd.
# All Rights Reserved.
#
# This program is copyright property of the author mentioned above.
# You can`t redistribute it and/or modify it.
#
#################################################################################

from odoo import models, fields, api, _
from datetime import datetime, date, time, timedelta
from dateutil.relativedelta import relativedelta
from pytz import timezone
import pytz

def start_end_date_global(start, end, tz):
    tz = pytz.timezone(tz) or 'UTC'
    current_time = datetime.now(tz)
    hour_tz = int(str(current_time)[-5:][:2])
    min_tz = int(str(current_time)[-5:][3:])
    sign = str(current_time)[-6][:1]
    sdate = start + " 00:00:00"
    edate = end + " 23:59:59"
    if sign == '-':
        start_date = (datetime.strptime(sdate, '%Y-%m-%d %H:%M:%S') + timedelta(hours=hour_tz,
                                                                                minutes=min_tz)).strftime(
            "%Y-%m-%d %H:%M:%S")
        end_date = (datetime.strptime(edate, '%Y-%m-%d %H:%M:%S') + timedelta(hours=hour_tz,
                                                                              minutes=min_tz)).strftime(
            "%Y-%m-%d %H:%M:%S")
    if sign == '+':
        start_date = (datetime.strptime(sdate, '%Y-%m-%d %H:%M:%S') - timedelta(hours=hour_tz,
                                                                                minutes=min_tz)).strftime(
            "%Y-%m-%d %H:%M:%S")
        end_date = (datetime.strptime(edate, '%Y-%m-%d %H:%M:%S') - timedelta(hours=hour_tz,
                                                                              minutes=min_tz)).strftime(
            "%Y-%m-%d %H:%M:%S")
    return start_date, end_date

class posSessions(models.Model):
    _inherit = "pos.session"

    def get_pos_name(self):
        if self and self.config_id:
            return self.config_id.name

    def get_current_date_x(self):
        if self._context and self._context.get('tz'):
            tz = self._context['tz']
            tz = timezone(tz)
        else:
            tz = pytz.utc
        if tz:
#             tz = timezone(tz)
            c_time = datetime.now(tz)
            return c_time.strftime('%d/%m/%Y')
        else:
            return date.today().strftime('%d/%m/%Y')

    def get_current_time_x(self):
        if self._context and self._context.get('tz'):
            tz = self._context['tz']
            tz = timezone(tz)
        else:
            tz = pytz.utc
        if tz:
#             tz = timezone(tz)
            c_time = datetime.now(tz)
            return c_time.strftime('%I:%M %p')
        else:
            return datetime.now().strftime('%I:%M:%S %p')

    def get_inventory_details(self):
        product_category = self.env['product.category'].search([])
        product_product = self.env['product.product']
        stock_location = self.config_id.stock_location_id;
        inventory_records = []
        final_list = []
        product_details = []
        if self and self.id:
            for order in self.order_ids:
                for line in order.lines:
                    product_details.append({
                        'id': line.product_id.id,
                        'qty': line.qty,
                    })
        custom_list = []
        for each_prod in product_details:
            if each_prod.get('id') not in [x.get('id') for x in custom_list]:
                custom_list.append(each_prod)
            else:
                for each in custom_list:
                    if each.get('id') == each_prod.get('id'):
                        each.update({'qty': each.get('qty') + each_prod.get('qty')})
        for each in custom_list:
            product_id = product_product.browse(each.get('id'))
            if product_id:
                inventory_records.append({
                    'product_id': [product_id.id, product_id.name],
                    'category_id': [product_id.id, product_id.categ_id.name],
                    'used_qty': each.get('qty'),
                    'quantity': product_id.with_context(
                        {'location': stock_location.id, 'compute_child': False}).qty_available,
                    'uom_name': product_id.uom_id.name or ''
                })
            if inventory_records:
                temp_list = []
                temp_obj = []
                for each in inventory_records:
                    if each.get('product_id')[0] not in temp_list:
                        temp_list.append(each.get('product_id')[0])
                        temp_obj.append(each)
                    else:
                        for rec in temp_obj:
                            if rec.get('product_id')[0] == each.get('product_id')[0]:
                                qty = rec.get('quantity') + each.get('quantity')
                                rec.update({'quantity': qty})
                final_list = sorted(temp_obj, key=lambda k: k['quantity'])
        return final_list or []
    
    @api.model
    def payment_by_journal_pie_chart(self, company_id):
        domain = []
        if company_id:
            domain += [('company_id', '=', int(company_id))]
        else:
            domain += [('company_id', '=', self.env.user.company_id.id)]

        pos_ids = self.env['pos.order'].search(domain).ids

        SQL = ""
        if len(pos_ids) > 1:
            SQL = "absl.pos_statement_id IN  %s" % str(tuple(pos_ids))
        else:
            if len(pos_ids) > 0:
                SQL = "absl.pos_statement_id =  %s" % pos_ids[0]
        if len(pos_ids) > 0:
            sql_query = """SELECT SUM(amount) AS amount, aj.name AS journal
                            FROM account_bank_statement_line AS absl
                            INNER JOIN account_bank_statement AS abs ON abs.id = absl.statement_id
                            INNER JOIN account_journal AS aj ON aj.id = abs.journal_id
                            WHERE %s
                            GROUP BY journal
                            """ % str(SQL)
            self._cr.execute(sql_query)
            journal_data = self._cr.dictfetchall()
            return journal_data

    @api.model
    def get_journal_line_chart_data(self, start_date, end_date, journal, company_id):
        current_time_zone = self.env.user.tz or 'UTC'
        s_date, e_date = start_end_date_global(start_date, end_date, current_time_zone)
        if company_id:
            pass
        else:
            company_id = self.env.user.company_id.id

        flag = False
        sql = ""
        if journal:
            sql = "AND aj.id = " + str(journal)
            flag_val = False
        else:
            sql = ""
            flag_val = True

        sql_query = """SELECT
                         SUM(amount) AS amount, extract(day from po.date_order AT TIME ZONE 'UTC' AT TIME ZONE '%s') AS time_duration,
                         aj.name AS journal, aj.id
                         FROM account_bank_statement_line AS absl
                         INNER JOIN account_bank_statement AS abs ON abs.id = absl.statement_id
                         INNER JOIN account_journal AS aj ON aj.id = abs.journal_id
                         INNER JOIN pos_order AS po ON po.id = absl.pos_statement_id
                         WHERE po.date_order >= '%s'
                         AND po.date_order <= '%s' %s
                         AND po.company_id = %s
                         GROUP BY time_duration, journal, aj.id ORDER BY extract(day from po.date_order AT TIME ZONE 'UTC' AT TIME ZONE '%s') ASC
                     """ % (current_time_zone, s_date, e_date, sql, company_id, current_time_zone)
        self._cr.execute(sql_query)
        month_data = self._cr.dictfetchall()
        

        option_list = [{'journal': i.get('journal'), 'id': i.get('id')} for i in month_data]
        
        option_final_list = [dict(tupleized) for tupleized in set(tuple(item.items()) for item in option_list)]
        

        final_list = []
        for i in month_data:
            if not final_list:
                s = i.get('journal')
                final_list.append({'Date': i.get('time_duration'),
                                   i.get('journal').replace(" ", "_"): i.get('amount')})
            else:
                flag = False
                for f_list in final_list:
                    if f_list.get('Date') == i.get('time_duration'):
                        f_list.update({i.get('journal').replace(" ", "_"): i.get('amount')})
                        flag = True
                if not flag:
                    final_list.append({'Date': i.get('time_duration'),
                                       i.get('journal').replace(" ", "_"): i.get('amount')})

        payment_name_list = []
        for l in final_list:
            payment_name_list += l.keys()
        payment_name_dict = dict([(i, 0) for i in set(payment_name_list)])
        for l in final_list:
            for p in payment_name_dict:
                if p not in l.keys():
                    l.update({p: 0.0})
        day_date_lst = [l.get('Date') for l in final_list]
        current_month_day_lst = [float(i) for i in range(1, int(datetime.today().day) + 1)]
        for j in list(set(current_month_day_lst) - set(day_date_lst)):
            payment_name_dict = dict([(i, 0) for i in set(payment_name_list)])
            payment_name_dict.update({'Date': j})
            final_list.append(payment_name_dict)
        return {'data': sorted(final_list, key=lambda i: i['Date']), 'journal': option_final_list, 'flag': flag_val}

    @api.model
    def getActiveSession(self, start_date, end_date, company_id):
        if company_id:
            pass
        else:
            company_id = self.env.user.company_id.id
        current_time_zone = self.env.user.tz or 'UTC'
        s_date, e_date = start_end_date_global(start_date, end_date, current_time_zone)
        today_sales_sql = """SELECT 
                                SUM(pol.price_subtotal_incl) AS today_sales,
                                SUM (pol.qty) AS today_product
                                FROM pos_order as po
                                INNER JOIN pos_order_line AS pol ON po.id = pol.order_id
                                WHERE po.date_order >= '%s' 
                                AND po.date_order <= '%s' 
                                AND po.company_id = %s
                            """ % (s_date, e_date, company_id)
        
        self._cr.execute(today_sales_sql)
        today_sales_data = self._cr.dictfetchall()

        today_order_sql = """SELECT COUNT(id) AS today_order
                                FROM pos_order
                                WHERE date_order >= '%s' 
                                AND date_order <= '%s' 
                                AND company_id = %s
                            """ % (s_date, e_date, company_id)
        self._cr.execute(today_order_sql)
        today_order_data = self._cr.dictfetchall()

        SQL = """SELECT COUNT(*) AS session
                    FROM pos_session AS ps
                    LEFT JOIN pos_config AS pc ON pc.id = ps.config_id
                    WHERE ps.state = 'opened' AND pc.company_id = %s
                """ % (company_id)
        self._cr.execute(SQL)
        active_session = self._cr.dictfetchall()
        sale_data = self.get_total_sale_data_tiles(company_id)
        product_sold = self.convert_number(sale_data.get('product_count') if sale_data else 0)
        order_count = self.convert_number(sale_data.get('order_count') if sale_data else 0)
        total_amount = self.convert_number(sale_data.get('total_amount') if sale_data else 0)
        today_sales = self.convert_number(today_sales_data[0].get('today_sales') or 0)
        today_order = self.convert_number(today_order_data[0].get('today_order' or 0))
        today_product = self.convert_number(today_sales_data[0].get('today_product') or 0)

        return {'session': active_session[0]['session'] or 0,
                'order': order_count or 0,
                'total_sale': total_amount or 0,
                'product_sold': product_sold or 0,
                'currency': self.env.user.currency_id.symbol,
                'today_sales': today_sales or 0,
                'today_order': today_order or 0,
                'today_product': today_product or 0,
                'login_user' : self.env.user.name,
                'login_user_img' : self.env.user.image_1920
                }
    @api.model
    def getCompany(self):
        return {'company': [{'id': alw_cmp.id, 'company': alw_cmp.name} for alw_cmp in self.env.user.company_ids],
                'company_id': self.env.user.company_id.id}

    @api.model
    def get_total_sale_data_tiles(self, company_id):
        if company_id:
            pass
        else:
            company_id = self.env.user.company_id.id
        query = """SELECT COUNT(order_detail.ord) AS order_count,
                    SUM(order_detail.prod) AS product_count,
                    SUM(order_detail.amount) AS total_amount
                    FROM 
                    (SELECT SUM(posl.qty) AS prod,
                        SUM(posl.price_subtotal_incl) AS amount,
                        posl.order_id AS ord
                        FROM pos_order_line AS posl
                        WHERE posl.company_id = %s
                        GROUP BY ord) AS order_detail;
                """ % company_id
        self._cr.execute(query)
        total_sale_data_query = self._cr.dictfetchall()
        return total_sale_data_query[0] if total_sale_data_query else 0

    def convert_number(self, number):
        if number:
            if number < 1000:
                return number
            if number >= 1000 and number < 1000000:
                total = number / 1000
                return str("%.2f" % total) + 'K'
            if number >= 1000000:
                total = number / 1000000
                return str("%.2f" % total) + 'M'
        else:
            return 0

    @api.model
    def get_session_report(self):
        try:
#             sql query for get "In Progress" session
            self._cr.execute("""
                select ps.id,pc.name, ps.name from pos_session ps
                left join pos_config pc on (ps.config_id = pc.id)
                where ps.state='opened'
            """)
            session_detail = self._cr.fetchall()
#
            self._cr.execute("""
                SELECT pc.name, ps.name, sum(absl.amount) FROM pos_session ps
                JOIN pos_config pc on (ps.config_id = pc.id)
                JOIN account_bank_statement_line absl on (ps.name = absl.ref)
                WHERE ps.state='opened'
                GROUP BY ps.id, pc.name;
            """)
            session_total = self._cr.fetchall()
    
#             sql query for get payments total of "In Progress" session
            lst = []
            for pay_id in session_detail:
                self._cr.execute("""
                    select pc.name, aj.name, abs.total_entry_encoding from account_bank_statement abs
                    join pos_session ps on abs.pos_session_id = ps.id
                    join pos_config pc on ps.config_id = pc.id
                    join account_journal aj on  abs.journal_id = aj.id
                    where pos_session_id=%s
                """%pay_id[0])
                bank_detail = self._cr.fetchall()
                for i in bank_detail:
                    if i[2] != None:
                        lst.append({'session_name':i[0],'journals':i[1],'total':i[2]})

            cate_lst = []
            for cate_id in session_detail:
                self._cr.execute("""
                    select pc.name, sum(pol.price_unit), poc.name from pos_category pc
                    join product_template pt on pc.id = pt.pos_categ_id
                    join product_product pp on pt.id = pp.product_tmpl_id
                    join pos_order_line pol on pp.id = pol.product_id
                    join pos_order po on pol.order_id = po.id
                    join pos_session ps on ps.id = po.session_id
                    join pos_config poc ON ps.config_id = poc.id
                    where po.session_id = %s
                    group by pc.name, poc.name
                """%cate_id[0])
                cate_detail = self._cr.fetchall()
                for j in cate_detail:
                    cate_lst.append({'cate_name':j[0],'cate_total':j[1],'session_name':j[2]})
            categ_null = []
            for cate_id_null in session_detail:
                self._cr.execute(""" 
                    select sum(pol.price_unit), poc.name from pos_order_line pol
                    join pos_order po on po.id = pol.order_id
                    join product_product pp on pp.id = pol.product_id
                    join product_template pt on pt.id = pp.product_tmpl_id
                    join pos_session ps on ps.id = po.session_id
                    join pos_config poc on ps.config_id = poc.id
                    where po.session_id = %s and pt.pos_categ_id is null
                    group by poc.name
                """%cate_id_null[0])
                categ_null_detail = self._cr.fetchall()
                for k in categ_null_detail:
                    categ_null.append({'cate_name':'Undefined Category','cate_total':k[0],'session_name':k[1]})
            all_cat = []
            for sess in session_total:
                def_cate_lst = []
                for j in cate_lst:
                    if j['session_name'] == sess[0]:
                        def_cate_lst.append(j)
                for k in categ_null:
                    if k['session_name'] == sess[0]:
                        def_cate_lst.append(k)
                all_cat.append(def_cate_lst)
            return {'session_total':session_total,'payment_lst':lst,'all_cat':all_cat}
        except Exception as e:
            return {'error':'Error Function Working'}