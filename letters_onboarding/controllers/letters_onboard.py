from odoo import http
from odoo.http import request


class OnboardingController(http.Controller):

    @http.route('/letters/letters_dashboard_onboarding', auth='user', type='json')
    def googlesheet_dashboard_onboarding(self):

        company = request.env.company


        # if not request.env.is_admin() or \
        #         company.employee_dashboard_onboarding_state == 'closed':
        #     return {}
        #
        return {
            'html': request.env.ref('letters_onboarding.letters_dashboard_onboarding_panel').render({
                'company': company,
                # 'state': company.get_and_update_employee_dashboard_onboarding_state()
            })
        }