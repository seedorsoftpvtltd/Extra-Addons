# -*- coding: utf-8 -*-

from odoo import models, fields, api, tools, _
import pytz
from datetime import datetime, date, time, timedelta
from dateutil.relativedelta import relativedelta
from operator import itemgetter
from timeit import itertools
import calendar
from calendar import month

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

class pos_order(models.Model):
    _inherit = 'pos.order'

    @api.model
    def get_dashboard_data(self):
        company_id = self.env['res.users'].browse([self._uid]).company_id.id
        res_pos_order = {'total_sales':0,'total_orders':0}
        active_sessions = self.env['pos.session'].search([('state','=','opened')]).ids
        closed_sessions = self.env['pos.session'].search([('stop_at', '>=', fields.Date.today().strftime('%Y/%m/%d') + " 00:00:00"),
                                                          ('stop_at', '<=', fields.Date.today().strftime('%Y/%m/%d') + " 23:59:59"),
                                                          ('state','in',['closing_control','closed'])]).ids
        res_pos_order['closed_sessions'] = len(closed_sessions)
        res_pos_order['active_sessions'] = len(active_sessions)
        pos_ids = self.search([('company_id', '=', company_id)])
        if pos_ids:
            total_sales = 0;
            existing_partner_sale = 0
            new_partner_sale = 0
            without_partner_sale = 0
            for pos_id in pos_ids:
                total_sales += pos_id.amount_total
                if pos_id.partner_id:
                    orders = self.search([('partner_id','=',pos_id.partner_id.id),
                                        ('company_id', '=', company_id),
                                        ('date_order', '>=', fields.Date.today().strftime('%Y/%m/%d') + " 00:00:00"),
                                        ('date_order', '<=', fields.Date.today().strftime('%Y/%m/%d') + " 23:59:59"),])
                    if orders and len(orders) > 1:
                        existing_partner_sale += pos_id.amount_total
                    else:
                        new_partner_sale += pos_id.amount_total
                else:
                    orders = self.search([('partner_id','=',False),
                                        ('company_id', '=', company_id),
                                        ('date_order', '>=', fields.Date.today().strftime('%Y/%m/%d') + " 00:00:00"),
                                        ('date_order', '<=', fields.Date.today().strftime('%Y/%m/%d') + " 23:59:59")])

                    if orders and len(orders) > 1:
                        without_partner_sale += pos_id.amount_total
            res_pos_order['client_based_sale'] = {'new_client_sale' : new_partner_sale,'existing_client_sale':existing_partner_sale,'without_client_sale':without_partner_sale}
            res_pos_order['total_sales'] = total_sales
            res_pos_order['total_orders'] = len(pos_ids)
            current_time_zone = self.env.user.tz or 'UTC'
#             orders = []
            if self.env.user.tz:
                tz = pytz.timezone(self.env.user.tz)
            else:
                tz = pytz.utc
            c_time = datetime.now(tz)
            hour_tz = int(str(c_time)[-5:][:2])
            min_tz = int(str(c_time)[-5:][3:])
            sign = str(c_time)[-6][:1]
            sdate = c_time.strftime("%Y-%m-%d 00:00:00")
            edate = c_time.strftime("%Y-%m-%d 23:59:59")
            if sign == '-':
                start_date = (datetime.strptime(sdate, '%Y-%m-%d %H:%M:%S') + timedelta(hours=hour_tz, minutes=min_tz)).strftime("%Y-%m-%d %H:%M:%S")
                end_date = (datetime.strptime(edate, '%Y-%m-%d %H:%M:%S') + timedelta(hours=hour_tz, minutes=min_tz)).strftime("%Y-%m-%d %H:%M:%S")
            if sign == '+':
                start_date = (datetime.strptime(sdate, '%Y-%m-%d %H:%M:%S') - timedelta(hours=hour_tz, minutes=min_tz)).strftime("%Y-%m-%d %H:%M:%S")
                end_date = (datetime.strptime(edate, '%Y-%m-%d %H:%M:%S') - timedelta(hours=hour_tz, minutes=min_tz)).strftime("%Y-%m-%d %H:%M:%S")
            self._cr.execute("""SELECT extract(hour from po.date_order AT TIME ZONE 'UTC' AT TIME ZONE '%s') AS date_order_hour,
                                       SUM((pol.qty * pol.price_unit) * (100 - pol.discount) / 100) AS price_total
                            FROM pos_order_line AS pol
                            LEFT JOIN pos_order po ON (po.id=pol.order_id)
                            WHERE po.date_order >= '%s'
                              AND po.date_order <= '%s'
                            GROUP BY  extract(hour from po.date_order AT TIME ZONE 'UTC' AT TIME ZONE '%s');
                            """ % (current_time_zone, start_date, end_date, current_time_zone))
            result_data_hour = self._cr.dictfetchall()
            hour_lst = [hrs for hrs in range(0,24)]
            for each in result_data_hour:
                if each['date_order_hour'] != 23:
                    each['date_order_hour'] = [each['date_order_hour'],each['date_order_hour'] + 1]
                else:
                    each['date_order_hour'] = [each['date_order_hour'],0]
                hour_lst.remove(int(each['date_order_hour'][0]))
            for hrs in hour_lst:
                hr = []
                if hrs != 23:
                    hr += [hrs, hrs+1]
                else:
                    hr += [hrs, 0]
                result_data_hour.append({'date_order_hour': hr, 'price_total': 0.0})
            sorted_hour_data = sorted(result_data_hour, key=lambda l: l['date_order_hour'][0])
            res_pos_order['sales_based_on_hours'] = sorted_hour_data
            # this month data
        res_curr_month = self.pos_order_month_based(1)
        res_pos_order ['current_month'] = res_curr_month
#             Last 6 month data
        last_6_month_res = self.pos_order_month_based(12)
        res_pos_order ['last_6_month_res'] = last_6_month_res
        return res_pos_order

    def pos_order_month_based(self,month_count):
        tz = pytz.utc
        c_time = datetime.now(tz)
        hour_tz = int(str(c_time)[-5:][:2])
        min_tz = int(str(c_time)[-5:][3:])
        sign = str(c_time)[-6][:1]
        current_time_zone = self.env.user.tz or 'UTC'
        stdate = c_time.strftime("%Y-%m-01 00:00:00")
        eddate = (c_time + relativedelta(day=1, months=+month_count, days=-1)).strftime("%Y-%m-%d 23:59:59")
        # this month data 
        if sign == '-':
            mon_stdate = (datetime.strptime(stdate, '%Y-%m-%d %H:%M:%S') + timedelta(hours=hour_tz, minutes=min_tz)).strftime("%Y-%m-%d %H:%M:%S")
            mon_eddate = (datetime.strptime(eddate, '%Y-%m-%d %H:%M:%S') + timedelta(hours=hour_tz, minutes=min_tz)).strftime("%Y-%m-%d %H:%M:%S")
        if sign == '+':
            mon_stdate = (datetime.strptime(stdate, '%Y-%m-%d %H:%M:%S') - timedelta(hours=hour_tz, minutes=min_tz)).strftime("%Y-%m-%d %H:%M:%S")
            mon_eddate = (datetime.strptime(eddate, '%Y-%m-%d %H:%M:%S') - timedelta(hours=hour_tz, minutes=min_tz)).strftime("%Y-%m-%d %H:%M:%S")
        if month_count == 12:
            self._cr.execute("""SELECT extract(month from po.date_order AT TIME ZONE 'UTC' AT TIME ZONE '%s') AS date_order_month,
                                   SUM((pol.qty * pol.price_unit) * (100 - pol.discount) / 100) AS price_total
                        FROM pos_order_line AS pol
                        LEFT JOIN pos_order po ON (po.id=pol.order_id)
                        WHERE po.date_order >= '%s'
                          AND po.date_order <= '%s'
                        GROUP BY extract(month from po.date_order AT TIME ZONE 'UTC' AT TIME ZONE '%s');
                        """ % (current_time_zone, mon_stdate, mon_eddate, current_time_zone))
        else:
            self._cr.execute("""SELECT extract(day from po.date_order AT TIME ZONE 'UTC' AT TIME ZONE '%s') AS date_order_day,
                                        extract(month from po.date_order AT TIME ZONE 'UTC' AT TIME ZONE '%s') AS date_order_month,
                                       SUM((pol.qty * pol.price_unit) * (100 - pol.discount) / 100) AS price_total
                            FROM pos_order_line AS pol
                            LEFT JOIN pos_order po ON (po.id=pol.order_id)
                            WHERE po.date_order >= '%s'
                              AND po.date_order <= '%s'
                            GROUP BY  extract(day from po.date_order AT TIME ZONE 'UTC' AT TIME ZONE '%s'),
                                extract(month from po.date_order AT TIME ZONE 'UTC' AT TIME ZONE '%s')
                                ORDER BY extract(day from po.date_order AT TIME ZONE 'UTC' AT TIME ZONE '%s') DESC;
                            """ % (current_time_zone,current_time_zone, mon_stdate, mon_eddate, current_time_zone,current_time_zone,current_time_zone))
        result_this_month = self._cr.dictfetchall()
        return result_this_month

    @api.model
    def graph_date_on_canvas(self,start_date,end_date):
        data = {}
        company_id = self.env['res.users'].browse([self._uid]).company_id.id
        domain = [('company_id', '=', company_id)]
        if start_date:
            domain += [('date_order', '>=', start_date)]
        else:
            domain += [('date_order', '>=', str(fields.Date.today()) + " 00:00:00")]
        if end_date:
            domain += [('date_order', '<=', end_date)]
        else:
            domain += [('date_order', '<=', str(fields.Date.today()) + " 23:59:59")]
        pos_ids = self.search(domain)
        if pos_ids:
            self._cr.execute("""select aj.name, aj.id, sum(amount)
                                from account_bank_statement_line as absl,
                                     account_bank_statement as abs,
                                     account_journal as aj 
                                where absl.statement_id = abs.id
                                      and abs.journal_id = aj.id 
                                     and absl.pos_statement_id IN %s
                                group by aj.name, aj.id """ % "(%s)" % ','.join(map(str, pos_ids.ids)))
            data = self._cr.dictfetchall()
        total = 0.0
        for each in data:
           total += each['sum']
        for each in data:
           each['per'] = (each['sum'] * 100) / total
        return data

    @api.model
    def graph_best_product(self,start_date,end_date):
        data = {}
        company_id = self.env['res.users'].browse([self._uid]).company_id.id
        domain = [('company_id', '=', company_id)]
        if start_date:
            domain += [('date_order', '>=', start_date)]
        else:
            domain += [('date_order', '>=', fields.Date.today().strftime('%m/%d/%Y') + " 00:00:00")]
        if end_date:
            domain += [('date_order', '<=', end_date)]
        else:
            domain += [('date_order', '<=', fields.Date.today().strftime('%m/%d/%Y') + " 23:59:59")]
        pos_ids = self.search(domain)
        if pos_ids:
            order_ids = []
            for pos_id in pos_ids:
                order_ids.append(pos_id.id)
            self._cr.execute("""
                SELECT pt.name, sum(psl.qty), SUM((psl.qty * psl.price_unit) * (100 - psl.discount) / 100) AS price_total FROM pos_order_line AS psl
                JOIN pos_order AS po ON (po.id = psl.order_id)
                JOIN product_product AS pp ON (psl.product_id = pp.id)
                JOIN product_template AS pt ON (pt.id = pp.product_tmpl_id)
                where po.id IN %s
                GROUP BY pt.name
                ORDER BY sum(psl.qty) DESC limit 50;
                """ % "(%s)" % ','.join(map(str, pos_ids.ids)))
            data = self._cr.dictfetchall()
        return data

    @api.model
    def orders_by_salesperson(self,start_date,end_date):
        data = {}
        company_id = self.env['res.users'].browse([self._uid]).company_id.id
        domain = [('company_id', '=', company_id)]
        if start_date:
            domain += [('date_order', '>=', start_date)]
        else:
            domain += [('date_order', '>=', fields.Date.today().strftime('%m/%d/%Y') + " 00:00:00")]
        if end_date:
            domain += [('date_order', '<=', end_date)]
        else:
            domain += [('date_order', '<=', fields.Date.today().strftime('%m/%d/%Y') + " 23:59:59")]
        pos_ids = self.search(domain)
        if pos_ids:
            order_ids = []
            for pos_id in pos_ids:
                order_ids.append(pos_id.id)
            self._cr.execute("""
                SELECT po.user_id, count(DISTINCT(po.id)) As total_orders, SUM((psl.qty * psl.price_unit) * (100 - psl.discount) / 100) AS price_total FROM pos_order_line AS psl
                JOIN pos_order AS po ON (po.id = psl.order_id)
                where po.id IN %s
                GROUP BY po.user_id
                ORDER BY count(DISTINCT(po.id)) DESC;
                """ % "(%s)" % ','.join(map(str, pos_ids.ids)))
            data = self._cr.dictfetchall()
        return data

    @api.model
    def session_details_on_canvas(self):
        data = {}
        domain_active_session = []
        close_session_list = []
        active_session_list = []
        company_id = self.env['res.users'].browse([self._uid]).company_id.id
        domain = [('company_id', '=', company_id),
                  ('date_order', '>=', fields.Date.today().strftime('%Y/%m/%d') + " 00:00:00"),
                  ('date_order', '<=', fields.Date.today().strftime('%Y/%m/%d') + " 23:59:59")]
        domain_active_session += domain
        domain_active_session += [('state','=','paid')]
        domain += [('state','=','done')]
        active_pos_ids = self.search(domain_active_session)
        posted_pos_ids = self.search(domain)
        if active_pos_ids:
            self._cr.execute("""select aj.name, aj.id, sum(amount),abs.pos_session_id
                                from account_bank_statement_line as absl,
                                     account_bank_statement as abs,
                                     account_journal as aj 
                                where absl.statement_id = abs.id
                                      and abs.journal_id = aj.id 
                                     and absl.pos_statement_id IN %s
                                group by aj.name, abs.pos_session_id, aj.id """ % "(%s)" % ','.join(map(str, active_pos_ids.ids)))
            active_session_data = self._cr.dictfetchall()
            session_group = {}
            sort_group = sorted(active_session_data, key=itemgetter('pos_session_id'))
            for key, value in itertools.groupby(sort_group, key=itemgetter('pos_session_id')):
                if key not in session_group:
                    session_group.update({key:[x for x in value]})
                else:
                    session_group[key] = [x for x in value]
            for k, v in session_group.items():
                total_sum = 0
                for each in v:
                    total_sum += float(each['sum'])
                active_session_list.append({'pos_session_id' : self.env['pos.session'].browse(k).read(), 'sum' : total_sum})
        if posted_pos_ids:
            self._cr.execute("""select aj.name, aj.id, sum(amount),abs.pos_session_id
                                from account_bank_statement_line as absl,
                                     account_bank_statement as abs,
                                     account_journal as aj 
                                where absl.statement_id = abs.id
                                      and abs.journal_id = aj.id 
                                     and absl.pos_statement_id IN %s
                                group by aj.name, abs.pos_session_id, aj.id """ % "(%s)" % ','.join(map(str, posted_pos_ids.ids)))

            posted_session_data = self._cr.dictfetchall()
            session_group = {}
            sort_group = sorted(posted_session_data, key=itemgetter('pos_session_id'))
            for key, value in itertools.groupby(sort_group, key=itemgetter('pos_session_id')):
                if key not in session_group:
                    session_group.update({key:[x for x in value]})
                else:
                    session_group[key] = [x for x in value]
            for k, v in session_group.items():
                total_sum = 0
                for each in v:
                    total_sum += float(each['sum'])
                close_session_list.append({'pos_session_id' : self.env['pos.session'].browse(k).read(), 'sum' : total_sum})
        return {'close_session': close_session_list, 'active_session': active_session_list}


    @api.model
    def employee_work_hour(self, start, end, company_id):
        current_time_zone = self.env.user.tz or 'UTC'
        s_date, e_date = start_end_date_global(start, end, current_time_zone)
        if company_id:
            pass
        else:
            company_id = self.env.user.company_id.id
        query = """SELECT p.id AS eid, SUM(ha.worked_hours) AS total_time
                    FROM hr_attendance AS ha
                    INNER JOIN hr_employee AS p ON ha.employee_id = p.id
                    WHERE
                    ha.check_out > '%s'
                    AND ha.check_out <= '%s'
                    AND p.company_id = % s
                    GROUP BY eid;
                """ % (s_date, e_date, company_id)
        self._cr.execute(query)
        result = self._cr.dictfetchall()
        for each in result:
            each['total_time'] = int(each['total_time'])
            each['ename'] = self.env['hr.employee'].browse([int(each['eid'])]).name
            each['eimage'] = self.env['hr.employee'].browse([int(each['eid'])]).image
        return result

    @api.model
    def sales_data_per_salesperson(self, start, end, company_id):
        current_time_zone = self.env.user.tz or 'UTC'
        s_date, e_date = start_end_date_global(start, end, current_time_zone)
        t_start_date, t_end_date = start_end_date_global(str(date.today()), str(date.today()), current_time_zone)
        if company_id:
            pass
        else:
            company_id = self.env.user.company_id.id
        top_sale_person_weekly = self.staff_sale_info(s_date, e_date, company_id, '')
        top_sale_person_today = self.staff_sale_info(t_start_date, t_end_date, company_id, 1)
        query = """SELECT ord.person_id As person_id ,count(ord.order_name) AS num_order, sum(ord.amount) AS amount FROM
                    (SELECT pos.user_id AS person_id, posl.order_id As order_name, 
                    SUM(posl.price_subtotal_incl) as amount
                    FROM pos_order_line AS posl
                    LEFT JOIN pos_order AS pos ON pos.id = posl.order_id
                    WHERE pos.company_id = %s
                    AND pos.date_order >= '%s'
                    AND pos.date_order <= '%s'
                    GROUP BY order_name, person_id) AS ord
                    GROUP BY person_id
                    ORDER BY amount DESC
            """ % (company_id, s_date, e_date)
        self._cr.execute(query)
        sale_per_salesperson = self._cr.dictfetchall()
        top_staff = {'top_staff': 'No data found', 'amount': 0.0}
        if top_sale_person_today:
            top_staff.update({'amount': top_sale_person_today[0].get('amount') or 0.0,
                              'top_staff': self.env['res.users'].browse(
                                  top_sale_person_today[0].get('person_id')).display_name})

        if len(sale_per_salesperson) > 0:
            for each in sale_per_salesperson:
                user_id = self.env['res.users'].browse([each['person_id']])
                each['person_name'] = user_id.display_name
                each['person_image'] = user_id.image_1920
            return {'salesperson_data': sale_per_salesperson, 'top_staff': top_staff,
                    'currency': self.env.user.currency_id.symbol}

    @api.model
    def weekly_gross_sales_data(self, start, end, company_id):
        current_time_zone = self.env.user.tz or 'UTC'
        start_date,end_date = start_end_date_global(start, end, current_time_zone)
        sql_query = """SELECT extract(day from date_order AT TIME ZONE 'UTC' AT TIME ZONE '%s') AS day_name,
                        to_char(date_order AT TIME ZONE 'UTC' AT TIME ZONE '%s','DY') AS day,
                        SUM(amount_total) AS sale_total
                        FROM pos_order AS pos
                        WHERE
                        date_order >= '%s'
                        AND date_order <= '%s'
                        AND company_id = %s
                        GROUP BY day_name, day;
                """ % (current_time_zone, current_time_zone, start_date, end_date, company_id)

        self._cr.execute(sql_query)
        return {'week_data': self._cr.dictfetchall()}

    @api.model
    def weekly_gross_sales(self, current_week_start_date, current_week_end_date, last_week_start_date,
                           last_week_end_date, company_id):
        if company_id:
            pass
        else:
            company_id = self.env.user.company_id.id
        current_week = self.weekly_gross_sales_data(current_week_start_date, current_week_end_date, company_id)
        last_week = self.weekly_gross_sales_data(last_week_start_date, last_week_end_date, company_id)
        final_dict = {}
        final_list = []
        for each in current_week['week_data']:
            final_dict[each['day']] = {'current_week': each.get('sale_total') or 0, 'last_week': 0}
        for each in last_week['week_data']:
            if each.get('day') in final_dict:
                final_dict[each['day']].update({'last_week': each.get('sale_total') or 0})
            else:
                final_dict[each['day']] = {'current_week': 0, 'last_week': each.get('sale_total') or 0}
        for key, val in final_dict.items():
            final_list.append({'day': key, 'current_week': val.get('current_week'), 'last_week': val.get('last_week')})
        final_data_list = []
        days = ['SUN', 'MON', 'TUE', 'WED', 'THU', 'FRI', 'SAT']

        for each_day in days:
            this_week = 0.0
            last_week = 0.0
            for each in final_list:
                if each_day == each.get('day'):
                    this_week = each.get('current_week')
                    last_week = each.get('last_week')
            final_data_list.append({'day': each_day, 'current_week': this_week or 0.0, 'last_week': last_week or 0.0})
        return {'weekly_compare_sales': final_data_list}

    @api.model
    def top_items_by_sales(self, start, end, company_id):
        if company_id:
            pass
        else:
            company_id = self.env.user.company_id.id
        current_time_zone = self.env.user.tz or 'UTC'
        s_date, e_date = start_end_date_global(start, end, current_time_zone)
        sql_query = """SELECT 
                        SUM(pol.price_subtotal_incl) AS amount, 
                        pt.name AS product_name, pp.default_code AS code,
                        SUM(pol.qty) AS total_qty , pp.id AS product_id
                        FROM pos_order_line AS pol
                        INNER JOIN pos_order AS po ON po.id = pol.order_id
                        INNER JOIN product_product AS pp ON pol.product_id=pp.id
                        INNER JOIN product_template AS pt ON pt.id=pp.product_tmpl_id
                        WHERE po.date_order >= '%s'
                        AND po.date_order <= '%s'
                        AND po.company_id = %s
                        GROUP BY product_name, pp.id
                        ORDER BY amount DESC LIMIT 5
                    """ % (s_date, e_date, company_id)
        self._cr.execute(sql_query)
        result_top_product = self._cr.dictfetchall()
        data_source = []
        count = 0
        for each in result_top_product:
            count += 1
            data_source.append(['<strong>' + str(count) + '</strong>',  each.get('product_name'),
                 self.env.user.currency_id.symbol + ' ' + str("%.2f" % each.get('amount')), each.get('total_qty')])
        return data_source

    @api.model
    def sales_based_on_current_year(self, start, end, company_id):
        if company_id:
            pass
        else:
            company_id = self.env.user.company_id.id
        current_time_zone = self.env.user.tz or 'UTC'
        s_date, e_date = start_end_date_global(start, end, current_time_zone)
        query = """SELECT
                    extract(month from o.date_order AT TIME ZONE 'UTC' AT TIME ZONE '%s') AS order_month,
                    SUM(pol.price_subtotal_incl) AS price_total
                    FROM pos_order_line AS pol
                    INNER JOIN pos_order o ON (o.id=pol.order_id)
                    AND o.date_order >= '%s'
                    AND o.date_order <= '%s'
                    AND o.company_id = %s
                    GROUP BY  order_month
                    ORDER BY extract(month from o.date_order AT TIME ZONE 'UTC' AT TIME ZONE '%s') ASC
                """ % (current_time_zone, s_date, e_date, company_id, current_time_zone)
        self._cr.execute(query)
        data_year = self._cr.dictfetchall()
        final_list = []
        for each in range(1, int(datetime.today().month) + 1):
            total = 0
            for each_1 in data_year:
                if each == int(each_1.get('order_month')):
                    total += each_1.get('price_total')
                    break
            final_list.append({'order_month': each, 'price_total': total or 0.0})
        for each in final_list:
            each['order_month'] = calendar.month_abbr[int(each['order_month'])]
        return {'final_list': final_list, 'currency': self.env.user.currency_id.symbol}

    @api.model
    def sales_based_on_current_month(self, start, end, company_id):
        if company_id:
            pass
        else:
            company_id = self.env.user.company_id.id
        current_time_zone = self.env.user.tz or 'UTC'
        s_date, e_date = start_end_date_global(start, end, current_time_zone)
        query = """SELECT 
                    extract(day from po.date_order AT TIME ZONE 'UTC' AT TIME ZONE '%s') AS order_day,
                    SUM(pol.price_subtotal_incl) AS price_total
                    FROM pos_order_line AS pol
                    INNER JOIN pos_order po ON (po.id=pol.order_id)
                    WHERE 
                    po.date_order >= '%s'
                    AND po.date_order <= '%s'
                    AND po.company_id = %s
                    GROUP BY order_day
                    ORDER BY extract(day from po.date_order AT TIME ZONE 'UTC' AT TIME ZONE '%s') ASC
                """ % (current_time_zone, s_date, e_date, company_id, current_time_zone)
        self._cr.execute(query)
        result_data_month = self._cr.dictfetchall()
        final_list = []
        for each in range(1, int(datetime.today().day) + 1):
            total = 0
            for each_1 in result_data_month:
                if each == int(each_1.get('order_day')):
                    total += each_1.get('price_total')
                    break
            final_list.append({'days': each, 'price': total or 0.0})
        return {'final_list': final_list, 'currency': self.env.user.currency_id.symbol}

    @api.model
    def sales_based_on_hours(self, start, end, company_id):
        res_pos_order = {'total_sales': 0, 'total_orders': 0}
        if company_id:
            pass
        else:
            company_id = self.env.user.company_id.id
        current_time_zone = self.env.user.tz or 'UTC'
        s_date, e_date = start_end_date_global(start, end, current_time_zone)
        query = """SELECT extract(hour from po.date_order AT TIME ZONE 'UTC' AT TIME ZONE '%s') AS date_order_hour,
                    SUM(pol.price_subtotal_incl) AS price_total
                    FROM pos_order_line AS pol
                    LEFT JOIN pos_order po ON (po.id=pol.order_id)
                    WHERE po.date_order >= '%s'
                    AND po.date_order <= '%s'
                    AND po.company_id = %s
                    GROUP BY extract(hour from po.date_order AT TIME ZONE 'UTC' AT TIME ZONE '%s')
                    ORDER BY price_total DESC
                """ % (current_time_zone, s_date, e_date, company_id, current_time_zone)

        self._cr.execute(query)
        result_data_hour = self._cr.dictfetchall()
        count = 0
        top_hour_dict = {'top_hour': 0, 'amount': 0.0}
        if result_data_hour:
            for each in result_data_hour:
                if count == 0:
                    top_hour_dict.update(
                        {'top_hour': each.get('date_order_hour'), 'amount': each.get('price_total') or 0.0})
                    count += 1
                    break
        hour_lst = [hrs for hrs in range(0, 24)]
        for each in result_data_hour:
            if each['date_order_hour'] != 23:
                each['date_order_hour'] = [each['date_order_hour'], each['date_order_hour'] + 1]
            else:
                each['date_order_hour'] = [each['date_order_hour'], 0]
            hour_lst.remove(int(each['date_order_hour'][0]))
        for hrs in hour_lst:
            hr = []
            if hrs != 23:
                hr += [hrs, hrs + 1]
            else:
                hr += [hrs, 0]
            result_data_hour.append({'date_order_hour': hr, 'price_total': 0.0})
        sorted_hour_data = sorted(result_data_hour, key=lambda l: l['date_order_hour'][0])
        res_pos_order['sales_based_on_hours'] = sorted_hour_data
        return {'pos_order': res_pos_order, 'top_hour': top_hour_dict, 'currency': self.env.user.currency_id.symbol}

    @api.model
    def daily_gross_sales(self, start, end, company_id):
        res_pos_order = {}
        if company_id:
            pass
        else:
            company_id = self.env.user.company_id.id
        current_day_data = self.get_daily_gross_sales_data(start, company_id)
        last_current_day_data = self.get_daily_gross_sales_data(end, company_id)
        final_dict = {}
        final_list = []
        for each in current_day_data:
            final_dict[each['date_order_hour']] = {'today': each.get('price_total') or 0, 'last': 0}
        for each in last_current_day_data:
            if each.get('date_order_hour') in final_dict:
                final_dict[each['date_order_hour']].update({'last': each.get('price_total') or 0})
            else:
                final_dict[each['date_order_hour']] = {'today': 0, 'last': each.get('price_total') or 0}
        for key, val in final_dict.items():
            final_list.append({'date_order_hour': key, 'today': val.get('today'), 'last': val.get('last')})
        hour_lst = [hrs for hrs in range(0, 24)]
        for each in final_list:
            if each['date_order_hour'] != 23:
                each['date_order_hour'] = [each['date_order_hour'], each['date_order_hour'] + 1]
            else:
                each['date_order_hour'] = [each['date_order_hour'], 0]
            hour_lst.remove(int(each['date_order_hour'][0]))
        for hrs in hour_lst:
            hr = []
            if hrs != 23:
                hr += [hrs, hrs + 1]
            else:
                hr += [hrs, 0]
            final_list.append({'date_order_hour': hr, 'last': 0.0, 'today': 0.0})
        sorted_hour_data = sorted(final_list, key=lambda l: l['date_order_hour'][0])
        res_pos_order['sales_based_on_hours'] = sorted_hour_data
        return res_pos_order

    @api.model
    def products_category(self, start, end, order, option, company_id):
        if company_id:
            pass
        else:
            company_id = self.env.user.company_id.id
        current_time_zone = self.env.user.tz or 'UTC'
        s_date, e_date = start_end_date_global(start, end, current_time_zone)
        query = """pcat.name AS category FROM pos_order_line AS pol
                    INNER JOIN pos_order AS po ON po.id = pol.order_id
                    INNER JOIN product_product AS pt ON pt.id = pol.product_id
                    INNER JOIN product_template AS ptt ON ptt.id = pt.product_tmpl_id
                    INNER JOIN pos_category AS pcat ON pcat.id= ptt.pos_categ_id
                    WHERE po.date_order > '%s' AND po.date_order <= '%s' AND po.company_id = %s
                    GROUP BY category
                """ % (s_date, e_date, company_id)
        if option == "Price":
            price = "SELECT ROUND(SUM(pol.price_subtotal_incl), 2) as value, "
            query = price + query
            if order == "Top":
                query += "ORDER BY value DESC LIMIT 5"
            else:
                query += "ORDER BY value ASC  LIMIT 5"
        else:
            quantity = "SELECT SUM(pol.qty) as value,"
            query = quantity + query
            if order == "Top":
                query += "ORDER BY value DESC LIMIT 5;"
            elif order == "Bottom":
                query += "ORDER BY value ASC LIMIT 5;"
        self._cr.execute(query)
        product_categories = self._cr.dictfetchall()
        final_list = []
        return {'data_source': product_categories}

    @api.model
    def customer_avg_spent_per_visit(self, start, end, company_id):
        if company_id:
            pass
        else:
            company_id = self.env.user.company_id.id
        current_time_zone = self.env.user.tz or 'UTC'
        start_date,end_date = start_end_date_global(start, end, current_time_zone)
        cust_data = self.env['pos.order'].search(
            [('date_order', '>=', start_date), ('date_order', '>=', end_date),
             ('company_id', '=', company_id)])
        total_amount = 0.0
        for eaach in cust_data:
            total_amount += eaach.amount_total
        return {'cust_avg_spent_per_visit': total_amount / 30 if total_amount else 0,
                'currency_icon': self.env.user.currency_id.symbol}

    @api.model
    def customer_avg_visit(self, company_id):
        if company_id:
            pass
        else:
            company_id = self.env.user.company_id.id
        sql_query = "SELECT COUNT(partner_id) AS customer FROM pos_order WHERE company_id = %s AND date_order > current_date - 30" % company_id
        self._cr.execute(sql_query)
        cust_data = self._cr.dictfetchall()
        cust_avg = cust_data[0]['customer'] / 30
        return {'cust_avg_visit': cust_avg if cust_avg else 0}

    @api.model
    def get_the_top_customer(self, start, end, company_id):
        if company_id:
            pass
        else:
            company_id = self.env.user.company_id.id
        current_time_zone = self.env.user.tz or 'UTC'
        s_date, e_date = start_end_date_global(start, end, current_time_zone)
        sql_query = """SELECT 
                        SUM(pol.price_subtotal_incl) AS amount, 
                        cust.name AS customer,
                        SUM(pol.qty) AS total_product
                        FROM pos_order_line AS pol
                        INNER JOIN pos_order AS po ON po.id = pol.order_id
                        INNER JOIN res_partner AS cust ON cust.id = po.partner_id
                        WHERE po.date_order >= '%s'
                        AND po.date_order <= '%s'
                        AND po.company_id = %s
                        GROUP BY cust.name
                        ORDER BY amount DESC LIMIT 10
                    """ % (s_date, e_date, company_id)
        self._cr.execute(sql_query)
        top_customer = self._cr.dictfetchall()
        return {'top_customer': top_customer, 'currency': self.env.user.currency_id.symbol}

    @api.model
    def sales_data_per_week(self, start, end, company_id):
        if company_id:
            pass
        else:
            company_id = self.env.user.company_id.id
        current_time_zone = self.env.user.tz or 'UTC'
        s_date, e_date = start_end_date_global(start, end, current_time_zone)
        sday = datetime.strptime(s_date, '%Y-%m-%d %H:%M:%S').day
        eday = datetime.strptime(e_date, '%Y-%m-%d %H:%M:%S').day
        query = """SELECT
                    extract(day from date_order AT TIME ZONE 'UTC' AT TIME ZONE '%s') AS dn,
                    to_char(date_order AT TIME ZONE 'UTC' AT TIME ZONE '%s','DY') AS day,
                    COUNT(id) AS total_order,
                    SUM(amount_total) AS sale_total
                    FROM pos_order
                    where date_order > '%s'
                    AND date_order <= '%s'
                    AND company_id = %s
                    GROUP BY dn,day;
                """ % (current_time_zone, current_time_zone, s_date, e_date, company_id)
        
        self._cr.execute(query)
        result = self._cr.dictfetchall()
        days = ['SUN', 'MON', 'TUE', 'WED', 'THU', 'FRI', 'SAT']
        final_data_list = []
        for d in days:
            order = 0.0
            amount = 0.0
            for each in result:
                if d == each.get('day'):
                    order = each.get('total_order')
                    amount = each.get('sale_total')
            final_data_list.append({'day': d, 'sale_total': amount or 0.0, 'count': order or 0.0})
        return final_data_list

    @api.model
    def staff_sale_info(self, s_date, e_date, company_id, limit):
        sql = ''
        if limit:
            sql = 'LIMIT 1'
        query = """SELECT ord.person_id As person_id ,count(ord.order_name) AS num_order, sum(ord.amount) AS amount FROM
                   (SELECT pos.user_id AS person_id, posl.order_id As order_name, 
                   SUM(posl.price_subtotal_incl) AS amount
                   FROM pos_order_line AS posl
                   LEFT JOIN pos_order AS pos ON pos.id = posl.order_id
                   WHERE pos.company_id = %s
                   AND pos.date_order >= '%s'
                   AND pos.date_order <= '%s'
                   GROUP BY order_name, person_id) AS ord
                   GROUP BY person_id
                   ORDER BY amount DESC %s 
           """ % (company_id, s_date, e_date, sql)
        self._cr.execute(query)
        return self._cr.dictfetchall()

    @api.model
    def get_daily_gross_sales_data(self, filter_date, company_id):
        current_time_zone = self.env.user.tz or 'UTC'
        s_date, e_date = start_end_date_global(filter_date, filter_date, current_time_zone)
        sql_query = """SELECT extract(hour from po.date_order AT TIME ZONE 'UTC' AT TIME ZONE '%s') AS date_order_hour,
                        SUM(pol.price_subtotal_incl) AS price_total
                        FROM pos_order_line AS pol
                        INNER JOIN pos_order po ON (po.id=pol.order_id)
                        WHERE
                        po.date_order BETWEEN '%s' AND '%s'
                        AND po.company_id = %s
                        GROUP BY extract(hour from po.date_order AT TIME ZONE 'UTC' AT TIME ZONE '%s')
                    """ % (current_time_zone, s_date, e_date, company_id, current_time_zone)
        self._cr.execute(sql_query)
        result_data_hour = self._cr.dictfetchall()
        return result_data_hour