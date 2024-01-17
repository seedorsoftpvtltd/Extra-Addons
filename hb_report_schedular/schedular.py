from odoo import api, fields, models, _
import requests
import time
import sys
import requests
import json
from odoo.http import request


class payrollRep(models.Model):
    _inherit = 'hr.payslip'
    
#    trigger = fields.Boolean(string='Trigger',compute='_trigger')
   
#    @api.depends('state')
#    def _trigger(self):
#        for rec in self:
#            if rec.state == 'done':
#                rec['trigger'] = True
#            else:
#                rec['trigger'] = False


#    def trigger(self):
#        self.env.cr.execute("SELECT state FROM hr_payslip WHERE id=%s", (self.id,))
#        ding = self.env.cr.fetchone()
#        print(ding[0])
#        if ding[0] == 'done':
#            self.trig_payslip_report()

#    def write(self, vals):
#        res = super(payrollRep, self).write(vals)
#        print(res,'ressssssss')
#        for rec in self:
#            if res == True and rec.state == 'done':
#                self._cr.execute("UPDATE hr_payslip SET state='done' WHERE id=%s", (rec.id,))
#                print(rec.state, 'statew')
#                rec.trigger()
#                print(rec)
#        return res

    def write(self, vals):
        res = super(payrollRep, self).write(vals)
        for rec in self:
            if rec.state == 'done':
                rec.trig_payslip_report()
            if rec.state == 'paid':
                rec.trig_payslip_report()
            print(rec.state, 'state')
        return res


    def trig_payslip_report(self):
        payload = json.dumps({
            "params": {
                "clientid": str(self.env.cr.dbname),
                "poll_status": "true",
            }
        })

        print(payload)
        headers = {
            'Content-Type': 'application/json'
        }
        #url = "http://report.seedors.com:9014/start-job"
        url = "http://eiuat.seedors.com:8290/services/etl-control/emolument-report-trigger"
        print(url)
        response = requests.request("PUT", url, headers=headers, data=payload, verify=False)
        print(response.text)
        print(response)
        print(response.status_code)
        print("//////////////////////////////////////////////")

        return True

#    def write(self, vals):
#        res = super(payrollRep, self).write(vals)
#        for rec in self:
#            if rec.trigger == True:
#                rec.trig_payslip_report()
#            if rec.state == 'paid':
#                rec.trig_payslip_report()
#        return res





