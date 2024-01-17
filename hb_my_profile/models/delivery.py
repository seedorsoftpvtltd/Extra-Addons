import datetime
import requests
from pytz import timezone
from odoo import api, fields, models, _
from dateutil.relativedelta import relativedelta
from dateutil import tz
from odoo.exceptions import UserError


class DeliveryCnt(models.Model):
    _inherit = "res.users"

    cnt_del = fields.Integer(string="My Orders", compute='_cnt_del')
    last_delivery_date = fields.Date(string="Last Service Date - My", compute='_cnt_del')
    cnt_pend_picking = fields.Integer(string="Pending Services - My", compute='_cnt_del')
    cnt_allorders = fields.Integer(string="My Orders", compute='_cnt_del')
    last_picking_date = fields.Date(string="Last Service Date - My", compute='_cnt_del')
    last_picking_time = fields.Char(string="Pending Services - My", compute='_cnt_del')

    def _cnt_del(self):
        for rec in self:
#            url = "http://eiuat.seedors.com:8290/services/MobileOrderApi/get-all-orders-count?receiver=126&clientid=bookseedorpremiumuat"
            url = "http://eiuat.seedors.com:8290/services/MobileOrderApi/get-all-orders-count?receiver={}&clientid={}".format(rec.id, self.env.cr.dbname)
            # url1 = "http://eiuat.seedors.com:8290/services/MobileOrderApi/get-all-placed-orders?clientid=bookseedorpremiumuat"
            url1 = "http://eiuat.seedors.com:8290/services/MobileOrderApi/get-all-placed-orders?clientid={}".format(self.env.cr.dbname)
#            if url:
#                raise UserError(_(url))
            print(url)
            payload = {}
            headers = {
                'Accept': 'application/json'
            }

            response = requests.request("GET", url, headers=headers, data=payload)
            response1 = requests.request("GET", url1, headers=headers, data=payload)
            print(response1.json())
            try:
                allorderscount = len(response1.json()['orders']['order'])
            except:
                allorderscount = 0
            h = response.json()
            onprocesscount = []
            historycount = []
            orderqueuecount = []
            pick_dates = []
            delivery_dates = []
            print(response.json())
            try:
                pay = response.json()['orders']['order']
            except:
                rec['last_picking_time'] = ''
                rec['last_picking_date'] = ''
                rec['cnt_allorders'] = ''
                rec['cnt_pend_picking'] = ''
                rec['last_delivery_date'] = ''
                rec['cnt_del'] = ''
                return True
            for i in pay:
                # print(i)
                if str(i['processstatus']) == 'onprocess':
                    onprocesscount.append(i)
                    if i['pickingdate'] != None:
                        pick_dates.append(i['pickingdate'])
                if str(i['processstatus']) == 'completed':
                    historycount.append(i)
                    if i['deliverydate'] != None:
                        delivery_dates.append(i['deliverydate'])
                if str(i['processstatus']) == 'ordered':
                    orderqueuecount.append(i)
            # print(pick_dates, delivery_dates)
            for i in range(0, len(delivery_dates)):
                # print(delivery_dates[i], 'delivery dates')
                # print(i)
                date = datetime.datetime.strptime(delivery_dates[i], '%Y-%m-%d %H:%M:%S')
                now = datetime.datetime.now()
                today = now.strftime('%Y-%m-%d %H:%M:%S')
                today1 = datetime.datetime.strptime(today, '%Y-%m-%d %H:%M:%S')
                # print(today1)
                if i == 0:
                    deli_min = (today1 - date).days
                    min_date = date
                min = (today1 - date).days
                # minn = relativedelta(today1,date)
                # # print(minn, 'minnn')
                # durat = ' {} days {} hours'.format(minn.days,
                #                                                    minn.hours)
                # print(durat, 'hrs')
                # print(min)
                if min < deli_min:
                    deli_min = min  # last del
                    min_date = date  # last del date
                else:
                    pass
            print(deli_min)
            print(min_date)

            last_delivery_date = min_date
            deliverycount = len(delivery_dates)

            for i in range(0, len(pick_dates)):
                # print(delivery_dates[i], 'delivery dates')
                # print(i)
                date = datetime.datetime.strptime(pick_dates[i], '%Y-%m-%d %H:%M:%S')
                print(date, 'dateeeeeeeeeeeeeeeeeeee')
                now = datetime.datetime.now()
                today = now.strftime('%Y-%m-%d %H:%M:%S')
                today1 = datetime.datetime.strptime(today, '%Y-%m-%d %H:%M:%S')
                # if rec.tz:
                #     today1 = todayy.astimezone(timezone(rec.tz))
                # else:
                #     today1 = todayy

                # print(todayy, 'todayyyyyyyyyyyyyyyyyyyy')
                print(today1, 'todayyyyyyyyyyyyyyyyyyyy')
                if i == 0:
                    pick_min = (today1 - date).days
                    min_date = date
                min = (today1 - date).days
                print(min, 'min')
                print(pick_min, 'pickmin')
                if min < pick_min:
                    pick_min = min  # last del
                    min_date = date  # last del date
                else:
                    pass
            print(pick_min, 'pick_min')
            print(min_date, 'min_date')
            minn = relativedelta(today1, date)
            # print(minn, 'minnn')
            # durat = '{} year {} month {} days {} hours'.format(minn.year, minn.month, minn.days,
            #                                                    minn.hours)
            if minn.days == 0:
                durat = '{} hours'.format(minn.hours)
            elif minn.days > 0:
                durat = '{} days {} hours'.format(minn.days, minn.hours)
            else:
                durat = '{} year {} month {} days {} hours'.format(minn.year, minn.month, minn.days, minn.hours)

            print(durat)

            picking_count = len(pick_dates)
            last_picking_date = min_date
            last_picking_time = durat

            print('------------Deliver Status----------------------')
            print(last_delivery_date)
#            rec['last_delivery_date'] = last_delivery_date
            if last_delivery_date:
                rec['last_delivery_date'] = last_delivery_date
            else:
                rec['last_delivery_date'] = ''
            print(deliverycount)
#            rec['cnt_del'] = deliverycount
            if deliverycount:
                rec['cnt_del'] = deliverycount
            else:
                rec['cnt_del'] = ''
            print('-------------------------------------------------')
            print('------------Picking Status----------------------')
            print(picking_count)
            rec['cnt_pend_picking'] = picking_count
#            print(last_picking_date)
            rec['last_picking_date'] = last_picking_date
            print(last_picking_time)
            rec['last_picking_time'] = last_picking_time
            print('-------------------------------------------------')
#            rec['cnt_allorders'] = allorderscount
            if allorderscount:
                rec['cnt_allorders'] = allorderscount
            else:
                rec['cnt_allorders'] = ''

            return True



