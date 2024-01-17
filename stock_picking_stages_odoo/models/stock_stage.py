# -*- coding: utf-8 -*-

# Part of Probuse Consulting Service Pvt Ltd.
# See LICENSE file for full copyright and licensing details.

from odoo import models, fields, api

class CustomStockPickingStage(models.Model):
    _name = 'custom.stock.picking.stage'
    _description = 'Stock Picking Stages'

    name = fields.Char(
        string='Name',
        required=True,
    )
    sequence = fields.Integer(
    	string='Sequence',
    )
            
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: