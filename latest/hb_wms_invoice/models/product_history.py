from odoo import models, fields, api, _
from datetime import datetime


class ProductHistory(models.Model):
    _name = 'product.history'

    product_id = fields.Many2one('product.product', string='Product', required=True)
    quantity = fields.Float(string='Quantity', required=True)
    in_date = fields.Datetime(string='In Date')
    out_date = fields.Datetime(string='Out Date')
    location_id = fields.Many2one('stock.location', string='Location', required=True)
    partner_id = fields.Many2one('res.partner', string='Partner')
    lot_id = fields.Many2one('stock.production.lot', string="Tracking No")
    pallet_id = fields.Many2one('stock.quant.package', string='Pallet Id')
    in_ref = fields.Many2one('stock.picking', string='In Ref No')
    out_ref = fields.Many2one('stock.picking', string='Out Ref No')
    move_line_id = fields.Many2one('stock.move.line', string='Product Moves')
    uom_id = fields.Many2one('uom.uom', string='Product UOM')

    @api.model
    def create(self, vals):
        res = super(ProductHistory, self).create(vals)
        if res.in_date != False:
            summary_vals = {
                'product_id': res.product_id.id,
                'in_qty': res.quantity,
                'in_date': res.in_date,
                'location_id': res.location_id.id,
                'partner_id': res.partner_id.id,
                'lot_id': res.lot_id.id,
                'pallet_id': res.pallet_id.id,
                'uom_id': res.uom_id.id,

            }
            self.env['product.summary'].create(summary_vals)
            return res
        else:
            tracking_numers = self.env['product.summary'].search([('lot_id', '=', res.lot_id.id)])
            if tracking_numers:
                tracking_no = tracking_numers[-1]
                print(tracking_no, 'tracking number', tracking_no.out_date)
                if tracking_no:
                    if tracking_no.out_date == False:
                        summary_vals = {
                            'out_date': res.out_date,
                            'out_qty': res.quantity,
                        }
                        print('~~~~~~~~~~~~~~~~~~~')
                        tracking_no.write(summary_vals)
                    else:
                        summary_vals = {
                            'product_id': tracking_no.product_id.id,
                            'in_qty': tracking_no.quantity,
                            'in_date': tracking_no.in_date,
                            'location_id': res.location_id.id,
                            'partner_id': tracking_no.partner_id.id,
                            'lot_id': res.lot_id.id,
                            'pallet_id': res.pallet_id.id,
                            'out_date': res.out_date,
                            'out_qty': res.quantity,

                        }
                        self.env['product.summary'].create(summary_vals)

            return res


class ProductSummary(models.Model):
    _name = 'product.summary'

    product_id = fields.Many2one('product.product', string='Product')
    quantity = fields.Float(string='Quantity')
    in_date = fields.Datetime(string='In Date')
    out_date = fields.Datetime(string='Out Date')
    location_id = fields.Many2one('stock.location', string='Location')
    partner_id = fields.Many2one('res.partner', string='Partner')
    lot_id = fields.Many2one('stock.production.lot', string="Tracking No")
    pallet_id = fields.Many2one('stock.quant.package', string='Pallet Id')
    in_qty = fields.Float(string='In Quantity')
    out_qty = fields.Float(string='Out Quantity')
    duration = fields.Float(string='Duration', compute='_duration')
    storage_product = fields.Boolean(string='Is Storage control Product', compute='_storage_product', default=False, store=True)
    uom_id = fields.Many2one('uom.uom')

    def _duration(self):
        for rec in self:
            if rec.out_date and rec.in_date:
                rec['duration'] = abs((fields.Datetime.to_datetime(rec.out_date)
                                       - fields.Datetime.to_datetime(rec.in_date)).days)
            else:
                rec['duration'] = 1

    @api.constrains('in_qty', 'out_qty')
    def qty(self):
        for rec in self:
            # rec['quantity'] = (rec.in_qty - rec.out_qty)
            rec['quantity'] = rec.in_qty

    def _storage_product(self):
        for rec in self:
            if rec.product_id.storage_type:
                rec['storage_product'] = True
            else:
                rec['storage_product'] = False


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    def button_validate(self):
        res = super(StockPicking, self).button_validate()
        for rec in self:
            for mvl in rec.move_line_ids:
                mvl.product_history()


