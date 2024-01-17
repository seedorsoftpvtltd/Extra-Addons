from odoo import api, fields, models, _
from odoo.exceptions import ValidationError
import datetime
import logging
_logger = logging.getLogger(__name__)


class Warehouseorder(models.Model):
    _inherit = 'warehouse.order.line'
    x_sku_id = fields.Many2one('product.product', 'Product Code', compute='_skucode', store=False)
    x_length = fields.Float('Length', related='x_sku_id.product_length', store=True)
    x_breadth = fields.Float('Breadth', related='x_sku_id.product_width', store=True)
    x_height = fields.Float('Height', related='x_sku_id.product_height', store=True)
    x_weight = fields.Float('Weight', related='x_sku_id.weight', store=True)


    @api.depends('product_id')
    def _skucode(self):
        print('qqqqqqqqqqqq')
        for rec in self:
            if rec.product_id:
                print(rec.product_id)
                rec['x_sku_id'] = rec.product_id.id
            else:
                rec['x_sku_id'] = ''

    def _fromitemmaster(self):

        for rec in self:

            if rec.x_sku_id:
                rec['x_height'] = rec.x_sku_id.product_height
                rec['x_weight'] = rec.x_sku_id.weight
                rec['x_breadth'] = rec.x_sku_id.product_width
                rec['x_length'] = rec.x_sku_id.product_length
                rec['name'] = rec.x_sku_id.description
                rec['partner_id'] = rec.x_sku_id.customer_id.id
                rec['product_id'] = rec.x_sku_id.id
                rec['sku'] = rec.x_sku_id.name
                rec['x_volume'] = rec.x_sku_id.volume
            else:
                rec['name'] = rec.product_id.name
                rec['sku'] = rec.product_id.name


class GoodsOrderLineextend(models.Model):
    _inherit = 'goods.order.line'

    x_sku_id = fields.Many2one('product.product', string="Product Code", compute='_skucode', store=False)
    x_length = fields.Float('Length', related='x_sku_id.product_length', store=True)
    x_breadth = fields.Float('Breadth', related='x_sku_id.product_width', store=True)
    x_height = fields.Float('Height', related='x_sku_id.product_height', store=True)
    x_weight = fields.Float('Weight', related='x_sku_id.weight', store=True)

    @api.depends('product_id')
    def _skucode(self):
        for rec in self:
            print('qssssssss')

            if rec.product_id:

                rec['x_sku_id'] = rec.product_id.id
            else:
                rec['x_sku_id'] = ''

class WarehouseDelMove(models.Model):
    _inherit = 'stock.move'

    x_sku_id = fields.Many2one('product.product', 'Product Code', store=False)
    sku = fields.Char(string="sku", compute='_fromitemmaster', store=False)

    @api.depends('warehouse_line_id', 'goods_line_id')
    def _fromitemmaster(self):
        print('xxxxxxxxxxx')
        for rec in self:
            if rec.product_id.name:
                rec['x_sku_id'] = rec.product_id.id
            if rec.warehouse_line_id:
                print('sssssssssss')
                rec['x_sku_id'] = rec.warehouse_line_id.x_sku_id.id
            if rec.goods_line_id:
                rec['x_sku_id'] = rec.goods_line_id.x_sku_id.id

            if rec.x_sku_id:
                print('ccccccccccc',rec.x_sku_id.id)
                rec['x_height'] = rec.warehouse_line_id.x_height
                rec['x_weight'] = rec.warehouse_line_id.x_weight
                rec['x_breadth'] = rec.warehouse_line_id.x_breadth
                rec['x_length'] = rec.warehouse_line_id.x_length
                rec['x_volume'] = rec.warehouse_line_id.x_volume
                rec['name'] = rec.x_sku_id.product_description.name
                rec['partner_id'] = rec.x_sku_id.customer_id.id
                rec['product_id'] = rec.x_sku_id.id
                rec['sku'] = rec.x_sku_id.name

            else:
                rec['name'] = rec.product_id.name
                rec['sku'] = rec.product_id.name



