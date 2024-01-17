from odoo import api, fields, models, _
from odoo.exceptions import UserError, AccessError, MissingError, ValidationError

class quantpack(models.Model):
    _inherit = 'stock.quant.package'

    _sql_constraints = [
        ('barcode', 'unique(barcode, company_id)', 'Barcode must be unique.'),
    ]

class WarehouselMoveDim(models.Model):
    _inherit = 'stock.move'

    boe_no = fields.Char('BOE No', store=True, related='picking_id.x_billno')


class TrackingNoExt(models.Model):
    _inherit = 'stock.production.lot'

    x_bill = fields.Char(string='BOE No', store=True)
    item_boe = fields.Char(string='Item No as per BOE')
    x_length = fields.Float(string='Length', store=True)
    x_breadth = fields.Float(string='Breadth', store=True)
    x_height = fields.Float(string='Height', store=True)
    volume = fields.Float(string='Volume', store=True)
    net_weight = fields.Float(string='Net Weight', store=True)
    gross_weight = fields.Float(string='Gross Weight', store=True)


class MOVELINEDIM(models.Model):
    _inherit = 'stock.move.line'

    x_bill = fields.Char(string="BOE No", store=True, related='picking_id.x_billno')
    item_boe = fields.Char(string='Item No as per BOE', store=True, related='move_id.per_boe')

    # @api.model_create_multi
    def create(self, vals_list):
        self.expiry_date = self.create_date
        print('create', self.x_bill)
        res = super(MOVELINEDIM, self).create(vals_list)
        if self.picking_code == 'incoming':
            if self.picking_code == 'incoming':
                if self.x_bill:
                    if self.lot_id:
                        print('create......................')
                        self.lot_id.x_bill = self.x_bill
            if self.picking_code == 'incoming':
                if self.item_boe:
                    if self.lot_id:
                        self.lot_id.item_boe = self.item_boe
            if self.picking_code == 'incoming':
                if self.x_length:
                    if self.lot_id:
                        self.lot_id.x_length = self.x_length
            if self.picking_code == 'incoming':
                if self.x_breadth:
                    if self.lot_id:
                        self.lot_id.x_breadth = self.x_breadth
            if self.picking_code == 'incoming':
                if self.x_height:
                    if self.lot_id:
                        self.lot_id.x_height = self.x_height
            if self.picking_code == 'incoming':
                if self.volume:
                    if self.lot_id:
                        self.lot_id.volume = self.volume
            if self.picking_code == 'incoming':
                if self.net_weight:
                    if self.lot_id:
                        self.lot_id.net_weight = self.net_weight
            if self.picking_code == 'incoming':
                if self.gross_weight:
                    if self.lot_id:
                        self.lot_id.gross_weight = self.gross_weight
        return res

    def write(self, vals):
        print('qqqqqqqqqqqqqqqqqq')
        res = super(MOVELINEDIM, self).write(vals)
        for rec in self:
            print('write', vals.get('x_bill'), rec.x_bill,rec.lot_id,  rec.picking_code)
            if rec.picking_code == 'incoming':
                if rec.x_bill:
                    if rec.lot_id:
                        print('write......................')
                        rec.lot_id.x_bill = rec.x_bill
                        print(rec.lot_id.x_bill, '-----------------------boe')

        for rec in self:
            if rec.picking_code == 'incoming':
                if rec.item_boe:
                    if rec.lot_id:
                        rec.lot_id.item_boe = rec.item_boe
        for rec in self:
            if rec.picking_code == 'incoming':
                if rec.x_length:
                    if rec.lot_id:
                        rec.lot_id.x_length = rec.x_length
        for rec in self:
            if rec.picking_code == 'incoming':
                if rec.x_breadth:
                    if rec.lot_id:
                        rec.lot_id.x_breadth = rec.x_breadth
        for rec in self:
            if rec.picking_code == 'incoming':
                if rec.x_height:
                    if rec.lot_id:
                        rec.lot_id.x_height = rec.x_height
        for rec in self:
            if rec.picking_code == 'incoming':
                if rec.volume:
                    if rec.lot_id:
                        rec.lot_id.volume = rec.volume
        for rec in self:
            if rec.picking_code == 'incoming':
                if rec.net_weight:
                    if rec.lot_id:
                        rec.lot_id.net_weight = rec.net_weight
        for rec in self:
            if rec.picking_code == 'incoming':
                if rec.gross_weight:
                    if rec.lot_id:
                        rec.lot_id.gross_weight = rec.gross_weight

        return res

    @api.constrains('lot_id')
    def _onchange_lot_dim(self):
        print('_onchange_lot_sl_bs_onchange_lot_sl_bs_onchange_lot_sl_bs_onchange_lot_sl_bs', self.x_bill, 'bill')
        if self.picking_code == 'incoming':
            if self.x_bill:
                if self.lot_id:
                    self.lot_id.x_bill = self.x_bill
            if self.item_boe:
                if self.lot_id:
                    self.lot_id.item_boe = self.item_boe
            if self.x_length:
                if self.lot_id:
                    self.lot_id.x_length = self.x_length
            if self.x_breadth:
                if self.lot_id:
                    self.lot_id.x_breadth = self.x_breadth
            if self.x_height:
                if self.lot_id:
                    self.lot_id.x_height = self.x_height
            if self.volume:
                if self.lot_id:
                    self.lot_id.volume = self.volume
            if self.net_weight:
                if self.lot_id:
                    self.lot_id.net_weight = self.net_weight
            if self.gross_weight:
                if self.lot_id:
                    self.lot_id.gross_weight = self.gross_weight

    @api.onchange('lot_id')
    def _onchange_lot_dim(self):
        print('onchange',  self.x_bill)
        if self.picking_code != 'incoming':
            print('onchngebilllllllllll')
            self['x_bill'] = self.lot_id.x_bill
            self['item_boe'] = self.lot_id.item_boe

    @api.constrains('lot_id')
    def _lot_dim(self):
        for rec in self:
            print('constrains', rec.lot_id.x_bill)
            if rec.picking_code != 'incoming':
                rec['x_bill'] = rec.lot_id.x_bill
                # rec['x_bill'] = rec.lot_id.warehouse_order_ids.picking_id.x_billno

