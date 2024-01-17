# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.

import time
from odoo import api, fields, models, _
from datetime import datetime
import odoo.addons.decimal_precision as dp
from odoo.exceptions import UserError


class createwarehouseorder(models.TransientModel):
        _name = 'create.warehouseorder'
        _description = "Create warehouse Order"

        new_order_line_ids = fields.One2many( 'getsale.orderdata', 'new_order_line_id',String="Order Line")
        partner_id = fields.Many2one('res.partner', string='Vendor', required = True)
        date_order = fields.Datetime(string='Order Date', required=True, copy=False, default=fields.Datetime.now)


        @api.model
        def default_get(self,  default_fields):
                res = super(createwarehouseorder, self).default_get(default_fields)
                data = self.env['sale.order'].browse(self._context.get('active_ids',[]))
                update = []
                # for record in data.order_line:
                #
                #         update.append((0,0,{
                #                                         'product_id' : record.product_id.id,
                #                                         'product_uom' : record.product_uom.id,
                #                                         'order_id': record.order_id.id,
                #                                         'name' : record.name,
                #                                         'product_qty' : record.product_uom_qty,
                #                                         'price_unit' : record.price_unit,
                #                                         'product_subtotal' : record.price_subtotal,
                #                                         }))
                # res.update({'new_order_line_ids':update,
                #             'partner_id':data.partner_id.id,})
                res.update({
                            'partner_id': data.partner_id.id, })
                return res

        def action_create_warehouse_order(self):
                self.ensure_one()
                res = self.env['warehouse.order'].browse(self._context.get('id',[]))
                sale=self.env['sale.order'].browse(self._context.get('active_id',[]))
                sale_line=self.env['sale.order'].browse(self._context.get('active_id',[]))
                print(sale_line)
                idf=[]
                ipp=[]
                for rec in sale_line.order_line:
                    idf.append(rec.id)
                    idf.append(rec.product_id.id)
                    ipp.append(idf)
                    idf=[]
                print(ipp)

                value = []
                pricelist = self.partner_id.property_product_pricelist
                partner_pricelist = self.partner_id.property_product_pricelist
                sale_order_name = ""
                val = ''
                for data in self.new_order_line_ids:
                        sale_order_name = data.order_id.name
                        order=data.order_id
                        for i in ipp:
                            if i[1] == data.product_id.id:
                                val=i[0]
                        if partner_pricelist:
                                product_context = dict(self.env.context, partner_id=self.partner_id.id, date=self.date_order, uom=data.product_uom.id)
                                final_price, rule_id = partner_pricelist.with_context(product_context).get_product_price_rule(data.product_id, data.product_qty or 1.0, self.partner_id)
                        else:
                                final_price = data.product_id.standard_price

                        # value.append([0,0,{
                        #                                       'product_id' : data.product_id.id,
                        #                                       'name' : data.name,
                        #                                       'product_qty' : data.product_qty,
                        #                                       'order_id':data.order_id.id,
                        #                                       'product_uom' : data.product_uom.id,
                        #                                       'taxes_id' : data.product_id.supplier_taxes_id.ids,
                        #                                       'date_planned' : data.date_planned,
                        #                                       'price_unit' : final_price,
                        #                                       # 'sale_war_id':val,
                        #
                        #                                       }])
                        # print(value.sale_war_id)
                res.create({
                                                'partner_id' : self.partner_id.id,
                                                'date_order' : str(self.date_order),
                                                # 'order_line':value,
                                                # 'origin' : sale_order_name,
                                                #'partner_ref' : sale_order_name
                                                'active_sale_id':sale.id,
                                        })

                return res


class Getsaleorderdata(models.TransientModel):
        _name = 'getsale.orderdata'
        _description = "Get Sale Order Data"

        new_order_line_id = fields.Many2one('create.warehouseorder')

        product_id = fields.Many2one('product.product', string="Product", required=True)
        name = fields.Char(string="Description")
        product_qty = fields.Float(string='Quantity', required=True)
        date_planned = fields.Datetime(string='Scheduled Date', default = datetime.today())
        product_uom = fields.Many2one('product.uom', string='Product Unit of Measure')
        order_id = fields.Many2one('sale.order', string='Order Reference', required=True, ondelete='cascade', index=True, copy=False)
        price_unit = fields.Float(string='Unit Price', required=True, digits=dp.get_precision('Product Price'))
        product_subtotal = fields.Float(string="Sub Total", compute='_compute_total')

        @api.depends('product_qty', 'price_unit')
        def _compute_total(self):
                for record in self:
                        record.product_subtotal = record.product_qty * record.price_unit


class Warehouse(models.Model):
        _inherit='warehouse.order'

        active_sale_id =fields.Many2one('sale.order',string='Sale ID')

class Warehouseee(models.Model):
     _inherit = 'warehouse.order.line'

     sale_war_id = fields.Many2one('sale.order.line', string='Sale Order ID')

class ANS(models.Model):
       _inherit ='sale.order'
       compute_order_count=fields.Integer(string="ASN Count",compute="_compute_order_count")

       def _compute_order_count(self):
           obj = self.env['warehouse.order']

           print("------------------------>>>")

           for serv in self:
               cnt = obj.search_count([('active_sale_id', '=', serv.id)
                                       ])
               if cnt != 0:

                   serv['compute_order_count'] = cnt
               else:

                   serv['compute_order_count'] = 0
