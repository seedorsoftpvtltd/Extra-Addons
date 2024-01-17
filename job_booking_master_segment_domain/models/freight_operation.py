from odoo import _, api, fields, models


class FreightOperation(models.Model):
    _inherit = "freight.operation"

    set_conf = fields.Boolean(string="Settings Config", compute="compute_hide")

    @api.depends('name')
    def compute_hide(self):
        enable_val = self.env['res.config.settings'].get_values()['enable_domain']
        self.set_conf = enable_val


class OperationService(models.Model):
    _inherit = "operation.service"

    @api.onchange('product_id')
    def domain_change(self):
        if self.operation_id.set_conf:
            return {'domain': {
                'product_id': [('type', '=', 'service'), ('company_id', '=', self.operation_id.company_id.id),
                               ('property_account_income_id', '!=', False),
                               ('property_account_expense_id', '!=', False),
                               ('x_medium', '=', self.operation_id.x_job_type.id),
                               ('x_transport', '=', self.operation_id.transport),
                               ('x_segment', '=', self.operation_id.direction), '|',
                               ('x_ocean_shipping', '=', self.operation_id.ocean_shipping),
                               ('x_ocean_shipping', '=', self.operation_id.x_cb_type), '|',
                               ('x_land_shipping', '=', self.operation_id.x_cb_type),
                               ('x_land_shipping', '=', self.operation_id.land_shipping), '|',
                               ('x_air_shipping', '=', self.operation_id.freight_air_shipping),
                               ('x_air_shipping', '=', self.operation_id.x_cb_type)]}}
        else:
            return {'domain': {
                'product_id': [('type', '=', 'service'), ('company_id', '=', self.operation_id.company_id.id)]}}

# '|',('x_ocean_shipping', '=', self.operation_id.ocean_shipping), ('x_ocean_shipping', '=', self.operation_id.x_cb_type),'|',('x_land_shipping', '=', self.operation_id.x_cb_type), ('x_land_shipping', '=', self.operation_id.land_shipping),'|',('x_air_shipping', '=', self.operation_id.freight_air_shipping),('x_air_shipping', '=', self.operation_id.x_cb_type)
# <field name="product_id" string="Charges" required="1"   domain="[('type','=', 'service'), ('x_medium', '=', parent.x_job_type), ('x_transport', '=', parent.transport), ('x_segment', '=', parent.direction),'|',('x_ocean_shipping', '=', parent.ocean_shipping), ('x_ocean_shipping', '=', parent.x_cb_type),'|',('x_land_shipping', '=', parent.x_cb_type), ('x_land_shipping', '=', parent.land_shipping),'|',('x_air_shipping', '=', parent.freight_air_shipping),('x_air_shipping', '=', parent.x_cb_type)]"/>
