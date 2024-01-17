from odoo.http import request
from odoo import api, fields, models, tools, osv, http, _
from odoo.exceptions import AccessError, UserError, ValidationError


# class itemmaster(models.Model):
#     _inherit = 'item.master'
#
#     @api.model
#     def create(self, vals):
#         res = super(itemmaster, self).create(vals)
#         self.check()
#         return res
#
#     def check(self):
#         prod = self.env['item.master'].search([('id','!=',self.id),('name','=',self.name)])
#         print(prod,'-------------------------dup item-------------------------',self.name)
#         if prod:
#             raise UserError(_("Product Code Must be Unique"))


class batchserialLot(models.Model):
    _inherit = 'stock.production.lot'

    serialno = fields.Char(string="Serial No", store=True)
    batchno = fields.Char(string="Batch No", store=True)

    # def name_get(self):
    #     # res = []
    #     print('ooooooooooooo')
    #     res = super().name_get()
    #     for record in self:
    #         lot_name = record.name or ''
    #         lot_with_qty = lot_name + "(" + str(record.product_qty) + " " + record.product_uom_id.name + ")"
    #         if record.removal_date and not record.batchno and not record.serialno:
    #             lot_experience = lot_with_qty + str(record.removal_date) + ")"
    #             res.append((record.id, lot_experience))
    #             print(res, 'resssssssssssssssss')
    #         if not record.removal_date and record.batchno and not record.serialno:
    #             lot_experience = lot_with_qty + "(" + str(record.batchno) + ")"
    #             res.append((record.id, lot_experience))
    #         if not record.removal_date and not record.batchno and record.serialno:
    #             lot_experience = lot_with_qty + "(" + str(record.serialno) + ")"
    #             res.append((record.id, lot_experience))
    #         if record.removal_date and record.batchno and record.serialno:
    #             lot_experience = lot_with_qty + str(record.removal_date) + ")" + "(" + str(
    #                 record.serialno) + ")" + "(" + str(record.batchno) + ")"
    #             res.append((record.id, lot_experience))
    #         if record.removal_date and record.batchno and not record.serialno:
    #             lot_experience = lot_with_qty + str(record.removal_date) + ")" + "(" + str(record.batchno) + ")"
    #             res.append((record.id, lot_experience))
    #         if record.removal_date and not record.batchno and record.serialno:
    #             lot_experience = lot_with_qty + str(record.removal_date) + ")" + "(" + str(
    #                 record.serialno) + ")"
    #             res.append((record.id, lot_experience))
    #         if not record.removal_date and record.batchno and record.serialno:
    #             lot_experience = lot_with_qty + "(" + str(
    #                 record.serialno) + ")" + "(" + str(record.batchno) + ")"
    #             res.append((record.id, lot_experience))
    #         else:
    #             print('rrrrrrrrrrrrrrrr', res)
    #             res.append((record.id, lot_with_qty))
    #
    #     return res

    def name_gett(self):
        # res = []
        print('ooooooooooooo')
        res = super().name_gett()
        for record in self:
            lot_name = record.name or ''
            lot_with_qty = "(QTY:" + str(record.product_qty) + " " + record.product_uom_id.name + ")" + lot_name
            if record.location_id:
                lot_with_qtyy = " (LOC:" + str(record.location_id.name) + ")" + "(QTY:" + str(record.product_qty) + " " + record.product_uom_id.name + ")" + lot_name
                if record.removal_date and not record.batchno and not record.serialno:
                    lot_experience = " (LOC:" + str(record.location_id.name) + ")" + " (EXP:" + str(record.removal_date) + ")" + lot_with_qty
                    res.append((record.id, lot_experience))
                    print(res, 'resssssssssssssssss')
                elif not record.removal_date and record.batchno and not record.serialno:
                    lot_experience = " (LOC:" + str(record.location_id.name) + ")" + "(BTH:" + str(record.batchno) + ")" + lot_with_qty
                    res.append((record.id, lot_experience))
                elif not record.removal_date and not record.batchno and record.serialno:
                    lot_experience = " (LOC:" + str(record.location_id.name) + ")" + "(SRL: " + str(record.serialno) + ")" + lot_with_qty
                    res.append((record.id, lot_experience))
                elif record.removal_date and record.batchno and record.serialno:
                    lot_experience = " (LOC:" + str(record.location_id.name) + ")" + " (EXP:" + str(record.removal_date) + ")" + "(SRL: " + str(
                        record.serialno) + ")" + "(BTH:" + str(record.batchno) + ")" + lot_with_qty
                    res.append((record.id, lot_experience))
                    print('resss')
                elif record.removal_date and record.batchno and not record.serialno:
                    lot_experience = " (LOC:" + str(record.location_id.name) + ")" + " (EXP:" + str(record.removal_date) + ")" + "(BTH:" + str(
                        record.batchno) + ")" + lot_with_qty
                    res.append((record.id, lot_experience))
                elif record.removal_date and not record.batchno and record.serialno:
                    lot_experience = " (LOC:" + str(record.location_id.name) + ")" + " (EXP:" + str(record.removal_date) + ")" + "(SRL: " + str(
                        record.serialno) + ")" + lot_with_qty
                    res.append((record.id, lot_experience))
                elif not record.removal_date and record.batchno and record.serialno:
                    lot_experience = " (LOC:" + str(record.location_id.name) + ")" + "(SRL: " + str(record.serialno) + ")" + "(BTH:" + str(
                        record.batchno) + ")" + lot_with_qty
                    res.append((record.id, lot_experience))
                else:
                    res.append((record.id, lot_with_qtyy))

        return res


