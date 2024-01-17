# from odoo import api, fields, models,

from odoo import models, fields, api, _


class HrEmployeePrivate(models.Model):
    _inherit = "hr.employee"

    last_check_in = fields.Datetime(string="Check In")
    last_check_out = fields.Datetime(string="Check Out")


class HrEmployeeBase(models.AbstractModel):
    _inherit = "hr.employee.base"

    # is_absent = fields.Boolean(store=True)

