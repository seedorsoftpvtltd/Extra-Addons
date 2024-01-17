# Copyright 2016-2017 LasLabs Inc.
# Copyright 2019 Simone Orsi - Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

import json

from odoo import http
from odoo.http import request

from odoo.addons.website_sale.controllers.main import WebsiteSaleForm


class WebsiteSaleForm(WebsiteSaleForm):
    @http.route(
        "/website/recaptcha/",
        type="http",
        auth="public",
        methods=["POST"],
        website=True,
        multilang=False,
    )
    def recaptcha_public(self):
        recaptcha_model = request.env["website.form.recaptcha"].sudo()
        creds = recaptcha_model._get_api_credentials(request.website)
        return json.dumps({"site_key": creds["site_key"]})

    def extract_data(self, model, values):
        """ Inject ReCaptcha validation into pre-existing data extraction """
        res = super(WebsiteSaleForm, self).extract_data(model, values)
        if model.website_form_recaptcha:
            recaptcha_model = request.env["website.form.recaptcha"].sudo()
            recaptcha_model._validate_request(request, values)
        return res
    
#    def checkout_form_validate(self, data):
#        error_message = []
#        res = super(WebsiteSaleForm, self).checkout_form_validate()
        #if self.g-recaptcha-response:
#        if not data.get('g-recaptcha-response'):
#            error_message["g-recaptcha-response"](_('Please click on captcha.'))
#        return error_message
        # else:
        #     return res

