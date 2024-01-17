from odoo import models, fields, api, _
from datetime import datetime
import odoo.addons.decimal_precision as dp
from odoo.exceptions import UserError, ValidationError


class PurchaseOrderWizard(models.TransientModel):
    _name = "create.multivendor"

    vendor_ids = fields.Many2many('res.partner', string="Vendor", required=True)
    date_order = fields.Datetime(string='Order Date', required=True, copy=False, default=fields.Datetime.now)
    new_order_line_ids = fields.One2many('sale.order.line', 'order_id', String="Order Line",
                                         compute="compute_order")

    @api.depends('date_order')
    def compute_order(self):
        data = self.env['sale.order'].browse(self._context.get('active_ids', []))
        self.new_order_line_ids = []
        if data.order_line:
            self.new_order_line_ids = data.order_line

    @api.model
    def default_get(self, fields):
        res = super(PurchaseOrderWizard, self).default_get(fields)
        data = self.env['sale.order'].browse(self._context.get('active_ids', []))
        if data.order_line:
            pass
        else:
            raise UserError(_('Kindly Create a Service Record'))
        return res

    @api.onchange('vendor_ids')
    def check_fun(self):
        data = self.env['sale.order'].browse(self._context.get('active_ids', []))
        a = []
        for line in self.new_order_line_ids:
            a.append(line.checklist_vendor)
        for line in range(0, len(data.order_line)):
            data.order_line[line].update({'checklist_vendor': a[line]})

    def action_create_purchase_order(self):
        res = self.env['sale.order'].browse(self._context.get('id', []))
        data = self.env['sale.order'].browse(self._context.get('active_ids', []))
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

            # return {
            #     'effect': {
            #         'fadeout': 'slow',
            #         'message': 'Purchase Order is created successfully',
            #         'img_url': 'https://thehub.santanderbank.com/wp-content/uploads/2018/01/2.gif',
            #
            #     }
            # }

# def so_notify(self):
#     notification = {
#         'type': 'ir.actions.client',
#         'tag': 'display_notification',
#         'params': {
#             'title': ('Success'),
#             'message': 'Your Purchase Order is created successfully.',
#             'type': 'success',  # types: success,warning,danger,info
#             'sticky': False,  # True/False will display for few seconds if false
#         },
#     }
#
#     return notification, {'type': 'ir.actions.act_window_close'}
