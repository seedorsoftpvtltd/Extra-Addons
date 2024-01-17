# -*- coding: utf-8 -*-
# Copyright 2019, 2020 Odoo VietNam
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).

from odoo import models, fields

class ResCompany(models.Model):

    _inherit = 'res.company'

    dashboard_background = fields.Binary(attachment=True)