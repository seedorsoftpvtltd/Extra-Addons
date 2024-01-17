# -*- coding: utf-8 -*-

# Part of Probuse Consulting Service Pvt Ltd. See LICENSE file for full copyright and licensing details.

from odoo import http, fields, _
from odoo.http import request

class WebsiteCustomerActivityComment(http.Controller):
        
    @http.route(['/custom_activity/comment'], type='http', auth="user", website=True)
    def custom_activity_comment(self, **kw):
        custom_activity_comment = kw.get('custom_activity_comment')
        custom_activity_id = kw.get('custom_calendar_activity_id')
        if custom_activity_comment and custom_activity_id:
            record_id = request.env['mail.activity'].sudo().browse(int(custom_activity_id))
            custom_res_model_id = record_id.res_model_id
            custom_res_model = record_id.res_model
            group_msg = _(custom_activity_comment)
            custom_partners = record_id.custom_partner_ids.ids
            if request.env.user.partner_id.id not in custom_partners:
                return request.redirect("/")
            else:
                message_vals = {
                    'custom_date': fields.date.today(),
                    'custom_partner_id': request.env.user.partner_id.id,
                    'custom_message_body': group_msg,
                    'custom_activity_id': record_id.id
                }
                custom_message_id = request.env['custom.activity.message'].sudo().create(message_vals)
            
#     
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:hashiftwidth=4: