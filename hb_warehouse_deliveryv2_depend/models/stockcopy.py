from odoo import api, fields, models, _
from odoo.http import request
import os
from odoo.exceptions import UserError, AccessError, MissingError, ValidationError
import datetime


class qualitycheck(models.Model):
    _inherit = 'qc.inspection'

    is_checked = fields.Boolean('QC Checked')
    checked_by = fields.Many2one('res.users', string="Checked By")


class Warehousemoveline(models.Model):
    _inherit = 'stock.move.line'

    putaway_upadted = fields.Boolean('Putaway Updated')
    putaway_updated_by = fields.Many2one('res.users', string="'Putaway Updated By")
    allocated = fields.Boolean(string="Allocated")
    x_sku_id = fields.Many2one('item.master', 'Product Code', related='move_id.x_sku_id')
    location_ref_id = fields.Many2one('stock.location', string="Reference Location", related='lot_id.location_id',
                                      compute='_location_out')
    location_barcode = fields.Char(string="Location Barcode", related='location_dest_id.barcode')

    # location_dest_id = fields.Many2one('stock.location', string='To', domain=lambda self: self._location_destination_domain())
    #
    # def _location_out(self):
    #     for rec in self:
    #         if rec.picking_code == 'outgoing' and rec.lot_id:
    #             rec['location_id'] = rec.lot_id.location_id.id

    def _location_destination_domain(self):
        print('domain........................................')
        domain = []
        if self.picking_code == 'outgoing':
            domain.append(('id', '=', 'location_ref_id'))

        return domain

    def lot_auto_create(self):
        for rec in self:
            print('lot auto generate......................................')
            print(rec.product_id, 'self.product_id', rec.move_id)
            sequence = rec.env['ir.sequence'].next_by_code('stock.production.lot.seq.cust')
            vals = {'name': sequence,
                    'product_id': rec.product_id.id,
                    'partner_id': rec.picking_id.partner_id.id,
                    'location_id': rec.location_dest_id.id,
                    }
            lot = rec.env['stock.production.lot'].create(vals)
            lot.generate_name()
            print(lot, 'generated lot ------------------------------', lot.id, lot.name)
            rec['lot_id'] = lot
            rec['lot_name'] = lot.name
            # val = {'lot_id':lot.id}
            # self.update(val)
            print(rec.lot_id, '-------------lot_id--------------------', rec.lot_name)

    def write(self, vals):
        print('Updation started')
        res = super(Warehousemoveline, self).write(vals)
        for rec in self:
            print(rec.lot_id.location_id, '/////////////////////////////////////')
            if vals.get('lot_id'):
                rec.lot_id.location_id = rec.location_dest_id.id
                print(rec.lot_id.location_id, '==============================')

        return res

    # @api.model_create_multi
    # def create(self, vals_list):
    #     print('creation started')
    #     res = super(Warehousemoveline, self).create(vals_list)
    #     id = self.env['stock.move'].search([('id', '=', self.id)])
    #     idd = 'stock.move,%s' % self.id
    #     vals = {'object_id': idd,
    #             'name': 'hb',
    #             'date': datetime.datetime.now()
    #             }
    #
    #     print(self.id, id)
    #     # exist_ins = self.env['qc.inspection'].search([('object_id','=', id)])
    #     # if not exist_ins:
    #     ins = self.env['qc.inspection'].create(vals)
    #     print(ins, 'insssssssssssssssssssssssssssssssssssssssssss', self.id, id)

    # return res


class Lotpartner(models.Model):
    _inherit = 'stock.production.lot'

    partner_id = fields.Many2one('res.partner', string="Partner")
    location_id = fields.Many2one('stock.location', string="Location")


