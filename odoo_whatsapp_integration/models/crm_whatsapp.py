from odoo import models, fields, api, _

class SaleOrderValidation(models.Model):
    _inherit = 'crm.lead'

    def crm_whatsapps(self):
        if self.mobile:
            self.env['whatsapp.wizard'].write({'mobile_number':self.mobile})
        record_phone = self.mobile
        if not record_phone[0] == "+":
            view = self.env.ref('odoo_whatsapp_integration.warn_message_wizard')
            view_id = view and view.id or False
            context = dict(self._context or {})
            context['message'] = "No Country Code! Please add a valid mobile number along with country code!"
            return {
                'name': 'Invalid Mobile Number',
                'type': 'ir.actions.act_window',
                'view_type': 'form',
                'view_mode': 'form',
                'res_model': 'display.error.message',
                'views': [(view.id, 'form')],
                'view_id': view.id,
                'target': 'new',
                'context': context
            }
        else:
            return {'type': 'ir.actions.act_window',
                    'name': _('Whatsapp Message'),
                    'res_model': 'whatsapp.wizard',
                    'target': 'new',
                    'view_mode': 'form',
                    'view_type': 'form',
                    'context': {
                        'default_mobile_number': self.mobile,
                        'default_template_id': self.env.ref('odoo_whatsapp_integration.whatsapp_crm_template').id},
                    }