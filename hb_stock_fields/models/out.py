from odoo import api, fields, models, _
from odoo.exceptions import UserError, AccessError, MissingError, ValidationError


class MOVELINEDIM(models.Model):
    _inherit = 'stock.move.line'

    @api.model_create_multi
    def create(self, vals):
        res = super(MOVELINEDIM, self).create(vals)
        print('//////////sl,bt////////')
        for rec in self.move_id.goods_line_id.serialno:
            vals['serialno'] = rec.id
        for rec in self.move_id.goods_line_id.batchno:
            vals['batchno'] = rec.id

        return res

    def write(self, vals):
        print('//////////sl,bt////////')

        for rec in self.move_id.goods_line_id.serialno:
            vals['serialno'] = rec.id
        for rec in self.move_id.goods_line_id.batchno:
            vals['batchno'] = rec.id

        return super(MOVELINEDIM, self).write(vals)

    @api.onchange('serialno', 'batchno')
    def _onchange(self):
        if self.picking_code == 'internal':
            if self.serialno:
                self['lot_id'] = self.serialno.lot_id.id
            else:
                self['lot_id'] = self.batchno.lot_id.id