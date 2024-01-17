# -*- encoding: utf-8 -*-
from odoo import api, models

class IrCron(models.Model):
    _inherit = 'ir.cron'

    @api.model
    def product_stock_expiration_send_email(self):
        user_ids = self.env.user.company_id.notification_user_ids
        if user_ids:
            ctx = {}
            email_list = [user.email for user in user_ids if user.email]
            if email_list:
                ctx['email_to'] = ','.join([email for email in email_list if email])
                ctx['email_from'] = self.env.user.email
                ctx['send_email'] = True
                template = self.env.ref('product_expiration_alert.email_template_product_stock_expiration')
                mail_id = template.with_context(ctx).send_mail(self.env.user.id, force_send=True, raise_exception=False)
                return mail_id
