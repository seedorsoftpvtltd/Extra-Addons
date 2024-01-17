# -*- coding: utf-8 -*-


from odoo import models, fields, api

class MailActivity(models.Model):
    _inherit = "mail.activity"
    
    rt_activity_alarm_reminder_datetime = fields.Datetime(string="Reminder Date-Time")
    
    
    
    # ------------------------------------------------------
    # ORM overrides
    # ------------------------------------------------------

    @api.model
    def create(self, values):
        activity = super(MailActivity, self).create(values)
        if activity.rt_activity_alarm_reminder_datetime:
            if activity.rt_activity_alarm_reminder_datetime.date() == fields.Date.today():
                self.env['bus.bus'].sendone(
                    (self._cr.dbname, 'res.partner', activity.user_id.partner_id.id),
                    {'type': 'activity_updated', 'activity_created': True})
        return activity

    def write(self, values):
        res = super(MailActivity, self).write(values)

        if values.get('rt_activity_alarm_reminder_datetime',False):
            for activity in self:
                self.env['bus.bus'].sendone(
                    (self._cr.dbname, 'res.partner', activity.user_id.partner_id.id),
                    {'type': 'activity_updated', 'rt_activity_alarm_reminder_datetime_updated': True})
        return res

    def unlink(self):
        for activity in self:
            if activity.rt_activity_alarm_reminder_datetime:
                if activity.rt_activity_alarm_reminder_datetime.date() == fields.Date.today():
                    self.env['bus.bus'].sendone(
                        (self._cr.dbname, 'res.partner', activity.user_id.partner_id.id),
                        {'type': 'activity_updated', 'activity_deleted': True})
        return super(MailActivity, self).unlink()    