from odoo import api, fields, models, _
from odoo.http import request
import os
from odoo.exceptions import UserError, AccessError, MissingError, ValidationError
import datetime


class warehouseorderline(models.Model):
    _inherit = 'qc.inspection'
