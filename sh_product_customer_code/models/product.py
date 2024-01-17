# -*- coding: utf-8 -*-
# Copyright (C) Softhealer Technologies.

import logging
import re
from odoo import api, fields, models
from odoo.osv import expression
_logger = logging.getLogger(__name__)


class ShProductTemplate(models.Model):
    _inherit = 'product.template'

    sh_product_customer_ids = fields.One2many(
        'sh.product.customer.info', 'product_tmpl_id', string="Customer Code")

    code_id = fields.Char(
        related='sh_product_customer_ids.product_code', string='Code', readonly=False)

#     variant_customer_ids = fields.One2many(
#         'sh.product.customer.info', 'product_tmpl_id', string="Customer Variant Code")


class ShProductProduct(models.Model):
    _inherit = 'product.product'

    @api.model
    def _name_search(self, name, args=None, operator='ilike', limit=100, name_get_uid=None):

        if not args:
            args = []
        if name:
            
            positive_operators = ['=', 'ilike', '=ilike', 'like', '=like']
            product_ids = []
            partners = []
            if operator in positive_operators:
                product_ids = self._search(
                    [('default_code', '=', name)] + args, limit=limit, access_rights_uid=name_get_uid)
                if not product_ids:
                    product_ids = self._search(
                        [('barcode', '=', name)] + args, limit=limit, access_rights_uid=name_get_uid)
            if not product_ids and operator not in expression.NEGATIVE_TERM_OPERATORS:

                product_ids = self._search(
                    args + [('default_code', operator, name)], limit=limit)
                if not limit or len(product_ids) < limit:
                    # we may underrun the limit because of dupes in the results, that's fine
                    limit2 = (limit - len(product_ids)) if limit else False
                    product2_ids = self._search(
                        args + [('name', operator, name), ('id', 'not in', product_ids)], limit=limit2, access_rights_uid=name_get_uid)
                    product_ids.extend(product2_ids)
            elif not product_ids and operator in expression.NEGATIVE_TERM_OPERATORS:
                domain = expression.OR([
                    ['&', ('default_code', operator, name),
                     ('name', operator, name)],
                    ['&', ('default_code', '=', False),
                     ('name', operator, name)],
                ])
                domain = expression.AND([args, domain])
                product_ids = self._search(
                    domain, limit=limit, access_rights_uid=name_get_uid)
            if not product_ids and operator in positive_operators:
                ptrn = re.compile('(\[(.*?)\])')
                res = ptrn.search(name)
                if res:
                    product_ids = self._search([('default_code', '=', res.group(
                        2))] + args, limit=limit, access_rights_uid=name_get_uid)
            # still no results, partner in context: search on supplier info as last hope to find something
            if not product_ids and self._context.get('partner_id'):
                suppliers_ids = self.env['product.supplierinfo']._search([
                    ('name', '=', self._context.get('partner_id')),
                    '|',
                    ('product_code', operator, name),
                    ('product_name', operator, name)], access_rights_uid=name_get_uid)
                if suppliers_ids:
                    product_ids = self._search(
                        [('product_tmpl_id.seller_ids', 'in', suppliers_ids)], limit=limit, access_rights_uid=name_get_uid)
            # still no results, partner in context: search on supplier info as last hope to find something
            
            if not product_ids and self._context.get('partner_id'):
                sh_partner_id = self._context.get('partner_id')
                partners.append(sh_partner_id)

                if sh_partner_id:
                    # Partner Parent Child Record Can Show now
                    Partner = self.env['res.partner'].browse(sh_partner_id)
                    if Partner and Partner.child_ids:
                        for child in Partner.child_ids:
                            partners.append(child.id)

                    if Partner and Partner.parent_id:
                        partners.append(Partner.parent_id.id)
                        if Partner.parent_id.child_ids:
                            for child in Partner.parent_id.child_ids:
                                partners.append(child.id)
                        
                    customer_ids = self.env['sh.product.customer.info']._search([
                        ('name', 'in', partners),
                        '|',
                        ('product_code', operator, name),
                        ('product_name', operator, name)], access_rights_uid=name_get_uid)
                    if customer_ids:
                        product_ids = self._search(
                            [('product_tmpl_id.sh_product_customer_ids', 'in', customer_ids)], limit=limit, access_rights_uid=name_get_uid)
        else:
            product_ids = self._search(
                args, limit=limit, access_rights_uid=name_get_uid)
        super(ShProductProduct, self)._name_search(
            name, args=None, operator='ilike', limit=100, name_get_uid=None)
        return self.browse(product_ids).name_get()
