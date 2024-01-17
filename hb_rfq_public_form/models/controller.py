from odoo import http, fields, models, _
from odoo.http import request


class MyController(http.Controller):

    @http.route('/seedor/rfqform/<int:id>', type='http', auth='public', website=True)
    def handle_form(self, id, **post):
        po = request.env['purchase.order'].sudo().search([('id', '=', id)])
        tax = request.env['account.tax'].search([('type_tax_use','=','purchase')])
        print(po, 'po', id, 'id')
        if po:
            vals = {
                'po': po,
                'po_lines': po.order_line,
                'po_tax': tax,
            }
            return request.render("hb_rfq_public_form.template_rfq", vals)
        else:
            return http.request.render('hb_rfq_public_form.not_found_page')

    @classmethod
    def _auth_method_public(cls):
        return []

    @classmethod
    def _check_method_public(cls):
        return True

    @http.route('/seedor/rfqform/submit', type='http', auth='public', website=True)
    def handle_form_submission(self, **post):
        print(post, 'post')
        service_ids = [key.split('_')[-1] for key in post if key.startswith('service_id_')]
        prices = [post.get('price_' + service_id) for service_id in service_ids]
        taxes = [post.get('po_tax_id_' + service_id) for service_id in service_ids]
        qty = [post.get('service_qty_' + service_id) for service_id in service_ids]
        print(service_ids)
        print(taxes)
        print(service_ids, 'service_ids')
        for i in range(len(service_ids)):
            line_id = service_ids[i]
            price = prices[i]
            po_tax_id = taxes[i]
            po_qty = qty[i]
            print(price, po_tax_id, 'price', 'po_tax_id')
            record = request.env['purchase.order.line'].search([('id', '=', line_id)])
            if po_tax_id:
                po_tax = request.env['account.tax'].search([('id','=',po_tax_id)])
            if record:
                record.write({'price_unit': price})
                if po_tax_id:
                    record.write({'taxes_id': po_tax})
                record.write({'product_qty': po_qty})
                # record.order_id.write({'state':'to approve'})
                record.order_id.with_context(mail_notrack=True).write({'state':'to approve'})
        return request.render('hb_rfq_public_form.rfq_template_success')

