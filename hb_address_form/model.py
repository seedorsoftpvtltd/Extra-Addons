from odoo import api, http,  fields, models, _
import requests
import time
#from odoo.http import request


class Partner(models.Model):
    _inherit = "res.partner"

    comp_email = fields.Char(string="Company Email")
    comp_mobile = fields.Char(string="Company Mobile")
    comp_website = fields.Char(string="Company Website")
#    comp_vat = fields.Char(string="VAT/GSTIN")

class WebsiteSalee(http.Controller):

        def _get_mandatory_billing_fields(self):
            return ["name", "email", "street", "city", "country_id","company_name","comp_website","phone","street2","zip","comp_email"]

# class SalesOrderExtend(models.Model):
#     _inherit = "sale.order"
#
#
#     def call_proxy(self):
#         print(self.website_id.id)
#         if self.website_id.id == 1:
#            url = "http://bam.bookseedor.com:8086/seedorproxy/bookseedor/%s" % self.id
#            print(url)
#            print("seedor")
#            response = requests.request("GET", url, verify=False)
#            return True
#         elif self.website_id.id == 2:
#            url = "http://bam.bookseedor.com:8086/seedorproxy/support/%s" % self.id
#            response = requests.request("GET", url, verify=False)
#            print("support")
#            return True
#         else:
#            return True
#
#
#     def action_confirm(self):
#         res = super(SalesOrderExtend, self).action_confirm()
#         if res:
#             self.call_proxy()
#             return True
#         else:
#             return False
#         return res
#
#
