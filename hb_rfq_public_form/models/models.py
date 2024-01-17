from odoo import api, fields, models, _


# class PurchaseOrderLine(models.Model):
#     _inherit = 'purchase.order.line'
#
#     def write(self, vals):
#         public_group = self.env.ref(
#             'base.group_public')  # Assuming 'base.group_public' is the XML ID of the public group
#         if public_group in self.env.user.groups_id:
#             # Allow access for users belonging to the public group
#             vals['user_id'] = False  # Remove any assigned user
#
#         return super(PurchaseOrderLine, self).write(vals)


class PurchaseOrderEXT(models.Model):
    _inherit = "purchase.order"

    rfq_form_url = fields.Char('RFQ Form URL', store=True)

    @api.constrains('name')
    def rfq_form_url_generate(self):
        base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')
        url = '%s/seedor/rfqform/%s' % (base_url, self.id)
        self.rfq_form_url = url
        print(self.rfq_form_url, 'url')

    def send_rfq_mail_template(self):
        template_id = self.env.ref(
            'hb_rfq_public_form.email_template_edi_rfq')

        for record in self:
            template_id.send_mail(record.id, force_send=True)
            record['state'] = 'sent'

        return True
