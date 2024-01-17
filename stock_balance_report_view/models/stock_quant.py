from odoo import models, fields, api, _


class StockQuant(models.Model):
    _inherit = "stock.quant"

    x_loc_code = fields.Char(string="Location Code", related="location_id.name")
    x_war_code = fields.Char(string="Warehouse Code", related="lot_id.x_war_code")
    x_war_name = fields.Char(string="Warehouse Name", related="lot_id.x_war_name")
    x_asn = fields.Char(string="ASN ID", compute="_compute_asn")
    x_ccode = fields.Char(string="Client Code", related="owner_id.x_code")
    x_cname = fields.Char(string="Client Name", related="owner_id.name")
    x_sku_code = fields.Char(string="SKU Code", related="product_id.name")
    x_sku_name = fields.Char(string="SKU Name", related="product_id.description")
    x_hs = fields.Char(string="HS Code", related="product_id.hs_code_id.local_code")
    x_grn = fields.Char(string="GRN No", related="lot_id.x_grn")
    x_boe = fields.Char(string="Bill of Entry No", related="lot_id.x_bill")
    x_pallet = fields.Char(string="Pallet ID", related="lot_id.x_pallet_id.name")
    # x_ltype = fields.Selection(string="Location Type", related="location_id.usage")
    x_barcode = fields.Char(string="Barcode", related="location_id.barcode")
    x_uom = fields.Many2one('uom.uom', string='UOM', related="product_id.uom_id")
    x_currency = fields.Many2one('res.currency', string="Currency", related="product_id.cost_currency_id")

    x_weight = fields.Float(string="Gross Weight", related="lot_id.gross_weight")
    x_volume = fields.Float(string="Available Volume", related="lot_id.volume")
    net_weight = fields.Float(string='Net Weight', store=True, related="lot_id.net_weight")

    item_boe = fields.Char(string='Item No as per BOE', related="lot_id.item_boe")
    sche_date = fields.Datetime(string="IN Date",store=True, readonly=False, compute="_compute_indate")

    x_ex = fields.Float(string="EX Rate", related="x_currency.rate")
    x_batchno = fields.Char(string="Batch No", related="lot_id.batchno")
    x_prod = fields.Datetime(string="Production Date", related="lot_id.use_date")
    x_exp = fields.Datetime(string="Expiry Date", related="lot_id.removal_date")
    x_coo = fields.Char(string="COO", compute="_compute_coo")
    x_ltype = fields.Many2many('stock.location.storage.type', 'x_stock_location_storage_type_stock_quant_rel',
                               'stock_quant_id', 'stock_location_storage_type_id', string="Location Type",
                               compute="_compute_x_ltype")
    x_sarea = fields.Many2many('stock.location.tag', string="Storage Area", related="location_id.tag_ids")
    x_stype = fields.Many2one('storage.type', string="Storage Type", related="product_id.storage_type")
    x_container_no = fields.Char(string="Container No", compute="_compute_containerno")
    putaway_zone = fields.Char(string="Putaway Zone", related="location_id.zone_location_id.name")
    x_tno = fields.Char(string="Truck Number", compute="_compute_truckno")
    total_nw = fields.Float(string="Net Weight", store=True, compute='_compute_total_nw')
    total_gw = fields.Float(string="Gross Weight", store=True, compute='_compute_total_gw')

    @api.depends('lot_id.gross_weight', 'quantity')
    def _compute_total_gw(self):
        for rec in self:
            rec['total_gw'] = rec.lot_id.gross_weight * rec.quantity

    @api.depends('lot_id.net_weight', 'quantity')
    def _compute_total_nw(self):
        for rec in self:
            rec['total_nw'] = rec.lot_id.net_weight * rec.quantity

    @api.depends('location_id')
    def _compute_valuegoods(self):
        for rec in self:
            mv = self.env['stock.move.line'].search([('lot_id', 'in', rec.lot_id.ids)])
            if mv:
                for m in mv:
                    if m.move_id.value_goods:
                        rec.value_goods = m.move_id.value_goods
                    else:
                        rec.value_goods = 0
            else:
                rec.value_goods = 0


    value_goods = fields.Float(string="Value", compute="_compute_valuegoods")

    @api.depends('lot_id.x_asn')
    def _compute_asn(self):
        for rec in self:
            if rec.lot_id.x_asn:
                rec['x_asn'] = rec.lot_id.x_asn
            else:
                grn = rec.x_grn
                asn = self.env['stock.picking'].search([('name', '=', grn)])
                if asn:
                    rec['x_asn'] = asn[0].warehouse_id.name
                else:
                    rec['x_asn'] = ''

    @api.depends("x_we", "quantity")
    def _compute_grossweight(self):
        for rec in self:
            if rec.x_we:
                rec['x_weight'] = rec.x_we * rec.quantity
            else:
                rec['x_weight'] = ''

    @api.depends("x_vol", "quantity")
    def _compute_availablevolume(self):
        for rec in self:
            if rec.x_vol:
                rec['x_volume'] = rec.x_vol * rec.quantity
            else:
                rec['x_volume'] = ''

    @api.depends("lot_id", "product_id")
    def _compute_coo(self):
        for rec in self:
            if rec.lot_id.x_coo:
                rec['x_coo'] = rec.lot_id.x_coo.name
            else:
                rec['x_coo'] = rec.product_id.country_id.name

    @api.depends("location_id")
    def _compute_x_ltype(self):
        for rec in self:
            if rec.location_id:
                rec['x_ltype'] = rec.location_id.location_storage_type_ids

    @api.depends('location_id')
    def _compute_containerno(self):
        for rec in self:
            mv = self.env['stock.move.line'].search([('lot_id', 'in', rec.lot_id.ids)])
            if mv:
                for m in mv:
                    if m.picking_id.warehouse_id.multi_container_ids:
                        container_no = []
                        for trk in m.picking_id.warehouse_id.multi_container_ids:
                            if trk.container_serial_no:
                                container_no.append(trk.container_serial_no)
                        result = ','.join(container_no)
                        rec.x_container_no = result
                    else:
                        rec.x_container_no = ''
            else:
                rec.x_container_no = ''

    @api.depends('location_id')
    def _compute_indate(self):
        for rec in self:
            mv = self.env['stock.move.line'].search([('lot_id', 'in', rec.lot_id.ids)])
            if mv:
                for m in mv:
                    if m.picking_id.scheduled_date:
                        rec.sche_date = m.picking_id.scheduled_date
                    else:
                        rec.sche_date = ''
            else:
                rec.sche_date = ''

    @api.depends('location_id')
    def _compute_truckno(self):
        for rec in self:
            mv = self.env['stock.move.line'].search([('lot_id', 'in', rec.lot_id.ids)])
            if mv:
                for m in mv:
                    if m.picking_id.warehouse_id.multi_container_ids:
                        container_no = []
                        for trk in m.picking_id.warehouse_id.multi_container_ids:
                            if trk.truck_no:
                                container_no.append(trk.truck_no)
                        result = ','.join(container_no)
                        rec.x_tno = result
                    else:
                        rec.x_tno = ''
            else:
                rec.x_tno = ''
