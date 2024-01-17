from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError, Warning


class RfqConfirm(models.TransientModel):
    _name = "rfq.wizard"

    services = fields.One2many('rfq.services.wizard', 'parent_id', string='Services')
    requisition_id = fields.Many2one('purchase.requisition', string='Requisition ID')
    rfq_services_rejected = fields.Text(string='Rejected Services', compute='_confirm_services')
    approve = fields.Boolean(string='To Proceed further please Approve')


    def create(self, vals):
        print('create')
        res = super(RfqConfirm, self).create(vals)
        print(res.requisition_id)
        print(self.requisition_id)
        if not res.requisition_id:
            raise Warning(_('requisiiton id not found, create..................'))
        if res.requisition_id:
            pline = self.env['purchase.order.line'].search([])
            for p in pline:
                if p.requisition_id == res.requisition_id:
                    self.env['rfq.services.wizard'].create({
                        'purchase_line_id': p.id,
                        'parent_id': res.id,
                    })
        return res

    def unl(self, id):
        self.env['purchase.order.line'].search([('id', '=', id)]).unlink()

    def rfq_service_confirmation(self):
        rfq_line_rejected = self.env['purchase.order.line'].search([('confirm', '=', False)])
        rfqs = self.env['purchase.order'].search([('requisition_id', '=', self.requisition_id.id)])
        for line in rfq_line_rejected:
            print(line, 'line')
            rfq_ser = self.services.search([])
            for s in rfq_ser:
                s.unlink()
                # line.order_id = False
                id = line.id
                self.unl(id)
#                line.order_id.button_confirm()
#        for rfq in rfqs:
#            for rfq_line in rfq.order_line:
#                if rfq_line.confirm == True and rfq_line.order_id.state != 'purchase':
#                    rfq_line.order_id.button_confirm()
        rfq_id = []
        for rfq in rfqs:
            for rfq_line in rfq.order_line:
                if rfq_line.confirm == True and rfq_line.order_id.state != 'purchase':
                    rfq_id.append(rfq_line.order_id)
        for confirm in rfq_id:
            confirm.button_confirm()
            confirm.write({'state':'purchase'})


    @api.depends('services')
    def _confirm_services(self):
        rfq_service_approved = []
        rfq_service_rejected = []
        for rec in self.services:
            if rec.confirm == True:
                service = rec.purchase_line_id
                service.write({'confirm': True})
        if not self.requisition_id:
            raise Warning(_('requisiiton id not found'))
        rfqs = self.env['purchase.order'].search([('requisition_id', '=', self.requisition_id.id)])
        if not rfqs:
            raise Warning(_('rfqs not found'))
        for rfq in rfqs:
            for rfq_line in rfq.order_line:
                if not rfq_line:
                    raise Warning(_('rfq_line not found'))
                if rfq_line.confirm == True:
                    # print(rfq_line.product_id.name, rfq_line)
                    rfq_service_approved.append(rfq_line.product_id.name)
                    # print(rfq_service_approved)
                    self[
                        'rfq_services_rejected'] = 'Unselected services discarded once you approve the selected services.'
                else:
                    print(rfq_line.product_id.name, rfq_line)
                    rfq_service_rejected.append(rfq_line.product_id.name)
                    print(rfq_service_rejected)
                    self[
                        'rfq_services_rejected'] = 'The Following Services has beem rejected. Please ensure this. Proceeding further discard the rejected services' + str(
                        rfq_service_rejected)[1:-1]



class RfqServiceConfirm(models.TransientModel):
    _name = "rfq.services.wizard"

    parent_id = fields.Many2one('rfq.wizard', string='RFQ')
    requisition_id = fields.Many2one('purchase.requisition', string='Requisition ID',
                                     related='parent_id.requisition_id')
    purchase_line_id = fields.Many2one('purchase.order.line', string='Service Line')
    product_id = fields.Many2one('product.product', string='Services', related='purchase_line_id.product_id')
    product_qty = fields.Float(string='Qty', related='purchase_line_id.product_qty')
    product_uom = fields.Many2one(string='UOM', related='purchase_line_id.product_uom')
    price_unit = fields.Float(string='Unit Price', related='purchase_line_id.price_unit')
    confirm = fields.Boolean(sring='Confirm Service')
    vendor_id = fields.Many2one('res.partner', string='Vendor', related='purchase_line_id.partner_id')
    purchase_id = fields.Many2one('purchase.order', string='RFQ Reference',  related='purchase_line_id.order_id')


class PurchaseOrderLineEXT(models.Model):
    _inherit = 'purchase.order.line'

    confirm = fields.Boolean(string='Confirm Service', store=True)
    requisition_id = fields.Many2one('purchase.requisition', string='Requisition ID', related='order_id.requisition_id')


class SaleOrderEXT(models.Model):
    _inherit = "sale.order"

    requis_id = fields.Many2one('purchase.requisition', string='Requisition ID')

    def services_confirm(self):
        wizard = self.env['rfq.wizard'].create({
            'requisition_id': self.requis_id.id,
        })
        print(wizard, 'wiz', wizard.requisition_id)
        view_id = self.env.ref('hb_rfq_public_form.view_rfq_wizard').id
        print(view_id)
        return {
            'name': _('Services Confirmation'),
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'rfq.wizard',
            'res_id': wizard.id,
            'views': [(view_id, 'form')],
            'view_id': view_id,
            'target': 'new',
        }

    def create_purchase_agreement(self):
        for rec in self:
            agree_lines = []
            for l in rec.order_line:
                lines = {
                    'product_id': l.product_id.id,
                    'product_qty': l.product_uom_qty,
                    'product_uom_id': l.product_id.uom_id.id,
                    'price_unit': l.price_unit,
                }
                agree_lines.append((0, 0, lines))
            vals = {
                'user_id': self.env.user.id,
                'company_id': self.env.company.id,
                'line_ids': agree_lines
            }
            purchase_agreement = self.env['purchase.requisition'].create(vals)
            purchase_agreement.action_in_progress()
            print(purchase_agreement)
            rec['requis_id'] = purchase_agreement.id
            # return rec.requis_id

    def purchase_comparison(self):
        for rec in self:
            requisition = rec.requis_id
            return requisition.purchase_comparison()
