from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError
from lxml import etree
from datetime import datetime


class SubJob(models.Model):
    _name = 'sub.job'
    _description = 'Sub Job'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _check_company_auto = True

    user_id = fields.Many2one('res.users', string='User', default=lambda self: self.env.user, tracking=True)
    company_id = fields.Many2one('res.company', string='Company', required=True,
                                 default=lambda self: self.env.company)
    name = fields.Char(string='Order Reference', required=True, copy=False, readonly=True,
                       states={'draft': [('readonly', False)]}, index=True, default=lambda self: _('New'))

    job_type = fields.Many2one("utm.medium", readonly=True)
    partner_id = fields.Many2one("res.partner", string="Client Name", readonly=True,
                                 domain="[('company_id', '=', company_id)]")
    client_no = fields.Char(string="Client No", readonly=True, related="partner_id.x_code")
    client_ref = fields.Char(string="Client Ref")
    consignee_id = fields.Many2one("res.partner", string="Consignee", readonly=True,
                                   domain="[('company_id', '=', company_id)]")
    received_qty = fields.Integer(string="Received Qty", readonly=True)
    manifest_qty = fields.Integer(string="Manifest Qty", readonly=True)
    weight = fields.Float(string="Weight", readonly=True, digits=(6, 3))
    volume = fields.Float(string="Volume", readonly=True, digits=(6, 3))
    port_of_origin = fields.Many2one('freight.port', string="Port Of Origin", readonly=True)
    port_final_destination = fields.Many2one('freight.port', string="Port Of Final Destination", readonly=True)
    remarks = fields.Text(string="Remarks", readonly=True)
    shipper = fields.Many2one("res.partner", string="Shipper", readonly=True)
    flight = fields.Char(string="Vessel/Flight", readonly=True)
    mbl_no = fields.Char(string="MBL No", readonly=True)
    hbl_no = fields.Char(string="HBL No", readonly=True)
    transport = fields.Selection(
        [("land", "Land"), ("ocean", "Ocean"), ("air", "Air")],
        string="Transport", readonly=True
    )
    truck_no = fields.Char(sting='Truck No')

    def default_warehouse(self):
        default_value = self.env['stock.warehouse'].search([('company_id', '=', self.env.company.id)]).id
        return default_value

    stock_warehouse_id = fields.Many2one("stock.warehouse", string="Warehouse", readonly=True,
                                         default=default_warehouse)
    storage_type = fields.Many2one('storage.type', string='Storage Type')
    eta = fields.Date(string="Receipt Date", tracking=True)
    etd = fields.Date(string="Delivery Date", tracking=True)
    container_qty = fields.Float(string="Container Qty", readonly=True)
    container_type = fields.Many2one('x_type', string='Container Type', readonly=True)
    container_no = fields.Char(string="Container No", readonly=True)
    place_of_delivery = fields.Char(string="Place Of Delivery")
    shipment_no = fields.Char(string="Deliver To")
    notify_party = fields.Many2one('res.partner', string="Notify Party", domain="[('company_id', '=', company_id)]")
    billno = fields.Char(string="B/E No", readonly=True)

    # delivery details fields
    driver_id = fields.Char(string='Driver ID')
    delivery_received_by = fields.Many2one('res.partner', string="Delivery Received By",
                                           domain="[('company_id', '=', company_id)]")
    driver = fields.Char(string="Driver Name")
    driver_number = fields.Char(string="Driver Phone Number")
    truck_in_date = fields.Date(string="Truck In Date")
    truck_out_date = fields.Date(string="Truck Out Date")
    delivery_date = fields.Date(string="Delivery Date")
    cargo_received_by = fields.Many2one('res.partner', string="Cargo Received By",
                                        domain="[('company_id', '=', company_id)]")
    receiver_name = fields.Many2one('res.partner', string="Receiver Name", domain="[('company_id', '=', company_id)]")
    received_date = fields.Date(string="Received Date")

    state = fields.Selection([('draft', 'Draft'),
                              ('confirm', 'Confirm'),
                              ('cancel', 'Cancel'), ], string='State', default='draft', readonly=True, tracking=True)

    origin = fields.Char(string="Source Document", readonly=True)

    job_id = fields.Many2one("freight.operation")
    jobline_id = fields.Many2one("freight.operation.line")
    accountmove_id = fields.Many2one("account.move")
    grn_id = fields.Many2one('stock.picking')
    delivery_id = fields.Many2one('stock.picking')
    subjob_line_ids = fields.One2many("sub.job.line", "subjob_id")

    style = fields.Many2one('report.template.settings')

    po_count = fields.Integer('PO Count', compute='_compute_po_count')
    do_count = fields.Integer('DO Count', compute='_compute_do_count')
    inv_count = fields.Integer('DO Count', compute='_compute_inv_count')

    def _compute_po_count(self):
        obj = self.env['stock.picking'].search([('subjob_id', '=', self.id)]).filtered(
            lambda rec: rec.picking_type_code == 'incoming')
        if obj:
            self.po_count = len(obj)
        else:
            self.po_count = 0

    def _compute_do_count(self):
        obj = self.env['stock.picking'].search([('subjob_id', '=', self.id)]).filtered(
            lambda rec: rec.picking_type_code == 'outgoing')
        if obj:
            self.do_count = len(obj)
        else:
            self.do_count = 0

    def _compute_inv_count(self):
        obj = self.env['account.move'].search([('subjob_id', '=', self.id)])
        if obj:
            self.inv_count = len(obj)
        else:
            self.inv_count = 0

    @api.model
    def create(self, vals):
        vals['name'] = self.env['ir.sequence'].next_by_code('sub.job') or _('New')
        return super(SubJob, self).create(vals)

    def action_cancel(self):
        self.state = 'cancel'
        job_line = self.env['freight.operation.line'].search([('subjob_id', '=', self.id)])
        job_line.update({'subjob_id': False})

    def action_grn(self):
        obj = self.env['stock.picking'].search([('subjob_id', '=', self.id)]).filtered(
            lambda rec: rec.picking_type_code == 'incoming')
        return {
            'name': _('Delivery Order'),
            'view_mode': 'form,tree',
            'res_model': 'stock.picking',
            'res_id': obj.id,
            'type': 'ir.actions.act_window',
        }

    def action_do(self):
        obj = self.env['stock.picking'].search([('subjob_id', '=', self.id)]).filtered(
            lambda rec: rec.picking_type_code == 'outgoing')
        return {
            'name': _('Delivery Order'),
            'view_mode': 'form,tree',
            'res_model': 'stock.picking',
            'res_id': obj.id,
            'type': 'ir.actions.act_window',
        }

    def action_create_grn(self):
        # pick_type = self.env['stock.picking.type'].search([('code', '=', 'incoming')
        #                                                       , ('company_id', '=', self.company_id.id)])
        pick_type = self.stock_warehouse_id.in_type_id
        if pick_type:
            if self.storage_type:
                for rec in self:
                    vals = {
                        'name': self.env['ir.sequence'].next_by_code('sub.job.grn') or _('New'),
                        'x_job_type': rec.job_type.id,
                        'partner_id': rec.partner_id.id,
                        'picking_type_id': pick_type.id,
                        'x_transport_mode': rec.transport,
                        'x_wt': rec.weight,
                        'x_vol': rec.volume,
                        'x_flight': rec.flight,
                        'x_hbl': rec.hbl_no,
                        'x_eta': rec.eta,
                        'etd': rec.etd,
                        "x_billno": self.billno,
                        'storage_type': rec.storage_type,
                        'origin': rec.name,
                        # 'location_id': self.env.ref('stock.stock_location_stock').id,
                        'location_id': self.partner_id.property_stock_supplier.id,
                        # 'location_dest_id': self.env.ref('stock.stock_location_customers').id,
                        'location_dest_id': self.stock_warehouse_id.lot_stock_id.id,
                        'subjob_id': self.id,
                        'driver_id': self.driver_id,
                        'x_deliveryreceivedby': self.delivery_received_by.id,
                        'x_driver1': self.driver,
                        'x_driver_number': self.driver_number,
                        'truck_in_date': self.truck_in_date,
                        'x_truck_out_date': self.truck_out_date,
                        'x_deliverydate': self.delivery_date,
                        'x_cargoreceivedby': self.cargo_received_by.id,
                        'x_receiver_name': self.receiver_name.id,
                        'x_received_date': self.received_date,
                        'company_id': self.company_id.id,
                    }
                    new_grn = self.env['stock.picking'].create(vals)
                    for rec_line in rec.subjob_line_ids:
                        vals_line = {
                            'name': rec_line.product_id.name,
                            "product_id": rec_line.product_id.id,
                            "product_uom_qty": rec_line.product_qty,
                            'picking_id': new_grn.id,
                            'product_uom': rec_line.product_id.uom_id.id,
                            'location_id': self.partner_id.property_stock_supplier.id,
                            'location_dest_id': self.stock_warehouse_id.lot_stock_id.id,
                        }
                        new_stockmove = self.env['stock.move'].create(vals_line)
                        vals_stock_line = {
                            'picking_id': new_grn.id,
                            'move_id': new_stockmove.id,
                            "product_id": rec_line.product_id.id,
                            'product_uom_id': rec_line.product_id.uom_id.id,
                            'qty_done': rec_line.product_qty,
                            'location_id': self.partner_id.property_stock_supplier.id,
                            'location_dest_id': self.stock_warehouse_id.lot_stock_id.id,
                        }
                        new_stockmove = self.env['stock.move.line'].create(vals_stock_line)

                    new_grn.action_confirm()
                    new_grn.action_assign()
                    new_grn.button_validate()
                    self.update({'grn_id': new_grn.id})
                    self.update({'state': 'confirm'})
            else:
                raise UserError(_('Please choose Storage Type'))
        else:
            raise UserError(_('stock picking type is empty'))

    def action_delivery_goods(self):
        obj = self.env['stock.picking'].search([('subjob_id', '=', self.id)])
        # pick_type = self.env['stock.picking.type'].search([('code', '=', 'outgoing')
        #                                                       , ('company_id', '=', self.company_id.id)])
        pick_type = self.stock_warehouse_id.out_type_id
        if pick_type:
            if obj:
                for rec in obj:
                    vals = {
                        'name': self.env['ir.sequence'].next_by_code('sub.job.do') or _('New'),
                        'x_job_type': rec.x_job_type.id,
                        'partner_id': rec.partner_id.id,
                        'picking_type_id': pick_type.id,
                        'x_transport_mode': rec.x_transport_mode,
                        'x_wt': rec.x_wt,
                        'x_vol': rec.x_vol,
                        'x_flight': rec.x_flight,
                        'x_hbl': rec.x_hbl,
                        'x_eta': rec.x_eta,
                        'etd': rec.etd,
                        "x_billno": rec.x_billno,
                        'storage_type': rec.storage_type,
                        'origin': rec.name,
                        'subjob_id': self.id,
                        'location_id': pick_type.default_location_src_id.id,
                        'location_dest_id': self.env.ref('stock.stock_location_customers').id,
                        'driver_id': rec.driver_id,
                        'x_deliveryreceivedby': rec.x_deliveryreceivedby.id,
                        'x_driver1': rec.x_driver1,
                        'x_driver_number': rec.x_driver_number,
                        'truck_in_date': rec.truck_in_date,
                        'x_truck_out_date': rec.x_truck_out_date,
                        'x_deliverydate': rec.x_deliverydate,
                        'x_cargoreceivedby': rec.x_cargoreceivedby.id,
                        'x_receiver_name': rec.x_receiver_name.id,
                        'x_received_date': rec.x_received_date,
                        'x_sign': rec.x_sign,
                        'move_ids_without_package': [(0, 0, {
                            'name': rec.move_ids_without_package.product_id.name,
                            'product_id': rec.move_ids_without_package.product_id.id,
                            'product_uom_qty': rec.move_ids_without_package.product_uom_qty,
                            'product_uom': rec.move_ids_without_package.product_id.uom_id.id,
                            # 'reserved_availability':rec.move_ids_without_package.product_uom_qty,
                        })]

                    }
                    new_do = self.env['stock.picking'].create(vals)
                    stock_move = self.env['stock.move'].search([('picking_id', '=', new_do.id)])
                    stock_line = self.env['stock.move.line'].create({
                        'picking_id': new_do.id,
                        'move_id': stock_move.id,
                        'lot_id': self.env['stock.move.line'].search([('picking_id', '=', self.grn_id.id)]).lot_id.id,
                        'product_id': rec.move_ids_without_package.product_id.id,
                        'product_uom_id': rec.move_ids_without_package.product_id.uom_id.id,
                        'location_id': pick_type.default_location_src_id.id,
                        'location_dest_id': self.env.ref('stock.stock_location_customers').id,
                        'qty_done': rec.move_ids_without_package.product_uom_qty,
                    })
                    new_do.action_confirm()
                    new_do.action_assign()
                    # new_do.move_line_ids_without_package.qty_done = new_do.move_ids_without_package.reserved_availability
                    new_do.button_validate()
                    self.update({'delivery_id': new_do.id})

            else:
                raise UserError(_("GRN is not created"))
        else:
            raise UserError(_('stock picking type is empty'))

    def create_cfsinvoice(self):
        if self.storage_type:
            if (self.po_count == 0 and self.do_count == 0) or (self.po_count == 1 and self.do_count == 1):
                current_user = self.env.uid
                # customer_journal_id = self.env['ir.config_parameter'].sudo().get_param(
                #     'stock_move_invoice.customer_journal_id') or False
                # if not customer_journal_id:
                #     raise UserError(_("Please configure the journal from settings"))
                now = self.etd
                stoarge_type = self.storage_type
                eta = self.eta
                if eta == False:
                    raise UserError(_("Please make sure ETA in sub job"))
                if now == False:
                    raise UserError(_("Please make sure ETD in sub job"))
                dur = abs((eta - now).days) + 1
                invoice_line_list = []
                agreement_id = self.env['agreement'].search([('type', '=', 'cfs')])
                for temp in agreement_id.charge_lines_new:
                    if temp.charge_type == 'fixed' and temp.charge_unit_type == 'cbm' and temp.storage_type == self.storage_type:
                        if self.weight / 1000 <= self.volume:
                            meass = self.volume
                            if meass <= 1:
                                meas = 1
                            else:
                                meas = meass
                            uom = 'cbm'
                            print(uom, 'uom', meas, 'meas')
                        else:
                            meass = self.weight / 1000
                            if meass <= 1:
                                meas = 1
                            else:
                                meas = meass
                            uom = 'weight'

                        temp_line_values = {
                            'product_id': temp.product_id and temp.product_id.id or False,
                            'name': temp.product_id.name or '',
                            'price_unit': temp.list_price or 0.00,
                            'quantity': meas,
                            'currency_id': temp.currency_id.id,
                            'account_id': temp.product_id.property_account_income_id.id if temp.product_id.property_account_income_id
                            else temp.product_id.categ_id.property_account_income_categ_id.id,
                            'tax_ids': [(6, 0, temp.product_id.taxes_id.ids)],

                        }
                        invoice_line_list.append((0, 0, temp_line_values))
                for temp in agreement_id.charge_lines_new:
                    if temp.charge_type == 'fixed' and temp.charge_unit_type == 'cbm' and temp.storage_type == False:
                        if self.weight / 1000 <= self.volume:
                            meass = self.volume
                            if meass <= 1:
                                meas = 1
                            else:
                                meas = meass
                            uom = 'cbm'
                            print(uom, 'uom', meas, 'meas')
                        else:
                            meass = self.weight / 1000
                            if meass <= 1:
                                meas = 1
                            else:
                                meas = meass
                            uom = 'weight'
                            print(uom, 'uom', meas, 'meas')
                        temp_line_values = {
                            'product_id': temp.product_id and temp.product_id.id or False,
                            'name': temp.product_id.name or '',
                            'price_unit': temp.list_price or 0.00,
                            'quantity': meas,
                            'currency_id': temp.currency_id.id,
                            'account_id': temp.product_id.property_account_income_id.id if temp.product_id.property_account_income_id
                            else temp.product_id.categ_id.property_account_income_categ_id.id,
                            'tax_ids': [(6, 0, temp.product_id.taxes_id.ids)],
                        }
                        invoice_line_list.append((0, 0, temp_line_values))
                for temp in agreement_id.charge_lines_new:
                    if temp.charge_type == 'fixed' and temp.charge_unit_type == 'shipment' and temp.storage_type == self.storage_type:
                        temp_line_values = {
                            'product_id': temp.product_id and temp.product_id.id or False,
                            'name': temp.product_id.name or '',
                            'price_unit': temp.list_price or 0.00,
                            'quantity': 1,
                            'currency_id': temp.currency_id.id,
                            'account_id': temp.product_id.property_account_income_id.id if temp.product_id.property_account_income_id
                            else temp.product_id.categ_id.property_account_income_categ_id.id,
                            'tax_ids': [(6, 0, temp.product_id.taxes_id.ids)],

                        }
                        invoice_line_list.append((0, 0, temp_line_values))

                for temp in agreement_id.charge_lines_new:
                    if temp.charge_type == 'fixed' and temp.charge_unit_type == 'shipment' and temp.storage_type == False:
                        temp_line_values = {
                            'product_id': temp.product_id and temp.product_id.id or False,
                            'name': temp.product_id.name or '',
                            'price_unit': temp.list_price or 0.00,
                            'quantity': 1,
                            'currency_id': temp.currency_id.id,
                            'account_id': temp.product_id.property_account_income_id.id if temp.product_id.property_account_income_id
                            else temp.product_id.categ_id.property_account_income_categ_id.id,
                            'tax_ids': [(6, 0, temp.product_id.taxes_id.ids)],

                        }
                        invoice_line_list.append((0, 0, temp_line_values))
                for temp in agreement_id.charge_lines_new:
                    if self.weight / 1000 <= self.volume:
                        meass = self.volume
                        if meass <= 1:
                            meas = 1
                        else:
                            meas = meass
                        uom = 'cbm'
                        print(uom, 'uom', meas, 'meas')
                    else:
                        meass = self.weight / 1000
                        if meass <= 1:
                            meas = 1
                        else:
                            meas = meass
                        uom = 'weight'
                        print(uom, 'uom', meas, 'meas')
                    if temp.charge_type == 'storage' and temp.storage_type == self.storage_type:
                        if int(dur) >= temp.fromm:
                            if int(dur) >= temp.to and temp.to != 0:
                                temp_line_values = {
                                    'product_id': temp.product_id and temp.product_id.id or False,
                                    'name': temp.product_id.name or '',
                                    'price_unit': temp.list_price or 0.00,
                                    'quantity': meas * (abs(temp.to - temp.fromm) + 1),
                                    'currency_id': temp.currency_id.id,
                                    'x_cbm': self.volume,
                                    'x_weight': self.weight / 1000,
                                    'uom_type': uom,
                                    'account_id': temp.product_id.property_account_income_id.id if temp.product_id.property_account_income_id
                                    else temp.product_id.categ_id.property_account_income_categ_id.id,
                                    'tax_ids': [(6, 0, temp.product_id.taxes_id.ids)],
                                }
                                invoice_line_list.append((0, 0, temp_line_values))
                            else:
                                temp_line_values = {
                                    'product_id': temp.product_id and temp.product_id.id or False,
                                    'name': temp.product_id.name or '',
                                    'price_unit': temp.list_price or 0.00,
                                    'quantity': meas * (abs(dur - temp.fromm) + 1),
                                    'currency_id': temp.currency_id.id,
                                    'x_cbm': self.volume,
                                    'x_weight': self.weight / 1000,
                                    'uom_type': uom,
                                    'account_id': temp.product_id.property_account_income_id.id if temp.product_id.property_account_income_id
                                    else temp.product_id.categ_id.property_account_income_categ_id.id,
                                    'tax_ids': [(6, 0, temp.product_id.taxes_id.ids)],
                                }
                                invoice_line_list.append((0, 0, temp_line_values))

                invoice = self.env['account.move'].create({
                    'name': self.env['ir.sequence'].next_by_code('sub.job.inv') or _('New'),
                    'type': 'out_invoice',
                    'invoice_origin': self.name,
                    'invoice_user_id': current_user,
                    'narration': self.name,
                    'partner_id': self.partner_id.id,
                    'currency_id': self.env.user.company_id.currency_id.id,
                    # 'journal_id': int(customer_journal_id),
                    'invoice_payment_ref': self.name,
                    'subjob_id': self.id,
                    'invoice_line_ids': invoice_line_list,
                    'invoice_date': datetime.today(),
                    'x_consignee1': self.consignee_id.id,
                    'x_port': self.port_of_origin,
                    'x_final': self.port_final_destination,
                    'x_master': self.mbl_no,
                    'x_hn': self.hbl_no,
                    'x_weight': self.weight,
                    'x_volume': self.volume,
                    'x_etd': self.etd,
                    'x_eta': self.eta,
                    'x_grn_inv_type': self.job_type.id,
                })
                self.update({'accountmove_id': invoice.id})
                self.update({'state': 'confirm'})
            else:
                raise UserError(_("Please Validate Delivery Order First"))
        else:
            raise UserError(_('Please choose Storage Type'))

    def action_inv(self):
        obj = self.env['account.move'].search([('narration', '=', self.name)])
        if self.inv_count == 0:
            raise UserError(_("Current Record had no sub job"))
        else:
            return {
                'name': _('SUB JOB INVOICE'),
                'view_mode': 'form,tree',
                'res_model': 'account.move',
                'res_id': obj.id,
                'type': 'ir.actions.act_window',
                # 'context': ctx,
            }