class Saleorderline(models.Model):
    _inherit = 'sale.order.line'

    x_length = fields.Float('Length')
    x_breadth = fields.Float('Breadth')
    x_height = fields.Float('Height')
    x_dimension = fields.Float('Dimension')
    x_weight = fields.Float('Weight')
    x_volume = fields.Float('Volume')
    sku = fields.Char(string="sku", compute='_fromitemmaster', store=True)
    x_sku_id = fields.Many2one('item.master', 'Product Code')
    medium_id = fields.Many2one('utm.medium', string="Medium Id", related='order_id.medium_id')
    medium = fields.Boolean('Medium', compute='_medium')

    def _action_launch_stock_rule(self, previous_product_uom_qty=False):
        print('Delivery Order Creation from sale order has been Disabled')
        return True

    #    @api.model
    #    def create(self, vals):
    #        res = super(Saleorder, self).create(vals)
    #        print('x_length', self.x_length)
    #        if self.medium_id.name == 'Warehouse':
    #            if not self.x_sku_id:
    #                raise ValidationError(_("Please Select the Product Code."))
    #            if self.x_length <= 0 or self.x_weight <= 0 or self.x_height <= 0 or self.x_breadth <= 0:
    #                raise ValidationError(_("Please check the Measurements."))
    #        return res

    #    @api.model
    #    def write(self, vals):
    #        res = super(Saleorder, self).write(vals)
    #        for rec in self:
    #            if rec.medium_id.name == 'Warehouse':
    #                if not rec.x_sku_id:
    #                    raise ValidationError(_("Please Select the Product Code."))
    #                if rec.x_length <= 0 or rec.x_weight <= 0 or rec.x_height <= 0 or rec.x_breadth <= 0:
    #                    raise ValidationError(_("Please check the Measurements."))
    #        return res

    @api.depends('medium_id')
    def _medium(self):
        for rec in self:
            if rec.medium_id.name == 'Warehouse':
                print(rec.medium_id.name, 'rec.medium_id........................')
                rec['medium'] = False
            else:
                print(rec.medium_id.name, 'rec.medium_id.........................')
                rec['medium'] = True

    @api.depends('x_sku_id')
    def _fromitemmaster(self):
        for rec in self:
            if rec.x_sku_id:
                rec['x_height'] = rec.x_sku_id.height
                rec['x_weight'] = rec.x_sku_id.weight
                rec['x_breadth'] = rec.x_sku_id.width
                rec['x_length'] = rec.x_sku_id.length
                rec['name'] = rec.x_sku_id.description
                rec['x_volume'] = rec.x_sku_id.volume
                #                rec['partner_id'] = rec.x_sku_id.partner_id.id
                rec['product_id'] = rec.x_sku_id.product_id
                rec['sku'] = rec.x_sku_id.name
            else:
                rec['name'] = rec.product_id.name
                rec['sku'] = rec.product_id.name


