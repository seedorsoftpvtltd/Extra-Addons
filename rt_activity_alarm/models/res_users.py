# -*- coding: utf-8 -*-

from odoo import _, api, exceptions, fields, models, modules
from odoo.addons.base.models.res_users import is_selection_groups
from pytz import utc
from datetime import datetime
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT
import pytz
class Users(models.Model):
    _inherit = 'res.users'

    @api.model
    def rt_activity_alarm_systray_get_reminder_activities(self):
        # ---------------------------------
        # Search Using Environment.    
        query = """SELECT id
                    FROM mail_activity
                    WHERE user_id = %(user_id)s AND
                    rt_activity_alarm_reminder_datetime::date = %(today)s::date;
                    """
        self.env.cr.execute(query, {
            'today': fields.Date.context_today(self),
            'user_id': self.env.uid,
        })
        activity_data = self.env.cr.dictfetchall()
        activity_ids = [ activity['id'] for activity in activity_data ]               
        domain = [('id','in', activity_ids)]
        order = "rt_activity_alarm_reminder_datetime asc"
        activities = self.env['mail.activity'].search(domain,order = order)
        list_activities_dic = []
        list_times = []
        if activities:
            user_tz = pytz.timezone(self.env.context.get('tz') or self.env.user.tz or 'UTC')
            utc_tz = pytz.timezone('UTC')
            for activity in activities:
                utc_time_hour_minute = ''
                user_time_hour_minute = ''
                user_tz_reminder_datetime = ''
                user_tz_date_deadline = ''
                user_tz_create_date = ''               
                if activity.rt_activity_alarm_reminder_datetime:
                    # UTC TimeZone Reminder Date Time
                    utc_dt = pytz.utc.localize(activity.rt_activity_alarm_reminder_datetime)
                    reminder_datetime = utc_dt.astimezone(utc_tz)
                    utc_time_hour_minute = str(reminder_datetime.hour) or ''
                    utc_time_hour_minute += ':' + str(reminder_datetime.minute) or ''
                    
                    # User TimeZone Reminder Date Time
                    user_dt = pytz.utc.localize(activity.rt_activity_alarm_reminder_datetime)
                    reminder_datetime = user_dt.astimezone(user_tz)
                    user_time_hour_minute = str(reminder_datetime.hour) or ''
                    user_time_hour_minute += ':' + str(reminder_datetime.minute) or ''  
                                     
                    user_tz_reminder_datetime = reminder_datetime
                    
                    # User TimeZone Due Date  
                    user_tz_create_date = pytz.utc.localize(activity.create_date)
                    user_tz_create_date = user_tz_create_date.astimezone(user_tz)
                                                             
                module = self.env[activity.res_model]._original_module
                module_icon_path = module and modules.module.get_module_icon(module) or ''               
                activity_dic = {
                    'summary':activity.summary or '',
                    'note':activity.note or '',
                    'reminder_datetime':activity.rt_activity_alarm_reminder_datetime,
                    'res_id':activity.res_id,
                    'res_model':activity.res_model,
                    'res_model_name':activity.res_model_id.name if activity.res_model_id else '',   
                    'res_name':activity.res_name,
                    'activity_id':activity.id,                     
                    'activity_type_icon':activity.icon, 
                    'activity_type_name':activity.activity_type_id.name if activity.activity_type_id else '',  
                    'module_icon_path':module_icon_path,  
                    'utc_time_hour_minute':utc_time_hour_minute,  
                    'user_time_hour_minute':user_time_hour_minute, 
                    'user_tz_reminder_datetime':user_tz_reminder_datetime,
                    'user_tz_create_date':user_tz_create_date,
                    'user_id_name':activity.user_id.name if activity.user_id else '',
                    'user_id':activity.user_id.id if activity.user_id else False,
                    'date_deadline':activity.date_deadline,
                    'state':activity.state,         
                    } 
                list_activities_dic.append(activity_dic)
                list_times.append(utc_time_hour_minute)
        
        return {
            'list_activities_dic':list_activities_dic,
            'list_times':list_times,
            }
    
        # Search Using Environment.   
        # ---------------------------------
       