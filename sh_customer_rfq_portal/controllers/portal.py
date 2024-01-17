# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import http, fields
from odoo.http import request
from odoo.addons.portal.controllers.portal import CustomerPortal
import json


class CustomerRfqProductPortal(CustomerPortal):

    def _prepare_portal_layout_values(self):
        values = super(CustomerRfqProductPortal,
                       self)._prepare_portal_layout_values()
        values.update({
            'page_name': 'customer_rfq_portal',
            'default_url': '/my/customer_portal_rfq',
        })
        return values

    @http.route(['/my/customer_portal_rfq'], type='http', auth="user", website=True)
    def portal_my_requestproduct_customer_rfq(self, **kw):
        values = self._prepare_portal_layout_values()
        return request.render("sh_customer_rfq_portal.sh_portal_request_customer_rfq_product", values)

    @http.route(['/my/customer_rfq_create'], type='http', auth="user", website=True)
    def create_customer_rfq(self, **post):
        if 'js_id_product_list' in post:
            del post['js_id_product_list']
        counter = 0
        lines = []
        quote_msg = {}
        if len(post) > 3:
            for i in range(0, len(post)):
                counter = counter + 1
                product = 'product_id_' + str(counter)
                product_id = post.get(product)
                total_qty = 'total_qty_' + str(counter)
                total_product_qty = post.get(total_qty)
                line_vals = {}
                if product_id != None:
                    product = request.env['product.product'].sudo().search(
                        [('id', '=', int(product_id))], limit=1)
                    line_vals.update({
                        'product_id': product.id,
                        'name': product.name,
                        'product_uom': product.uom_id.id,
                    })
                    if total_product_qty not in ['', None, '0']:
                        line_vals.update({
                            'product_uom_qty': float(total_product_qty)
                        })
                    elif total_product_qty in ['', None, '0']:
                        line_vals.update({
                            'product_uom_qty': 1.0
                        })
                if len(line_vals) > 0:
                    lines.append((0, 0, line_vals))
            order_id = request.env['sale.order'].sudo().create({
                'partner_id': request.env.user.partner_id.id,
                'date_order': fields.Datetime.now(),
                'company_id': request.env.company.id,
                'user_id': request.env.user.id,
                'partner_invoice_id': int(post.get('js_id_invoice_address_list')),
                'partner_shipping_id': int(post.get('js_id_shipping_address_list')),
            })
            if order_id:
                if post.get('note'):
                    order_id.sudo().write({
                        'note': post.get('note')
                    })
                order_id.order_line = lines
                quote_msg = {
                    'success': 'Quotation ' + order_id.name + ' created successfully.'
                }
        values = {
            'page_name': 'customer_rfq_portal',
            'default_url': '/my/customer_portal_rfq',
            'quote_msg': quote_msg,
        }
        return request.render("sh_customer_rfq_portal.sh_portal_request_customer_rfq_product", values)

    @http.route('/pack-qty-data', type="http", auth="public", website=True, csrf=False)
    def pack_qty_data(self, **kw):
        dic = {}
        if kw.get('product_id') and kw.get('product_id') != '':
            product_id = request.env['product.product'].sudo().search(
                [('id', '=', int(kw.get('product_id')))], limit=1)
            if product_id and product_id.image_1920:
                dic.update({
                    'image': '/web/image/product.product/'+str(product_id.id)+'/image_256',
                })
        return json.dumps(dic)
