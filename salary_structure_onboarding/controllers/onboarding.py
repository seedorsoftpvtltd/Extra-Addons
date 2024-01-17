from odoo import http
from odoo.http import request


class SalaryStructureController(http.Controller):

    @http.route('/salary_structure/salary_structure_dashboard_onboarding', auth='user', type='json')
    def salary_structure_dashboard_onboarding(self):
        company = request.env.company
        print('dashboard opened!!!!!!!!!!!!!!!!!!!!')

        # if not request.env.is_admin() or \
        #         company.employee_dashboard_onboarding_state == 'closed':
        #     return {}
        #
        return {
            'html': request.env.ref('salary_structure_onboarding.salary_structure_dashboard_onboarding_panel').render({
                'company': company,
                # 'state': company.get_and_update_employee_dashboard_onboarding_state()
            })
        }