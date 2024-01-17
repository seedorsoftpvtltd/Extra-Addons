from odoo import models, fields, api, _

class SaleEstimate(models.Model):
    _inherit = 'sale.estimate.line.job'

    def compute_hide(self):
        enable_val = self.env['res.config.settings'].get_values()['enable_domain']
        self.set_conf = enable_val

    set_conf = fields.Boolean(string="Settings Config", compute="compute_hide")



    @api.onchange('product_id')
    def domain_change(self):
        if self.set_conf:
            return {'domain': {
                'product_id': [('company_id','=',self.estimate_id.company_id.id),'|',('type','=', 'service'), ('x_medium', '=', self.estimate_id.x_esti_type),
                               ('x_transport', '=', self.estimate_id.x_transport_esti),
                               ('x_segment', '=', self.estimate_id.x_segment_esti),
                               ('x_ocean_shipping', '=', self.estimate_id.x_ocean_shipping_esti),
                               ('x_land_shipping', '=', self.estimate_id.x_land_shipping_esti),
                               ('x_air_shipping', '=', self.estimate_id.x_air_shipping_esti)]}}
        else:
            return {'domain': {'product_id': [('type', '=', 'service'),('company_id','=',self.estimate_id.company_id.id)]}}


# domain="['|',('type','=', 'service'), ('x_medium', '=', parent.x_esti_type), ('x_transport', '=', parent.x_transport_esti), ('x_segment', '=', parent.x_segment_esti), ('x_ocean_shipping', '=', parent.x_ocean_shipping_esti), ('x_land_shipping', '=', parent.x_land_shipping_esti), ('x_air_shipping', '=', parent.x_air_shipping_esti)]"