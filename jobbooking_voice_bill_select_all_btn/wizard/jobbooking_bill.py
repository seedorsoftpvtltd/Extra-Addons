from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class CreatePatientWizard(models.TransientModel):
    _inherit = "create.bill.wizard"
    _description = "Create Bill Wizard"

    selectall = fields.Boolean(string="Select All")

    @api.onchange('selectall')
    def onchange_select(self):
        for rec in self.service_ids:
            if self.selectall:
                rec.isbill = True
            else:
                rec.isbill = False
