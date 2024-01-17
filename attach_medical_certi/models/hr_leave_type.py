# -*- coding: utf-8 -*-

from odoo import api, fields, models


class HrLeaveType(models.Model):

    _inherit = 'hr.leave.type'

    is_certificate_required = fields.Boolean('Certificate Required')
