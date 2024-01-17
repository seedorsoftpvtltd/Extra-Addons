from odoo import _, api, fields, models


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    set_conf = fields.Boolean(string="Settings Config", compute="compute_hide")

    @api.depends('name')
    def compute_hide(self):
        enable_val = self.env['res.config.settings'].get_values()['enable_domain']
        self.set_conf = enable_val

    @api.onchange('product_id')
    def domain_change(self):
        if self.set_conf:
            return {'domain': {'product_id': [('type','=', 'service'), ('x_medium.name', '=', self.order_id.medium_id.name), ('x_transport', '=', self.order_id.fright_transport), ('x_segment', '=', self.order_id.fright_direction),'|',('x_ocean_shipping', '=', self.order_id.fright_ocean_shipping), ('x_ocean_shipping', '=', self.order_id.x_cb_type),'|',('x_land_shipping', '=', self.order_id.x_cb_type), ('x_land_shipping', '=', self.order_id.fright_land_shipping),'|',('x_air_shipping', '=', self.order_id.freight_air_shipping),('x_air_shipping', '=', self.order_id.x_cb_type)]}}
        else:
            return {'domain': {'product_id': [('type', '=', 'service')]}}




