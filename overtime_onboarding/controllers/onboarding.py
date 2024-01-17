from odoo import http
from odoo.http import request


class OvertimeController(http.Controller):

    @http.route('/overtime/overtime_dashboard_onboarding', auth='user', type='json')
    def overtime_dashboard_onboarding(self):
        company = request.env.company
        print('dashboard opened!!!!!!!!!!!!!!!!!!!!')

        # if not request.env.is_admin() or \
        #         company.employee_dashboard_onboarding_state == 'closed':
        #     return {}
        #
        return {
            'html': request.env.ref('overtime_onboarding.overtime_dashboard_onboarding_panel').render({
                'company': company,
                # 'state': company.get_and_update_employee_dashboard_onboarding_state()
            })
        }