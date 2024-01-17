from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError



class OperationTypes(models.Model):
    _inherit='res.partner'

    @api.model
    def search(self, args, offset=0, limit=None, order=None, count=False):
        if 'allowed_company_ids' in self._context:
            current_company_id = self._context['allowed_company_ids']
            args.append(('company_id', 'in', current_company_id))
        # current_company_id = self.env.company.id
        # args.append(('company_id', '=', current_company_id))
        return super(OperationTypes, self).search(args, offset, limit, order, count)
