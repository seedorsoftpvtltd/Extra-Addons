from odoo import models, fields, api

class VisitorGatePass(models.Model):
    _inherit = 'visitor.gate.pass.custom'


    gate_product_line_ids = fields.One2many(
    	'visitor.gate.product.line.custom',
    	'visitor_gate_pass_id',
    	string="Product Line",
        copy=False,
    )

    custom_stock_picking_id = fields.Many2one(
    	'stock.picking',
    	string="Picking",
        copy=False,
    )

    def view_stock_picking(self):
        action = self.env.ref('stock.action_picking_tree_all').read()[0]
        action['domain'] = [('id', '=', self.custom_stock_picking_id.id)]

        return action