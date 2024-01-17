from odoo import models, fields, api, _


class StockPicking(models.Model):
    _inherit = "stock.picking"

    multi_container_id = fields.Many2one('multiple.container')
    multi_container_ids = fields.One2many('multiple.container', 'picking_id',
                                          compute='_compute_move_without_container',
                                          inverse='_set_with_container')
    # multi_container_ids = fields.One2many('multiple.container', 'order_id')
    multi_container_ids_for_delivery = fields.One2many('multiple.container', 'picking_id')

    def _compute_move_without_container(self):
        print(self.multi_container_ids)
        multi_id = self.env['multiple.container'].search([('order_id.id', '=', self.warehouse_id.id)])
        for picking in self:
            picking.container_qty = len(multi_id)
            picking.multi_container_ids = multi_id.ids

    def _set_with_container(self):
        new_mwp = self[0].multi_container_ids
        old_mwp = self.env['multiple.container'].search([('order_id.id', '=', self.warehouse_id.id)])

        filter_newm = new_mwp.filtered(lambda x: x.id not in old_mwp.ids)
        for new in filter_newm:
            create_cont = self.env['multiple.container'].create({
                'company_id': self.company_id.id,
                'container': new.container.id,
                'container_serial_no': new.container_serial_no,
                'agent_seal': new.agent_seal,
                'developer_seal': new.developer_seal,
                'custom_seal': new.custom_seal,
                'truck_no': new.truck_no,
                'order_id': self.warehouse_id.id,
                'picking_id': self.id,
            })


    @api.constrains('multi_container_ids_for_delivery')
    def depend_container_qty(self):
        for rec in self:
            if rec.picking_type_id.name == 'Delivery Orders':
                self.container_qty = len(self.multi_container_ids_for_delivery)
