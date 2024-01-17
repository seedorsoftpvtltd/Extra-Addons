from odoo import models, fields, api, _


class OperationType(models.Model):
    _inherit='stock.picking.type'

    @api.model
    def search(self, args, offset=0, limit=None, order=None, count=False):
        current_company_id = self.env.company.id
        args.append(('company_id', '=', current_company_id))
        return super(OperationType, self).search(args, offset, limit, order, count)
