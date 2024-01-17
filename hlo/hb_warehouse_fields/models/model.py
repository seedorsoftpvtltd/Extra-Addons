from dateutil import parser
from odoo import api, models, fields, _
from datetime import datetime, date
from odoo.exceptions import AccessError, UserError, ValidationError
from odoo.tools.float_utils import float_round

class PartnerInh(models.Model):
    _inherit = "res.partner"

    vatt = fields.Char(string="TAN")

    _sql_constraints = [
        ('vatt', 'unique(vatt)', 'TAN already exists!')
   ]

class PackageInherit(models.Model):
    _inherit = "stock.quant.package"

    new_name = fields.Char(string="Reference", compute='_xname')
    hb = fields.Char(string="HB", related="name")
    barcode = fields.Char(string="Barcode")

    _sql_constraints = [
        ('barcode', 'unique(name, company_id)', 'Barcode must be unique.'),
    ]

    def _xname(self):
        for record in self:
            if record.packaging_id:
                record['new_name'] = str(record.packaging_id.shipper_package_code) + '-' + str(record.hb)
            else:
                record['new_name'] = record.hb


class Stockmoveline(models.Model):
    _inherit = "stock.move.line"

    pack = fields.Char(string="Package", compute="_pack")
    inv_meth = fields.Selection(string="Invoice Method", related="move_id.inv_meth", store=True, readonly=False)
#    result_package_id = fields.Many2one(
#        'stock.quant.package', 'Destination Package',
#        ondelete='restrict', required=False, check_company=True,
#        domain="['|', '|', ('location_id', '=', False), ('location_id', '=', location_dest_id), ('id', '=', package_id)]",
#        help="If set, the operations are packed into this package", related='location_dest_id.x_pallet')
    loc = fields.Many2one('stock.location', 'To', compute='_locloc')

    @api.onchange('location_dest_id')
    def _locloc(self):
        for rec in self:
            if rec.inv_meth == 'pallet':
                rec['loc'] = rec.location_dest_id
            else:
                rec['loc'] = False

    @api.onchange('result_package_id')
    def _pack(self):
        for record in self:
            if record.result_package_id:
                record['pack'] = record.result_package_id.new_name
            else:
                record['pack'] = ""

class StockmovE(models.Model):
    _inherit = "stock.move"

    returnpick = fields.Char(string="Return", related='picking_id.returnpick')
    storage_fee = fields.Char(string="Storage Fee", compute='_storage_fee')
    start_date = fields.Datetime(string="Start Date")
    end_date = fields.Datetime(string="End Date")
    quantt = fields.Float(string="Updated Quantity")
    count = fields.Char(string="Count", compute="_countt")

    @api.onchange('move_line_ids')
    def _countt(self):
        for rec in self:
            rec.count = len(rec.move_line_ids.search([('inv_meth', '=', 'pallet')]).mapped('location_id'))

 #       a = self.search([('inv_meth', '=', 'pallet')])
  #      for cnt in a:
   #         cnt.count = len(cnt.move_line_ids.mapped('location_id'))


    @api.depends('product_id.standard_price', 'x_cbm', 'x_days')
    def _storage_fee(self):
        for rec in self:
            #rec['storage_fee'] = float(rec.product_id.standard_price) * float(rec.x_cbm) * float(rec.x_days)
            rec['storage_fee'] = float(rec.product_id.standard_price) * float(rec.x_cbm)

class AccInh(models.Model):
    _inherit = "account.move.line"

    storage_fee = fields.Char(string="Storage Fee")
    x_days = fields.Char(string="Days")




