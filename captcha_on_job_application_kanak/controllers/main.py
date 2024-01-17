# -*- coding: utf-8 -*-

from odoo import http
from odoo.http import request
from odoo.addons.website_form.controllers.main import WebsiteForm


class WebsiteFormCustom(WebsiteForm):
    @http.route('/website_form/<string:model_name>', type='http', auth="public", methods=['POST'], website=True)
    def website_form(self, model_name, **kwargs):
        if model_name == 'hr.applicant':
            if 'g-recaptcha-response' in kwargs:
                if request.website.is_captcha_valid(kwargs['g-recaptcha-response']):
                    del kwargs['g-recaptcha-response']
                    return super(WebsiteFormCustom, self).website_form(model_name, **kwargs)
                else:
                    return super(WebsiteFormCustom, self).website_form(None, **kwargs)
            else:
                return super(WebsiteFormCustom, self).website_form(None, **kwargs)
        return super(WebsiteFormCustom, self).website_form(model_name, **kwargs)
