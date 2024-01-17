
from odoo import api, fields, models, _
import requests
import time
#url= '';

class MailMessage(models.Model):
    _inherit = "mail.message"

    channel_type = fields.Selection(related='channel_ids.channel_type', string="Channel Type")
    
    @api.constrains('channel_ids')
    def fields(self):
        for re in self:
            re.record_name = re.channel_ids.name
            re.display_name = re.channel_ids.name    
    
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
            print(tt)
            response = requests.request("GET", url, verify=False)
            print(response.text)

            
 #       print('value = '+str(value))
        # print(url)
        # response = requests.request("GET", url, verify=False)
        return True
#                        url = "http://eiuat.seedors.com:8290/message-notifier/%s/%s/%s" %(self.env.cr.dbname, self.id, tt)
#                        print(url)

#                        print('value = '+str(value))
        # print(url)
#        response = requests.request("GET", url, verify=False)
#        return True


#    def write(self, vals):
#        res = super(MailMessage, self).write(vals)
#        self.call_chat()
#        return res


    @api.model_create_multi
    def create(self, values_list):
        messages = super(MailMessage, self).create(values_list)
#        time.sleep(10)
        messages.call_chat()
        return messages




