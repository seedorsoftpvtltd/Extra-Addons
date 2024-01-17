from odoo import models, fields, api, _
from odoo.exceptions import UserError


class SaleOrder(models.Model):
    _inherit = "sale.order"

    po_count = fields.Integer('PO Count', compute='_compute_po_count')
    show_po_ids = fields.One2many('purchase.order', 'sale_id', string='PO Show', compute='_compute_po')

    @api.onchange('partner_id')
    def _compute_po(self):
        dataa = self.env['purchase.order'].search([('origin', '=', self.name),
                                                  ('state', 'in', ['purchase', 'to approve'])])

        data_conf = self.env['purchase.order'].search([('origin', '=', self.name),
                                                       ('state', 'in', ['purchase'])])
        # if data:
        #     self.show_po_ids = data
        # else:
        #     self.show_po_ids = data

        if dataa:
            for data in dataa:
                if data:
                    self.show_po_ids = data
                else:
                    self.show_po_ids = data
        else:
            self.show_po_ids = dataa
        if data_conf:
            for df in data_conf:
                for dd in df.order_line:
                    for sale_line in dd.sale_line_id:
                        sale_line.vendor_id = dd.partner_id
                        sale_line.cost_price = dd.price_unit
                        sale_line.x_costtax = dd.taxes_id
                        sale_line.x_cost_subtotal = dd.price_subtotal



    def _compute_po_count(self):
        obj = self.env['purchase.order'].search([('origin', '=', self.name)])
        if obj:
            self.po_count = len(obj)
        else:
            self.po_count = 0

    def action_create_po(self):
        return {
            'name': _('Purchase Order'),
            'type': 'ir.actions.act_window',
            'res_model': 'purchase.order',
            'view_mode': 'tree,form',
            'target': 'current',
            'context': {},
            'domain': [('origin', '=', self.name)],
        }


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    checklist_vendor = fields.Boolean(string='Select', store=True)


class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    sale_line_id = fields.Many2many('sale.order.line', string='Sale line Item', store=True)
    sale_id = fields.Many2one('sale.order')

    def button_confirm(self):
        purchase_orders = self.env['purchase.order'].search([('origin', '=', self.origin)])
        for frt in purchase_orders:
            if frt.state =='purchase':
                for tr in self.order_line.sale_line_id:
                    if tr.id in frt.order_line.sale_line_id.ids:
                        wiz = self.env['validate.pop'].create({'purchase_id': self.id})
                        view_id = self.env.ref('multi_rfq_quotation.view_validate_pop_form').id
                        return {
                            'name': _('Validation Wizard'),
                            'type': 'ir.actions.act_window',
                            'view_mode': 'form',
                            'res_model': 'validate.pop',
                            'target': 'new',
                            'view_id': view_id,
                            'context': self.env.context,
                            'res_id': wiz.id,
                        }
        super(PurchaseOrder, self).button_confirm()



class PurchaseOrderLine(models.Model):
    _inherit = "purchase.order.line"

    sale_line_id = fields.Many2one('sale.order.line', string='Sale line Item', store=True)
