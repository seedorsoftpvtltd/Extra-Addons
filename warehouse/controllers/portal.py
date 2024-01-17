import base64
from collections import OrderedDict

from odoo import http
from odoo.exceptions import AccessError, MissingError
from odoo.http import request
from odoo.tools import image_process
from odoo.tools.translate import _
from odoo.addons.portal.controllers.portal import pager as portal_pager, CustomerPortal
from odoo.addons.web.controllers.main import Binary



class CustomerPortal(CustomerPortal):

    def _prepare_home_portal_values(self):
        values = super(CustomerPortal, self)._prepare_home_portal_values()
        values['warehouse_count'] = request.env['warehouse.order'].search_count([
            ('state', 'in', ['warehouse', 'done', 'cancel'])
        ]) if request.env['warehouse.order'].check_access_rights('read', raise_exception=False) else 0
        return values

    def _warehouse_order_get_page_view_values(self, order, access_token, **kwargs):
        #
        def resize_to_48(b64source):
            if not b64source:
                b64source = base64.b64encode(Binary().placeholder())
            return image_process(b64source, size=(48, 48))

        values = {
            'order': order,
            'resize_to_48': resize_to_48,
        }
        return self._get_page_view_values(order, access_token, values, 'my_warehouses_history', True, **kwargs)

    @http.route(['/my/warehouse', '/my/warehouse/page/<int:page>'], type='http', auth="user", website=True)
    def portal_my_warehouse_orders(self, page=1, date_begin=None, date_end=None, sortby=None, filterby=None, **kw):
        values = self._prepare_portal_layout_values()
        partner = request.env.user.partner_id
        warehouseOrder = request.env['warehouse.order']

        domain = []

        archive_groups = self._get_archive_groups('warehouse.order', domain) if values.get('my_details') else []
        if date_begin and date_end:
            domain += [('create_date', '>', date_begin), ('create_date', '<=', date_end)]

        searchbar_sortings = {
            'date': {'label': _('Newest'), 'order': 'create_date desc, id desc'},
            'name': {'label': _('Name'), 'order': 'name asc, id asc'},
            'amount_total': {'label': _('Total'), 'order': 'amount_total desc, id desc'},
        }
        # default sort by value
        if not sortby:
            sortby = 'date'
        order = searchbar_sortings[sortby]['order']

        searchbar_filters = {
            'all': {'label': _('All'), 'domain': [('state', 'in', ['warehouse', 'done', 'cancel'])]},
            'warehouse': {'label': _('Warehouse Booking'), 'domain': [('state', '=', 'warehouse')]},
            'cancel': {'label': _('Cancelled'), 'domain': [('state', '=', 'cancel')]},
            'done': {'label': _('Locked'), 'domain': [('state', '=', 'done')]},
        }
        # default filter by value
        if not filterby:
            filterby = 'all'
        domain += searchbar_filters[filterby]['domain']

        # count for pager
        warehouse_count = warehouseOrder.search_count(domain)
        # make pager
        pager = portal_pager(
            url="/my/warehouse",
            url_args={'date_begin': date_begin, 'date_end': date_end},
            total=warehouse_count,
            page=page,
            step=self._items_per_page
        )
        # search the Warehouse Booking to display, according to the pager data
        orders = warehouseOrder.search(
            domain,
            order=order,
            limit=self._items_per_page,
            offset=pager['offset']
        )
        request.session['my_warehouses_history'] = orders.ids[:100]

        values.update({
            'date': date_begin,
            'orders': orders,
            'page_name': 'warehouse',
            'pager': pager,
            'archive_groups': archive_groups,
            'searchbar_sortings': searchbar_sortings,
            'sortby': sortby,
            'searchbar_filters': OrderedDict(sorted(searchbar_filters.items())),
            'filterby': filterby,
            'default_url': '/my/warehouse',
        })
        return request.render("warehouse.portal_my_warehouse_orders", values)

    @http.route(['/my/warehouse/<int:order_id>'], type='http', auth="public", website=True)
    def portal_my_warehouse_order(self, order_id=None, access_token=None, **kw):
        try:
            order_sudo = self._document_check_access('warehouse.order', order_id, access_token=access_token)
        except (AccessError, MissingError):
            return request.redirect('/my')

        values = self._warehouse_order_get_page_view_values(order_sudo, access_token, **kw)
        if order_sudo.company_id:
            values['res_company'] = order_sudo.company_id
        return request.render("warehouse.portal_my_warehouse_order", values)
