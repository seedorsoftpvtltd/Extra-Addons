from odoo import api, fields, models
import base64
from datetime import datetime
class report(models.Model):

    _inherit='sale.order'

    @api.model
    def orders_line(self):

            details = []
            for rec in self:
                curr_date=datetime.now().strftime('%m/%d/%Y')
                if rec.date_order == curr_date:
                     for line in rec.order_line:
                         product=line.product_id
                         quantity=line.qty_invoiced
                         amount=line.price_subtotal
                     details.append({'product':product, 'quantity': quantity, 'amount': amount})



    def monthlyreport(self):

            template = self.env.ref(
                'odoo_mo_monthlysales.email_monthly_salessss').render_qweb_pdf(self.id)
            data_record = base64.b64encode(template[0])
            ir_values = {
            'name': "Daily Sales Report",
            'type': 'binary',
            'res_model':'sale.order',
            'datas': data_record,
            'store_fname': data_record,
            'mimetype': 'application/x-pdf',
            }

            data_id = self.env['ir.attachment'].create(ir_values)
            template = self.env.ref('odoo_mo_monthlysales.email_template_sale_report')
            template.attachment_ids = [(6, 0, [data_id.id])]
            # email_values = {'email_to': self.env.user.email,
            #                 'email_from': self.env.user.email}
            template.sudo().send_mail(self.id, force_send=True)

            # template.attachment_ids = [(3, data_id.id)]
            return True

