from odoo import api, fields, models, _
import requests


class delchrng(models.AbstractModel):
    _inherit = 'base'

 
    ####################   FOR MOBILE APP DELIVERY CONCEPT    #################
    def seedor_del_chrg(self, product_id, quantity, total):
      # product_id = [5, 4, 1, 3]
        wei = 0
        vol = 0
        for pro in product_id:
            prod = self.env['product.product'].search([('id', '=', pro)])
            print(prod, '------------------------------Product ID-------------------------------')
            print(prod.weight, prod.volume, 'Weight, Volume')
            wei += prod.weight
            vol += prod.volume
        # total = 100
        weight = wei
        volume = vol
        # quantity = 40
        print('total:', total, 'weight:', weight, 'volume:', volume, 'quantity:', quantity, '----------------Input for _get_price_from_picking---------------- ')
        carr_id = self.env['delivery.carrier'].search([('name', '=', 'Seedor Delivery Charge')])
        # price_based_rule = carr_id._get_price_from_picking(total, weight, volume, quantity)
        # print(price_based_rule,'hbhbhb')
        if carr_id.delivery_type == 'base_on_rule':
            if carr_id.price_rule_ids:
                price_based_rule = carr_id._get_price_from_picking(total, weight, volume, quantity)
                print(price_based_rule)
                if price_based_rule <= 0:
                    msg = "The shipping is free since the order amount exceeds %.2f." % (carr_id.amount)
                    print(price_based_rule, msg, '----------------Delivery Charge------------------')
                    return price_based_rule, msg
                else:
                    print(price_based_rule, '----------------Delivery Charge------------------')
                    return price_based_rule,'ok'
            else:
                price = 0
                amnt = float(price) * (1.0 + (carr_id.margin / 100.0))
                if total <= carr_id.amount:
                    print(amnt)
                    return amnt, 'ok'
                else:
                    amnt = 0
                    msg = "The shipping is free since the order amount exceeds %.2f." % (carr_id.amount)
                    print(amnt, msg, '----------------Delivery Charge------------------')
                    return amnt, msg, 'ok'


        else:
            if carr_id.delivery_type == 'fixed':
                price = carr_id.fixed_price
                amnt =[]
                amnt2 = float(price) * (1.0 + (carr_id.margin / 100.0))
                amnt.append(amnt2)
                if total <= carr_id.amount:
                    print(amnt)
                    return amnt, 'ok'
                else:
                    amnt = 0
                    msg = "The shipping is free since the order amount exceeds %.2f." % (carr_id.amount)
                    print(amnt, msg, '----------------Delivery Charge------------------')

                    return amnt, msg, 'ok'


# class DelChrg(models.Model):
#     _inherit = "sale.order"
#
#     delivery_charge = fields.Boolean(string="Delivery Charge")
#
#     def create(self, vals):
#         res = super(DelChrg, self).create(vals)
#         for rec in res:
#             if rec.delivery_charge == True:
#                 product = self.env['product.product'].search([('name', '=', 'Delivery Charge')])
#                 vals = {
#                     'product_id': product.id,
#                     'name': product.name,
#                     'order_id': rec.id,
#                     'tax_id': product.taxes_id,
#                 }
#                 print(vals)
#                 rec.order_line.create(vals)
#                 return res
#             else:
#                 return res
#
#     def write(self, vals):
#         res = super(DelChrg, self).write(vals)
#         for rec in self:
#             if rec.delivery_charge == True:
#                 product = self.env['product.product'].search([('name', '=', 'Delivery Charge')])
#                 vals = {
#                     'product_id': product.id,
#                     'name': product.name,
#                     'order_id': rec.id,
#                     'tax_id': product.taxes_id,
#                 }
#                 print(vals)
#                 rec.order_line.create(vals)
#                 return res
#             else:
#                 return res

