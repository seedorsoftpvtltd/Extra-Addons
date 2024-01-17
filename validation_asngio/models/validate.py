from odoo import models, api, exceptions


class WarehouseASNOrder(models.Model):
    _inherit = 'warehouse.order'

    def button_confirm(self):
        for order in self:
            if not order.order_line:
                raise exceptions.ValidationError("Kindly add the products in goods tab")
        return super(WarehouseASNOrder, self).button_confirm()


class WarehouseGIOOrder(models.Model):
    _inherit = 'goods.issue.order'

    def action_confirm(self):
        for gio in self:
            if not gio.order_line:
                raise exceptions.ValidationError("Kindly add the products in goods order lines tab")
        return super(WarehouseGIOOrder, self).action_confirm()

