from odoo import api, models, fields, _


class ReportWizard(models.TransientModel):
    _name = 'report.wizard.quant'

    partner_id = fields.Many2many('res.partner', string="Customer")
    ason_date = fields.Date('Inventory Date')
    # end_date = fields.Date('End Date')
    # overall_report = fields.Boolean('View All Records')
    product_id = fields.Many2many('product.product', string='Product')

    def view_stock_balance(self):
        if self.partner_id and not self.product_id:
            domain = [('owner_id', '=', self.partner_id.id), ('create_date', '<=', self.ason_date),
                      ("on_hand", "=", True), ('product_id.x_medium.name', '=', 'Warehouse'), ('quantity','>',0), ('location_id.usage','=','internal')]
            return {
                'type': 'ir.actions.act_window',
                'name': _('Stock Balance Report'),
                'res_model': 'stock.quant',
                'view_mode': 'tree',
                'limit': 80,
                'search_view_id': self.env.ref('stock.view_stock_quant_tree').id,
                'domain': domain,
            }
        elif not self.partner_id and self.product_id:
            prod = []
            for product in self.product_id:
                prod.append(product.id)
            part = []
            for partner in self.partner_id:
                part.append(partner.id)
            domain = [('create_date', '<=', self.ason_date),
                      ("on_hand", "=", True), ('product_id.x_medium.name', '=', 'Warehouse'), ('product_id', 'in', prod), ('quantity','>',0), ('location_id.usage','=','internal')]
            return {
                'type': 'ir.actions.act_window',
                'name': _('Stock Balance Report'),
                'res_model': 'stock.quant',
                'view_mode': 'tree',
                'limit': 80,
                'search_view_id': self.env.ref('stock.view_stock_quant_tree').id,
                'domain': domain,
            }
        elif self.partner_id and self.product_id:
            prod = []
            for product in self.product_id:
                prod.append(product.id)
            part = []
            for partner in self.partner_id:
                part.append(partner.id)
            domain = [('owner_id', 'in', part), ('create_date', '<=', self.ason_date),
                      ("on_hand", "=", True), ('product_id.x_medium.name', '=', 'Warehouse'), ('product_id', 'in', prod), ('quantity','>',0), ('location_id.usage','=','internal')]
            return {
                'type': 'ir.actions.act_window',
                'name': _('Stock Balance Report'),
                'res_model': 'stock.quant',
                'view_mode': 'tree',
                'limit': 80,
                'search_view_id': self.env.ref('stock.view_stock_quant_tree').id,
                'domain': domain,
            }
        elif not self.partner_id and not self.product_id:
            prod = []
            for product in self.product_id:
                prod.append(product.id)
            part = []
            for partner in self.partner_id:
                part.append(partner.id)
            domain = [('create_date', '<=', self.ason_date),
                      ("on_hand", "=", True), ('product_id.x_medium.name', '=', 'Warehouse'), ('quantity','>',0), ('location_id.usage','=','internal')]
            return {
                'type': 'ir.actions.act_window',
                'name': _('Stock Balance Report'),
                'res_model': 'stock.quant',
                'view_mode': 'tree',
                'limit': 80,
                'search_view_id': self.env.ref('stock.view_stock_quant_tree').id,
                'domain': domain,
            }

        else:
            domain = [("on_hand", "=", True), ('product_id.x_medium.name', '=', 'Warehouse'), ('quantity','>',0), ('location_id.usage','=','internal')]
            return {
                'type': 'ir.actions.act_window',
                'name': _('Stock Balance Report'),
                'res_model': 'stock.quant',
                'view_mode': 'tree',
                'limit': 80,
                'search_view_id': self.env.ref('stock.view_stock_quant_tree').id,
                'domain': domain,
            }

    def view_stock_balancee(self):

        # domain = [('picking_code','in',['incoming','outgoing']), ('x_job_type','=','Warehouse')]
        domain = [("on_hand", "=", True), ('product_id.x_medium.name', '=', 'Warehouse'), ('quantity','>',0), ('location_id.usage','=','internal')]
        return {
            'type': 'ir.actions.act_window',
            'name': _('Stock Balance Report'),
            'res_model': 'stock.quant',
            'view_mode': 'tree',
            'limit': 80,
            'search_view_id': self.env.ref('stock.view_stock_quant_tree').id,
            # 'views': ['list'],
            'domain': domain,
        }
