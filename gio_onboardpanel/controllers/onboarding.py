
from odoo import http
from odoo.http import request


class OnboardingController(http.Controller):

    @http.route('/gio/onboarding_panel', auth='user', type='json')
    def gio_onboarding(self):

        company = request.env.company
        return {
            'html': request.env.ref('gio_onboardpanel.kanban_onboarding_panel').render({
                'company': company,
            })
        }
