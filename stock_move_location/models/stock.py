from odoo import api, fields, models, _
from odoo.fields import first
from odoo.exceptions import ValidationError, UserError


class Stockmoveline(models.Model):
    _inherit = 'stock.move.line'

    int_track_id = fields.Many2one('internal.qts', string="Tracking Number", store=True)

    # def write(self, vals):
    #     res = super(Stockmoveline, self).write(vals)
    #     for rec in self:
    #         if rec.picking_code not in ['incoming', 'outgoing']:
    #             if vals.get('int_track_id'):
    #                 if vals.get('int_track_id').lot_id != rec.lot_id:
    #                     rec['lot_id'] = rec.int_track_id.lot_id.id
    #                 if vals.get('int_track_id').int_location_id != rec.location_id:
    #                     rec['location_id'] = rec.int_track_id.int_location_id.id
    #             if vals.get('lot_id'):
    #                 if rec.int_track_id and rec.int_track_id.int_location_id != rec.location_id:
    #                     rec['location_id'] = rec.int_track_id.int_location_id.id
    #                 if not rec.int_track_id and rec.location_id != rec.lot_id.location_id:
    #                     rec['int_track_id'] = rec.int_track_id.lot_id.id
    #                     rec['location_id'] = rec.lot_id.location_id.id
    # 
    #     return res

    @api.onchange('int_track_id')
    def onchange_int_track_id(self):
        if self.picking_code not in ['incoming','outgoing']:
            if self.int_track_id:
                if self.int_track_id.lot_id != self.lot_id:
                    self['lot_id'] = self.int_track_id.lot_id.id
                if self.int_track_id.int_location_id != self.location_id:
                    self['location_id'] = self.int_track_id.int_location_id.id

    @api.onchange('lot_id')
    def onchange_lot_id(self):
        if self.picking_code not in ['incoming', 'outgoing']:
            if self.lot_id:
                if self.int_track_id and self.int_track_id.int_location_id != self.location_id:
                    self['location_id'] = self.int_track_id.int_location_id.id
                if not self.int_track_id and self.location_id != self.lot_id.location_id:
                    self['location_id'] = self.lot_id.location_id.id

    @api.constrains('int_track_id')
    def constrains_int_track_id(self):
        for rec in self:
            if rec.picking_code not in ['incoming', 'outgoing']:
                if rec.int_track_id:
                    if rec.int_track_id.lot_id != rec.lot_id:
                        rec['lot_id'] = rec.int_track_id.lot_id.id
                    if rec.int_track_id.int_location_id != rec.location_id:
                        rec['location_id'] = rec.int_track_id.int_location_id.id

    @api.constrains('lot_id')
    def constrains_lot_id(self):
        for rec in self:
            if rec.picking_code not in ['incoming', 'outgoing']:
                if rec.lot_id:
                    if rec.int_track_id and rec.int_track_id.int_location_id != rec.location_id:
                        rec['location_id'] = rec.int_track_id.int_location_id.id
                    if not rec.int_track_id and rec.location_id != rec.lot_id.location_id:
                        rec['location_id'] = rec.lot_id.location_id.id




