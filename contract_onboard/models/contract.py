from datetime import timedelta, datetime
import calendar
from dateutil.relativedelta import relativedelta

from odoo import fields, models, api, _
from odoo.exceptions import ValidationError, UserError, RedirectWarning
from odoo.tools.misc import DEFAULT_SERVER_DATE_FORMAT, format_date
from odoo.tools.float_utils import float_round, float_is_zero
from odoo.tools import date_utils
from odoo.tests.common import Form


class Contract(models.Model):
    _inherit = "res.company"

    @api.model
    def onboard_contract3_action(self):
        company = self.env.company
        # company.sudo().set_onboarding_step_done('onboarding_step2_state')
        return {
            'type': 'ir.actions.act_window',
            'name': _('Salary Structure'),
            'res_model': 'hr.payroll.structure',
            'view_mode': 'tree',
            'limit': 99999999,
            'views': [[False, 'kanban'], [False, 'list'], [False, 'form']],
        }
