from odoo import http
from odoo.addons.website.controllers.main import Website


class Website(Website):

   @http.route(auth='public')
   def index(self, **kw):
       super(Website, self).index()
       return http.request.render('homepage_product.index', {})