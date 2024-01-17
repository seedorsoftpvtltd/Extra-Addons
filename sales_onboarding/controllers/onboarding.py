
from odoo import http
from odoo.http import request


class SalesController(http.Controller):

    @http.route('/sales/sales_dashboard_onboarding', auth='user', type='json')
    def sales_dashboard_onboarding(self):
        company = request.env.company
        print('dashboard opened!!!!!!!!!!!!!!!!!!!!1')

        # if not request.env.is_admin() or \
        #         company.employee_dashboard_onboarding_state == 'closed':
        #     return {}
        #
        return {
            'html': request.env.ref('sales_onboarding.sales_dashboard_onboarding_panel').render({
                'company': company,
                # 'state': company.get_and_update_employee_dashboard_onboarding_state()
            })
        }
