from odoo import models, fields, api, _
from odoo.exceptions import UserError

class ValidatePop(models.TransientModel):
    _name = 'validate.pop'

    message = fields.Text('Confirmation Message', readonly=True, default=lambda self: self._get_message())
    purchase_id = fields.Many2one('purchase.order')
    @api.model
    def _get_message(self):
        return 'You already have a confirmed purchase order. Do you want to overwrite?'

    def confirm_overwrite(self):
        purchase_order = self.purchase_id
        purchase_orders = self.env['purchase.order'].search(
            [('origin', '=', purchase_order.origin), ('state', '=', 'purchase')])

        for sale in purchase_order.order_line.sale_line_id:
            if purchase_orders:
                for purchase_sale_line in purchase_orders:
                    for line in purchase_sale_line.order_line.sale_line_id:
                        if sale.id == line.id:
                            print(purchase_sale_line)
                            purchase_sale_line.button_cancel()
                            purchase_order.button_confirm()
            else:
                raise UserError(_('No confirmed purchase order found.'))