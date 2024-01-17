from odoo import http
from odoo.http import request


class CalendarController(http.Controller):

    @http.route('/calendar/calendar_dashboard_onboarding', auth='user', type='json')
    def calendar_dashboard_onboarding(self):
        company = request.env.company
        print('dashboard opened!!!!!!!!!!!!!!!!!!!!1')

        # if not request.env.is_admin() or \
        #         company.employee_dashboard_onboarding_state == 'closed':
        #     return {}
        #
        return {
            'html': request.env.ref('calendar_onboard.calendar_dashboard_onboarding_panel').render({
                'company': company,
                # 'state': company.get_and_update_employee_dashboard_onboarding_state()
            })
        }