class Warehouseorder(models.Model):
    _inherit = 'warehouse.order.line'

    x_length = fields.Float('Length', related='x_sku_id.length', store=True)
    x_breadth = fields.Float('Breadth', related='x_sku_id.width', store=True)
    x_height = fields.Float('Height', related='x_sku_id.height', store=True)
    x_dimension = fields.Float('Dimension')
    x_weight = fields.Float('Weight', related='x_sku_id.weight', store=True)
    sku = fields.Char(string="sku", compute='_fromitemmaster', store=True)
    x_sku_id = fields.Many2one('item.master', 'Product Code')
    x_volume = fields.Float('Volume')

    # @api.model
    #    def create(self, vals_list):
    #        print('creation starteddddddddddddddddddddddddddddddddddddddddddddddddddddddddddd')
    #        res = super(Warehouseorder, self).create(vals_list)
    #        self['x_sku_id'] = self.sale_war_id.x_sku_id.id
    #        print(self.x_sku_id, 'Product Code', self.sale_war_id, 'self.sale_war_id')
    #        self._fromitemmaster()
    #        if not self.x_sku_id:
    #            raise ValidationError(_("Please Select the Product Code."))
    #        if self.x_length <= 0 or self.x_weight <= 0 or self.x_height <= 0 or self.x_breadth <= 0:
    #            raise ValidationError(_("Please check the Measurements."))
    #        return res

    #    @api.model
    #    def write(self, vals):
    #        res = super(Warehouseorder, self).write(vals)
    #        for rec in self:
    #            if not rec.x_sku_id:
    #                raise ValidationError(_("Please Select the Product Code."))
    #            if rec.x_length <= 0 or rec.x_weight <= 0 or rec.x_height <= 0 or rec.x_breadth <= 0:
    #                raise ValidationError(_("Please check the Measurements."))

    #        return res

    @api.depends('sale_war_id')
    def _fromitemmaster(self):
        print('_fromitemmaster meth called')
        for rec in self:
            if rec.sale_war_id:
                print(rec.sale_war_id, ']]]]]]]]]]]]]]]]]]]]]]]]rec.sale_war_id]]]]]]]]]]]]]]]]]]]]]]]]]')
                rec['x_sku_id'] = rec.sale_war_id.x_sku_id.id

            if rec.x_sku_id:
                rec['x_height'] = rec.x_sku_id.height
                rec['x_weight'] = rec.x_sku_id.weight
                rec['x_breadth'] = rec.x_sku_id.width
                rec['x_length'] = rec.x_sku_id.length
                rec['name'] = rec.x_sku_id.description
                rec['partner_id'] = rec.x_sku_id.partner_id.id
                rec['product_id'] = rec.x_sku_id.product_id
                rec['sku'] = rec.x_sku_id.name
                rec['x_volume'] = rec.x_sku_id.volume
            else:
                rec['name'] = rec.product_id.name
                rec['sku'] = rec.product_id.name

    # @api.depends('x_sku_id')
    # def _fromitemmaster(self):
    #     print('_fromitemmaster meth called')
    #     for rec in self:
    #         if rec.sale_war_id:
    #             print(rec.sale_war_id, ']]]]]]]]]]]]]]]]]]]]]]]]rec.sale_war_id]]]]]]]]]]]]]]]]]]]]]]]]]')
    #             rec['x_sku_id'] = rec.sale_war_id.x_sku_id.id
    #
    #         if rec.x_sku_id:
    #             rec['x_height'] = rec.x_sku_id.height
    #             rec['x_weight'] = rec.x_sku_id.weight
    #             rec['x_breadth'] = rec.x_sku_id.width
    #             rec['x_length'] = rec.x_sku_id.length
    #             rec['name'] = rec.x_sku_id.description
    #             rec['partner_id'] = rec.x_sku_id.partner_id.id
    #             rec['product_id'] = rec.x_sku_id.product_id
    #             rec['sku'] = rec.x_sku_id.name
    #             rec['x_volume'] = rec.x_sku_id.volume
    #         else:
    #             rec['name'] = rec.product_id.name
    #             rec['sku'] = rec.product_id.name


