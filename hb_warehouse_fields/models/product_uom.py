from odoo import fields, models, api, _


class product_uom_wizardd(models.TransientModel):
    _name = 'product.uom.wizardd'

    multi_uom_lines = fields.One2many('multi.uom.qtyy', 'product_uom_id', string="Available Quantity  By UOM ")
    uom_id = fields.Many2one('uom.uom', string="Default UOM", readonly=True)

    @api.model
    def default_get(self, fields_list):
        lst = []
        res = super(product_uom_wizardd, self).default_get(fields_list)
        if self._context.get('active_id'):
            ware_id = self.env['warehouse.order.line'].browse(self._context.get('active_id'))
            print(ware_id)
            prod_id = ware_id.product_id
            print(prod_id)
            print(prod_id.uom_id.category_id.id)
            uom_ids = self.env['uom.uom'].search([('category_id', '=', prod_id.uom_id.category_id.id)])
            print(uom_ids)
#            for each in uom_ids:
#                available_qty = prod_id.uom_id._compute_quantity(prod_id.qty_available, each)
#                lst += [(0, 0, {'uom_id': each.id, 'available_qty': available_qty,
#                                'product_id': prod_id})]
#            res.update({'multi_uom_lines': lst, 'uom_id': prod_id.uom_id.id})
            for each in uom_ids:
                available_qty = prod_id.uom_id._compute_quantity(ware_id.qty_received, each)
                lst += [(0, 0, {'uom_id': each.id, 'available_qty': available_qty,
                                'product_id': prod_id})]
            res.update({'multi_uom_lines': lst, 'uom_id': prod_id.uom_id.id})
        return res


class multi_uom_qtyy(models.TransientModel):
    _name = 'multi.uom.qtyy'

    product_uom_id = fields.Many2one('product.uom.wizardd', string="UOM")
    uom_id = fields.Many2one('uom.uom', string="UOM")
    available_qty = fields.Float(string="Available Quantity")



