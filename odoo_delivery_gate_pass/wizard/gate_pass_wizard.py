from odoo import models, fields, api, _
from odoo.exceptions import Warning, UserError


class CreateVisitorGatePassWizard(models.TransientModel):
    _name = "create.visitor.gate.pass.wizard"


    gate_visitor_name = fields.Char(required=True, string="Visitor Name")
    gate_partner_id = fields.Many2one('hr.employee', required=True, string="Employee")
    gate_mobile_number = fields.Char(required=True,  string="Phone/Mobile")
    gate_purpose = fields.Text(required=True, string="Purpose")
    gate_department_id = fields.Many2one('hr.department', required=True, string="Department")
    gate_user_id = fields.Many2one('res.users', required=True, default=lambda self: self.env.user, string='Created By', readonly=True)
    gate_company_id = fields.Many2one('res.company', required=True, default=lambda self: self.env.user.company_id, string='Company', readonly=True)
    gate_out_datetime = fields.Datetime(string="Date Time Out", required=True)


    @api.onchange('gate_partner_id')
    def _onchange_partner(self):
        self.gate_department_id = self.gate_partner_id.department_id

    def create_visitor_gate_pass(self):
        gate_pass_obj = self.env['visitor.gate.pass.custom']
        gate_product_line_obj = self.env['visitor.gate.product.line.custom']
        custom_picking_id = self.env['stock.picking'].browse(self.env.context.get('active_id'))
        pass_val = {
            'gate_visitor_name': self.gate_visitor_name,
            'gate_partner_id': self.gate_partner_id.id,
            'gate_mobile_number': self.gate_mobile_number,
            'gate_purpose': self.gate_purpose,
            'gate_department_id': self.gate_department_id.id,
            'gate_user_id': self.gate_user_id.id,
            'gate_company_id': self.gate_company_id.id,
            'gate_out_datetime': self.gate_out_datetime,
            'custom_stock_picking_id': custom_picking_id.id,
        }   
        custom_gate_pass = gate_pass_obj.create(pass_val)

        custom_picking_id.write({
                'custom_gate_pass_id': custom_gate_pass.id
            })

        for line in custom_picking_id.move_ids_without_package:
            product_line = {
                'custom_product_id': line.product_id.id,
                'custom_product_uom_id': line.product_uom.id,
                'custom_product_uom_qty': line.product_uom_qty,
                'visitor_gate_pass_id': custom_gate_pass.id,
            }
            product_line_id = gate_product_line_obj.create(product_line)

        action = self.env.ref('visitor_gate_pass.visitor_gate_pass_action').read()[0]
        action['domain'] = [('id','=',custom_gate_pass.id)]
        return action
    