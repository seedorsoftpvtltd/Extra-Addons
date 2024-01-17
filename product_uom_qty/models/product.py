# -*- coding: utf-8 -*-
#################################################################################
# Author      : Acespritech Solutions Pvt. Ltd. (<www.acespritech.com>)
# Copyright(c): 2012-Present Acespritech Solutions Pvt. Ltd.
# All Rights Reserved.
#
# This program is copyright property of the author mentioned above.
# You can`t redistribute it and/or modify it.
#
#################################################################################

from odoo import fields, models, api, _


class product_uom_wizard(models.TransientModel):
    _name = 'product.uom.wizard'

    multi_uom_lines = fields.One2many('multi.uom.qty', 'product_uom_id', string="Available Quantity  By UOM ")
    uom_id = fields.Many2one('uom.uom', string="Default UOM", readonly=True)

    @api.model
    def default_get(self, fields_list):
        lst = []
        res = super(product_uom_wizard, self).default_get(fields_list)
        if self._context.get('active_id'):
            product_id = self.env['product.product'].browse(self._context.get('active_id'))
            uom_ids = self.env['uom.uom'].search([('category_id', '=', product_id.uom_id.category_id.id)])
            for each in uom_ids:
                available_qty = product_id.uom_id._compute_quantity(product_id.qty_available, each)
                lst += [(0, 0, {'uom_id':each.id, 'available_qty':available_qty, 'product_id':self._context.get('active_id')})]
            res.update({'multi_uom_lines':lst, 'uom_id':product_id.uom_id.id})
        return res


class multi_uom_qty(models.TransientModel):
    _name = 'multi.uom.qty'

    product_uom_id = fields.Many2one('product.uom.wizard', string="UOM")
    uom_id = fields.Many2one('uom.uom', string="UOM")
    available_qty = fields.Float(string="Available Quantity")

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
