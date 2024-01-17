from odoo import api, fields, models, _
from odoo.fields import first
from odoo.exceptions import ValidationError, UserError


class LotInternalQties(models.Model):
    _name = 'internal.qts'

    lot_id = fields.Many2one('stock.production.lot', string="Tracking No", store=True)
    int_qty = fields.Float(string='Internal Qty', store=True, related='move_line_id.qty_done')
    int_location_id = fields.Many2one('stock.location', store=True, related='move_line_id.location_dest_id')
    int_package_id = fields.Many2one('stock.quant.package', store=True, related='move_line_id.result_package_id')
    move_line_id = fields.Many2one('stock.move.line', store=True)
    internal_transfer = fields.Boolean(string="Internal Transfer Applied", store=True, default=False)
    product_id = fields.Many2one('product.product', string='Product', related='lot_id.product_id')

    def name_get(self):
        res = []
        for record in self:
            lot_name = record.lot_id.name or ''
            lot_with_qty = lot_name + "(LOC:" + str(record.int_location_id.name) + ")" + "(QTY:" + str(
                record.int_qty) + " " \
                           + record.product_id.uom_id.name + ")"
            res.append((record.id, lot_with_qty))
        return res


class StockMoveLotExtend(models.Model):
    _inherit = 'stock.production.lot'

    internal_qties = fields.One2many('internal.qts', 'lot_id', string='Internal Quantities', store=True)
    internal_transfer = fields.Boolean(string='Internal Transfer', store=True)

    @api.constrains('location_id')
    def compute_internal_qties(self):
        for rec in self:
            existing_mls = []
            if rec.internal_qties:
                for int in rec.internal_qties:
                    existing_mls.append(int.move_line_id.id)
            if rec.internal_qties:
                # for int in rec.internal_qties:
                move_lines = self.env['stock.move.line'].search(
                    [('company_id', '=', self.company_id.id), ('lot_id', '=', rec.id),
                     ('picking_code', 'in', ['incoming', 'internal']), ('location_dest_id.usage', '=', 'internal')])
                for mls in move_lines:
                    if mls.picking_id and mls.id not in existing_mls:
                        warehouse = self.env['stock.warehouse'].search([('company_id', '=', self.company_id.id)])[0]
                        pick_types = []
                        for ware in warehouse:
                            pick_types.append(ware.in_type_id.id)
                            pick_types.append(ware.int_type_id.id)
                        if mls.picking_id.picking_type_id.id in pick_types:
                            if mls.picking_code == 'incoming':
                                internal_transfer = False
                            elif mls.picking_code == 'internal':
                                internal_transfer = True
                            else:
                                internal_transfer = False
                            values = {'int_qty': mls.qty_done,
                                      'int_location_id': mls.location_dest_id.id,
                                      'int_package_id': mls.result_package_id.id,
                                      'lot_id': rec.id,
                                      'move_line_id': mls.id,
                                      'internal_transfer': internal_transfer}
                            int = self.env['internal.qts'].create(values)
                            mls['int_track_id'] = int
                            location = mls.location_id
                            quantity = mls.qty_done
                            current_id = mls
                            rec.adjust_inqty(location, quantity, current_id)
            else:
                move_lines = self.env['stock.move.line'].search(
                    [('company_id', '=', self.company_id.id), ('lot_id', '=', rec.id),
                     ('picking_code', 'in', ['incoming', 'internal']), ('location_dest_id.usage', '=', 'internal')])
                for mls in move_lines:
                    if mls.picking_id:
                        warehouse = self.env['stock.warehouse'].search([('company_id', '=', self.company_id.id)])[0]
                        pick_types = []
                        for ware in warehouse:
                            pick_types.append(ware.in_type_id.id)
                            pick_types.append(ware.int_type_id.id)

                        if mls.picking_id.picking_type_id.id in pick_types:
                            if mls.picking_code == 'incoming':
                                internal_transfer = False
                            elif mls.picking_code == 'internal':
                                internal_transfer = True
                            else:
                                internal_transfer = False
                            values = {'int_qty': mls.qty_done,
                                      'int_location_id': mls.location_dest_id.id,
                                      'int_package_id': mls.result_package_id.id,
                                      'lot_id': rec.id,
                                      'move_line_id': mls.id,
                                      'internal_transfer': internal_transfer}
                            int = self.env['internal.qts'].create(values)
                            mls['int_track_id'] = int.id
                            location = mls.location_id
                            quantity = mls.qty_done
                            current_id = mls
                            rec.adjust_inqty(location, quantity, current_id)

    def adjust_inqty(self, location, quantity, current_id):
        for r in self.internal_qties:
            bla = str(r.int_location_id) + str(location.id) + str(r.move_line_id) + str(current_id)
            # raise UserError(_(bla))
            if r.int_location_id == location and r.move_line_id != current_id:
                r['int_qty'] = r.int_qty - quantity

        # recs = self.internal_qties.search(
        #     [('int_location_id', '=', location.id), ('move_line_id', '!=', current_id)])
        # if recs:
        #     rec = recs[0]
        #     rec['int_qty'] = rec.int_qty - quantity
        # for rec in self.internal_qties:
        #     if rec.int_qty == 0:
        #         rec.unlink()

        # moved_qties = 0
        # for rec in self.internal_qties:
        #     if rec.internal_transfer == True:
        #         moved_qties += rec.int_qty
        # for rec in self.internal_qties.search([('int_location_id','=',location.id),('int_qty','=',quantity)]):
        #     qty = rec.int_qty
        #     if rec.internal_transfer == False:
        #         rec['int_qty'] = qty - moved_qties


    def name_get(self):
        # res = []
        print('ooooooooooooo')
        res = super().name_get()
        for record in self:
            if record.internal_transfer == True:
                lot_name = record.name or ''
                lot_with_qty = "(QTY:" + str(record.product_qty) + " " + record.product_uom_id.name + ")" + lot_name
                if record.internal_qties:

                    bla = []
                    for rec in record.internal_qties:
                        bla.append(" (LOC:" + str(rec.int_location_id.name) + ")" + "(QTY:" + str(
                            rec.int_qty) + " " + record.product_uom_id.name + ")")
                    bla.append(str(lot_name))
                    cleaned_list = [item.strip(" '") for item in bla]
                    result = ', '.join(cleaned_list)
                    lot_with_qtyy = result
                    # lot_with_qtyy = " (LOC:" + str(record.location_id.name) + ")" + "(QTY:" + str(
                    #     record.product_qty) + " " + record.product_uom_id.name + ")" + lot_name
                    if record.removal_date and not record.batchno and not record.serialno:
                        lot_experience = " (LOC:" + str(record.location_id.name) + ")" + " (EXP:" + str(
                            record.removal_date) + ")" + lot_with_qty
                        res.append((record.id, lot_experience))
                        print(res, 'resssssssssssssssss')
                    elif not record.removal_date and record.batchno and not record.serialno:
                        lot_experience = " (LOC:" + str(record.location_id.name) + ")" + "(BTH:" + str(
                            record.batchno) + ")" + lot_with_qty
                        res.append((record.id, lot_experience))
                    elif not record.removal_date and not record.batchno and record.serialno:
                        lot_experience = " (LOC:" + str(record.location_id.name) + ")" + "(SRL: " + str(
                            record.serialno) + ")" + lot_with_qty
                        res.append((record.id, lot_experience))
                    elif record.removal_date and record.batchno and record.serialno:
                        lot_experience = " (LOC:" + str(record.location_id.name) + ")" + " (EXP:" + str(
                            record.removal_date) + ")" + "(SRL: " + str(
                            record.serialno) + ")" + "(BTH:" + str(record.batchno) + ")" + lot_with_qty
                        res.append((record.id, lot_experience))
                        print('resss')
                    elif record.removal_date and record.batchno and not record.serialno:
                        lot_experience = " (LOC:" + str(record.location_id.name) + ")" + " (EXP:" + str(
                            record.removal_date) + ")" + "(BTH:" + str(
                            record.batchno) + ")" + lot_with_qty
                        res.append((record.id, lot_experience))
                    elif record.removal_date and not record.batchno and record.serialno:
                        lot_experience = " (LOC:" + str(record.location_id.name) + ")" + " (EXP:" + str(
                            record.removal_date) + ")" + "(SRL: " + str(
                            record.serialno) + ")" + lot_with_qty
                        res.append((record.id, lot_experience))
                    elif not record.removal_date and record.batchno and record.serialno:
                        lot_experience = " (LOC:" + str(record.location_id.name) + ")" + "(SRL: " + str(
                            record.serialno) + ")" + "(BTH:" + str(
                            record.batchno) + ")" + lot_with_qty
                        res.append((record.id, lot_experience))
                    else:
                        res.append((record.id, lot_with_qtyy))
            else:
                lot_name = record.name or ''
                lot_with_qty = "(QTY:" + str(record.product_qty) + " " + record.product_uom_id.name + ")" + lot_name
                if record.location_id:
                    lot_with_qtyy = " (LOC:" + str(record.location_id.name) + ")" + "(QTY:" + str(
                        record.product_qty) + " " + record.product_uom_id.name + ")" + lot_name
                    if record.removal_date and not record.batchno and not record.serialno:
                        lot_experience = " (LOC:" + str(record.location_id.name) + ")" + " (EXP:" + str(
                            record.removal_date) + ")" + lot_with_qty
                        res.append((record.id, lot_experience))
                        print(res, 'resssssssssssssssss')
                    elif not record.removal_date and record.batchno and not record.serialno:
                        lot_experience = " (LOC:" + str(record.location_id.name) + ")" + "(BTH:" + str(
                            record.batchno) + ")" + lot_with_qty
                        res.append((record.id, lot_experience))
                    elif not record.removal_date and not record.batchno and record.serialno:
                        lot_experience = " (LOC:" + str(record.location_id.name) + ")" + "(SRL: " + str(
                            record.serialno) + ")" + lot_with_qty
                        res.append((record.id, lot_experience))
                    elif record.removal_date and record.batchno and record.serialno:
                        lot_experience = " (LOC:" + str(record.location_id.name) + ")" + " (EXP:" + str(
                            record.removal_date) + ")" + "(SRL: " + str(
                            record.serialno) + ")" + "(BTH:" + str(record.batchno) + ")" + lot_with_qty
                        res.append((record.id, lot_experience))
                        print('resss')
                    elif record.removal_date and record.batchno and not record.serialno:
                        lot_experience = " (LOC:" + str(record.location_id.name) + ")" + " (EXP:" + str(
                            record.removal_date) + ")" + "(BTH:" + str(
                            record.batchno) + ")" + lot_with_qty
                        res.append((record.id, lot_experience))
                    elif record.removal_date and not record.batchno and record.serialno:
                        lot_experience = " (LOC:" + str(record.location_id.name) + ")" + " (EXP:" + str(
                            record.removal_date) + ")" + "(SRL: " + str(
                            record.serialno) + ")" + lot_with_qty
                        res.append((record.id, lot_experience))
                    elif not record.removal_date and record.batchno and record.serialno:
                        lot_experience = " (LOC:" + str(record.location_id.name) + ")" + "(SRL: " + str(
                            record.serialno) + ")" + "(BTH:" + str(
                            record.batchno) + ")" + lot_with_qty
                        res.append((record.id, lot_experience))
                    else:
                        res.append((record.id, lot_with_qtyy))

        return res
