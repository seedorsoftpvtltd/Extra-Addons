# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
import time
from datetime import date
from odoo.exceptions import UserError


class MrpProduction(models.Model):
    _inherit = 'mrp.production'


    @api.onchange('product_id', 'picking_type_id', 'company_id', 'product_qty', 'date_planned_start')
    def onchange_product_id(self):
        if not self.product_id:
            self.bom_id = False
        else:
            bom = self.env['mrp.bom']._bom_selection(product=self.product_id, picking_type=self.picking_type_id, company_id=self.company_id.id, product_qty=self.product_qty, date_planned_start=self.date_planned_start)
            if bom.type == 'normal':
                self.bom_id = bom.id
            else:
                self.bom_id = False
            self.product_uom_id = self.product_id.uom_id.id
            return {'domain': {'product_uom_id': [('category_id', '=', self.product_id.uom_id.category_id.id)]}}

    @api.onchange('bom_id')
    def _onchange_bom_id(self):
        self.move_raw_ids = [(2, move.id) for move in self.move_raw_ids.filtered(lambda m: m.bom_line_id)]
        self.picking_type_id = self.bom_id.picking_type_id or self.picking_type_id


class MrpBom(models.Model):
    _inherit = 'mrp.bom'

    date_start = fields.Date(string='Validity Start Date', required=True, track_visibility='onchange', default=fields.Date.context_today)
    date_end = fields.Date(string='Validity End Date', required=True, track_visibility='onchange', default=time.strftime('%Y-12-31'))
    qty_min = fields.Float(string='Minimum Lot Quantity', digits='Product Unit of Measure', required=True, default="1.00")
    qty_max = fields.Float(string='Maximum Lot Quantity', digits='Product Unit of Measure', required=True, default="99999.00")

    @api.constrains('type', 'picking_type_id')
    def _check_picking_type(self):
        if self.type == 'normal' and not self.picking_type_id:
            raise UserError(_('please enter an operation'))
        return True

    @api.model
    def _bom_selection(self, product_tmpl=None, product=None, picking_type=None, company_id=False, product_qty=None, date_planned_start=None):
        if product and not product_tmpl:
            product_tmpl = product.product_tmpl_id
            domain = ['|', ('product_id', '=', product.id), '&', ('product_id', '=', False), ('product_tmpl_id', '=', product_tmpl.id)]
        elif product_tmpl:
            domain = [('product_tmpl_id', '=', product_tmpl.id)]
        else:
            return False
        if picking_type:
            domain = domain + [('picking_type_id', '=', picking_type.id)]
        if company_id or self.env.context.get('company_id'):
            domain = domain + [('company_id', '=', company_id or self.env.context.get('company_id'))]
        domain = domain + [('qty_min', '<=', product_qty)] + [('qty_max', '>', product_qty)]
        date_planned_start = date_planned_start.date()
        domain = domain + [('date_start', '<=', date_planned_start)] + [('date_end', '>', date_planned_start)]
        return self.search(domain, order='sequence, product_id', limit=1)


class ChangeProductionQty(models.TransientModel):
    _inherit = 'change.production.qty'


    def change_prod_qty(self):
        res = super().change_prod_qty()
        for wizard in self:
            product_tmpl= wizard.mo_id.product_tmpl_id
            product= wizard.mo_id.product_id
            picking_type= wizard.mo_id.picking_type_id
            company_id= wizard.mo_id.company_id.id
            product_qty= wizard.mo_id.product_qty
            date_planned_start= wizard.mo_id.date_planned_start
            new_bom_id = wizard.mo_id.bom_id._bom_selection(product_tmpl=product_tmpl, product=product, picking_type=picking_type, company_id=company_id, product_qty=product_qty, date_planned_start=date_planned_start)
            production = wizard.mo_id
            for move_raw in production.move_raw_ids:
                move_raw.picking_id.action_cancel()
            production.write({'bom_id': new_bom_id.id})
        return res





