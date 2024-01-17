# -*- coding: utf-8 -*-

from odoo import models, fields, api

class MailActivity(models.Model):

    _inherit = 'mail.activity'

    custom_partner_ids = fields.Many2many(
        'res.partner',
        string='Portal Share',
        copy=True
    )
    is_share_portal_custom = fields.Boolean(
        string='Is Share Portal?',
        copy=True
    )
    is_custom_description_probc = fields.Boolean(
        string='Portal Show Description?',
        copy=True
    )
    custom_message_ids = fields.One2many(
        'custom.activity.message', 
        'custom_activity_id', 
        string='Customer Message',
        copy=False
    )

    def open_activity_message(self):
        self.ensure_one()
        action = self.env.ref('schedule_activity_share_portal.action_custom_activity_message_').read()[0]
        action['domain'] = [('custom_activity_id','in', self.ids)]
        return action

    @api.onchange('activity_type_id')
    def onchange_activity_type_id(self):
        for rec in self:
            rec.is_share_portal_custom = rec.activity_type_id.is_share_portal
            rec.is_custom_description_probc = rec.activity_type_id.is_custom_description

class MailActivityMessage(models.Model):

    _name='custom.activity.message'
    _rec_name = 'custom_activity_id'

    custom_activity_id = fields.Many2one(
        'mail.activity',
        string='Custom Activity',
        copy=False
    )
    custom_date = fields.Date(
        string='Message Sent Date'
    )
    custom_user_id = fields.Many2one(
        'res.users',
        string='Activity User',
        related='custom_activity_id.user_id',
        store=True
    )
    custom_partner_id = fields.Many2one(
        'res.partner',
        string='Portal Agent / Contact'
    )
    custom_message_body = fields.Char(
        string='Received Message'
    )


class MailActivityType(models.Model):

    _inherit = 'mail.activity.type'

    is_share_portal = fields.Boolean(
        string='Is Share Portal?'
    )
    is_custom_description = fields.Boolean(
        string='Portal Show Description??'
    )

    
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
