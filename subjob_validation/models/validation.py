from odoo import api, fields, models, _
from odoo.exceptions import UserError
class Freight_Operation(models.Model):
    _inherit='freight.operation'

    def action_create_asn(self):
        moves = super(Freight_Operation, self).action_create_asn()
        for rec in self:
            if not rec.operation_line_ids:
               raise UserError(_('Please Fill Consignment Details.'))
        return moves