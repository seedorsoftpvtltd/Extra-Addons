from odoo import models, fields, api, _


class Agreement(models.Model):
    _inherit = "product.template"

    is_default_agreement_service = fields.Boolean('Agreement Default', default=False)
