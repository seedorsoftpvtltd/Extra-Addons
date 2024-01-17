from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class CreatePatientWizard(models.TransientModel):
    _inherit = "create.invoice.wizard"
    _description = "Create Invoice Wizard"

    selectall = fields.Boolean(string="Select All")

    @api.onchange('selectall')
    def onchange_select(self):
        for rec in self.service_ids:
            if self.selectall:
                rec.isinvoice = True
            else:
                rec.isinvoice = False
