from odoo import models, fields, api, _
import logging

_logger = logging.getLogger(__name__)


class ChartofAccounts(models.Model):
    _inherit = 'account.account'

    @api.model
    def search(self, args, offset=0, limit=None, order=None, count=False):
        current_company_id = self.env.company.id
        args.append(('company_id', '=', current_company_id))
        return super(ChartofAccounts, self).search(args, offset, limit, order, count)


class Products(models.Model):
    _inherit = 'product.template'

    @api.model
    def search(self, args, offset=0, limit=None, order=None, count=False):
        current_company_id = self.env.company.id
        args.append(('company_id', '=', current_company_id))
        return super(Products, self).search(args, offset, limit, order, count)


class Services(models.Model):
    _inherit = 'product.product'

    @api.model
    def search(self, args, offset=0, limit=None, order=None, count=False):
        if 'allowed_company_ids' in self._context:
            current_company_id = self._context['allowed_company_ids']
            args.append(('company_id', 'in', current_company_id))
        # current_company_id = self.env.company.id
        # args.append(('company_id', '=', current_company_id))
        return super(Services, self).search(args, offset, limit, order, count)


class HSCode(models.Model):
    _inherit = 'hs.code'

    @api.model
    def search(self, args, offset=0, limit=None, order=None, count=False):
        current_company_id = self.env.company.id
        args.append(('company_id', '=', current_company_id))
        return super(HSCode, self).search(args, offset, limit, order, count)


class Journals(models.Model):
    _inherit = 'account.journal'

    @api.model
    def search(self, args, offset=0, limit=None, order=None, count=False):
        current_company_id = self.env.company.id
        args.append(('company_id', '=', current_company_id))
        return super(Journals, self).search(args, offset, limit, order, count)


class Taxes(models.Model):
    _inherit = 'account.tax'

    @api.model
    def search(self, args, offset=0, limit=None, order=None, count=False):
        if 'allowed_company_ids' in self._context:
            current_company_id = self._context['allowed_company_ids']
            args.append(('company_id', 'in', current_company_id))
        # current_company_id = self.env.company.id
        # args.append(('company_id', '=', current_company_id))
        return super(Taxes, self).search(args, offset, limit, order, count)


class JobBooking(models.Model):
    _inherit = 'freight.operation'

    @api.model
    def search(self, args, offset=0, limit=None, order=None, count=False):
        current_company_id = self.env.company.id
        args.append(('company_id', '=', current_company_id))
        return super(JobBooking, self).search(args, offset, limit, order, count)
