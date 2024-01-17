from odoo import models, fields, api, _


class WarehouseOrder(models.Model):
    _inherit = 'warehouse.order'

    sample_service_id = fields.Many2one('product.product')

    @api.onchange('partner_id')
    def onchange_agreement(self):
        for rec in self:
            agree = self.env['agreement'].search([('partner_id', '=', rec.partner_id.id)])
            if agree:
                for agr in agree:
                    rec['agreement_id'] = agr.id
            else:
                rec['agreement_id'] = None

    @api.onchange('partner_id')
    def service_set(self):
        product_model = self.env['product.template']
        for rec in self:
            product = product_model.search([('is_default_agreement_service', '=', True)])
            if product:
                for pro in product:
                    prod = self.env['product.product'].search([('product_tmpl_id', '=', pro.id)])
                    rec.sample_service_id = prod.id
            else:
                rec.sample_service_id = None

    def button_confirm(self):
        res = super(WarehouseOrder, self).button_confirm()
        for rec in self:
            agreement_model = self.env['agreement']
            charge_model = self.env['charge.types']
            product_model = self.env['product.product']
            medium_model = self.env['utm.medium']
            if not rec.agreement_id:
                if not rec.sample_service_id:
                    new_service = product_model.create({
                        'name': 'Warehouse Sample Service',
                        'x_medium': medium_model.browse(12).id,
                        'type': 'service',
                        'lst_price': 1.000,
                        'company_id': rec.company_id.id,
                        'is_default_agreement_service': True,
                        'uom_id': self.env['uom.uom'].browse(3013).id,
                        'uom_po_id': self.env['uom.uom'].browse(3013).id,
                    })
                    rec.sample_service_id = new_service.id
                    service = new_service
                else:
                    service = rec.sample_service_id

                agreement_name = rec.partner_id.name + " Agreement"
                charges = charge_model.search([('restricted', '=', True)])
                charge_line_vals = []
                if charges:
                    for charge in charges:
                        charge_vals = {
                            'storage_uom': 'day',
                            'charge_unit_type': charge.id,
                            'product_id': service.id,
                            'list_price': 1.000,
                            'storage_type': None,
                        }
                        charge_line_vals.append((0, 0, charge_vals))
                vals = {
                    'name': agreement_name,
                    'code': "Auto",
                    'type': "warehouse",
                    'partner_id': rec.partner_id.id,
                    'company_id': rec.company_id.id,
                    'charge_lines': charge_line_vals,
                }
                new_agreement = agreement_model.create(vals)
                rec.agreement_id = new_agreement.id
                return res
        return res
