from datetime import datetime
from odoo import api, fields, models
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT, DEFAULT_SERVER_DATE_FORMAT, misc, ustr


class EstimateF(models.Model):
    _inherit = "sale.estimate.job"

    veh_service_id = fields.Many2one('fleet.vehicle.log.services', string='Vehicle Service', store=True)


class estimateOrderF(models.Model):
    _inherit = "fleet.vehicle.log.services"

    estimate_count = fields.Integer('estimate Count', compute='_compute_est_count')

    def _compute_est_count(self):
        obj = self.env['sale.estimate.job']
        for serv in self:
            cnt = obj.search_count([
                ('veh_service_id', '=', serv.id)])
            if cnt != 0:
                serv['estimate_count'] = cnt
            else:
                serv['estimate_count'] = 0

    def action_create_estimaterec(self):
        self.ensure_one()
        res = self.env['sale.estimate.job'].browse(self._context.get('veh_service_id', []))
        print(res)
        value = []
        pricelist = self.purchaser_id.property_product_pricelist
        partner_pricelist = self.purchaser_id.property_product_pricelist
        service_order_name = self.name
        td_date = datetime.now()
        val = []
        product = self.env['product.product'].search([('name', '=', 'Service')])
        for rec in self:
            val.append([0, 0, {
                'job_type': 'labour',
                'product_id': product.id,
                'product_description': ustr(rec.cost_subtype_id and
                                            rec.cost_subtype_id.name) + ' - Service Cost',
                'price_unit': rec.amount,
                'product_uom': product.uom_id.id,
                # 'account_id': rec.vehicle_id and
                #               rec.vehicle_id.income_acc_id.id or False,
            }])

        for chkk in self.checklist_ids:
            for chk in chkk.checklist:
                # if chk.red or chk.yellow:
                if partner_pricelist:
                    product_context = dict(self.env.context, partner_id=self.purchaser_id.id, date=td_date,
                                           uom=chk.name.uom_id.id)
                    final_price, rule_id = partner_pricelist.with_context(product_context).get_product_price_rule(
                        chk.name, chk.qty or 1.0, self.purchaser_id)

                else:
                    final_price = chk.name.standard_price

                value.append([0, 0, {
                    'job_type': 'material',
                    'product_id': chk.name.id,
                    'product_description': chk.name.name,
                    'product_uom_qty': chk.qty,
                    # 'order_id': chk.order_id.id,
                    'product_uom': chk.name.uom_id.id,
                    # 'taxes_id': chk.name.supplier_taxes_id.ids,
                    # 'date_planned': td_date,
                    'price_unit': final_price,

                }])

        for temp in self.template_line_ids:
            # if temp.result == 'failure':
            if partner_pricelist:
                product_context = dict(self.env.context, partner_id=self.purchaser_id.id, date=td_date,
                                       uom=temp.service_prod.uom_id.id)
                final_price, rule_id = partner_pricelist.with_context(product_context).get_product_price_rule(
                    temp.service_prod, temp.qty or 1.0, self.purchaser_id)

            else:
                final_price = temp.name.standard_price

            value.append([0, 0, {
                'job_type': 'material',
                'product_id': temp.service_prod.id,
                'product_description': temp.service_prod.name,
                'product_uom_qty': temp.qty,
                # 'order_id': temp.order_id.id,
                'product_uom': temp.service_prod.uom_id.id,
                # 'taxes_id': temp.service_prod.supplier_taxes_id.ids,
                # 'date_planned': td_date,
                'price_unit': final_price,

            }])

        res.create({
            'partner_id': self.purchaser_id.id,
            # 'date_order': str(td_date),
            'estimate_ids': value,
            'labour_estimate_line_ids': val,
            # 'origin': service_order_name,
            'reference': service_order_name,
            'veh_service_id': self.id,
            'pricelist_id': pricelist.id,
        })

        return res
