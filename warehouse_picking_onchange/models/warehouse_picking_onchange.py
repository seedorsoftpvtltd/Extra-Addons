# from odoo import api, fields, models,

from odoo import models, fields, api, _


class warehouseOrder(models.Model):
    _inherit = 'warehouse.order'

    @api.onchange('x_ware')
    def _onchange_x_ware(self):
        if self.x_ware:
            picking_type = self.env['stock.picking.type'].search([
                ('warehouse_id', '=', self.x_ware.id),
                ('code', '=', 'incoming')
            ], limit=1)
            self.picking_type_id = picking_type
        else:
            self.picking_type_id = False
