from odoo import api, fields, models, _
import requests


class SalesOrderExtend(models.Model):
    _inherit = "sale.order"


    def call_proxybook(self):
#        print(self.website_id.id)
        url = "http://miprod.seedors.com:8086/seedorproxy/bookseedor/%s" % self.id
        print(url)
        print("seedor")
        response = requests.request("GET", url, verify=False)
        return True

#    def action_confirm(self):
#        res = super(SalesOrderExtend, self).action_confirm()
#        if res:
#            self.call_proxybook()
#            return True
#        else:
#            return False
#        return res

    def action_confirm(self):
        res = super(SalesOrderExtend, self).action_confirm()
        #        return res
        if res:
            if self.website_id:
                self.call_proxybook()
                return True
            else:
                return False
        return res

class ProductprodExtend(models.Model):
    _inherit = "product.product"

    price_ids = fields.One2many('product.pricelist.item','product_id', string="Product Prices")


class SaleordlineExtend(models.Model):
    _inherit = "sale.order.line"

    x_category = fields.Many2one('product.category',related='product_id.categ_id',string="Category")

