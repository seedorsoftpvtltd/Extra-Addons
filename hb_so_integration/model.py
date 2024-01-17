from odoo import api, models, fields, _
from odoo.exceptions import AccessError, UserError, ValidationError
import requests
import json


class SOIntegration(models.Model):
    _inherit = 'sale.order'

    so_copy_status = fields.Selection([('done', 'SO copied to Destination DB'), ('error', 'SO not copied to Destination DB')] , string="SO Status")

    def so(self):
        print(self.env.cr.dbname)
        payload = json.dumps({"orderid": self.id,"db": str(self.env.cr.dbname)})

        print(payload)
        headers = {
            'Content-Type': 'application/json'
        }
#        url = "http://eiuat.seedors.com:8290/subscription"
        url = "https://miprod.seedors.com/subscription"
        print(url)
        response = requests.request("POST", url, headers=headers, data=payload, verify=False)
        print(response.text)
        print(response)
        print(response.status_code)
        if response.status_code == 200:
            self['so_copy_status'] = 'done'
            print(self.so_copy_status,'.......................................................')
        else:
            self['so_copy_status'] = 'error'
            print(self.so_copy_status,'.........................................................')
        return True

    def action_confirm(self):
        res = super(SOIntegration, self).action_confirm()
        if res:
            self.so()
        return res
