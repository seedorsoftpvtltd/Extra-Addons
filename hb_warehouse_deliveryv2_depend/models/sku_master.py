from odoo import api, fields, models, _
from odoo.http import request
import os
from odoo.exceptions import UserError, AccessError, MissingError, ValidationError


class SKUMaster(models.Model):
    _name = 'item.master'

    name = fields.Char(string="Name", store=True, readonly=True, related='sku_no')
    weight = fields.Float(string="Weight")
    length = fields.Float(string="Length")
    height = fields.Float(string="Height")
    width = fields.Float(string="Width")
    product_id = fields.Many2one('product.product', string="Product", required=True)
    partner_id = fields.Many2one('res.partner', string="Customer", required=True)
    description = fields.Char(string="Description", required=True)
    sku_no = fields.Char(string="Product Code", required=True, store=True)
    company_id = fields.Many2one('res.company', string='Company', default=lambda self: self.env.company.id)
    volume = fields.Float(string="Volume", readonly=False)
    product_date = fields.Datetime(string="Product Date", related='product_id.product_date')
    expiry_date = fields.Datetime(string="Expiry Date", related='product_id.expiry_date')
    availability = fields.Char(string="Availability", compute='_availability')


    def _availability(self):
        for rec in self:
            # rec['availability'] = (r.free_qty for r in rec.product_id)
            avail = 0
            for r in rec.product_id:
                qty = r.free_qty
                avail = qty
                print(qty, avail)
            rec['availability'] = avail
            print(rec.availability)

    @api.model
    def create(self, vals):
        res = super(SKUMaster, self).create(vals)
        if self.product_id:
            self.product_id.write({'item': self})
        print(self.product_id.item, 'self.product_id.item')
        return res

    # @api.model
    def write(self, vals):
        res = super(SKUMaster, self).write(vals)
        if vals.get('product_id'):
            self.product_id.write({'item': self})
        print(self.product_id.item, 'self.product_id.item')

        return res

    # def name_get(self):
    #     res = super().name_get()
    #     new_res = []
    #     for _i in res:
    #         avail = {r.availability for r in self}
    #         print(avail)
    #         name = "({})".format(avail)
    #         new_res.append((_i[0], name))
    #     return new_res

    # @api.model
    # def create(self, vals):
    #     res = super(SKUMaster, self).create(vals)
    #     self['name'] = self.sku_no
    #     return res
    #
    # @api.model
    # def write(self, vals):
    #     res = super(SKUMaster, self).write(vals)
    #     if vals.get('sku_id'):
    #         vals['name'] = vals.sku_no
    #     return res

    @api.depends('sku_no')
    def _namee(self):
        for rec in self:
            rec['name'] = rec.sku_no

    # @api.depends('length', 'height', 'width')
    # def _volume(self):
    #     for rec in self:
    #         rec['volume'] = (rec.length * rec.height * rec.width) / 1000.0 ** 3


class Productmaster(models.Model):
    _inherit = 'product.template'

    item = fields.Many2one('item.master', string="Item")
    product_date = fields.Datetime(string="Product Date")
    expiry_date = fields.Datetime(string="Expiry Date")
    is_serial = fields.Boolean(string="Serial Number", compute='_with_serial', readonly=False)

    # @api.onchange('is_serial')
    def _with_serial(self):
        if self.is_serial == True:
            self['tracking'] = 'serial'
        else:
            self['tracking'] = 'lot'


class asnline(models.Model):
    _inherit = 'warehouse.order.line'

    expiry_date = fields.Date(string="Expiry Date")
    production_date = fields.Date(string="Production Date")
    container = fields.Many2one('freight.container', string="Container ID")
    container_qty = fields.Float(sttring="No of Containers")
    container_no = fields.Char(string="Container No")

