from odoo.addons.portal.controllers.web import Home
from odoo import http
from odoo.http import request


class WebsiteSort(Home):

   @http.route()
   def index(self, **kw):
       super(WebsiteSort, self).index()
       website_product_ids = request.env['product.template'].search([('is_published', '=', True)])
       #website_product_ids = request.env['product.template']
       return request.render('website.homepage', {
           'website_product_ids': website_product_ids
       })