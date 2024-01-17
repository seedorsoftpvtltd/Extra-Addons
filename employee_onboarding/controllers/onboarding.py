from odoo import http
from odoo.http import request


class OnboardingController(http.Controller):

    @http.route('/employee/employee_dashboard_onboarding', auth='user', type='json')
    def account_dashboard_onboarding(self):

        company = request.env.company
        print('dashboard opened!!!!!!!!!!!!!!!!!!!!1')

        # if not request.env.is_admin() or \
        #         company.employee_dashboard_onboarding_state == 'closed':
        #     return {}
        #
        return {
            'html': request.env.ref('employee_onboarding.employee_dashboard_onboarding_panel').render({
                'company': company,
                'state': company.get_and_update_employee_dashboard_onboarding_state()
            })
        }
