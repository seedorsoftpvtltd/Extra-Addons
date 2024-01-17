# -*- coding: utf-8 -*-
from odoo import http

# class CurrencyScraping(http.Controller):
#     @http.route('/currency_scraping/currency_scraping/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/currency_scraping/currency_scraping/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('currency_scraping.listing', {
#             'root': '/currency_scraping/currency_scraping',
#             'objects': http.request.env['currency_scraping.currency_scraping'].search([]),
#         })

#     @http.route('/currency_scraping/currency_scraping/objects/<model("currency_scraping.currency_scraping"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('currency_scraping.object', {
#             'object': obj
#         })