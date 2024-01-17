from odoo import models, fields, api, _
from datetime import datetime
import odoo.addons.decimal_precision as dp
from odoo.exceptions import UserError, ValidationError


class PurchaseOrderWizard(models.TransientModel):
    _name = "create.multivendor"

    vendor_ids = fields.Many2many('res.partner', string="Vendor", required=True)
    date_order = fields.Datetime(string='Order Date', required=True, copy=False, default=fields.Datetime.now)
    new_order_line_ids = fields.One2many('getsale.orderdata', 'new_order_line_id', String="Order Line")

    @api.model
    def default_get(self, default_fields):
        res = super(PurchaseOrderWizard, self).default_get(default_fields)
        data = self.env['sale.order'].browse(self._context.get('active_ids', []))
        print(data.order_line)
        update = []
        for record in data.order_line:
            update.append((0, 0, {
                'product_id': record.product_id.id,
                'name': record.name,
                'product_qty': record.product_uom_qty,
            }))
        res.update({'new_order_line_ids': update})
        return res

    def action_create_purchase_order(self):
        res = self.env['sale.order'].browse(self._context.get('id', []))
        data = self.env['sale.order'].browse(self._context.get('active_ids', []))
        a = []
        for line in self.new_order_line_ids:
            a.append(line.checklist_vendor)
        for line in range(0, len(data.order_line)):
            data.order_line[line].update({'checklist_vendor': a[line]})
        vald = []
        for check_val in data.order_line:
            vald.append(check_val.checklist_vendor)

        if not data.requis_id:
            data.create_purchase_agreement()  ##Added for purchase requisation by HB
            requisition_id = data.requis_id.id
        else:
            requisition_id = data.requis_id.id  ##Added for purchase requisation by HB

        if True in vald:
            for partner in self.vendor_ids:
                purchase_order_vals = {
                    'partner_id': partner.id,
                    'origin': data.name,
                    'date_order': self.date_order,

                    'requisition_id': requisition_id,  ##Added for purchase requisation by HB
                }

                purchase_order = self.env['purchase.order'].create(purchase_order_vals)
                if data.order_line:
                    purchase_order_lines = []
                    for check_line in data.order_line:
                        if check_line.checklist_vendor:
                            purchase_line_vals = {
                                'order_id': purchase_order.id,
                                'product_id': check_line.product_id.id,
                                'name': check_line.product_id.name,
                                'product_qty': check_line.product_uom_qty,
                                'product_uom': check_line.product_uom.id,
                                'date_planned': self.date_order,
                                'price_unit': check_line.price_unit,
                                'taxes_id': check_line.tax_id,
                                'sale_line_id': check_line.id,

                            }

                            purchase_order_line = self.env['purchase.order.line'].create(purchase_line_vals)

                            purchase_order_lines.append(purchase_order_line)

                purchase_order.send_rfq_mail_template()  # automated action
        else:
            raise UserError(_('Kindly select anyone of the services'))


class Getsaleorderdata(models.TransientModel):
    _name = 'getsale.orderdata'
    _description = "Get Sale Order Data"

    new_order_line_id = fields.Many2one('create.multivendor')

    product_id = fields.Many2one('product.product', string="Product")
    name = fields.Char(string="Description")
    product_qty = fields.Float(string='Quantity')
    checklist_vendor = fields.Boolean(string=' ')
