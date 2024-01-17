# -*- coding: utf-8 -*-

# Part of Probuse Consulting Service Pvt Ltd.
# See LICENSE file for full copyright and licensing details.

from odoo import models, fields, api, _

class StockPicking(models.Model):
    _inherit = 'stock.picking'
    
    def _get_default_stage_id(self):
        """ Gives minimum sequence stage """
        stages =  self.env['custom.stock.picking.stage'].search([],order="sequence, id desc", limit=1).id
        return stages

    
    custom_stage_id = fields.Many2one(
        'custom.stock.picking.stage',
        string="Stage",
        ondelete='restrict',
        tracking=True, 
        index=True,
        default=_get_default_stage_id, 
        copy=False
    )

 
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
