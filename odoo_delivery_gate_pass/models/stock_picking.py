from odoo import models, fields, api


class Picking(models.Model):
    _inherit = "stock.picking"

    custom_gate_pass_id = fields.Many2one(
    	'visitor.gate.pass.custom',
    	string="Gate Pass",
        copy=False,
    )


    def view_gate_pass(self):
        action = self.env.ref('visitor_gate_pass.visitor_gate_pass_action').read()[0]
        action['domain'] = [('id', '=', self.custom_gate_pass_id.id)]

        return action

    def print_visitor_card_stock(self):
        return self.env.ref('odoo_delivery_gate_pass.stock_gate_visitor_pass_report').report_action(self)
    