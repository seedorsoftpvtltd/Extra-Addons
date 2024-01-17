# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import http, fields
from odoo.http import request
from odoo.addons.sh_customer_rfq_portal.controllers.portal import CustomerRfqProductPortal
import json


class CustomerRfqProductPortalPack(CustomerRfqProductPortal):

    @http.route(['/my/customer_rfq_create'], type='http', auth="user", website=True)
    def create_customer_rfq(self, **post):
        del post['js_id_product_list']
        counter = 0
        lines = []
        quote_msg = {}
        if len(post) > 3:
            for i in range(0, len(post)):
                counter = counter + 1
                product = 'product_id_' + str(counter)
                product_id = post.get(product)
                pack_qty = 'pack_qty_' + str(counter)
                pack_product_qty = post.get(pack_qty)
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
                    if pack_product_qty not in ['', None, '0']:
                        line_vals.update({
                            'sh_bag_qty': int(pack_product_qty)
                        })
                    elif pack_product_qty in ['', None, '0']:
                        line_vals.update({
                            'sh_bag_qty': 1.0
                        })
                    if total_product_qty not in ['', None, '0']:
                        line_vals.update({
                            'product_uom_qty': float(total_product_qty)
                        })
                    elif total_product_qty in ['', None, '0']:
                        line_vals.update({
                            'product_uom_qty': 1.0 * product.sh_qty_in_bag
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
        return request.render("sh_customer_rfq_portal_pack.sh_portal_request_customer_rfq_product_pack", values)

    @http.route('/pack-qty-data', type="http", auth="public", website=True, csrf=False)
    def pack_qty_data(self, **kw):
        super(CustomerRfqProductPortalPack, self).pack_qty_data(**kw)
        dic = {}
        if kw and kw.get('product_id') and kw.get('product_id') != '':
            product_id = request.env['product.product'].sudo().search(
                [('id', '=', int(kw.get('product_id')))], limit=1)
            if product_id and kw.get('packtQty', False):
                dic.update({
                    'total_qty': product_id.sh_qty_in_bag * float(kw.get('packtQty'))
                })
            elif product_id and not kw.get('packtQty', False):
                dic.update({
                    'total_qty': 0.0
                })
            if product_id and product_id.image_1920:
                dic.update({
                    'image': '/web/image/product.product/'+str(product_id.id)+'/image_256',
                })
        return json.dumps(dic)