class StockMove(models.Model):
    _inherit = 'stock.move.line'

    def product_history(self):
        for rec in self:
            if rec.qty_done:
                if rec.picking_code == 'incoming':
                    history_vals = {
                        'product_id': self.product_id.id,
                        'quantity': self.qty_done,
                        # 'in_date': fields.Datetime.now(),
                        'in_date': self.picking_id.scheduled_date,
                        'location_id': self.location_dest_id.id,
                        'partner_id': self.picking_id.partner_id.id,
                        'lot_id': self.lot_id.id,
                        'pallet_id': self.result_package_id.id,
                        'in_ref': self.picking_id.id,
                        'move_line_id': self.id,
                        'uom_id': self.product_uom_id.id,

                    }
                    self.env['product.history'].create(history_vals)
                elif rec.picking_code == 'outgoing':
                    history_vals = {
                        'product_id': self.product_id.id,
                        'quantity': self.qty_done,
                        # 'out_date': fields.Datetime.now(),
                        'out_date': self.picking_id.scheduled_date,
                        'location_id': self.location_id.id,
                        'partner_id': self.picking_id.partner_id.id,
                        'lot_id': self.lot_id.id,
                        'pallet_id': self.package_id.id,
                        'out_ref': self.picking_id.id,
                        'move_line_id': self.id,
                        'uom_id': self.product_uom_id.id

                    }
                    self.env['product.history'].create(history_vals)

    # @api.model
    # def create(self, vals):
    #     res = super(StockMove, self).create(vals)
    #     # if self.picking_id:
    #     if vals['quantity_done'] > 0:
    #         history_vals = {
    #             'product_id': vals.product_id,
    #             'quantity': vals.quantity_done,
    #             'in_date': fields.Datetime.now(),
    #             'location_id': vals.location_dest_id,
    #             'partner_id': vals.partner_id,
    #         }
    #         self.env['product.history'].create(history_vals)
    #     elif vals['quantity_done'] < 0:
    #         history_vals = {
    #             'product_id': vals.product_id,
    #             'quantity': vals.quantity_done,
    #             'out_date': fields.Datetime.now(),
    #             'location_id': vals.location_id,
    #             'partner_id': vals.partner_id,
    #         }
    #         self.env['product.history'].create(history_vals)
    #     return res


class SummarysheetLines(models.Model):
    _name = 'summary.sheet.lines'

    product_id = fields.Many2one('product.product', string='Product')
    quantity = fields.Float(string='Quantity')
    start_date = fields.Datetime(string='Start Date')
    end_date = fields.Datetime(string='End Date')
    location_id = fields.Many2one('stock.location', string='Location')
    partner_id = fields.Many2one('res.partner', string='Partner')
    lot_id = fields.Many2one('stock.production.lot', string="Tracking No")
    pallet_id = fields.Many2one('stock.quant.package', string='Pallet Id')
    in_qty = fields.Float(string='In Quantity')
    out_qty = fields.Float(string='Out Quantity')
    duration = fields.Float(string='Duration', compute='_duration')
    # storage_product = fields.Boolean(string='Is Storage control Product')
    cbm = fields.Float('CBM')
    sqm = fields.Float('SQM')
    weight = fields.Float('Weight')
    pallet = fields.Float('Pallet')
    container_type = fields.Many2one('freight.container')
    in_ref_no = fields.Many2one('stock.picking')
    out_ref_no = fields.Many2one('stock.picking')
    ref_no = fields.Char(string="Reference")
    added_service = fields.Many2one('added.service')
    sheet_id = fields.Many2one('summary.sheet')
    charge_type = fields.Selection(string="Charge Unit Type",
                                   selection=[('inbound', 'Handling Inbound'), ('outbound', 'Handling Outbound'),
                                              ('storage', 'Storage'), ('value_added', 'Value Added Services'),
                                              ('inventory_mgmnt', 'Inventory Management Services')])
    charge_unit_type = fields.Selection(string="Charge Type",
                                        selection=[('cbm', 'CBM'), ('pallet', 'Pallet'), ('weight', 'Weight'),
                                                   ('square', 'Square Units'), ('custom', 'Custom')])
    amount = fields.Float(string='Amount', compute='_compute_amount')

    def _compute_amount(self):
        for rec in self:
            if rec.charge_unit_type == 'cbm':
                rec['amount'] = rec.cbm
            elif rec.charge_unit_type == 'pallet':
                rec['amount'] = rec.pallet
            elif rec.charge_unit_type == 'weight':
                rec['amount'] = rec.weight
            elif rec.charge_unit_type == 'square':
                rec['amount'] = rec.sqm
            elif rec.charge_unit_type == 'custom':
                rec['amount'] = rec.quantity
            else:
                rec['amount'] = 0

    def _duration(self):
        for rec in self:
            if rec.end_date and rec.start_date:
                rec['duration'] = (abs((fields.Datetime.to_datetime(rec.end_date)
                                       - fields.Datetime.to_datetime(rec.start_date)).days) +1)
            else:
                rec['duration'] = 1


class Summarysheet(models.Model):
    _name = 'summary.sheet'

    name = fields.Char('Name')
    partner_id = fields.Many2one('res.partner')
    lines = fields.One2many('summary.sheet.lines', 'sheet_id',  string='Lines')
    invoice_id = fields.Many2one('account.move', store=True)