class deltransient(models.Model):
    _name = 'stock.keep'

    name = fields.Char('name', related='x_sku_id.name')
    x_sku_id = fields.Many2one('item.master', 'Product Code')
    product_id = fields.Many2one('product.product')
    partner_id = fields.Many2one('Customer')
    qty = fields.Float('Quanity')
    qty_avail = fields.Float('Available Quantity')
    qty_adjust = fields.Float('Quantity Deliver')
    create_move = fields.Boolean('Select')
    # move_state = fields.Selection([
    #     ('draft', 'New'), ('cancel', 'Cancelled'),
    #     ('waiting', 'Waiting Another Move'),
    #     ('confirmed', 'Waiting Availability'),
    #     ('partially_available', 'Partially Available'),
    #     ('assigned', 'Available'),
    #     ('done', 'Done')], string='Status',
    #     copy=False, default='draft', index=True, readonly=True)
    move_state = fields.Char('State')
    product_uom = fields.Many2one('uom.uom', string="Product UOM")
    location_d = fields.Many2one('stock.location', string="Loctaion")
    warehouse_line_id = fields.Many2one('stock.warehouse.line', string="Warehouse Order Line")
    new_pick = fields.Many2one('stock.picking', string="New Pick")
    x_length = fields.Float('Length', related='x_sku_id.length')
    x_breadth = fields.Float('Breadth', related='x_sku_id.width')
    x_height = fields.Float('Height', related='x_sku_id.height')
    x_dimension = fields.Float('Dimension')
    x_weight = fields.Float('Weight', related='x_sku_id.weight')
    x_gross = fields.Float('Gross')
    inv_meth = fields.Selection(string="Invoice Method",
                                selection=[('cbm', 'CBM'), ('pallet', 'Pallet'), ('weight', 'Weight'),
                                           ('carton_units', 'Carton/Units')])
    start_date = fields.Datetime(string="Start Date")

    # sku = fields.Char(string="sku", compute='_fromitemmaster', required=True)

    # @api.depends('x_sku_id')
    # def _fromitemmaster(self):
    #     for rec in self:
    #         rec['x_height'] = rec.x_sku_id.height
    #         rec['x_weight'] = rec.x_sku_id.weight
    #         rec['x_breadth'] = rec.x_sku_id.width
    #         rec['x_length'] = rec.x_sku_id.length
    #         rec['name'] = rec.x_sku_id.description
    #         rec['partner_id'] = rec.x_sku_id.partner_id.id
    #         rec['product_id'] = rec.x_sku_id.product_id
    #         rec['sku'] = rec.x_sku_id.name