class SubJobLine(models.Model):
    _name = 'sub.job.line'
    _description = 'Sub Job Line'

    # line_no = fields.Integer(string="SI No", readonly=True)
    product_id = fields.Many2one("product.product", string="Product Name", readonly=True)
    product_description = fields.Char(string="Description", readonly=False)
    product_qty = fields.Float(string="Product Quantity", readonly=True)
    uom_id = fields.Many2one("uom.uom", related="product_id.uom_id", readonly=True)

    subjob_id = fields.Many2one('sub.job', readonly=True)


class FreightOperation(models.Model):
    _inherit = "freight.operation"

    po_count = fields.Integer('PO Count', compute='_compute_po_count')
    subjob_link_id = fields.One2many('sub.job', 'job_id')
    billno = fields.Char(string="B/E No")
    company_id = fields.Many2one('res.company', string='Company', required=True,
                                 default=lambda self: self.env.company)

    def _compute_po_count(self):
        obj = self.env['sub.job'].search([('job_id', '=', self.id)])
        if obj:
            self.po_count = len(obj)
        else:
            self.po_count = 0

    def action_sub_job(self):
        if self.po_count == 0:
            raise UserError(_("Current Record had no sub job"))
        else:
            return {
                'name': _("sub job"),
                'type': 'ir.actions.act_window',
                'view_mode': 'tree,form',
                'res_model': 'sub.job',
                'target': 'current',
                'context': {},
                'domain': [('job_id', '=', self.id)],
            }

    def action_create_sub_job(self):
        sub_job = self.env['sub.job']
        current_date = datetime.today().date()
        if self.id:
            activeid = self.id
            data = self
            consignment_line_data = self.env['freight.operation.line'].search([('operation_id', '=', activeid)])
            for con_line in consignment_line_data:
                if con_line.id not in sub_job.search([]).jobline_id.ids:
                    vals = {
                        "job_type": data.x_job_type.id,
                        'job_date': current_date,
                        'partner_id': con_line.partner_id.id,
                        "consignee_id": data.consignee_id.id,
                        "received_qty": con_line.qty,
                        "manifest_qty": con_line.qty,
                        "weight": con_line.x_netweight,
                        "volume": con_line.x_volumeweight,
                        "port_of_origin": data.loading_port_id.id,
                        "port_final_destination": data.discharg_port_id.id,
                        "remarks": con_line.x_remark,
                        "flight": data.x_vessel,
                        "shipper": con_line.x_shipper.id,
                        "mbl_no": data.x_master_bl,
                        "hbl_no": con_line.x_hbl,
                        "billno": data.billno,
                        "transport": data.transport,
                        "container_type": data.x_container_type.id,
                        "container_no": data.x_container_no,
                        'place_of_delivery': data.x_placeofdelivery,
                        'eta': data.x_eta,
                        'etd': data.x_date,
                        'origin': data.name,
                        "job_id": data.id,
                        "jobline_id": con_line.id,
                        "subjob_line_ids": [(0, 0, {
                            "product_id": con_line.product_id.id,
                            "product_description": con_line.description,
                            "product_qty": con_line.qty,
                        })]

                    }
                    create_sub_job = self.env['sub.job'].create(vals)
                    con_line.update({'subjob_id': create_sub_job.id})


