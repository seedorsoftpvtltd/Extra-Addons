# from odoo import api, fields, models,

from odoo import models, fields, api, _


class AccountMoveLine(models.Model):
    _inherit = "account.move.line"

    @api.onchange("product_id", "quantity",)
    def _onchange_product_id_account_invoice_pricelist(self):
        print('............1')

        for sel in self:
            move = self.env['account.move.line'].browse(sel.move_id.id)
            # sel['currency_id'] = move.currency_id.id
            sel['company_id'] = self.env.company
            print(sel, 'sel.................1')
            # sel['currency_id'] = sel.move_id.currency_id
            print(sel.product_id, 'product_id.............1')
            print(sel.quantity, 'quantity................1')
            print(sel.move_id.currency_id, 'sel.move_id.currency_id,...........1')
            # sel['company_id'] = self.env.company
            print(self.env.company, 'self.env.company..........1')
            # sel['company_currency_id'] = sel.company_id.currency_id
            # sel['always_set_currency_id'] = sel.currency_id or sel.company_currency_id
            if not sel.move_id.pricelist_id:
                print(sel.move_id.pricelist_id, 'sel.move_id.pricelist_id...........1')
                return


            sel.with_context(check_move_validity=False).update(
                {"price_unit": sel._get_price_with_pricelist()}

            )
            # sel.untaxed_amount = sel.quantity * sel.price_unit

            print(self.price_unit, 'price unit........................1')
            print(sel._get_price_with_pricelist(), 'sel._get_price_with_pricelist().......1')

    # @api.onchange("product_id")
    # def _onchange_product_id(self):
    #     if self.product_id:
    #         self.currency_id = self.product_id.currency_id.id


class ProductProduct(models.Model):
    _inherit = "product.product"

    ware_tax_id = fields.Many2many('account.tax', 'ware_taxes_rel', 'prod_id', 'tax_id', string='Taxes',
                                   domain=[('type_tax_use', '=', 'none')])
