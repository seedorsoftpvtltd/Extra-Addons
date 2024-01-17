from odoo import api, fields, models, _
from odoo.fields import first
from odoo.exceptions import ValidationError, UserError


class Stockmoveline(models.Model):
    _inherit = 'stock.move.line'

    int_track_id = fields.Many2one('internal.qts', string="Tracking Number", store=True)

    @api.onchange('int_track_id')
    def onchange_int_track_id(self):
        pick_type = self.picking_id.picking_type_id.warehouse_id.pick_type_id.id
        if self.picking_id.picking_type_id.id == pick_type:
            if self.int_track_id:
                if self.int_track_id.lot_id != self.lot_id:
                    self['lot_id'] = self.int_track_id.lot_id.id
                if self.int_track_id.int_location_id != self.location_id:
                    self['location_id'] = self.int_track_id.int_location_id.id
                    self['package_id'] = self.int_track_id.int_package_id.id

    @api.onchange('lot_id')
    def onchange_lot_id(self):
        pick_type = self.picking_id.picking_type_id.warehouse_id.pick_type_id.id
        if self.picking_id.picking_type_id.id == pick_type:
            if self.lot_id:
                if self.int_track_id and self.int_track_id.int_location_id != self.location_id:
                    self['location_id'] = self.int_track_id.int_location_id.id
                if not self.int_track_id and self.location_id != self.lot_id.location_id:
                    self['location_id'] = self.lot_id.location_id.id
                    self['package_id'] = self.int_track_id.int_package_id.id


    @api.constrains('int_track_id')
    def constrains_int_track_id(self):
        for rec in self:
            pick_type = rec.picking_id.picking_type_id.warehouse_id.pick_type_id.id
            if rec.picking_id.picking_type_id.id == pick_type:
                if rec.int_track_id:
                    if rec.int_track_id.lot_id != rec.lot_id:
                        rec['lot_id'] = rec.int_track_id.lot_id.id
                    if rec.int_track_id.int_location_id != rec.location_id:
                        rec['location_id'] = rec.int_track_id.int_location_id.id
                        rec['package_id'] = rec.int_track_id.int_package_id.id

    @api.constrains('lot_id')
    def constrains_lot_id(self):
        for rec in self:
            pick_type = rec.picking_id.picking_type_id.warehouse_id.pick_type_id.id
            if rec.picking_id.picking_type_id.id == pick_type:
                if rec.lot_id:
                    if rec.int_track_id and rec.int_track_id.int_location_id != rec.location_dest_id:
                        rec['location_id'] = rec.int_track_id.int_location_id.id
                        rec['package_id'] = rec.int_track_id.int_package_id.id
                    if not rec.int_track_id:
                        mls = rec.picking_id.move_line_ids
                        ints = []
                        for m in mls:
                            if m.int_track_id:
                                ints.append(m.int_track_id)
                        if rec.lot_id and rec.lot_id.internal_qties:
                            for int in rec.lot_id.internal_qties:
                                if int not in ints and rec.location_id == int.int_location_id:
                                    rec['int_track_id'] = int.id
                    if not rec.int_track_id and rec.location_id != rec.lot_id.location_id:
                        rec['location_id'] = rec.lot_id.location_id.id

    @api.onchange("int_track_id")
    def _check_int_track_id(self):
        pick = self.picking_id
        if self.int_track_id:
            exist = pick.move_line_ids.search([('int_track_id','=', self.int_track_id.id)])
            if exist:
                raise UserError(_('Already selected from this tracking number!'))