class Warehousemoveline(models.Model):
    _inherit = 'stock.move.line'

    x_sku_id = fields.Many2one('product.product', 'Product Code', related='move_id.x_sku_id', store=False)
    x_sku_line_id = fields.Char(string="SKU Line", compute='_x_sku_line_id', store=False)



    def _x_sku_line_id(self):
        print('bbbbbbbbbbb')
        for rec in self:
            if rec.x_sku_id:
                rec['x_sku_line_id'] = str(rec.x_sku_id.name) + str(rec.id)

            else:
                rec['x_sku_line_id'] = ''

    def lot_auto_create(self):
        for rec in self:
            if rec.picking_id and not rec.start_date:
                rec['start_date'] = rec.picking_id.scheduled_date
            if not rec.picking_id and not rec.start_date:
                rec['start_date'] = datetime.datetime.now()

            print('lot auto generate......................................')
            print(rec.product_id, 'self.product_id', rec.move_id)
            sequence = rec.env['ir.sequence'].next_by_code('stock.production.lot.seq.cust')
            vals = {'name': sequence,
                    'product_id': rec.product_id.id,
                    'partner_id': rec.picking_id.partner_id.id,
                    'location_id': rec.location_dest_id.id,
                    'use_date': rec.production_date,
                    'removal_date': rec.expiry_date,
                    'company_id': self.env.company.id
                    }
            lot = rec.env['stock.production.lot'].create(vals)
            lot.generate_name()

            rec['lot_id'] = lot
            rec['lot_name'] = lot.name



