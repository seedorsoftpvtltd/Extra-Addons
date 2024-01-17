from datetime import datetime
from odoo import api, fields, models
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT, DEFAULT_SERVER_DATE_FORMAT, misc, ustr

class AccountInvoiceFi(models.Model):
    _inherit = "material.purchase.requisition"

    main_id1 = fields.Many2one('maintenance.request', string='Maintenance Req', store=True)

# class EmployeerFi(models.Model):
#     _inherit = "hr.employee"
#
#     emp_ref = fields.Char('Ref')
#
#     # @api.depends('name')
#     # def _ref(self):
#     #     for rec in self:
#     #         rec['emp_ref'] = rec.id
#     #         print(rec.emp_ref)

class PurchaseOrderFi(models.Model):
    _inherit = "maintenance.request"
    estimate_main_count1 = fields.Integer('Estimate Count', compute='_compute_esti_count1')
    def _compute_esti_count1(self):
        obj = self.env['material.purchase.requisition']
        for serv in self:
            cnt = obj.search_count([
                ('main_id1', '=', serv.id)])
            if cnt != 0:
                print("hii")
                serv['estimate_main_count1'] = cnt
            else:
                print("hello")
                serv['estimate_main_count1'] = 0

    def action_create_purchasematerial(self):
        print("hii")
        self.ensure_one()
        res = self.env['material.purchase.requisition'].browse(self._context.get('main_id1', []))
        print(res)
        value = []
        maintenance_pricelist1 = self.par_id.property_product_pricelist
        m_partner_pricelist1 = self.par_id.property_product_pricelist
        # service_order_name = self.name
        td_date = datetime.now()
        val = []
        for check in self.mchecklist_ids:
            for chk in check.checklist:
                if chk.red or chk.yellow:
                    if maintenance_pricelist1:
                        product_context = dict(self.env.context, partner_id=self.par_id.id, date=td_date,
                                               uom=chk.name.uom_id.id)
                        final_price, rule_id = maintenance_pricelist1.with_context(product_context).get_product_price_rule(
                            chk.name, chk.qty or 1.0, self.par_id)

                    else:
                        final_price = chk.name.standard_price

                    value.append([0, 0, {
                        'requisition_type': 'purchase',
                        'product_id': chk.name.id,
                        'description': chk.name.name,
                        'qty': chk.qty,
                        # 'order_id': chk.order_id.id,
                        'uom': chk.name.uom_id.id,
                        # 'taxes_id': chk.name.supplier_taxes_id.ids,
                        # 'date_planned': td_date,
                        # 'price_unit': final_price,
                    }])
        # for check in self.mchecklist_ids:
        #  for chk in check.checklist:
        #     if chk.result == 'failure':
        #         if m_partner_pricelist1:
        #             product_context = dict(self.env.context, partner_id=self.par_id.id, date=td_date,
        #                                    uom=chk.service_prod.uom_id.id)
        #             final_price, rule_id = m_partner_pricelist1.with_context(product_context).get_product_price_rule(
        #                 chk.service_prod, chk.qty or 1.0, self.par_id)
        #
        #         else:
        #             final_price = chk.name.standard_price
        #
        #         value.append([0, 0, {
        #             'requisition_type': 'purchase',
        #             'product_id': chk.service_prod.id,
        #             'description': chk.service_prod.name,
        #             'qty': chk.qty,
        #             # 'order_id': temp.order_id.id,
        #             'uom': chk.service_prod.uom_id.id,
        #             # 'taxes_id': temp.service_prod.supplier_taxes_id.ids,
        #             # 'date_planned': td_date,
        #             # 'price_unit': final_price,
        #         }])

        res.create({
            'employee_id': self.employee_id.id or '',
            'department_id': self.employee_id.department_id.id or '',
            # 'date_order': str(td_date),
            'requisition_line_ids': value,
            # 'origin': service_order_name,
            # 'partner_ref': service_order_name,
            'main_id1': self.id
        })

        return res