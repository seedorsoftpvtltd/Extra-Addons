# -*- coding: utf-8 -*-

from odoo import http, _
from odoo import http, _
from odoo.http import request
from odoo.addons.portal.controllers.portal import CustomerPortal, pager as portal_pager, get_records_pager
import base64
from odoo.tools import groupby as groupbyelem
from collections import OrderedDict
from operator import itemgetter
from odoo.osv.expression import OR
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT
import datetime


class PayslipPortal(CustomerPortal):

    def _prepare_portal_layout_values(self):
        values = super(PayslipPortal, self)._prepare_portal_layout_values()
        user = request.env.user.sudo()
        payslip_count = request.env['hr.payslip'].sudo().search_count([('employee_id.user_id', '=', user.id),('state','=','done')])
        values.update({
            'payslip_count': payslip_count,
        })
        return values

    @http.route(['/my/payslips', '/my/payslips/page/<int:page>'], type='http', auth="user", website=True)
    def my_payslips(self, page=1, date_begin=None, date_end=None, sortby=None, filterby=None, search=None, search_in='content', **kw):
        groupby = kw.get('groupby', 'none')
        values = self._prepare_portal_layout_values()
        user = request.env.user

        searchbar_sortings = {
            'date': {'label': _('Newest'), 'order': 'date_from desc'},
            'name': {'label': _('Title'), 'order': 'name'},
            'update': {'label': _('Last Update'), 'order': 'write_date desc'},
        }
        searchbar_filters = {
            'all': {'label': _('All'), 'domain': []},
        } 
        searchbar_inputs = {
            'all': {'input': 'all', 'label': _('Search in All')},
        }
        searchbar_groupby = {
            'none': {'input': 'none', 'label': _('None')},
        }

        domain = [('employee_id.user_id', '=', user.id),('state','=','done')]

        # default sort by value
        if not sortby:
            sortby = 'date'
        order = searchbar_sortings[sortby]['order']
        # default filter by value
        if not filterby:
            filterby = 'all'
        if searchbar_filters.get('filterby'):
            domain += searchbar_filters[filterby]['domain']

        # archive groups - Default Group By 'date'
        if date_begin and date_end:
            domain += [('date_from', '>', date_begin), ('date_from', '<=', date_end)]

        # search
        if search and search_in:
            search_domain = []
            if search_in in ('all'):
                search_domain = OR([search_domain, [('name', 'ilike', search)]])
            domain += search_domain

        # CR count
        payslip_count = request.env['hr.payslip'].sudo().search_count(domain)
        pager = portal_pager(
            url="/my/payslips",
            url_args={'date_begin': date_begin, 'date_end': date_end, 'sortby': sortby, 'filterby': filterby, 'search_in': search_in, 'search': search},
            total=payslip_count,
            page=page,
            step=self._items_per_page
        )
        # content according to pager and archive selected
        payslips = request.env['hr.payslip'].search(domain, order=order, limit=self._items_per_page, offset=pager['offset'])
        request.session['my_payslips_history'] = payslips.ids[:100]
        grouped_payslips = [payslips]

        values.update({
            'date': date_begin,
            'date_end': date_end,
            'payslips': payslips, #TODO master remove this, grouped_payslips is enough
            'grouped_payslips': grouped_payslips,
            'page_name': 'payslip',
            'default_url': '/my/payslips',
            'pager': pager,
            'searchbar_sortings': searchbar_sortings,
            'searchbar_groupby': searchbar_groupby,
            'searchbar_inputs': searchbar_inputs,
            'search_in': search_in,
            'sortby': sortby,
            'groupby': groupby,
            'searchbar_filters': OrderedDict(sorted(searchbar_filters.items())),
            'filterby': filterby,
        })
        return request.render("acs_hr_payslip_portal.my_payslips", values)


    @http.route(['/my/payslips/<int:payslip_id>'], type='http', auth="user", website=True)
    def my_payslip(self, payslip_id=None, **kw):
        payslip = request.env['hr.payslip'].browse(payslip_id)
        return request.render("acs_hr_payslip_portal.my_payslips_payslip", {'payslip': payslip, 'user': request.env.user})
