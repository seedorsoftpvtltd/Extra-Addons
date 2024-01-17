from odoo import api, fields, models, _
import json
import requests
from odoo.exceptions import UserError


class workflow(models.AbstractModel):
    _inherit = 'base'

    # process_def = fields.Text('Process Definition')
    # client_id = fields.Text('Client Id')
    # variables = fields.Text('Variables')
    #
    # @api.constrains('process_def','client_id','variables')
    # def workflow(self):
    #     print(self.env.cr.dbname)
    #     print(self._name)
    #     print(self.variables)
    #     payload = json.dumps({
    #         "processdefinition": self.process_def,
    #         "clientKey": self.client_id,
    #         "variable": self.variables,
    #     })
    #
    #     print(payload, '//////////////////////////////')
    #     headers = {
    #         'Content-Type': 'application/json'
    #     }
    #     url = "http://eiuat.seedors.com:8084/start-process"
    #     print(url)
    #     response = requests.request("POST", url, headers=headers, data=payload, verify=False)
    #     print(response.text)
    #     print(response)
    #     print(response.status_code)
    #     if response.status_code == 500:
    #         raise UserError(_('%s') % response.text)
    #     elif response.status_code == 400:
    #         raise UserError(_('%s') % response.text)
    #     elif response.status_code == 404:
    #         raise UserError(_('%s') % response.text)



    def workflow(self, process_def, client_id, variables):
        print(self.env.cr.dbname)
        print(self._name)
        print(variables)
        payload = json.dumps({
            "processdefinition": process_def,
            "clientKey": client_id,
            "variable": variables,
        })

        print(payload)
        headers = {
            'Content-Type': 'application/json'
        }
        url = "http://eiuat.seedors.com:8084/start-process"
        print(url)
        response = requests.request("POST", url, headers=headers, data=payload, verify=False)
        print(response.text)
        print(response)
        print(response.status_code)
        if response.status_code == 500:
            raise UserError(_('%s') % response.text)
        elif response.status_code == 400:
            raise UserError(_('%s') % response.text)
        elif response.status_code == 404:
            raise UserError(_('%s') % response.text)

