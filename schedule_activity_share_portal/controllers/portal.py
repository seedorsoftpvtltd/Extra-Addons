# -*- coding: utf-8 -*-

# Part of Probuse Consulting Service Pvt Ltd. See LICENSE file for full copyright and licensing details.

from collections import OrderedDict
import werkzeug

import base64
from odoo import http, _
from odoo.http import request
from odoo import models,registry, SUPERUSER_ID
from odoo.exceptions import AccessError, MissingError
from odoo.addons.portal.controllers.portal import CustomerPortal, pager as portal_pager, get_records_pager

from odoo.osv.expression import OR

class CustomerPortal(CustomerPortal):
    _items_per_page = 10

    def _prepare_portal_layout_values(self):
        values = super(CustomerPortal, self)._prepare_portal_layout_values()
        partner = request.env.user.partner_id
 
        Activity = request.env['mail.activity']
        custom_activity_count = Activity.sudo().search_count([
            ('is_share_portal_custom', '=', True),('custom_partner_ids', 'child_of', [partner.commercial_partner_id.id])
        ])
        values.update({
            'custom_activity_count': custom_activity_count,
        })
        return values

    def _activity_get_page_view_values(self, custom_activity_request, access_token, **kwargs):
        values = {
            'page_name': 'custom_activity_page_probc',
            'custom_activity_request': custom_activity_request,
        }

        return self._get_page_view_values(custom_activity_request, access_token, values, 'my_activity_history', False, **kwargs)

    @http.route(['/my/custom_activity_request', '/my/custom_activity_request/page/<int:page>'], type='http', auth="user", website=True)
    def portal_my_custom_activity(self, page=1, date_begin=None, date_end=None, sortby=None, filterby=None, search=None, search_in='activity_type_id', **kw):

        values = self._prepare_portal_layout_values()
        partner = request.env.user.partner_id
        activity_obj = http.request.env['mail.activity']
        domain = [
             ('is_share_portal_custom', '=', True),('custom_partner_ids', 'child_of', [partner.commercial_partner_id.id])
        ]

        custom_activity_count = activity_obj.sudo().search_count(domain)
        
        # pager
        pager = portal_pager(
            url="/my/custom_activity_request",
            total=custom_activity_count,
            page=page,
            step=self._items_per_page
        )
        searchbar_sortings = {
            'date_deadline': {'label': _('Due Date'), 'order': 'date_deadline desc'},
        }
        
        searchbar_inputs = {
            'activity_type_id': {'input': 'activity_type_id', 'label': _('Search in Activity Type')},
        }
        
        # default sort by value
        if not sortby:
            sortby = 'date_deadline'
        order = searchbar_sortings[sortby]['order']

        # search
        if search and search_in:
            search_domain = []
            if search_in in ('activity_type_id', 'all'):
                search_domain = OR([search_domain, [('activity_type_id', 'ilike', search)]])
            domain += search_domain

        # content according to pager and archive selected
        activities = activity_obj.sudo().search(domain, order=order, limit=self._items_per_page, offset=pager['offset'])

        values.update({
            'activities': activities,
            'page_name': 'custom_activity_page_probc',
            'pager': pager,
            'default_url': '/my/custom_activity_request',
            'searchbar_sortings': searchbar_sortings,
            'searchbar_inputs': searchbar_inputs,
            'search_in': search_in,
            'sortby': sortby,
        })
        return request.render("schedule_activity_share_portal.portal_my_activity_custom", values)

    @http.route(['/my/custom_activity_request/<int:activity_id>'], type='http', auth="user", website=True)
    def custom_portal_my_activity(self, activity_id, access_token=None, **kw):
        activity_id = request.env['mail.activity'].sudo().browse(activity_id)
        custom_partners = activity_id.custom_partner_ids.ids
        if request.env.user.partner_id.id in custom_partners:
            values = self._activity_get_page_view_values(activity_id, access_token, **kw)
            return request.render("schedule_activity_share_portal.custom_portal_my_activity", values)
        else:
            return request.redirect("/")