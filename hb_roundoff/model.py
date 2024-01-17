from odoo import api, models, fields, _


class AccountMoveroundInh(models.Model):
    _inherit = 'account.move'

    @api.constrains('amount_total','amount_residual')
    def roundoffacc(self):
        for record in self:
            print("///////////////////////////////////")
            record['amount_total'] = round(record.amount_total)
            record['amount_residual'] = round(record.amount_residual)


class AccountMovelineroundInh(models.Model):
    _inherit = 'account.move.line'

    @api.constrains('amount_total','amount_residual')
    def roundoffaccline(self):
        for record in self:
            record['amount_residual'] = round(record.amount_residual)



class SaleOrderroundInh(models.Model):
    _inherit = 'sale.order'

    @api.constrains('amount_total')
    def roundoffsale(self):
        for record in self:
            record['amount_total'] = round(record.amount_total)


class PurchaseOrderroundInh(models.Model):
    _inherit = 'purchase.order'

    @api.constrains('amount_total')
    def roundoffpurchase(self):
        for record in self:
            record['amount_total'] = round(record.amount_total)

