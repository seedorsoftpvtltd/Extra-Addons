from odoo import models,fields,api,_

class warehouseOrder(models.Model):
    _inherit = 'warehouse.order'

    def open_multi_product_selection_wizard(self):
        return self.env['warehouse.multi.products'].wizard_view()
    
class warehouse_multi_products(models.TransientModel):
    _name='warehouse.multi.products'
    _description = 'warehouse Multi Products Wizard'

    product_ids = fields.Many2many('product.product', string='Multi Goods to Sale')
    do_replace = fields.Boolean('Replace the Order lines with new selection')

    def wizard_view(self):
        view = self.env.ref('warehouse.view_warehouse_multi_products_wizard')
        return {
            'name': _('Multi Goods Selection'),
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'warehouse.multi.products',
            'views': [(view.id, 'form')],
            'view_id': view.id,
            'target': 'new',
        }

    def warehouse_multi_products(self):
        warehouse_order_line = self.env['warehouse.order.line']
        active_model = self._context.get('active_model', False)
        active_id = self._context.get('active_id', False)
        if active_model and active_id:
            active_record = self.env[active_model].browse(active_id)
            if active_record:
                if self.do_replace:
                    active_record.order_line.unlink()
                order_line_vals = []
                for prod in self.product_ids:
                    order_line = {
                        'order_id': active_record.id,
                        'product_id': prod.id,
                    }
                    new_order_line = warehouse_order_line.new(order_line)
                    new_order_line.onchange_product_id()
                    order_line = warehouse_order_line._convert_to_write(
                            {name: new_order_line[name] for name in new_order_line._cache})
                    order_line_vals.append((0,0,order_line))
                active_record.write({'order_line':order_line_vals})
        return True
