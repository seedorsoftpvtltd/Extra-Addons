from odoo import models, fields, api, _
import re
from odoo.exceptions import AccessError, UserError, ValidationError

class warehouseOrder(models.Model):
    _inherit = "warehouse.order"

    @api.constrains('x_billno')
    def constraint_serial_numner(self):
        tag = self.env['pattern.template'].search([('country_id.id', '=',
                                                     self.company_id.country_id.id)])
        for rec in self:
            if rec.x_billno:
                if tag.country_id:
                    if re.match(tag.name, str(rec.x_billno)):
                        return True
                    else:
                        raise ValidationError(
                            f"Bill of Entry No should be in a correct format. Example {tag.example}")
                else:
                    raise UserError(f"{self.company_id.country_id.name} Bill of Entry pattern is not created.")