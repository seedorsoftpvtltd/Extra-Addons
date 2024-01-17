from odoo import api, models, fields, _


class ReportWizard(models.TransientModel):
    _name = 'reportt.wizardd'

    partner_id = fields.Many2one('res.partner', string="Customer")
    product_id = fields.Many2many('product.product', string="Product")
    start_date = fields.Date('Start Date')
    end_date = fields.Date('End Date')
    overall_report = fields.Boolean('View All Records')

    def view_stock_movement(self):
        if self.product_id:
            id = []
            for prod in self.product_id:
                id.append(prod.id)
            domain = [('owner_id', '=', self.partner_id.id), ('create_date', '>=', self.start_date),
                      ('create_date', '<=', self.end_date), ('picking_code', 'in', ['incoming', 'outgoing']),
                      ('product_id.item', '!=', False),
                      ('product_id', 'in', id)
                      ]
            return {
                'type': 'ir.actions.act_window',
                'name': _('Stock Movement Report'),
                'res_model': 'stock.move.line',
                'view_mode': 'tree',
                'limit': 80,
                'search_view_id': self.env.ref('stock.view_move_line_tree').id,
                # 'views': ['list'],
                'domain': domain,
            }
        else:
            domain = [('owner_id', '=', self.partner_id.id), ('create_date', '>=', self.start_date),
                      ('create_date', '<=', self.end_date), ('picking_code', 'in', ['incoming', 'outgoing']),
                      ('product_id.item', '!=', False)
                      ]
            return {
                'type': 'ir.actions.act_window',
                'name': _('Stock Movement Report'),
                'res_model': 'stock.move.line',
                'view_mode': 'tree',
                'limit': 80,
                'search_view_id': self.env.ref('stock.view_move_line_tree').id,
                # 'views': ['list'],
                'domain': domain,
            }
        # domain = [('owner_id', '=', self.partner_id.id), ('create_date','>=',self.start_date),
        #           ('create_date','<=',self.end_date), ('picking_code','in',['incoming','outgoing']), ('x_job_type','=','Warehouse')]

    def view_stock_movementt(self):
        if self.product_id:
            id = []
            for prod in self.product_id:
                id.append(prod.id)
            domain = [('picking_code', 'in', ['incoming', 'outgoing']),
                      ('product_id.item', '!=', False),
                      ('product_id', 'in', id)]
            return {
                'type': 'ir.actions.act_window',
                'name': _('Stock Movement Report'),
                'res_model': 'stock.move.line',
                'view_mode': 'tree',
                'limit': 80,
                'search_view_id': self.env.ref('stock.view_move_line_tree').id,
                # 'views': ['list'],
                'domain': domain,
            }
        else:
            domain = [('picking_code', 'in', ['incoming', 'outgoing']),
                      ('product_id.item', '!=', False)
                      ]
            return {
                'type': 'ir.actions.act_window',
                'name': _('Stock Movement Report'),
                'res_model': 'stock.move.line',
                'view_mode': 'tree',
                'limit': 80,
                'search_view_id': self.env.ref('stock.view_move_line_tree').id,
                # 'views': ['list'],
                'domain': domain,
            }

        # domain = [('picking_code','in',['incoming','outgoing']), ('x_job_type','=','Warehouse')]

# class ReportWizardd(models.Model):
#     _inherit = 'stock.move.line'
#
#     def action_generate_wizard(self):
#         return {
#             'type': 'ir.actions.act_window',
#             'view_mode': 'form',
#             'res_model': 'reportt.wizardd',
#             'views': [(False, 'form')],
#             'view_id': False,
#             'target': 'new',
#             'context': self.env.context,
#         }