#
#
# class WarehouseDeliveryPicking(models.Model):
#     _inherit = 'stock.picking'
#
#     def button_validate(self):
#         print('hhhhh')
#         res = super(WarehouseDeliveryPicking, self).button_validate()
#         if self.picking_type_id.code == 'outgoing':
#             for rec in self.move_ids_without_package:
#                 in_move = self.env['stock.move'].search([('id', '=', rec.in_move.id)])
#                 in_move.moved_qty += rec.quantity_done
#                 in_move.rem_qty = float(in_move.quantity_done) - float(in_move.moved_qty)
#                 in_move.moved_count = in_move.count
#                 in_move.rem_count = float(in_move.count) - float(in_move.moved_count)
#                 print(in_move.moved_qty, 'in_move.moved_qty')
#                 print(in_move.rem_qty, 'in_move.rem_qty')
#                 print(in_move.moved_count, 'in_move.moved_count')
#                 print(in_move.rem_count, 'in_move.rem_count')
#         if self.picking_type_id.code == 'incoming':
#             h = []
#             for rec in self.move_ids_without_package:
#                 picking_type = self.env['stock.picking.type'].search([('code', '=', 'outgoing')])[0]
#                 print(picking_type)
#                 customer_location = self.env['stock.location'].search([('usage', '=', 'customer')])
#                 print(customer_location, 'customer_location')
#                 vals = {
#                     'partner_id': self.partner_id.id,
#                     'product_id': rec.product_id.id,
#                     #                    'quantity_done': rec.quantity_done,
#                     'quantity_done': rec.product_uom_qty,
#                     'name': rec.name,
#                     'product_uom': rec.product_uom.id,
#                     'location_id': rec.location_dest_id.id,
#                     'location_dest_id': customer_location.id,
#                     'warehouse_line_id': rec.warehouse_line_id.id,
#                     'x_sku_id': rec.x_sku_id.id,
#                     'picking_type_id': picking_type.id,
#                     # 'location_id': 8,
#                     # 'location_dest_id': 5,
#                     'x_length': rec.x_length,
#                     'x_breadth': rec.x_breadth,
#                     'x_height': rec.x_height,
#                     'x_dimension': rec.x_dimension,
#                     'x_weight': rec.x_weight,
#                     'x_gross': rec.x_gross,
#                     'inv_meth': rec.inv_meth,
#                     # 'x_volume' : rec.x_volume,
#                     # 'boe_no' : rec.boe_no,
#                     # 'coo' : rec.coo,
#                     # 'serial_no' : rec.serial_no,
#                     # 'remarks' : rec.remarks,
#
#                     # 'sh_sec_done_qty' : rec.sh_sec_done_qty,
#                     # 'sh_sec_qty' : rec.sh_sec_qty,
#                     # 'sh_sec_uom' : rec.sh_sec_uom.id,
#                     # 'sh_is_secondary_unit' : rec.sh_is_secondary_unit,
#                 }
#                 move = self.env['stock.move'].create(vals)
#                 # move._quantity_done_set()
#                 print(move.picking_id, 'picking_id')
#                 print(move.state, 'state')
#                 print(move.id, 'move')
#                 h.append(move.id)
#                 self['created_moves'] = h
#                 print(self['created_moves'], '<<<<<<<<<<<<<<<<<<<<<<<<<<<<HB>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
#                 keep_vals = {
#                     'partner_id': self.partner_id.id,
#                     'product_id': rec.product_id.id,
#                     #  'qty_avail': rec.quantity_done,
#                     'qty_avail': rec.product_uom_qty,
#                     'x_sku_id': rec.x_sku_id.id,
#                     'move_state': self.state,
#                     'location_d': self.location_dest_id.id,
#                     'product_uom': rec.product_uom.id,
#                     'warehouse_line_id': rec.warehouse_line_id.id,
#                     'x_length': rec.x_length,
#                     'x_breadth': rec.x_breadth,
#                     'x_height': rec.x_height,
#                     'x_dimension': rec.x_dimension,
#                     'x_weight': rec.x_weight,
#                     'x_gross': rec.x_gross,
#                     # 'x_volume' : rec.x_volume,
#                     'inv_meth': rec.inv_meth,
#                     'start_date': self.scheduled_date,
#                     'in_move': rec.id,
#                     # 'boe_no': rec.boe_no,
#                     # 'coo': rec.coo,
#                     # 'serial_no': rec.serial_no,
#                     # 'remarks': rec.remarks,
#
#                 }
#                 print(keep_vals, 'keepvalllllllllllllllllllllllllllll')
#                 keep = self.env['stock.keep'].create(keep_vals)
#                 print(keep, 'keep')
#             return res

class Saleorderline(models.Model):
    _inherit = 'sale.order.line'

    sku = fields.Char(string="sku", compute='_fromitemmaster', store=True)
    x_sku_id = fields.Many2one('product.product', 'Product Code', store=False)

    @api.depends('x_sku_id')
    def _fromitemmaster(self):
        for rec in self:
            if rec.x_sku_id:
                rec['x_height'] = rec.x_sku_id.height
                rec['x_weight'] = rec.x_sku_id.weight
                rec['x_breadth'] = rec.x_sku_id.width
                rec['x_length'] = rec.x_sku_id.length
                rec['name'] = rec.x_sku_id.product_description
                rec['x_volume'] = rec.x_sku_id.volume
                #                rec['partner_id'] = rec.x_sku_id.partner_id.id
                rec['product_id'] = rec.x_sku_id.id
                rec['sku'] = rec.x_sku_id.name
            else:
                rec['name'] = rec.product_id.name
                rec['sku'] = rec.product_id.name

class deltransient(models.Model):
    _inherit = 'stock.keep'

    x_sku_id = fields.Many2one('product.product', 'Product Code', store=False)
    x_length = fields.Float('Length', related='x_sku_id.product_length')
    x_breadth = fields.Float('Breadth', related='x_sku_id.product_width')
    x_height = fields.Float('Height', related='x_sku_id.product_height')
    x_weight = fields.Float('Weight', related='x_sku_id.weight')