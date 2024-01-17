from odoo import models, fields, api, _


class StockProductionLot(models.Model):
    _inherit = "stock.production.lot"

    # stock_movement_report_view
    x_name = fields.Char(string="ASN", related="warehouse_order_ids.name")


class StockMoveLine(models.Model):
    _inherit = "stock.move.line"

    x_war = fields.Char(string="Warehouse", related="lot_id.x_war_code")
    x_ccode = fields.Char(string="Customer Code", compute="_compute_ccode")
    owner_id = fields.Many2one(
        'res.partner', 'Customer Name',
        check_company=True,
        help="When validating the transfer, the products will be taken from this owner.")
    # x_sku_id = fields.Many2one('product.product', 'Product Code', related='move_id.x_sku_id')

    x_name = fields.Char(string="Product Name", related="product_id.description")
    barcode = fields.Char(string="BAR Code", related="product_id.barcode")
    x_hs = fields.Char(string="HS Code", related="product_id.hs_code_id.local_code")
    x_cntr_code = fields.Char(string="Truck-CNTR Code", compute="_compute_container")
    x_tno = fields.Char(string="TRK Number", compute="_compute_truckno")
    container_no = fields.Char(string="CNTR Number", compute="_compute_containerno")
    x_trans_type = fields.Char(string="Transaction Type", compute="_compute_transaction_type")
    origin = fields.Char(related='move_id.origin', string='Transaction ID')
    x_trans_date = fields.Datetime(string="Trans Date", store="true", readonly=False,
                                   related="picking_id.scheduled_date")
    x_trans_no = fields.Char(string='Trans No', related="picking_id.name")
    loc = fields.Many2one('stock.location', 'Location Code', compute='_locloc')

    loc_code = fields.Many2one('stock.location', 'Location Code', compute="_compute_loc_code")
    total_nw = fields.Float(string="Net Weight", store=True)
    total_gw = fields.Float(string="Gross Weight", store=True)

    @api.depends('picking_id')
    def _compute_loc_code(self):
        for rec in self:
            if rec.picking_code == "incoming":
                rec.loc_code = rec.location_dest_id
            elif rec.picking_code == "outgoing":
                rec.loc_code = rec.location_id
            else:
                rec.loc_code = None

    x_uom = fields.Many2one('uom.uom', string="UOM", related="move_id.product_uom")
    x_qty = fields.Float(string="QTY", compute="compute_qty")

    x_volu = fields.Float(string="Volume", related="move_id.x_volume1")
    x_vol = fields.Float(string="Volume", related="lot_id.volume")
    x_gross = fields.Float(string="Gross Weight", related="lot_id.gross_weight")
    # net_weight = fields.Float(string='Net Weight', related="move_id.net_weight")

    x_namee = fields.Char(string="In Transaction No", related="lot_id.x_name")
    result_package_id = fields.Many2one(
        'stock.quant.package', 'Pallet ID',
        ondelete='restrict', required=False, check_company=True,
        domain="['|', '|', ('location_id', '=', False), ('location_id', '=', location_dest_id), ('id', '=', package_id)]",
        help="If set, the operations are packed into this package")

    # x_ref_date = fields.Datetime(string="In Ref Date", related="picking_id.scheduled_date")
    x_ref_date = fields.Datetime(string="In Ref Date", compute="_compute_ref_date")