class WarehouseDelMove(models.Model):
    _inherit = 'stock.move'

    select = fields.Boolean('Select Goods')
    # name = fields.Char(string="Description", related='x_sku_id.description')
    x_sku_id = fields.Many2one('item.master', 'Product Code', readonly=False)
    sku = fields.Char(string="sku", compute='_fromitemmaster', store=True)
    # x_length = fields.Float('Length', related='x_sku_id.length')
    # x_breadth = fields.Float('Breadth', related='x_sku_id.width')
    # x_height = fields.Float('HHeight', related='x_sku_id.height')
    # x_dimension = fields.Float('Dimension')
    # x_weight = fields.Float('Weight', related='x_sku_id.weight')
    x_length = fields.Float('Length', store=True)
    x_breadth = fields.Float('Breadth', store=True)
    x_height = fields.Float('HHeight', store=True)
    x_dimension = fields.Float('Dimension')
    x_weight = fields.Float('Weight', store=True)
    x_gross = fields.Float('Gross')
    x_volume = fields.Float('Volume')
    qty_checked = fields.Boolean('Quantity Check - Checked')
    qty_checked_by = fields.Many2one('res.users', string="Quantity Check - Checked By")
    deliv_status = fields.Boolean('Delivery Status - Update')
    deliv_status_updated_by = fields.Many2one('res.users', string="Delivery Status - Updated By")
    inspection_created = fields.Boolean(string="Inspection Created")
    boe_no = fields.Char('BOE No')
    coo = fields.Char('COO')
    serial_no = fields.Char('Serial Number')
    remarks = fields.Char('Remarks')
    noofdays = fields.Float(string='No of Days', compute='_noofdays')

    def _noofdays(self):
        for rec in self:
            if rec.start_date and rec.end_date:
                rec['noofdays'] = abs((rec.end_date - rec.start_date).days)
                print(rec.noofdays,
                      '*************************************************************************************')
            else:
                rec['noofdays'] = 1

    @api.depends('warehouse_line_id')
    def _fromitemmaster(self):
        for rec in self:
            if rec.warehouse_line_id:
                rec['x_sku_id'] = rec.warehouse_line_id.x_sku_id.id

            if rec.x_sku_id:
                rec['x_height'] = rec.warehouse_line_id.x_height
                rec['x_weight'] = rec.warehouse_line_id.x_weight
                rec['x_breadth'] = rec.warehouse_line_id.x_breadth
                rec['x_length'] = rec.warehouse_line_id.x_length
                rec['x_volume'] = rec.warehouse_line_id.x_volume
                rec['name'] = rec.x_sku_id.description
                rec['partner_id'] = rec.x_sku_id.partner_id.id
                rec['product_id'] = rec.x_sku_id.product_id
                rec['sku'] = rec.x_sku_id.name
            else:
                rec['name'] = rec.product_id.name
                rec['sku'] = rec.product_id.name

    #    def insss(self):
    #        id = self.env['stock.move'].search([('id', '=', self.id)])
    #        idd = 'stock.move,%s' % self.id
    #        test_categ = self.env['qc.test.category'].search([('name', '=', 'Generic')])
    #        test = self.env['qc.test'].search([('category', '=', test_categ.id)])
    #        print(test_categ, test, 'testtttttttttttttttttttttttttttttestttttttttttttttt')
    #        vals = {'object_id': idd,
    #                'name': 'hb',
    #                'date': datetime.datetime.now(),
    #                'test': test.id,
    #                }
    #        print(vals, self.id, id)

    #        ins = self.env['qc.inspection'].create(vals)
    #        ins.inspection_lines = ins._prepare_inspection_lines(ins.test)
    #        print(ins, 'insssssssssssssssssssssssssssssssssssssssssss', self.id, id)
    #        self.inspection_created = True

    # @api.model_create_multi
    # def create(self, vals_list):
    #     print('creation started')
    #     res = super(WarehouseDelMove, self).create(vals_list)
    #     # self._generate_skuid()
    #     # self['product_id'] = self.x_sku_id.product_id.id
    #     # self['partner_id'] = self.x_sku_id.partner_id.id
    #     # self['x_length'] = self.x_sku_id.length
    #     # self['x_weight'] = self.x_sku_id.weight
    #     # self['x_height'] = self.x_sku_id.height
    #     # self['x_breadth'] = self.x_sku_id.width
    #     return res

    # def write(self, vals):
    #     print('Updation started')
    #     res = super(WarehouseDelMove, self).write(vals)
    #     print(vals, 'valsssssssssssssssssssssssssssss')
    #     for rec in self:
    #         # if rec.inspection_created == False:
    #         #     rec.ins()
    #
    #
    #         if vals.get('state') and rec.x_sku_id == False and rec.picking_type_id.code == 'incoming':
    #             rec._generate_skuid()
    #     return res

    def _generate_skuid(self):
        print('generate...')
        # sequence = self.env['ir.sequence'].next_by_code('stock.keep.seq')
        # print(sequence, self.partner_id.id, self.product_id.id, self.warehouse_line_id.order_id.name)
        # self['x_sku_id'] = str(self.warehouse_line_id.order_id.name) + str(self.picking_id.partner_id.id) + str(self.product_id.id) +  str(sequence)
        # # self['x_sku_id'] = 'sequence'
        # print(self.x_sku_id, 'self.x_sku_id----------------------------------------------------------------')
        for rec in self:
            print(rec.picking_type_id.code)
            if rec.picking_type_id.code == 'incoming':
                print('......................')
                sequence = self.env['ir.sequence'].next_by_code('stock.keep.seq')
                print(sequence, rec.picking_id.partner_id.id, rec.product_id.id, rec.warehouse_line_id.order_id.name)
                # if rec.partner_id and rec.product_id and rec.warehouse_line_id:
                rec['x_sku_id'] = str(rec.warehouse_line_id.order_id.name) + str(rec.picking_id.partner_id.id) + str(
                    rec.product_id.id) + str(sequence)
                print(rec.x_sku_id, 'self.x_sku_id----------------------------------------------------------------')