class FreightOperationLine(models.Model):
    _inherit = "freight.operation.line"

    subjob_id = fields.Many2one('sub.job')


class AccountMove(models.Model):
    _inherit = "account.move"

    subjob_id = fields.Many2one('sub.job')
    x_grn_inv_type = fields.Many2one('utm.medium', compute='compute_grn_type')

    @api.depends('picking_id')
    def compute_grn_type(self):
        if self.picking_id:
            self.x_grn_inv_type = self.picking_id.x_medium1
        elif self.subjob_id:
            self.x_grn_inv_type = self.subjob_id.job_type.id
        else:
            self.x_grn_inv_type = None


class StockPicking(models.Model):
    _inherit = "stock.picking"

    subjob_id = fields.Many2one('sub.job')

    x_transport_mode = fields.Selection([('land', 'Land'),
                                         ('air', 'Air'),
                                         ('ocean', 'Ocean'),
                                         ],
                                        string='Transport', compute='compute_transport_mode'
                                        )
    x_flight = fields.Char(string="Vessel/Flight", compute='compute_flight')
    x_hbl = fields.Char(string="BL/AWB", compute='compute_hbl')
    storage_type = fields.Many2one('storage.type', string="Storage Type", compute='compute_storage_type')
    etd = fields.Datetime(string="ETD", tracking=True)
    x_eta = fields.Datetime(string="ETA", compute='compute_stock_eta')
    company_id = fields.Many2one('res.company', string='Company', required=True,
                                 default=lambda self: self.env.company)

    @api.depends('warehouse_id')
    def compute_transport_mode(self):
        for rec in self:
            if rec.warehouse_id:
                rec.x_transport_mode = rec.warehouse_id.x_transport
            elif rec.subjob_id:
                rec.x_transport_mode = rec.subjob_id.transport
            else:
                rec.x_transport_mode = None

    @api.depends('warehouse_id')
    def compute_hbl(self):
        for rec in self:
            if rec.warehouse_id:
                rec.x_hbl = rec.warehouse_id.x_hbl
            elif rec.subjob_id:
                rec.x_hbl = rec.subjob_id.hbl_no
            else:
                rec.x_hbl = None

    @api.depends('warehouse_id')
    def compute_flight(self):
        for rec in self:
            if rec.warehouse_id:
                rec.x_flight = rec.warehouse_id.x_flight
            elif rec.subjob_id:
                rec.x_flight = rec.subjob_id.flight
            else:
                rec.x_flight = None

    @api.depends('warehouse_id')
    def compute_storage_type(self):
        for rec in self:
            if rec.warehouse_id:
                rec.storage_type = rec.warehouse_id.storage_type
            elif rec.subjob_id:
                rec.storage_type = rec.subjob_id.storage_type
            else:
                rec.storage_type = None

    @api.depends('warehouse_id')
    def compute_stock_eta(self):
        for rec in self:
            if rec.warehouse_id:
                rec.x_eta = rec.warehouse_id.x_eta
            elif rec.subjob_id:
                rec.x_eta = rec.subjob_id.eta
            else:
                rec.x_eta = None
