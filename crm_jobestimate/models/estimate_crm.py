from odoo import api, fields, models


class EstimateF(models.Model):
    _inherit = "crm.lead.line"
    remark = fields.Char(string='Remarks')


class crm_estimate_new(models.Model):
        _inherit = 'crm.lead'

        def action_create_estimate_from_crm(self):
            val = []
            res = self.env['sale.estimate.job'].browse(self._context.get('estim_id', []))
            print('aru')
            for rec in self.lead_line_ids:
                val.append([0, 0, {
                    'product_id': rec.product_id.id,
                    'product_uom': rec.product_id.uom_id.id,
                    'product_uom_qty': rec.product_qty,
                    'job_type': 'material',
                    'product_description': rec.name,
                    'price_unit': rec.price_unit,
                }])
            res.create({
                'partner_id': self.partner_id.id,
                'pricelist_id': self.partner_id.property_product_pricelist.id,
                'estim_id': self.id,
                'lead_ref': self.code,
                'x_consignee': self.x_consignee.id,
                'estimate_ids': val,
            })






