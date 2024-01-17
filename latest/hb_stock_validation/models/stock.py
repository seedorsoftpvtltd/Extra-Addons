from odoo import api, fields, models, tools, osv, http, _
import odoo.osv.osv
from odoo.exceptions import UserError, ValidationError


class wovalidation(models.Model):
    _inherit = "warehouse.order"

    @api.onchange('partner_id')
    def _partner_onchange(self):
        for rec in self.order_line:
            print(rec, 'rec')
            rec.write({'order_id': False})
            # rec.unlink()

    def button_confirm(self):
        print('button confirm')
        for rec in self:
            for r in rec.order_line:
                if rec.partner_id != r.product_id.customer_id and r.product_id.item:
                    raise UserError(_('Make sure the product is under the selected the customer!'))
        return super(wovalidation, self).button_confirm()


class giovalidation(models.Model):
    _inherit = "goods.issue.order"

    @api.onchange('partner_id')
    def _partner_onchange(self):
        for rec in self.order_line:
            print(rec, 'rec')
            rec.write({'order_id': False})
            # rec.unlink()

    def action_confirm(self):
        print('button confirm')
        for rec in self:
            for r in rec.order_line:
                if rec.partner_id != r.product_id.customer_id and r.product_id.item:
                    raise UserError(_('Make sure the product is under the selected the customer!'))
        return super(giovalidation, self).action_confirm()


class stockkvalidation(models.Model):
    _inherit = "stock.picking"

    @api.onchange('partner_id')
    def _partner_onchange(self):
        for mv in self.move_ids_without_package:
            print(mv, 'mv')
            mv.write({'picking_id': False, 'state':'draft'})
            mv.unlink()
        for mvl in self.move_line_ids:
            print(mvl, 'mvl')
            mvl.write({'picking_id': False, 'state': 'draft'})
            mvl.unlink()

    def action_confirm(self):
        print('button confirm')
        for rec in self:
            for r in rec.move_ids_without_package:
                if rec.partner_id != r.product_id.customer_id and r.product_id.item:
                    raise UserError(_('Make sure the product is under the selected the customer!'))
        return super(stockkvalidation, self).action_confirm()


class stockvalidation(models.Model):
    _inherit = "stock.picking"

    def action_generate_backorder_wizard(self):
        res = super(stockvalidation, self).action_generate_backorder_wizard()
        print('vanthennnnnnnnn')
        if self.picking_type_id.code != 'incoming':
            self.action_done()
        return res


class stockmoveline(models.Model):
    _inherit = "stock.move.line"

    @api.constrains('product_uom_qty')
    def auto_fill_qty(self):
        for rec in self:
            if rec.product_uom_qty and rec.picking_code == 'outgoing':
                rec['qty_done'] = rec.product_uom_qty

    # def create(self, vals):
    #     if self.picking_code == 'outgoing':
    #         self['qty_done'] = self.product_uom_qty
    #     return super(stockmoveline, self).create(vals)

