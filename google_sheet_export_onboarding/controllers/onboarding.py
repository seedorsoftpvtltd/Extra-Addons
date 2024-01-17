from odoo import http
from odoo.http import request


class OnboardingController(http.Controller):

    @http.route('/googlesheets/googlesheet_dashboard_onboarding', auth='user', type='json')
    def googlesheets_dashboard_onboarding(self):

        company = request.env.company


        # if not request.env.is_admin() or \
        #         company.employee_dashboard_onboarding_state == 'closed':
        #     return {}
        #
        return {
            'html': request.env.ref('google_sheet_export_onboarding.googlesheets_dashboard_onboarding_panel').render({
                'company': company,
                # 'state': company.get_and_update_employee_dashboard_onboarding_state()
            })
        }
