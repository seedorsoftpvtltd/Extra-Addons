# -*- coding:utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError

class PickingLotPrintWizard(models.TransientModel):
    _name = 'picking.lot.print.wizard'

    quantity = fields.Integer(
        string='Quantity',
        default=1,
        required=True,
    )

    # @api.multi #odoo13
    def action_print_lot_label(self):
        active_id = self._context.get('active_ids')
        picking_ids = self.env['stock.picking'].browse(active_id)
        if self.quantity <= 0:
            raise ValidationError(_('Please enter quantity greater than zero.'))
        lot_ids = self.env['stock.production.lot'].browse()

        for picking in picking_ids:
            for move in picking.move_lines:
                for move_line in move.move_line_ids:
                    lot_ids += move_line.lot_id

        active_ids = lot_ids.ids
        active_model = 'stock.production.lot'
        if not active_ids:
            raise ValidationError(_('No lot found!'))
        if self.quantity > 0:
            active_ids = active_ids * self.quantity
        active_ids = sorted(active_ids)
        # return self.env.ref(
        #     'stock.action_report_lot_barcode'
        # ).with_context(active_ids=active_ids, active_model=active_model).report_action([])
        return self.env.ref(
            'stock.action_report_lot_label'
        ).with_context(active_ids=active_ids, active_model=active_model).report_action([]) #odoo13
