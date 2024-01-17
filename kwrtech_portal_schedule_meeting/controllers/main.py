import pytz
from datetime import datetime, timedelta

from odoo import http
from odoo.http import request
from odoo.addons.website_form.controllers.main import WebsiteForm


class WebsiteMeeting(http.Controller):

    @http.route(['/schedule'], type='http', auth="user", methods=['GET'], website=True)
    def schedule(self, **kw):
        values = {
            'website': request.website,
            'members': [('{0} [{1}] ({2})'.format(emp.name, emp.job_title, emp.resource_calendar_id.tz), emp.user_id.id) for emp in request.env['hr.employee'].sudo().search([('user_id', '!=', None)])],
            'tzs': [(tz, tz) for tz in sorted(pytz.all_timezones, key=lambda tz: tz if not tz.startswith('Etc/') else '_')],
        }
        return request.render('kwrtech_portal_schedule_meeting.schedule_meeting', values)


class WebsiteForm(WebsiteForm):

    @http.route('/website_form/<string:model_name>', type='http', auth="public", methods=['POST'], website=True)
    def website_form(self, model_name, **kwargs):
        lang = request.env['ir.qweb.field'].user_lang()
        # Because timezone is considered in website_form/controllers/main.py:datetime()
        context = dict(request.context)
        context['tz'] = kwargs['timezone']
        request.context = context
        if model_name == 'calendar.event':
            attendees = request.env['res.users'].sudo().browse(int(kwargs['user_id'])).partner_id + request.env.user.partner_id
            kwargs['partner_ids'] = [(6, 0, attendees.ids)]
            time_from = kwargs['timeslot'].split(' - ')[0]
            hour_from = int(time_from.split(':')[0])
            minute_from = int(time_from.split(':')[1])
            meeting_date = pytz.timezone(kwargs['timezone']).localize(datetime.strptime(kwargs['meeting_date'], '%Y-%m-%d') + timedelta(hours=hour_from, minutes=minute_from))
            request.params.update({
                'partner_ids': ','.join([str(partner_id) for partner_id in attendees.ids]),
                'start': meeting_date.replace(tzinfo=None).strftime(lang.date_format + ' ' + lang.time_format),
                'stop': (meeting_date.replace(tzinfo=None) + timedelta(minutes=int(kwargs['duration']))).strftime(lang.date_format + ' ' + lang.time_format),
                'duration': (int(kwargs['duration']) / 60),
            })
        return super(WebsiteForm, self).website_form(model_name, **kwargs)
