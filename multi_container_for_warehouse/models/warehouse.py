from odoo import models, fields, api, _

class warehouseOrder(models.Model):
    _inherit = "warehouse.order"

    multi_container_qty = fields.Float(string='Container Quantity',compute='compute_container_qty')
    multi_container_ids = fields.One2many('multiple.container','order_id')
    multi_pick_ids = fields.One2many('multiple.container', 'picking_id')



    def compute_container_qty(self):
        cont = self.env['multiple.container'].search([('order_id','=',self.id)])
        self.multi_container_qty = len(cont)
        self.container_qty = len(cont)

