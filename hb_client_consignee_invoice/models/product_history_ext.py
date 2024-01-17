from odoo import models, fields, api, _
from datetime import datetime


class ProductHistorycci(models.Model):
    _inherit = 'product.history'

    gen_seperate_inv = fields.Boolean('Generate Sperate Invoice for Consignee', store=True)
    consignee = fields.Many2one('res.partner', store=True)

    def create_summary(self):
        for res in self:
            if res.in_date != False:
                print('if')
                summary_vals = {
                    'product_id': res.product_id.id,
                    'in_qty': res.quantity,
                    'in_date': res.in_date,
                    'location_id': res.location_id.id,
                    'partner_id': res.partner_id.id,
                    'lot_id': res.lot_id.id,
                    'pallet_id': res.pallet_id.id,
                    'uom_id': res.uom_id.id,
                    'charge_unit_type': res.charge_unit_type.id,
                    'gen_seperate_inv': res.gen_seperate_inv,
                    'consignee': res.consignee.id,

                }
                self.env['product.summary'].create(summary_vals)
                return res
            else:
                print('else')
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
                            summary_vals = {
                                'product_id': tracking_no.product_id.id,
                                'in_qty': tracking_no.quantity,
                                'in_date': tracking_no.in_date,
                                'location_id': res.location_id.id,
                                'partner_id': tracking_no.partner_id.id,
                                'lot_id': res.lot_id.id,
                                'pallet_id': res.pallet_id.id,
                                'out_date': False,
                                'out_qty': 0,
                                'uom_id': res.uom_id.id,
                                'charge_unit_type': res.charge_unit_type.id,
                                'gen_seperate_inv': res.lot_id.gen_seperate_inv,
                                'consignee': res.lot_id.consignee.id,

                            }
                            self.env['product.summary'].create(summary_vals)
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
                                'uom_id': res.uom_id.id,
                                'charge_unit_type': res.charge_unit_type.id,
                                'gen_seperate_inv': res.lot_id.gen_seperate_inv,
                                'consignee': res.lot_id.consignee.id,

                            }
                            self.env['product.summary'].create(summary_vals)

                return True


class ProductSummarycci(models.Model):
    _inherit = 'product.summary'

    gen_seperate_inv = fields.Boolean('Generate Sperate Invoice for Consignee', store=True)
    consignee = fields.Many2one('res.partner', store=True)


class SummarysheetLinescci(models.Model):
    _inherit = 'summary.sheet.lines'

    gen_seperate_inv = fields.Boolean('Generate Sperate Invoice for Consignee', store=True)
    consignee = fields.Many2one('res.partner', store=True)


class StockMovecci(models.Model):
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
                        'charge_unit_type': self.charge_unit_type.id,
                        'gen_seperate_inv': self.gen_seperate_inv,
                        'consignee':self.consignee.id,

                    }
                    self.env['product.history'].create(history_vals)
                elif rec.picking_code == 'outgoing':
                    inc = self.env['product.history'].search(
                        [('lot_id', '=', self.lot_id.id), ('charge_unit_type', '!=', False)])
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
                        'uom_id': self.product_uom_id.id,
                        'charge_unit_type': inc[0].charge_unit_type.id if inc else False,
                        'gen_seperate_inv': self.lot_id.gen_seperate_inv,
                        'consignee': self.lot_id.consignee.id,

                    }
                    self.env['product.history'].create(history_vals)
