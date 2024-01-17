from odoo import models, fields, api, _
import re
from odoo.exceptions import AccessError, UserError, ValidationError
import logging

_logger = logging.getLogger(__name__)


class WarehouseOrder(models.Model):
    _inherit = "warehouse.order"

    x_billno = fields.Char(string="Bill of Entry No", readonly=False, compute='_default_xbillno', store=True, )

    x_transport = fields.Selection([('land', 'Land'),
                                    ('air', 'Air'),
                                    ('ocean', 'Ocean'),
                                    ], string='Transport',
                                   readonly=False, compute="_default_xtransport",store=True,
                                   )

    # tag_ids = fields.Many2many('warehouse.tag', string='Regime Code', )

    @api.depends('active_sale_id')
    def _default_xbillno(self):
        for rec in self:
            if rec.active_sale_id:
                rec["x_billno"] = rec.active_sale_id.x_billno
            else:
                rec["x_billno"] = ""

    @api.depends('main_id')
    def _default_xtransport(self):
        print('transport')
        for rec in self:
            if rec.main_id:
                rec['x_transport'] = rec.main_id.x_transport
            else:
                rec['x_transport'] = ''


class Picking(models.Model):
    _inherit = "stock.picking"
    # ware_tax_id = fields.Many2many(string='Taxes', related='product_tmpl_id.ware_tax_id')

    # x_driver1 = fields.Char(string='Driver\'s Name')


    # warehouse_id = fields.Many2one('warehouse.order', string='Warehouse Order', )
    x_regime = fields.Many2many('warehouse.tag', string='Regime Code', related='warehouse_id.tag_ids', readonly=False,
                                )
    x_billno = fields.Char(string="Bill of Entry No", store=True, readonly=False, related='warehouse_id.x_billno')

    x_transport_mode = fields.Selection([('land', 'Land'),
                                         ('air', 'Air'),
                                         ('ocean', 'Ocean'),
                                         ], readonly=False,
                                        related='warehouse_id.x_transport', string='Transport', store=True
                                        )

    # @api.model
    # def fields_get(self, fields=None, attributes=None):
    #     fields = super(Picking, self).fields_get(fields, attributes=attributes)
    #     print(fields)
    #     if 'scheduled_date' in fields:
    #         if self.picking_type_code == 'incoming':
    #             fields['scheduled_date']['string'] = 'ETA'
    #     return fields
# class ProductProduct(models.Model):
#     _inherit = "product.product"
#
#     ware_tax_id = fields.Many2many('account.tax', 'ware_taxes_rel', 'prod_id', 'tax_id', string='Taxes',
#                                    domain=[('type_tax_use', '=', 'none')])