#    @api.depends('picking_id')
#    def _compute_ref_date(self):
#        for rec in self:
#            if rec.picking_code == 'outgoing':
#                rec['x_ref_date'] = rec.picking_id.scheduled_date
#            else:
#                rec['x_ref_date'] = None

    @api.depends('picking_id')
    def _compute_ref_date(self):
        for rec in self:
            if rec.picking_code == 'outgoing':
                inn = self.env['stock.picking'].search([('name', '=', rec.x_ref_no)])
                if inn:
                    rec['x_ref_date'] = inn.scheduled_date
                else:
                    rec['x_ref_date'] = None
            else:
                rec['x_ref_date'] = None

    # x_ref_no = fields.Char(string="In Ref No", related="lot_id.x_grn")
    x_ref_no = fields.Char(string="In Ref No", compute="_compute_ref_no")

    @api.depends('picking_id')
    def _compute_ref_no(self):
        for rec in self:
            if rec.picking_code == 'outgoing':
                rec['x_ref_no'] = rec.lot_id.x_grn
            else:
                rec['x_ref_no'] = None

    # x_bill = fields.Char(string="In BOE", related="lot_id.x_bill") # in hb_stock fields
    def _compute_in_boe(self):

        for rec in self:
            if rec.picking_code == 'outgoing':
                rec['x_bill'] = rec.lot_id.x_bill
            else:
                rec['x_bill'] = False
    x_bill = fields.Char(string="In BOE", store=True, readonly=False, compute=_compute_in_boe)

    # @api.depends('picking_id')


    production_date = fields.Date(string="MF Date")
    expiry_date = fields.Date(string="Exp Date")
    x_coo = fields.Many2one('res.country', string="COO", related="product_id.country_id")

    # item_boe = fields.Char(string='Item No as per BOE', related="lot_id.item_boe") # in hb_stock fields

    pallet = fields.Many2one('stock.quant.package', string=" Pallet ID", compute="_compute_pallet")

    @api.depends('picking_id')
    def _compute_pallet(self):
        for rec in self:
            if rec.picking_id.picking_type_id.code == 'incoming':
                if rec.result_package_id:
                    rec['pallet'] = rec.result_package_id.id
                else:
                    if rec.lot_id:
                        if rec.lot_id.x_pallet_id:
                            rec['pallet'] = rec.lot_id.x_pallet_id.id
                        else:
                            rec['pallet'] = False
                    else:
                        rec['pallet'] = False

            else:
                if rec.package_id:
                    rec['pallet'] = rec.package_id.id
                else:
                    if rec.lot_id:
                        if rec.lot_id.x_pallet_id:
                            rec['pallet'] = rec.lot_id.x_pallet_id.id
                        else:
                            rec['pallet'] = False
                    else:
                        rec['pallet'] = False

    @api.depends('picking_id')
    def _compute_transaction_type(self):
        for rec in self:
            if rec.picking_id.picking_type_id.code == 'outgoing':
                rec['x_trans_type'] = "GDN"
            elif rec.picking_id.picking_type_id.code == 'incoming':
                rec['x_trans_type'] = "GRN"
            else:
                rec['x_trans_type'] = False

    @api.depends('qty_done', 'picking_id.picking_type_id')
    def compute_qty(self):
        for rec in self:
            if rec.picking_id.picking_type_id.code == 'outgoing':
                rec['x_qty'] = float('-' + str(rec.qty_done))
            elif rec.picking_id.picking_type_id.code == 'incoming':
                rec['x_qty'] = rec.qty_done
            else:
                rec['x_qty'] = rec.qty_done

    # @api.depends('qty_done', 'x_volu')
    # def compute_vol(self):
    #     for rec in self:
    #         if rec.picking_id.picking_type_id.code == 'outgoing':
    #             rec['x_vol'] = float('-' + str(rec.x_volu * rec.qty_done))
    #         else:
    #             rec['x_vol'] = rec.x_volu * rec.qty_done

    @api.depends('qty_done', 'x_weight')
    def compute_x_gross(self):
        for rec in self:
            rec['x_gross'] = rec.x_weight * rec.qty_done

    @api.depends('picking_id')
    def _compute_container(self):
        for rec in self:
            if rec.picking_id.warehouse_id.multi_container_ids:
                x_cntr_code = []
                for cnt in rec.picking_id.warehouse_id.multi_container_ids:
                    if cnt.container.name:
                        x_cntr_code.append(cnt.container.name)
                result1 = ','.join(x_cntr_code)
                rec.x_cntr_code = result1
            else:
                rec.x_cntr_code = ''

    @api.depends('picking_id')
    def _compute_truckno(self):
        for rec in self:
            if rec.picking_id.warehouse_id.multi_container_ids:
                x_tno = []
                for trk in rec.picking_id.warehouse_id.multi_container_ids:
                    if trk.truck_no:
                        x_tno.append(trk.truck_no)
                result = ','.join(x_tno)
                rec.x_tno = result
            else:
                rec.x_tno = ''

    @api.depends('picking_id')
    def _compute_containerno(self):
        for rec in self:
            if rec.picking_id.warehouse_id.multi_container_ids:
                container_no = []
                for trk in rec.picking_id.warehouse_id.multi_container_ids:
                    if trk.container_serial_no:
                        container_no.append(trk.container_serial_no)
                result = ','.join(container_no)
                rec.container_no = result
            else:
                rec.container_no = ''

    @api.depends('picking_id')
    def _compute_ccode(self):
        for rec in self:
            if rec.picking_id.owner_id.x_code:
                rec.x_ccode = rec.picking_id.owner_id.x_code
            else:
                rec.x_ccode = ''