class WarehouseDeliveryPicking(models.Model):
    _inherit = 'stock.picking'

    cust_del_moves = fields.Many2many('stock.move', string="Moves", compute='_del_moves')
    created_moves = fields.Char('Created Move Ids')
    keep_ids = fields.Many2many('stock.keep', string="Stock Keep", compute='_keeps')
    is_placed = fields.Boolean('Is Placed')
    placed_by = fields.Many2one('res.users', string="Placed By")
    delivery_order = fields.Boolean(string="Pick Type")
    agreement_id = fields.Many2one('agreement', string="Agreement")
    picking_state = fields.Selection(string="Picking Stages",
                                     selection=[('1', 'Receive'), ('2', 'Putaway'), ('3', 'Pick')], store=True)

    def picktype(self):
        print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!pick type!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
        for rec in self:
            rec['owner_id'] = rec.partner_id.id
            print(rec.owner_id, 'rec.owner_id')
            # rec.agreement_id = rec.active_sale_id.agreement_id.id
            agree = self.env['agreement'].search([('partner_id', '=', rec.partner_id.id)])
            if rec.picking_type_id.code == 'outgoing':
                rec['delivery_order'] = True
                rec['picking_state'] = '3'
                rec.agreement_id = agree.id
                print('hhhhhh')
                rec['end_date'] = datetime.datetime.now()

            else:
                rec['delivery_order'] = False
                print('bbbbbb')
            if rec.picking_type_id.code == 'incoming' and rec.picking_state != '2':
                rec['picking_state'] = '1'

    @api.depends('origin')
    def _returnpick(self):
        for rec in self:
            res = super(WarehouseDeliveryPicking, self)._returnpick()
            rec.picktype()
            print('////////////////////////////////////////////////////////////////////')
            return res

    # @api.model
    # def create(self, vals):
    #     print('creation started')
    #     res = super(WarehouseDeliveryPicking, self).create(vals)
    #     # for rec in self:
    #     self.move_ids_without_package._generate_skuid()
    #
    #     return res

    def keep_select(self):
        print('keep select!!!!!!!!!!!!!!!!!!!!!!!')
        for rec in self:
            for k in rec.keep_ids:
                if k.create_move == True:
                    print(k.qty_adjust, 'k.qty_availlllllllllllllllllllllllllllllllllllllllll')
                    if k.qty_adjust == 0:
                        raise UserError("Please Enter the Quantity you want to Deliver")

                    k['qty_avail'] = k.qty_avail - k.qty_adjust
                    picking_type = self.env['stock.picking.type'].search([('code', '=', 'outgoing')])[0]
                    print(picking_type)
                    customer_location = self.env['stock.location'].search([('usage', '=', 'customer')])
                    print(customer_location, 'customer_location')
                    vals = {
                        'partner_id': k.partner_id.id,
                        'product_id': k.product_id.id,
                        'quantity_done': k.qty_adjust,
                        'product_uom': k.product_uom.id,
                        'location_id': k.location_d.id,
                        'location_dest_id': customer_location.id,
                        'warehouse_line_id': k.warehouse_line_id.id,
                        'x_sku_id': k.x_sku_id.id,
                        'picking_type_id': picking_type.id,
                        'name': k.product_id.name,
                        'x_length': k.x_length,
                        'x_breadth': k.x_breadth,
                        'x_height': k.x_height,
                        'x_dimension': k.x_dimension,
                        'x_weight': k.x_weight,
                        'x_gross': k.x_gross,
                        'inv_meth': k.inv_meth,
                        'start_date': k.start_date,
                        # 'x_volume':k.x_volume

                    }
                    moves = self.env['stock.move'].create(vals)
                    print(moves, 'mmoves from keep')
                    moves.picking_id = rec.id
                    for line in moves.move_line_ids:
                        line.picking_id = rec.id
                    if moves:
                        k.create_move = False

    @api.depends('partner_id')
    def _keeps(self):
        print('blaaaaaaaaaaaaaaaaa')
        for rec in self:
            if rec.picking_type_id.code == 'outgoing':
                moves = self.env['stock.keep'].search(
                    [('partner_id', '=', rec.partner_id.id), ('qty_avail', '!=', 0)])
                print(moves, 'moves')
                if moves:
                    rec['keep_ids'] = moves
                    print(rec.keep_ids, 'keep_ids')
                else:
                    rec['keep_ids'] = []
                    print(rec.keep_ids, 'keep_ids')
            else:
                rec['keep_ids'] = []
                print(rec.keep_ids, 'keep_ids')

    def del_orders(self):
        for rec in self:
            new_pick = rec._del_orders()
            return {
                'name': _('Delivery Order'),
                'view_mode': 'form,tree',
                'res_model': 'stock.picking',
                'res_id': new_pick,
                'type': 'ir.actions.act_window',
                # 'context': ctx,
            }

    def _del_orders(self):
        for rec in self:
            if rec.state != 'done':
                raise UserError(_('You can able to create the delivery order for the validated orders only. Please '
                                  'validate the order first'))
            if rec.state == 'done':
                picking_type = self.env['stock.picking.type'].search([('code', '=', 'outgoing')])[0]
                print(picking_type.name)
                customer_location = self.env['stock.location'].search([('usage', '=', 'customer')])
                print(customer_location, 'customer_location')

                del_order_picking = self.env['stock.picking'].create({
                    # 'warehouse_id':rec.warehouse_id.id,
                    'location_id': rec.location_dest_id.id,
                    'location_dest_id': customer_location.id,
                    # 'location_id':8,
                    # 'location_dest_id':5,
                    'partner_id': rec.partner_id.id,
                    'picking_type_id': picking_type.id,
                    'origin': _("Delivery of %s") % self.name,
                    # 'move_ids_without_package' : [233, 234, 235]
                })
                print(del_order_picking, 'del_order_picking')
                # exist_del = []
                if del_order_picking:
                    hb = rec.created_moves
                    h = hb.replace('[', '')
                    b = h.replace(']', '')
                    j = b.split(',')
                    print(j, '****************************************************', rec.created_moves,
                          len(rec.created_moves))
                    for bla in j:
                        new_move = self.env['stock.move'].search([('id', '=', int(bla))])
                        new_move.picking_id = del_order_picking.id
                        # keep = self.env['stock.keep'].search([('name','=','new_move.x_sku_id')])
                        keeps = self.env['stock.keep'].search([])
                        for keep in keeps:
                            if keep.name == new_move.x_sku_id:
                                keep['qty_adjust'] = new_move.quantity_done
                                keep['qty_avail'] = keep.qty_avail - keep.qty_adjust

                                print('keepppppppppppppppppppppppppppppppppppppppppppppppppp', keep,
                                      'new_move.x_sku_id', new_move.x_sku_id, )

                        print(int(bla), 'blaaaa')
                        print(new_move.warehouse_line_id, '')
                        for new_moveline in new_move.move_line_ids:
                            new_moveline.picking_id = del_order_picking.id
                        # exist_del.append(int(bla))
                    # print(exist_del, 'exist_del')
                    return del_order_picking.id

    def select_del(self):
        print(self)
        for rec in self:
            for h in rec.cust_del_moves:
                print(h.select)
                if h.select == True:
                    h.picking_id = rec.id

                    for mline in h.move_line_ids:
                        print(mline)
                        print(mline.picking_id)
                        mline.picking_id = rec.id

    @api.depends('partner_id')
    def _del_moves(self):
        print('bla')
        for rec in self:
            if rec.picking_type_id.code == 'outgoing':
                moves = self.env['stock.move'].search(
                    [('partner_id', '=', rec.partner_id.id), ('picking_id', '=', False), ('state', '=', 'draft')])
                print(moves, 'moves')
                if moves:
                    rec['cust_del_moves'] = moves
                    print(rec.cust_del_moves, 'cust_del_moves')
                else:
                    rec['cust_del_moves'] = []
                    print(rec.cust_del_moves, 'cust_del_moves')
            else:
                rec['cust_del_moves'] = []
                print(rec.cust_del_moves, 'cust_del_moves')

    # def del_orderss(self):
    #     for rec in self:
    #         if rec.picking_type_id.code == 'outgoing':
    #             moves = self.env['stock.move'].search(
    #                 [('partner_id', '=', rec.partner_id.id), ('picking_id', '=', False), ('state', '=', 'draft')])
    #             print(moves, 'moves')
    #             for mov in moves:
    #                 mov.update({'picking_id': rec.id})
    #                 print(rec.move_ids_without_package, 'move_ids_without_package')

    def button_validate(self):
        print('hhhhh')
        res = super(WarehouseDeliveryPicking, self).button_validate()
        if self.picking_type_id.code == 'incoming':
            h = []
            for rec in self.move_ids_without_package:
                picking_type = self.env['stock.picking.type'].search([('code', '=', 'outgoing')])[0]
                print(picking_type)
                customer_location = self.env['stock.location'].search([('usage', '=', 'customer')])
                print(customer_location, 'customer_location')
                vals = {
                    'partner_id': self.partner_id.id,
                    'product_id': rec.product_id.id,
                    #                    'quantity_done': rec.quantity_done,
                    'quantity_done': rec.product_uom_qty,
                    'name': rec.name,
                    'product_uom': rec.product_uom.id,
                    'location_id': rec.location_dest_id.id,
                    'location_dest_id': customer_location.id,
                    'warehouse_line_id': rec.warehouse_line_id.id,
                    'x_sku_id': rec.x_sku_id.id,
                    'picking_type_id': picking_type.id,
                    # 'location_id': 8,
                    # 'location_dest_id': 5,
                    'x_length': rec.x_length,
                    'x_breadth': rec.x_breadth,
                    'x_height': rec.x_height,
                    'x_dimension': rec.x_dimension,
                    'x_weight': rec.x_weight,
                    'x_gross': rec.x_gross,
                    'inv_meth': rec.inv_meth,
                    # 'x_volume' : rec.x_volume,
                    # 'boe_no' : rec.boe_no,
                    # 'coo' : rec.coo,
                    # 'serial_no' : rec.serial_no,
                    # 'remarks' : rec.remarks,

                    # 'sh_sec_done_qty' : rec.sh_sec_done_qty,
                    # 'sh_sec_qty' : rec.sh_sec_qty,
                    # 'sh_sec_uom' : rec.sh_sec_uom.id,
                    # 'sh_is_secondary_unit' : rec.sh_is_secondary_unit,
                }
                move = self.env['stock.move'].create(vals)
                # move._quantity_done_set()
                print(move.picking_id, 'picking_id')
                print(move.state, 'state')
                print(move.id, 'move')
                h.append(move.id)
                self['created_moves'] = h
                print(self['created_moves'], '<<<<<<<<<<<<<<<<<<<<<<<<<<<<HB>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
                keep_vals = {
                    'partner_id': self.partner_id.id,
                    'product_id': rec.product_id.id,
                    #  'qty_avail': rec.quantity_done,
                    'qty_avail': rec.product_uom_qty,
                    'x_sku_id': rec.x_sku_id.id,
                    'move_state': self.state,
                    'location_d': self.location_dest_id.id,
                    'product_uom': rec.product_uom.id,
                    'warehouse_line_id': rec.warehouse_line_id.id,
                    'x_length': rec.x_length,
                    'x_breadth': rec.x_breadth,
                    'x_height': rec.x_height,
                    'x_dimension': rec.x_dimension,
                    'x_weight': rec.x_weight,
                    'x_gross': rec.x_gross,
                    # 'x_volume' : rec.x_volume,
                    'inv_meth': rec.inv_meth,
                    'start_date': self.scheduled_date,
                    # 'boe_no': rec.boe_no,
                    # 'coo': rec.coo,
                    # 'serial_no': rec.serial_no,
                    # 'remarks': rec.remarks,

                }
                print(keep_vals, 'keepvalllllllllllllllllllllllllllll')
                keep = self.env['stock.keep'].create(keep_vals)
                print(keep, 'keep')
            return res
