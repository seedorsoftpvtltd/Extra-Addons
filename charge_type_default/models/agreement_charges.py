from odoo import models, fields, api, _


class AgreementCharges(models.Model):
    _inherit = "agreement.charges"

    name = fields.Char(string="Name", related="charge_unit_type.name")
