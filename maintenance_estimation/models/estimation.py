from datetime import datetime
from odoo import api, fields, models
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT, DEFAULT_SERVER_DATE_FORMAT, misc, ustr


class EstimateF(models.Model):
    _inherit = "sale.estimate.job"

    main_id = fields.Many2one('maintenance.request', string='Maintenance Req', store=True)

class EstimateMaintenance(models.Model):
    _inherit = "maintenance.request"
    par_id = fields.Many2one('res.partner', string='Maintenance Incharge',compute='_compute_admin', store=True)
    amount = fields.Integer(string='Maintenance Amount')
    estimate_main_count = fields.Integer('Estimate Count', compute='_compute_esti_count')
    
    @api.depends('employee_id')
    def _compute_admin(self):
        print("diii")
        for rec in self:
            print("hii")
            if rec.employee_id:
                rec['par_id']=rec.employee_id.user_partner_id
    
    def _compute_esti_count(self):
        obj = self.env['sale.estimate.job']
        for serv in self:
            cnt = obj.search_count([
                ('main_id', '=', serv.id)])
            if cnt != 0:
                print("hii")
                serv['estimate_main_count'] = cnt
            else:
                print("hello")
                serv['estimate_main_count'] = 0
    def action_create_maintenance_estim(self):
        self.ensure_one()
        res = self.env['sale.estimate.job'].browse(self._context.get('main_id', []))
        print(res)
        value = []
        maintenance_pricelist = self.par_id.property_product_pricelist
        m_partner_pricelist = self.par_id.property_product_pricelist
        # service_order_name = self.name
        td_date = datetime.now()
        val = []
        product = self.env['product.product'].search([('name', '=', 'Maintenance')])
        for rec in self:
            val.append([0, 0, {
                'job_type': 'labour',
                'product_id': product.id,
                'product_description': ustr(rec.maintenance_type),

                'price_unit':rec.amount,
                'product_uom': product.uom_id.id,
                # 'account_id': rec.vehicle_id and
                #               rec.vehicle_id.income_acc_id.id or False,
            }])

        for check in self.mchecklist_ids:
            for chk in check.checklist:
                # if chk.red or chk.yellow:
                if m_partner_pricelist:
                    product_context = dict(self.env.context, partner_id=self.employee_id.id, date=td_date,
                                           uom=chk.name.uom_id.id)
                    final_price, rule_id = m_partner_pricelist.with_context(product_context).get_product_price_rule(
                        chk.name, chk.qty or 1.0, self.employee_id)

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
        #
        # for temp in self.template_line_ids:
        #     # if temp.result == 'failure':
        #     if partner_pricelist:
        #         product_context = dict(self.env.context, partner_id=self.purchaser_id.id, date=td_date,
        #                                uom=temp.service_prod.uom_id.id)
        #         final_price, rule_id = partner_pricelist.with_context(product_context).get_product_price_rule(
        #             temp.service_prod, temp.qty or 1.0, self.purchaser_id)
        #
        #     else:
        #         final_price = temp.name.standard_price
        #
        #     value.append([0, 0, {
        #         'job_type': 'material',
        #         'product_id': temp.service_prod.id,
        #         'product_description': temp.service_prod.name,
        #         'product_uom_qty': temp.qty,
        #         # 'order_id': temp.order_id.id,
        #         'product_uom': temp.service_prod.uom_id.id,
        #         # 'taxes_id': temp.service_prod.supplier_taxes_id.ids,
        #         # 'date_planned': td_date,
        #         'price_unit': final_price,
        #
        #     }])

        res.create({
            'partner_id': self.par_id.id,
            # # 'date_order': str(td_date),
            'estimate_ids': value,
            'labour_estimate_line_ids': val,
            # 'origin': service_order_name,
            # 'reference': service_order_name,
            'main_id': self.id,
            'pricelist_id': maintenance_pricelist.id or False,
        })

        return res
