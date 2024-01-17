from odoo import models, fields, api, _
import logging


_logger = logging.getLogger(__name__)

class AccountMove(models.Model):
    _inherit='account.move'

    @api.model
    def search(self, args, offset=0, limit=None, order=None, count=False):
        current_company_id = self.env.company.id
        args.append(('company_id', '=', current_company_id))
        return super(AccountMove, self).search(args, offset, limit, order, count)

class AccountPayment(models.Model):
    _inherit='account.payment'

    @api.model
    def search(self, args, offset=0, limit=None, order=None, count=False):
        current_company_id = self.env.company.id
        args.append(('company_id', '=', current_company_id))
        return super(AccountPayment, self).search(args, offset, limit, order, count)