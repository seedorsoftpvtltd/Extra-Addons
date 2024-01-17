from odoo import models, fields, api, _
import html2text
import urllib.parse as parse


# class CRM_whatsapp(models.Model):
#     _inherit = 'crm.lead'
#
#     def chatter_msg(self):
#         # self.env['crm.lead'].write(
#             self.message_post(body=self.env.ref('odoo_whatsapp_integration.whatsapp_crm_template').body_html,
#                               subject="CRM Whatsapp Message")

class SendContactMessage(models.TransientModel):
    _name = 'whatsapp.wizard.crm'

    user_id = fields.Many2one('res.partner', string="Recipient Name", default=lambda self: self.env[self._context.get('active_model')].browse(self.env.context.get('active_ids')))
    mobile_number = fields.Char(required=True, store=True)
    message = fields.Text(string="Message",track_visibility='always')
    l_id=fields.Char(related='lead_id.mobile',readonly=False)
    template_id = fields.Many2one('mail.template', 'CRM Template', index=True ,track_visibility='always')
    lead_id=fields.Many2one('crm.lead',string='Lead')
    templateee_id = fields.Many2one(
        'mail.template', 'Message')
    model = fields.Char('mail.template.model_id')
    @api.onchange('template_id')
    def onchange_template_id_wrapper(self):
        self.ensure_one()
        res_id = self._context.get('active_id') or 1
        values = self.onchange_template_id(self.template_id.id, self.model, res_id)['value']
        for fname, value in values.items():
            setattr(self, fname, value)

    def onchange_template_id(self, template_id, model, res_id):
        if template_id:
            values = self.generate_email_for_composer(template_id, [res_id])[res_id]
        else:
            default_values = self.with_context(default_model=model, default_res_id=res_id).default_get(
                ['model', 'res_id', 'partner_ids', 'message'])
            values = dict((key, default_values[key]) for key in
                          ['body', 'partner_ids']
                          if key in default_values)
        values = self._convert_to_write(values)
        return {'value': values}

    def generate_email_for_composer(self, template_id, res_ids, fields=None):
        multi_mode = True
        if isinstance(res_ids, int):
            multi_mode = False
            res_ids = [res_ids]
        if fields is None:
            fields = ['body_html']
        returned_fields = fields + ['partner_ids']
        values = dict.fromkeys(res_ids, False)
        template_values = self.env['mail.template'].with_context(tpl_partners_only=True).browse(
            template_id).generate_email(res_ids, fields=fields)
        for res_id in res_ids:
            res_id_values = dict((field, template_values[res_id][field]) for field in returned_fields if
                                 template_values[res_id].get(field))
            res_id_values['message'] = html2text.html2text(res_id_values.pop('body_html', ''))
            values[res_id] = res_id_values

        return multi_mode and values or values[res_ids[0]]

    def send_custom_contact_message(self):
        # id = self.env['crm.lead'].browse(self.env.context.get('active_id'))
        if self.message:
            msgi=self.message
            print(";;;;;;;;;;")
            print(msgi)
            message_string = ''
            message = self.message.split(' ')
            for msg in message:
                message_string = message_string + msg + '%20'
            message_string = message_string[:(len(message_string) - 3)]
            # number = self.user_id.mobile
            print(self.mobile_number)
            mobno =self.l_id
            link = "https://web.whatsapp.com/send?phone=" + self.mobile_number
            send_msg = {
                'type': 'ir.actions.act_url',
                'url': link + "&text=" + message_string,
                'target': 'new',
                'res_id': self.id,


            }
            self.chatter_msg_crm(msgi)
            print(msgi)
            return send_msg


    def chatter_msg_crm(self,msgi):
        id = self.env['crm.lead'].browse(self.env.context.get('active_id'))
        print(msgi)
        res = id.message_post(body=msgi,
                              subject="CRM Whatsapp Message")
        return res

class chatter_msg(models.Model):
   _inherit='crm.lead'
   # def chatter_msg(self):
   #    id = self.env['crm.lead'].browse(self.env.context.get('active_id'))
   #    res = id.message_post(body=self.env.ref('odoo_whatsapp_integration.whatsapp_crm_template').body_html,subject="CRM Whatsapp Message")
   #    return res

