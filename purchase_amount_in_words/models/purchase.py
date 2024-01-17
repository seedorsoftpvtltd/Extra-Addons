from odoo import api, fields, models

class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    amount_total_words = fields.Char("Total (In Words)", compute="_compute_amount_total_words")

    @api.depends('amount_total')
    def _compute_amount_total_words(self):
        for receipt in self:
            receipt.amount_total_words = receipt.currency_id.amount_to_text(receipt.amount_total)

class SaleOrder(models.Model):
    _inherit = "sale.order"

    amount_words_tot = fields.Char("Total (In Words)", compute="_compute_amount_words_tot")

    @api.depends('amount_total')
    def _compute_amount_words_tot(self):
        for rec in self:
            if rec.currency_id:
                rec.amount_words_tot = rec.currency_id.amount_to_text(rec.amount_total)
            else:
                rec.amount_words_tot = False