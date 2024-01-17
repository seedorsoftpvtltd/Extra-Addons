from odoo import models, fields, api,_
from base64 import b64decode

class wizard_whataspp_payslip(models.Model):

   _name="wizard.whatsapp.payslip"
   mobile_number = fields.Char(required=True, store=True)
   attachment_ids = fields.Many2one('ir.attachment',string='Attachments')


   def send_custom_payslip_message(self):

      if self.attachment_ids:

         message_string = ''
         base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')
         message = self.attachment_ids
         path = message.local_url



         number = self.mobile_number

         link = "https://web.whatsapp.com/send?phone=" + number
         send_msg = {
            'type': 'ir.actions.act_url',
            'url': link + "&text="+base_url +path ,
            'target': 'new',
            'res_id': self.id,
         }
         return send_msg
