from datetime import datetime
from odoo import api, fields, models


class AccountInvoiceF(models.Model):
    _inherit = "material.purchase.requisition"

    veh_service_id = fields.Many2one('fleet.vehicle.log.services', string='Vehicle Service')

class EmployeerF(models.Model):
    _inherit = "hr.employee"

    emp_ref = fields.Char('Ref')

    # @api.depends('name')
    # def _ref(self):
    #     for rec in self:
    #         rec['emp_ref'] = rec.id
    #         print(rec.emp_ref)

class PurchaseOrderF(models.Model):
    _inherit = "fleet.vehicle.log.services"

    purchase_count = fields.Integer('Purchase Count', compute='_compute_purch_count')
    employee_id = fields.Many2one('hr.employee', string="Employee", compute='_compute_emp', required=True)
    emp_ref = fields.Char('Ref', compute='_compute_emp_ref')

    # @api.depends('purchaser_id')
    # def _compute_emp_ref(self):
    #     for rec in self:
    #         id = rec.purchaser_id.id
    #         rec['emp_ref'] = id
    #         print(id)

    @api.depends('purchaser_id')
    def _compute_emp(self):
        # print("hhhhhhhhhhhhhhhhhhh")
        # for rec in self:
        #     print("bbbbbbbbbbbbbb")
        #     emp_nm = rec.purchaser_id.name
        #     emp_id = str(rec.purchaser_id.id)
        #     empp = self.env['hr.employee'].search([('name', '=', emp_nm)])
        #     for re in empp:
        #         print(re, re.emp_ref, re.name)
        #     emp = self.env['hr.employee'].search([('name', '=', emp_nm),('emp_ref','=',emp_id)])
        #     print(emp)
        #     rec['employee_id'] = emp.id

        print("hhhhhhhhhhhhhhhhhhh")
        for rec in self:
            print("bbbbbbbbbbbbbb")
            emp_nm = rec.purchaser_id.name
            emp_id = str(rec.purchaser_id.id)
            empp = self.env['hr.employee'].search([('name', '=', emp_nm)])
            for re in empp:
                print(re, re.emp_ref, re.name)
            emp = self.env['hr.employee'].search([('name', '=', emp_nm), ('emp_ref', '=', emp_id)])
            print(emp)
            rec['employee_id'] = emp.id


    def _compute_purch_count(self):
        obj = self.env['material.purchase.requisition']
        for serv in self:
            cnt = obj.search_count([
                ('veh_service_id', '=', serv.id)])
            if cnt != 0:
                serv['purchase_count'] = cnt
            else:
                serv['purchase_count'] = 0
            print(self.purchase_count, 'counttt')

    def action_create_purchaserec(self):
        self.ensure_one()
        res = self.env['material.purchase.requisition'].browse(self._context.get('veh_service_id', []))
        print(res)
        value = []
        pricelist = self.purchaser_id.property_product_pricelist
        partner_pricelist = self.purchaser_id.property_product_pricelist
        service_order_name = self.name
        td_date = datetime.now()
        for chkk in self.checklist_ids:
            for chk in chkk.checklist:
                if chk.red or chk.yellow:
                    if partner_pricelist:
                        product_context = dict(self.env.context, partner_id=self.purchaser_id.id, date=td_date,
                                               uom=chk.name.uom_id.id)
                        final_price, rule_id = partner_pricelist.with_context(product_context).get_product_price_rule(
                            chk.name, chk.qty or 1.0, self.purchaser_id)

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

        for temp in self.template_line_ids:
            if temp.result == 'failure':
                if partner_pricelist:
                    product_context = dict(self.env.context, partner_id=self.purchaser_id.id, date=td_date,
                                           uom=temp.service_prod.uom_id.id)
                    final_price, rule_id = partner_pricelist.with_context(product_context).get_product_price_rule(
                        temp.service_prod, temp.qty or 1.0, self.purchaser_id)

                else:
                    final_price = temp.name.standard_price

                value.append([0, 0, {
                    'requisition_type': 'purchase',
                    'product_id': temp.service_prod.id,
                    'description': temp.service_prod.name,
                    'qty': temp.qty,
                    # 'order_id': temp.order_id.id,
                    'uom': temp.service_prod.uom_id.id,
                    # 'taxes_id': temp.service_prod.supplier_taxes_id.ids,
                    # 'date_planned': td_date,
                    # 'price_unit': final_price,
                }])

        res.create({
            'employee_id': self.employee_id.id or '',
            'department_id': self.employee_id.department_id.id or '',
            # 'date_order': str(td_date),
            'requisition_line_ids': value,
            # 'origin': service_order_name,
            # 'partner_ref': service_order_name,
            'veh_service_id': self.id
        })

        return res
