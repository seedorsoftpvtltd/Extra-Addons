from odoo import api, fields, models, tools, osv, http, _
from odoo.exceptions import UserError, ValidationError


class GioValidation(models.Model):
    _inherit = "goods.order.line"

    @api.onchange('product_uom_qty')
    def _compute_qty_at_datee(self):
        # res = super(GioValidation, self)._compute_qty_at_date()
        for lines in self:
            if lines.product_id and lines.product_uom_qty:
                product = lines.product_id.name
                qty = lines.product_uom_qty
                virtual_qty = lines.virtual_available_at_date
                free_qty = lines.free_qty_today
                available_qty = free_qty - virtual_qty
                print(qty, 'qty', virtual_qty, 'virtual_qty', free_qty, 'free_qty', available_qty, 'available_qty')
                if qty > virtual_qty:
                    raise ValidationError(
                        _('There is no on hand for the product' + ' ' + product + ' ' + '\n'
                                                                                        'Kindly check the Quantity ! ' + '\n'
                                                                                                                      'On Hand Quantity for the product' + ' ' + product + ' ' + 'is' + ' ' + str(
                            free_qty) + '\n'
                                        'Reserved Quantity for the product' + ' ' + product + ' ' + 'is' + ' ' + str(
                            free_qty - virtual_qty) + '\n'
                                                      'Available Quantity for the product' + ' ' + product + ' ' + 'is' + ' ' + str(
                            virtual_qty)
                          ))

            # return res
    def create(self, vals):
        res = super(GioValidation, self).create(vals)
        for lines in self:
            if lines.product_id and lines.product_uom_qty:
                product = lines.product_id.name
                qty = lines.product_uom_qty
                virtual_qty = lines.virtual_available_at_date
                free_qty = lines.free_qty_today
                available_qty = free_qty - virtual_qty
                print(qty, 'qty', virtual_qty, 'virtual_qty', free_qty, 'free_qty', available_qty, 'available_qty')
                if qty > virtual_qty:
                    raise ValidationError(
                        _('There is no on hand for the product' + ' ' + product + ' ' + '\n'
                                                                                        'Kindly check the Quantity ! ' + '\n'
                                                                                                                      'On Hand Quantity for the product' + ' ' + product + ' ' + 'is' + ' ' + str(
                            free_qty) + '\n'
                                        'Reserved Quantity for the product' + ' ' + product + ' ' + 'is' + ' ' + str(
                            free_qty - virtual_qty) + '\n'
                                                      'Available Quantity for the product' + ' ' + product + ' ' + 'is' + ' ' + str(
                            virtual_qty)
                          ))
            return res

    # def write(self, vals):
    #     print('cccccvvvvv')
    #     res = super(GioValidation, self).write(vals)
    #     for lines in self:
    #         if lines.product_id and lines.product_uom_qty:
    #             product = lines.product_id.name
    #             qty = lines.product_uom_qty
    #             virtual_qty = lines.virtual_available_at_date
    #             free_qty = lines.free_qty_today
    #             available_qty = free_qty - virtual_qty
    #             print(qty, 'qty', virtual_qty, 'virtual_qty', free_qty, 'free_qty', available_qty, 'available_qty')
    #             if qty > virtual_qty:
    #                 raise ValidationError(
    #                     _('There is no on hand for the product'+ ' ' + product + ' ' +'\n'
    #                                                                                   'Kindly check the Quantity ! ' + '\n'
    #                         'On Hand Quantity for the product' + ' ' + product + ' ' + 'is' + ' ' + str(
    #                         free_qty) + '\n'
    #                                     'Reserved Quantity for the product' + ' ' + product + ' ' + 'is' + ' ' + str(
    #                         free_qty - virtual_qty) + '\n'
    #                                                   'Available Quantity for the product' + ' ' + product + ' ' + 'is' + ' ' + str(
    #                         virtual_qty)
    #                       ))
    #         return res

