# -*- coding: utf-8 -*-
# Copyright (C) Softhealer Technologies.


from odoo import api, fields, models


class ShProductCustomerCode(models.Model):
    _name = 'sh.product.customer.info'
    _description = "Sh Product Customer Code"

    name = fields.Many2one(
        'res.partner', 'Customer',
        ondelete='cascade', required=True,
        help="Customer of this product")

    product_tmpl_id = fields.Many2one(
        'product.template', 'Product Template',
        index=True, ondelete='cascade')

    product_id = fields.Many2one(
        'product.product', 'Product Variant',
        help="If not set, the vendor price will apply to all variants of this product.")

    product_name = fields.Char(
        'Customer Product Name',
        help="This vendor's product name will be used when printing a request for quotation. Keep empty to use the internal one.")
    product_code = fields.Char(
        'Customer Product Code',
        help="This vendor's product code will be used when printing a request for quotation. Keep empty to use the internal one.")


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    sh_line_customer_code = fields.Char('Customer Product Code')

    sh_line_customer_product_name = fields.Char('Customer Product Name')

    @api.onchange('product_id')
    def product_id_change(self):
        res = super(SaleOrderLine, self).product_id_change()
        partners = []
        for line in self:
            if line.product_id:
                
                # Partner Parent Child Record Can Show now
                partners.append(line.order_id.partner_id.id)
                if line.order_id.partner_id and line.order_id.partner_id.child_ids:
                    for child in line.order_id.partner_id.child_ids:
                        partners.append(child.id)

                if line.order_id.partner_id and line.order_id.partner_id.parent_id:
                    partners.append(line.order_id.partner_id.parent_id.id)
                    if line.order_id.partner_id.parent_id.child_ids:
                        for child in line.order_id.partner_id.parent_id.child_ids:
                            partners.append(child.id)

                customer_code = self.env['sh.product.customer.info'].sudo().search(
                    [('name', 'in', partners), ('product_id', '=', line.product_id.id)], limit=1)

                if customer_code:
                    if customer_code.product_code:
                        line.sh_line_customer_code = customer_code.product_code
                    else:
                        line.sh_line_customer_code = False
                else:
                    line.sh_line_customer_code = False

                if customer_code:
                    if customer_code.product_name:
                        line.sh_line_customer_product_name = customer_code.product_name
                    else:
                        line.sh_line_customer_product_name = False
                else:
                    line.sh_line_customer_product_name = False

                des = " "
                if self.product_id.product_tmpl_id and customer_code:
                    if customer_code.product_code:
                        des += "[" + customer_code.product_code+"]"
                    if customer_code.product_name:
                        des += customer_code.product_name
                    line.name = des
        return res


class AccountMove(models.Model):
    _inherit = "account.move"

    @api.onchange('partner_id')
    def _onchange_partner_id(self):
        res = super(AccountMove, self)._onchange_partner_id()
        if self._origin:
            if self._origin.invoice_line_ids:
                # Partner Parent Child Record Can Show now
                partners = []
                partners.append(self.partner_id.id)
                if self.partner_id and self.partner_id.child_ids:
                    for child in self.partner_id.child_ids:
                        partners.append(child.id)

                if self.partner_id and self.partner_id.parent_id:
                    partners.append(self.partner_id.parent_id.id)
                    if self.partner_id.parent_id.child_ids:
                        for child in self.partner_id.parent_id.child_ids:
                            partners.append(child.id)
                    
                for line in self._origin.invoice_line_ids:
                    
                    customer_code = self.env['sh.product.customer.info'].sudo(
                    ).search([('name', 'in', partners),
                              ('product_id', '=', line.product_id.id)],
                             limit=1)
                    if customer_code:
                        if customer_code.product_code:
                            line.sh_line_customer_code = customer_code.product_code
                        else:
                            line.sh_line_customer_code = False
                    else:
                        line.sh_line_customer_code = False
                    if customer_code:
                        if customer_code.product_name:
                            line.sh_line_customer_product_name = customer_code.product_name
                        else:
                            line.sh_line_customer_product_name = False
                    else:
                        line.sh_line_customer_product_name = False
        return res


class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    sh_line_customer_code = fields.Char(string='Customer Product Code')
    sh_line_customer_product_name = fields.Char(string='Customer Product Name')

    def create(self, vals):
        res = super(AccountMoveLine, self).create(vals)
        for rec in res:
            if rec.product_id:
                # Partner Parent Child Record Can Show now
                partners = []
                partners.append(rec.move_id.partner_id.id)
                if rec.move_id.partner_id and rec.move_id.partner_id.child_ids:
                    for child in rec.move_id.partner_id.child_ids:
                        partners.append(child.id)
    
                if rec.move_id.partner_id and rec.move_id.partner_id.parent_id:
                    partners.append(rec.move_id.partner_id.parent_id.id)
                    if rec.move_id.partner_id.parent_id.child_ids:
                        for child in rec.move_id.partner_id.parent_id.child_ids:
                            partners.append(child.id)
                
                
                customer_code = self.env['sh.product.customer.info'].sudo(
                ).search([('name', 'in', partners),
                          ('product_id', '=', rec.product_id.id)],
                         limit=1)
                if customer_code:
                    if customer_code.product_code:
                        rec.sh_line_customer_code = customer_code.product_code
                    else:
                        rec.sh_line_customer_code = False
                else:
                    rec.sh_line_customer_code = False
                if customer_code:
                    if customer_code.product_name:
                        rec.sh_line_customer_product_name = customer_code.product_name
                    else:
                        rec.sh_line_customer_product_name = False
                else:
                    rec.sh_line_customer_product_name = False
        return res

    @api.onchange('product_id')
    def _onchange_product_id(self):
        res = super(AccountMoveLine, self)._onchange_product_id()

        for line in self:
            if line.product_id:
                
                # Partner Parent Child Record Can Show now
                partners = []
                partners.append(line.move_id.partner_id.id)
                if line.move_id.partner_id and line.move_id.partner_id.child_ids:
                    for child in line.move_id.partner_id.child_ids:
                        partners.append(child.id)
    
                if line.move_id.partner_id and line.move_id.partner_id.parent_id:
                    partners.append(line.move_id.partner_id.parent_id.id)
                    if line.move_id.partner_id.parent_id.child_ids:
                        for child in line.move_id.partner_id.parent_id.child_ids:
                            partners.append(child.id)
                    
                customer_code = self.env['sh.product.customer.info'].sudo(
                ).search([('name', 'in', partners),
                          ('product_id', '=', line.product_id.id)],
                         limit=1)
                if customer_code:
                    if customer_code.product_code:
                        line.sh_line_customer_code = customer_code.product_code
                    else:
                        line.sh_line_customer_code = False
                else:
                    line.sh_line_customer_code = False

                if customer_code:
                    if customer_code.product_name:
                        line.sh_line_customer_product_name = customer_code.product_name
                    else:
                        line.sh_line_customer_product_name = False
                else:
                    line.sh_line_customer_product_name = False

        return res