# class asnlineinn(models.Model):
#     _inherit = 'warehouse.order.line'
#
#     expiry_date = fields.Date(string="Expiry Date")
#     production_date = fields.Date(string="Production Date")


class batchserialmove(models.Model):
    _inherit = 'stock.move'

    expiry_date = fields.Date(string="Expiry Date")
    production_date = fields.Date(string="Production Date")


class batchserial(models.Model):
    _inherit = 'stock.move.line'

    serialno = fields.Char(string="Serial No")
    batchno = fields.Char(string="Batch No")
    expiry_date = fields.Date(string="Expiry Date")
    production_date = fields.Date(string="Production Date")

    @api.model_create_multi
    def create(self, vals_list):
        # print('oooooooooooooooooooo')
        res = super(batchserial, self).create(vals_list)
        if self.picking_code == 'incoming':
            if self.batchno:
                if self.lot_id:
                    self.lot_id.batchno = self.batchno
                    self.lot_id.removal_date = self.expiry_date
                    self.lot_id.use_date = self.production_date
                    # self.batchno.product_id = self.product_id.id
                    # self.batchno.lot_id = self.lot_id.id
        if self.picking_code == 'incoming':
            if self.serialno:
                if self.lot_id:
                    self.lot_id.serialno = self.serialno
                    self.lot_id.removal_date = self.expiry_date
                    self.lot_id.use_date = self.production_date
                    # self.serialno.product_id = self.product_id.id
                    # self.serialno.lot_id = self.lot_id.id
            if self.move_id.expiry_date:
                self.expiry_date = self.move_id.expiry_date
            if self.move_id.expiry_date:
                self.expiry_date = self.move_id.expiry_date

        return res

    def write(self, vals):
        # print('qqqqqqqqqqqqqqqqqq')
        res = super(batchserial, self).write(vals)
        for rec in self:
            if vals.get('lot_id'):
                rec.lot_id.serialno = rec.serialno
                rec.lot_id.removal_date = rec.expiry_date
                rec.lot_id.use_date = rec.production_date

        for rec in self:
            if rec.picking_code == 'incoming':
                if vals.get('serialno'):
                    if rec.lot_id:
                        rec.lot_id.serialno = rec.serialno
                        rec.lot_id.removal_date = rec.expiry_date
                        rec.lot_id.use_date = rec.production_date
                        # rec.serialno.product_id = rec.product_id.id
                        # rec.serialno.lot_id = rec.lot_id.id
        for rec in self:
            if rec.picking_code == 'incoming':
                if vals.get('batchno'):
                    if rec.lot_id:
                        rec.lot_id.batchno = rec.batchno
                        rec.lot_id.removal_date = rec.expiry_date
                        rec.lot_id.use_date = rec.production_date
                        # rec.batchno.product_id = rec.product_id.id
                        # rec.batchno.lot_id = rec.lot_id.id
        for rec in self:
            if rec.picking_code == 'incoming':
                if vals.get('production_date'):
                    if rec.lot_id:
                        rec.lot_id.batchno = rec.batchno
                        rec.lot_id.removal_date = rec.expiry_date
                        rec.lot_id.use_date = rec.production_date
                        # rec.batchno.product_id = rec.product_id.id
                        # rec.batchno.lot_id = rec.lot_id.id
        for rec in self:
            if rec.picking_code == 'incoming':
                if vals.get('expiry_date'):
                    if rec.lot_id:
                        rec.lot_id.batchno = rec.batchno
                        rec.lot_id.removal_date = rec.expiry_date
                        rec.lot_id.use_date = rec.production_date
                        # rec.batchno.product_id = rec.product_id.id
                        # rec.batchno.lot_id = rec.lot_id.id

        return res

    @api.constrains('lot_id', 'serialno', 'batchno','expiry_date', 'production_date')
    def _onchange_lot_sl_bs(self):
        print('_onchange_lot_sl_bs_onchange_lot_sl_bs_onchange_lot_sl_bs_onchange_lot_sl_bs')
        if self.picking_code == 'incoming':
            if self.batchno:
                if self.lot_id:
                    self.lot_id.batchno = self.batchno
                    self.lot_id.removal_date = self.expiry_date
                    self.lot_id.use_date = self.production_date
                    # self.batchno.product_id = self.product_id.id
                    # self.batchno.lot_id = self.lot_id.id
        if self.picking_code == 'incoming':
            if self.serialno:
                if self.lot_id:
                    self.lot_id.serialno = self.serialno
                    self.lot_id.removal_date = self.expiry_date
                    self.lot_id.use_date = self.production_date
                    # self.serialno.product_id = self.product_id.id
                    # self.serialno.lot_id = self.lot_id.id

    @api.onchange('lot_id')
    def _onchange_lot_sl(self):
        if self.picking_code != 'incoming':
            self['serialno'] = self.lot_id.serialno
            self['batchno'] = self.lot_id.batchno
            self['expiry_date'] = self.lot_id.removal_date
            self['production_date'] = self.lot_id.use_date

    @api.constrains('lot_id')
    def _lot_sl(self):
        for rec in self:
            if rec.picking_code != 'incoming':
                rec['serialno'] = rec.lot_id.serialno
                rec['batchno'] = rec.lot_id.batchno
                rec['expiry_date'] = rec.lot_id.removal_date
                self['production_date'] = self.lot_id.use_date

