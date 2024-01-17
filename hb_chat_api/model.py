from odoo import api, fields, models, _ 
import requests 
import time

#_logger = logging.getLogger(__name__)


class MailMessage(models.Model):
    _inherit = 'mail.message'

    # call = fields.Boolean(string="Call", compute='_call')
#     channel_type = fields.Selection(string="Channel Type", related='channel_ids.channel_type')
    channel_type = fields.Selection(related="channel_ids.channel_type", string="Channel type")
    res_id = fields.Many2oneReference('Related Document ID', index=True, model_field='model', default=1)    
   
    @api.constrains('channel_ids')
    def fieldss(self):
        for re in self:
            if re.model == 'mail.channel':
                re['record_name'] = re.channel_ids.name
                re['display_name'] = re.channel_ids.name
                re['res_id'] = re.channel_ids.id
   # @api.constrains('create')
    def call_chat(self):
        value = [];
        for m in self:
            mm = m.channel_ids
            print(mm)
            for mmm in mm:
                mmmm = mmm.channel_last_seen_partner_ids
                print(mmmm)
                for mmmmm in mmmm:
                    mmmmmm = mmmmm.partner_id
                    print(mmmmmm)
                    for mmmmmmm in mmmmmm:
                        value.append(mmmmmmm.id)
                        tt = mmmmmmm.id
        for i in value:
            url = "http://eiuat.seedors.com:8290/message-notifier/%s/%s/%s" % (
            self.env.cr.dbname, self.id, i)
#            url = "https://miprod.seedors.com/message-notifier/%s/%s/%s" % (self.env.cr.dbname, self.id, i)
            print(url)
            print(tt)
            response = requests.request("GET", url, verify=False)
            print(response.text)
#            _logger.debug('%s', url)

        print('value = '+str(value))
        # print(url)
        # response = requests.request("GET", url, verify=False)
        return True

    @api.depends('channel_ids')
    def _call(self):
        for rec in self:
            # if rec.model == 'mail.channel' and rec.channel_ids:
            if rec.model == 'mail.channel':
                rec.call = True
            else:
                print("False")
                rec.call = False

    # @api.model_create_multi
    # def create(self, values_list):
    #     messages = super(MailMessage, self).create(values_list)
    #     messages.call_chat()
    #     return messages

    def write(self, vals):

        print(self.channel_ids.id)
        for rec in self:
            if rec.record_name != False and  rec.model == 'mail.channel':
                print(rec.starred_partner_ids.id,"star")
                print(rec.record_name)
                rec.call_chat()
            res = super(MailMessage, self).write(vals)
            return res

# class Mailchannel(models.Model):
#     _inherit = 'mail.channel'
#
#     # def write(self, vals):
#     #     res = super(Mailchannel, self).write(vals)
#     #     if self.message_ids:
#     #         self.call_chat()
#     #     return res
#     @api.constrains('message_ids')
#     def call_chat(self):
#         url = "http://eiuat.seedors.com:8290/message-notifier/%s/%s" % (self.env.cr.dbname, self.id)
#         print(url)
#         response = requests.request("GET", url, verify=False)
#         return response



# @api.model_create_multi
# def create(self, values_list):
#     messages = super(MailMessage, self).create(values_list)
#     if self.channel_ids:
#         self.call_chat()
#     else:
#         print("////////////////////////////")
#
#
#     return messages
# @api.onchange('channel_ids')
# def onchange_channel_ids(self):
#     self.ensure_one()
#     self.call_chat()
# def _moderate_discard(self):
#     res = super(MailMessage, self)._moderate_discard()
#     self.call_chat()
#     return res

