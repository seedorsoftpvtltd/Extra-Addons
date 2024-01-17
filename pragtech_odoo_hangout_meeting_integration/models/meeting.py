import json
import logging
from datetime import datetime, timedelta
import datetime
import requests
from odoo.http import request
import base64
from dateutil.parser import parse as duparse
from odoo import api, fields, models
from odoo.exceptions import Warning, UserError
import dateutil.parser
import datetime
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT
import html2text
from datetime import date
_logger = logging.getLogger(__name__)


class CustomHangoutsMeet(models.Model):
    _inherit = 'calendar.event'
    _description = 'Hangouts Meet Details'

    meet_flag = fields.Boolean('Add Hangouts Meet', default=False)
    end_date_time = fields.Datetime(string='End Date', index=True)
    meet_url = fields.Text(string='Meet URL')
    meet_id = fields.Text(string='Meet ID')
    meet_code = fields.Char("Meeting Code")

    def create_attendees(self):
        current_user = self.env.user
        result = {}
        for meeting in self:
            alreay_meeting_partners = meeting.attendee_ids.mapped('partner_id')
            meeting_attendees = self.env['calendar.attendee']
            meeting_partners = self.env['res.partner']
            for partner in meeting.partner_ids.filtered(lambda partner: partner not in alreay_meeting_partners):
                values = {
                    'partner_id': partner.id,
                    'email': partner.email,
                    'event_id': meeting.id,
                }

                if self._context.get('google_internal_event_id', False):
                    values['google_internal_event_id'] = self._context.get(
                        'google_internal_event_id')

                # current user don't have to accept his own meeting
                if partner == self.env.user.partner_id:
                    values['state'] = 'accepted'

                attendee = self.env['calendar.attendee'].create(values)

                meeting_attendees |= attendee
                meeting_partners |= partner

            # # # if meeting_attendees and not self._context.get('detaching'):
            # # #     to_notify = meeting_attendees.filtered(lambda a: a.email != current_user.email)
            # # #     to_notify._send_mail_to_attendees('calendar.calendar_template_meeting_invitation')

            if meeting_attendees:
                meeting.write({'attendee_ids': [
                              (4, meeting_attendee.id) for meeting_attendee in meeting_attendees]})

            if meeting_partners:
                meeting.message_subscribe(partner_ids=meeting_partners.ids)

            # We remove old attendees who are not in partner_ids now.
            all_partners = meeting.partner_ids
            all_partner_attendees = meeting.attendee_ids.mapped('partner_id')
            old_attendees = meeting.attendee_ids
            partners_to_remove = all_partner_attendees + meeting_partners - all_partners

            attendees_to_remove = self.env["calendar.attendee"]
            if partners_to_remove:
                attendees_to_remove = self.env["calendar.attendee"].search(
                    [('partner_id', 'in', partners_to_remove.ids), ('event_id', '=', meeting.id)])
                attendees_to_remove.unlink()

            result[meeting.id] = {
                'new_attendees': meeting_attendees,
                'old_attendees': old_attendees,
                'removed_attendees': attendees_to_remove,
                'removed_partners': partners_to_remove
            }
        return result

    def action_id_calendar_view(self):
        calendar_view = self.env.ref('calendar.view_calendar_event_calendar')
        action_id = self.env['ir.actions.act_window'].search(
            [('view_id', '=', calendar_view.id)], limit=1).id
        return action_id

    def base_url(self):
        url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')
        return url

    def db_name(self):
        db_name = self._cr.dbname
        return db_name

    def send_mail_notification_mail(self):
        company_id = self.env['res.users'].search(
            [('id', '=', self._context.get('uid'))]).company_id

        template_id = self.env['ir.model.data'].get_object_reference(
            'pragtech_odoo_hangout_meeting_integration', 'calendar_template_meeting_invitation_of_meeting_creation_call')[1]
        login_user_id = self.env['res.users'].sudo().search(
            [('id', '=', self._context.get('uid'))], limit=1)
        for i in self.attendee_ids:
            if i.partner_id != login_user_id.partner_id:
                email_template_obj = i.env['mail.template'].browse(template_id)
                if template_id:

                    values = email_template_obj.generate_email(
                        i.id, fields=None)
                    values['mail_server_id'] = company_id.outgoing_server_mail_id.id
                    values['email_from'] = login_user_id.email
                    values['email_to'] = i.email
                    values['recipient_ids'] = False
                    values['message_type'] = "email"
                    values['res_id'] = False
                    values['reply_to'] = False
                    values['author_id'] = self.env['res.users'].browse(
                        request.env.uid).partner_id.id
                    mail_mail_obj = self.env['mail.mail']
                    msg_id = mail_mail_obj.sudo().create(values)
                    if msg_id:
                        mail_mail_obj.sudo().send([msg_id])
        return True

    def redirect_join_meet(self):
        url = "http://meet.google.com/"

        return {
            "type": "ir.actions.act_url",
            "url": url,
            "target": "new"
        }

    @api.model
    def create(self, vals_list):
        res = super(CustomHangoutsMeet, self).create(vals_list)
        if vals_list.get('meet_flag'):
            res.post_request_hangout_meet()
            res.send_mail_notification_mail()
        return res

    def post_request_hangout_meet(self):
        login_user_id = self.env['res.users'].sudo().search(
            [('id', '=', self._context.get('uid'))], limit=1)
        login_user_id.generate_refresh_token_from_access_token()

        start_datetime = fields.Datetime.context_timestamp(
            self, self.start_datetime).isoformat('T')
        end_datetime = fields.Datetime.context_timestamp(
            self, self.end_date_time).isoformat('T')

        if login_user_id.access_token and login_user_id.refresh_token:
            bearer = 'Bearer '+login_user_id.access_token
            payload = {}
            headers = {
                'Content-Type': "application/json",
                'Authorization': bearer
            }

            attendees_list = []
            attendees = self.sudo().partner_ids
            for i in attendees:

                attendees_list.append({"email": i.email})

            #######Note: requestId is just a unique string##########
            body = {
                "conferenceData": {"createRequest": {"requestId": "7qxalsvy038"}},
                "summary": self.name,
                "start": {"dateTime": start_datetime, "timeZone": "UTC"},
                "end": {"dateTime": end_datetime, "timeZone": "UTC"},
                "attendees": attendees_list,
                "description": self.description,
            }

            data_json = json.dumps(body)
            url = 'https://www.googleapis.com/calendar/v3/calendars/' + \
                login_user_id.calendar_id+'/events?conferenceDataVersion=1'

            hangout_meet_response = requests.request(
                "POST", url, headers=headers, data=data_json)

            if hangout_meet_response.status_code == 200:
                data_rec = hangout_meet_response.json()

                self.write({"meet_url": data_rec.get(
                    'hangoutLink'), "meet_id": data_rec.get('id')})
                hangout_meet_link = data_rec.get('hangoutLink')

                if hangout_meet_link:
                    self.write({"meet_code": hangout_meet_link.split('/')[3]})
            elif hangout_meet_response.status_code == 401:
                raise UserError("Please Authenticate with Hangouts Meet.")