class StockReturnInh(models.TransientModel):
    _inherit = 'stock.return.picking'

    date = fields.Datetime(string="Scheduled Date [IN]")

    def _create_returns(self):
        new_picking, pick_type_id = super(StockReturnInh, self)._create_returns()
        picking = self.env['stock.picking'].browse(new_picking)
        self.date = self.picking_id.scheduled_date
        picking.write({'date': self.date})
        for a in self.product_return_moves:
            a.move_id.returned_move_ids.sh_sec_uom = a.sh_sec_uom.id
            a.move_id.returned_move_ids.sh_is_secondary_unit = a.sh_is_secondary_unit
            a.move_id.returned_move_ids.sh_sec_qty = a.sh_sec_qty
            a.move_id.returned_move_ids.sh_sec_done_qty = a.sh_sec_done_qty

        return new_picking, pick_type_id

    @api.model
    def _prepare_stock_return_picking_line_vals_from_move(self, stock_move):
        quantity = stock_move.product_qty
        for move in stock_move.move_dest_ids:
            if move.origin_returned_move_id and move.origin_returned_move_id != stock_move:
                continue
            if move.state in ('partially_available', 'assigned'):
                quantity -= sum(move.move_line_ids.mapped('product_qty'))
            elif move.state in ('done'):
                quantity -= move.product_qty
        quantity = float_round(quantity, precision_rounding=stock_move.product_uom.rounding)
        return {
            'product_id': stock_move.product_id.id,
            'quantity': quantity,
            'move_id': stock_move.id,
            'uom_id': stock_move.product_id.uom_id.id,
            'sh_sec_uom': stock_move.sh_sec_uom.id,
            'sh_sec_qty': stock_move.sh_sec_qty,
            'sh_is_secondary_unit': stock_move.sh_is_secondary_unit,
            'sh_sec_done_qty': stock_move.sh_sec_done_qty,

        }


class Warehouseinv(models.Model):
    _inherit = 'warehouse.order'

    inv_meth = fields.Selection(string="Invoice Method", selection=[('cbm', 'CBM'), ('pallet', 'Pallet'),('weight','Weight'), ('carton_units', 'Carton/Units')])



class Warehouselineinv(models.Model):
    _inherit = 'warehouse.order.line'

    inv_meth = fields.Selection(string="Invoice Method", related='order_id.inv_meth')


class StockMoveinv(models.Model):
    _inherit = 'stock.move'

    inv_meth = fields.Selection(string="Invoice Method", selection=[('cbm', 'CBM'), ('pallet', 'Pallet'),('weight','Weight'), ('carton_units', 'Carton/Units')])

class StockReturnlineInh(models.TransientModel):
    _inherit = "stock.return.picking.line"

    # sh_sec_uom = fields.Many2one('uom.uom', string='Unit of Measure', related='move_id.sh_sec_uom', readonly=False)
    sh_sec_qty = fields.Float("Secondary Qty", digits='Product Unit of Measure')
    sh_sec_uom = fields.Many2one("uom.uom", 'Secondary UOM', related="move_id.sh_sec_uom")
    sh_is_secondary_unit = fields.Boolean("Related Sec Uni", related="move_id.sh_is_secondary_unit")
    sh_sec_done_qty = fields.Float("Secondary Done Qty", digits='Product Unit of Measure', related="move_id.sh_sec_done_qty")


    @api.onchange('quantity')
    def onchange_product_uom_done_qty_sh(self):
        if self and self.sh_is_secondary_unit == True and self.sh_sec_uom:
            self.sh_sec_done_qty = self.uom_id._compute_quantity(self.quantity, self.sh_sec_uom)

    # @api.onchange('sh_sec_done_qty')
    # def onchange_sh_sec_done_qty_sh(self):
    #     if self and self.sh_is_secondary_unit == True and self.uom_id:
    #         self.quantity = self.sh_sec_uom._compute_quantity(self.sh_sec_done_qty, self.uom_id)

    @api.onchange('quantity', 'uom_id')
    def onchange_product_uom_qty_sh(self):
        if self.sh_is_secondary_unit == True and self.sh_sec_uom:
            self.sh_sec_qty = self.uom_id._compute_quantity(self.quantity, self.sh_sec_uom)

    @api.onchange('sh_sec_qty', 'sh_sec_uom')
    def onchange_sh_sec_qty_sh(self):
        if self and self.sh_is_secondary_unit == True and self.uom_id:
            self.quantity = self.sh_sec_uom._compute_quantity(self.sh_sec_qty, self.uom_id)

class ProdTempInh(models.Model):
    _inherit = 'product.template'

    ware_tax_id = fields.Many2many('account.tax', 'ware_taxes_rel', 'prod_id', 'tax_id', string='Taxes',
        domain=[('type_tax_use', '=', 'none')])
