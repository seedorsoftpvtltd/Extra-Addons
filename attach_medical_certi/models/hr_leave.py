# -*- coding: utf-8 -*-

from odoo import api, fields, models


class HrLeave(models.Model):

    _inherit = 'hr.leave'

    is_certificate_required = fields.Boolean('Certificate Required', related='holiday_status_id.is_certificate_required')
    certificate = fields.Binary(string='Attach Certificate', attachment=True)
    file_name = fields.Char()
