# from odoo import api, fields, models,

from odoo import models, fields, api, _


class ResCompany(models.Model):
    _inherit = "res.company"

    description = fields.Text(string='Steps to Create API Key & Secret', )
