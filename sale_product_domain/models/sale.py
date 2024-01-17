from odoo import models, fields, api, _

class SaleOrder(models.Model):
    _inherit = "sale.order"

    company_id = fields.Many2one('res.company', string='Company', required=True,
                                 default=lambda self: self.env.company)

class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"


    def compute_hide(self):
        enable_val = self.env['res.config.settings'].get_values()['enable_domain']
        self.set_conf = enable_val

    set_conf = fields.Boolean(string="Settings Config", compute="compute_hide")

    @api.onchange('product_id')
    def domain_change(self):
        if self.set_conf:
            return {'domain': {
                'product_id': [('type', '=', 'service'),
                               ('company_id', '=', self.order_id.company_id.id),
                               ('property_account_income_id', '!=', False),
                               ('property_account_expense_id', '!=', False),
                               ('x_medium', '=', self.order_id.medium_id.id),
                               ('x_transport', '=', self.order_id.fright_transport),
                               ('x_segment', '=', self.order_id.fright_direction), '|',
                               ('x_ocean_shipping', '=', self.order_id.fright_ocean_shipping),
                               ('x_ocean_shipping', '=', self.order_id.x_cb_type), '|',
                               ('x_land_shipping', '=', self.order_id.x_cb_type),
                               ('x_land_shipping', '=', self.order_id.fright_land_shipping), '|',
                               ('x_air_shipping', '=', self.order_id.freight_air_shipping),
                               ('x_air_shipping', '=', self.order_id.x_cb_type)]}}
        else:
            return {'domain': {
                'product_id': [('type', '=', 'service'), ('company_id', '=', self.order_id.company_id.id)]}}

        # < field
        # name = "product_id"
        # string = "Services"
        # width = "100"
        # domain = "[('type','=', 'service'), ('x_medium', '=', parent.medium_id), ('x_transport', '=', parent.fright_transport), ('x_segment', '=', parent.fright_direction),'|',('x_ocean_shipping', '=', parent.fright_ocean_shipping), ('x_ocean_shipping', '=', parent.x_cb_type),'|',('x_land_shipping', '=', parent.x_cb_type), ('x_land_shipping', '=', parent.fright_land_shipping),'|',('x_air_shipping', '=', parent.freight_air_shipping),('x_air_shipping', '=', parent.x_cb_type)]" / >
