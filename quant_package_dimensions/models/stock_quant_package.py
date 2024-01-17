# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

import json
import logging

from odoo import api, fields, models, _
from odoo.addons.base.models.res_partner import WARNING_MESSAGE, WARNING_HELP
from odoo.exceptions import ValidationError
from odoo.tools.float_utils import float_round

_logger = logging.getLogger(__name__)


class stockQuantPackage(models.Model):
    _inherit = 'stock.quant.package'

    dimension = fields.Char('Dimension')
    gross_weight = fields.Float('Gross weight', default=0.0)