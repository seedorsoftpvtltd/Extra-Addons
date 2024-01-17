from odoo import http
from odoo.http import request


class OnboardingController(http.Controller):

    @http.route('/jobbooking_onboardpanel/CFS_onboarding_panel', auth='user', type='json')
    def cfs_onboarding(self):
        company = request.env.company

        return {
            'html': request.env.ref('jobbooking_onboardpanel.jobcfs_dashboard_onboarding_panel').render({
                'company': company,
            })
        }

    @http.route('/jobbooking_onboardpanel/freight_onboarding_panel', auth='user', type='json')
    def freight_onboarding(self):
        company = request.env.company

        return {
            'html': request.env.ref('jobbooking_onboardpanel.jobfreight_dashboard_onboarding_panel').render({

            })
        }

    @http.route('/jobbooking_onboardpanel/relocation_onboarding_panel', auth='user', type='json')
    def relocation_onboarding(self):
        company = request.env.company
        return {
            'html': request.env.ref('jobbooking_onboardpanel.jobrelocation_dashboard_onboarding_panel').render({
                'company': company,
            })
        }




