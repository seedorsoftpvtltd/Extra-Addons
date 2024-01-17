from odoo import api, models, fields, http, _
from datetime import datetime, date, timedelta
from odoo.exceptions import AccessError, UserError, ValidationError
import logging


class ASNinh(models.Model):
    _inherit = "warehouse.order"

    gen_seperate_inv = fields.Boolean('Generate Seperate Invoice for Consignee', store=True)


class PICKinh(models.Model):
    _inherit = "stock.picking"

    gen_seperate_inv = fields.Boolean('Generate Seperate Invoice for Consignee', related='warehouse_id.gen_seperate_inv',
                                      store=True)
    x_consignee = fields.Many2one('res.partner', related='warehouse_id.x_consignee', store=True)


class MOVELINEinh(models.Model):
    _inherit = "stock.move.line"

    gen_seperate_inv = fields.Boolean('Generate Seperate Invoice for Consignee', related='picking_id.gen_seperate_inv',
                                      store=True)
    consignee = fields.Many2one('res.partner', related='picking_id.x_consignee')

    @api.constrains('lot_id')
    def _onchange_lot_dim(self):
        print('_onchange_lot', )
        for rec in self:
            if rec.picking_code == 'incoming':
                if rec.gen_seperate_inv:
                    if rec.lot_id:
                        rec.lot_id.gen_seperate_inv = rec.gen_seperate_inv
                if rec.consignee:
                    if rec.lot_id:
                        rec.lot_id.consignee = rec.consignee

    @api.model_create_multi
    def create(self, vals_list):
        print('create', self.consignee)
        res = super(MOVELINEinh, self).create(vals_list)
        if self.picking_code == 'incoming':
            if self.picking_code == 'incoming':
                if self.gen_seperate_inv:
                    if self.lot_id:
                        print('create......................')
                        self.lot_id.gen_seperate_inv = self.gen_seperate_inv
            if self.picking_code == 'incoming':
                if self.consignee:
                    if self.lot_id:
                        self.lot_id.consignee = self.consignee
        return res

    def write(self, vals):
        print('qqqqqqqqqqqqqqqqqq')
        res = super(MOVELINEinh, self).write(vals)
        for rec in self:
            print('write', vals.get('consignee'), rec.consignee, rec.lot_id)
            if rec.picking_code == 'incoming':
                if rec.gen_seperate_inv:
                    if rec.lot_id:
                        print('write......................')
                        rec.lot_id.gen_seperate_inv = rec.gen_seperate_inv
                        print(rec.lot_id.gen_seperate_inv, '-----------------------boe')

        for rec in self:
            if rec.picking_code == 'incoming':
                if rec.consignee:
                    if rec.lot_id:
                        rec.lot_id.consignee = rec.consignee
        return res


class TRACKINGinh(models.Model):
    _inherit = "stock.production.lot"

    gen_seperate_inv = fields.Boolean('Generate Seperate Invoice for Consignee', store=True)
    consignee = fields.Many2one('res.partner',string='Consignee [for invoice generation]', store=True)


class GIOinh(models.Model):
    _inherit = "goods.issue.order"

    gen_seperate_inv = fields.Boolean('Generate Seperate Invoice for Consignee', store=True)
    consignee = fields.Many2one('res.partner',string='Consignee', store=True)