from odoo import api, fields, models, _
import requests

class SalesOrderExtend(models.Model):
    _inherit = "sale.order"


    def call_proxysupport(self):
        print(self.website_id.id)
#        url = "http://bookseedor.com:8086/seedorproxy/support/%s" % self.id
        url = "http://eiuat.seedors.com:8086/seedorproxy/support/%s" % self.id
#        url = "http://mi1.seedors.com:8086/seedorproxy/support/%s" % self.id
        response = requests.request("GET", url, verify=False)
        print(url)
        print("support")
        return True


    def action_confirm(self):
        res = super(SalesOrderExtend, self).action_confirm()
        if res:
            self.call_proxysupport()
            return True
        else:
            return False
        return res


