from odoo import models, fields, api, _
from odoo.exceptions import ValidationError,UserError
from datetime import datetime
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT as DTF

class CreateBillWizard(models.TransientModel):
    _name = "create.bill.wizard"
    _description = "Create Bill Wizard"


    service_ids = fields.One2many(
        "job.bill.wizard", "new_line_id_bill", string="Services"
    )
    partner_id = fields.Many2one('res.partner', string='Vendor')
    isbill = fields.Boolean(string="Select Bill")
    product_id = fields.Many2one('product.product', String='Service')
    qty = fields.Float(String='Quantity', readonly=True)
    cost_price =fields.Float(String='Cost Price', readonly=True)


    @api.model
    def default_get(self, default_fields):
        res = super(CreateBillWizard, self).default_get(default_fields)
        data = self.env['freight.operation'].browse(self._context.get('active_ids', []))
        update = []

        for record in data.service_ids:
            if record.isbill == False:
                print(record)
                update.append((0, 0, {
                    'vendor_id': record.vendor_id.id,
                    'isbill': record.isbill,
                    'product_id':record.product_id.id,
                    'qty':record.qty,
                    'cost_price':record.cost_price,
                }))
        res.update({'service_ids': update})
        return res


    def action_bill_inh(self):
        service = []
        ids=[]
        updated_service_ids = []
        data = self.env['freight.operation'].browse(self._context.get('active_ids', []))
        for rec in self.service_ids:
                service.append(rec.isbill)
        print(service)
        # if True not in service:
        #     # Display validation message or raise an exception
        #     raise ValidationError("Please select any of the above services to generate invoice")
        for line in range(0, len(data.service_ids)):
            if data.service_ids[line].isbill == False:
                ids.append(data.service_ids[line])
        print(ids)
        for recc in range(0, len(ids)):

                ids[recc].update({'isbill': service[recc]})

        #
        data.action_bill_inh1()

class JobBill(models.TransientModel):
    _name = 'job.bill.wizard'

    new_line_id_bill = fields.Many2one('create.bill.wizard')

    vendor_id = fields.Many2one('res.partner', string="Vendor",readonly=True)
    isbill = fields.Boolean(string="Is Bill")
    product_id = fields.Many2one('product.product', String='Product',readonly=True)
    qty = fields.Float(String='Quantity', readonly=True)
    cost_price =fields.Float(String='Cost Price', readonly=True)

class FreighOp(models.Model):
    _inherit='freight.operation'


    def action_bill_inh1(self):

        bill_obj = self.env["account.move"]
        # bill_line_obj = self.env['account.move.line']
        for operation in self:
            if not operation.service_ids:
                raise UserError(
                    _(
                        "Direct Shipment have No any Service Line"
                        " for Bill \n Please add service line"
                        " first to Generate Bill."
                    )
                )
            services = operation.mapped("routes_ids").mapped("service_ids")
            services.write({"operation_id": operation.id})
            for line in operation.service_ids:
                if not line.bill_id and not line.bill_line_id and line.isbill == True:
                    bill = bill_obj.search(
                        [
                            ("operation_id", "=", operation.id),
                            ("type", "=", "in_invoice"),
                            ("state", "=", "draft"),
                            ("partner_id", "=", line.vendor_id.id),
                        ],
                        limit=1,
                    )

                    bill_val = {
                            "operation_id": operation.id or False,
                            "type": "in_invoice",
                            "state": "draft",
                            "partner_id": line.vendor_id.id or False,
                            "invoice_date": datetime.now().strftime(DTF),
                        }
                    bill = bill_obj.create(bill_val)
                    operation.write({"bill_id": bill.id})
                    # Used write Call because of Bill Invoice is shows
                    # unbalanced issue when we direct create the line.
                    bill.write(
                        {
                            "invoice_line_ids": [
                                (
                                    0,
                                    0,
                                    {
                                        "move_id": bill.id,
                                        "service_id": line.id or False,
                                        "product_id": line.product_id
                                                      and line.product_id.id
                                                      or False,
                                        "name": line.product_id
                                                and line.product_id.name
                                                or "",
                                        "quantity": line.qty or 1.0,
                                        "product_uom_id": line.uom_id
                                                          and line.uom_id.id
                                                          or False,
                                        "price_unit": line.x_cost_price or 0.0,
                                        'tax_ids': [(6, 0, line.x_tax_ids.ids)] or [
                                            (6, 0, line.product_id.taxes_id.ids)],
                                    },
                                )
                            ]
                        }
                    )
                    ser_upd_vals = {
                        "bill_id": bill.id,
                    }
                    if bill.invoice_line_ids:
                        bill_l_id = bill.invoice_line_ids.search(
                            [
                                ("service_id", "=", line.id),
                                ("id", "in", bill.invoice_line_ids.ids),
                            ],
                            limit=1,
                        )
                        ser_upd_vals.update(
                            {"bill_line_id": bill_l_id and bill_l_id.id or False}
                        )
                    line.write(ser_upd_vals)
        # inv_obj = self.env["account.move"]
        # # inv_line_obj = self.env['account.move.line']
        # for operation in self:
        #     print("uuuuuuuuuuuuuuu")
        #     services = operation.mapped("routes_ids").mapped("service_ids")
        #     services.write({"operation_id": operation.id})
        #     invoice = inv_obj.search(
        #         [
        #             ("operation_id", "=", operation.id),
        #             ("type", "=", "in_invoice"),
        #             ("state", "=", "draft"),
        #             (
        #                 "partner_id",
        #                 "=",
        #                 operation.consignee_id and operation.consignee_id.id or False,
        #             ),
        #         ],
        #         limit=1,
        #     )
        #     done_line = operation.operation_line_ids.mapped("invoice_id")
        #     done_services = operation.service_ids.mapped("invoice_id")
        #     if len(done_line) < len(operation.operation_line_ids) or len(
        #             done_services
        #     ) < len(operation.service_ids):
        #         # if not invoice:
        #         #     print("eeeeeeeeeeeeeeeeeeeeeeeeeeee")
        #         inv_val = {
        #                 "operation_id": operation.id or False,
        #                 "type": "in_invoice",
        #                 "state": "draft",
        #                 "partner_id": operation.consignee_id.id or False,
        #                 "invoice_date": fields.Date.context_today(self),
        #                 # "x_clientrefno": operation.x_clientrefno or False,
        #             }
        #         invoice = inv_obj.create(inv_val)
        #         print("xxxxxxxxxxxxxxxxxxxxxxx")
        #         operation.write({"invoice_id": invoice.id})
        #         for line in operation.service_ids:
        #             if line.reimbursable == False and line.isbill == True:
        #                 if not line.invoice_id and not line.inv_line_id:
        #                     print("eeeeeeeeeeeeeeeeeeeeeeeeeeeee")
        #                     # we did the below code to update inv line id
        #                     # in service, other wise we can do that by
        #                     # creating common vals
        #                     invoice.write(
        #                         {
        #                             "invoice_line_ids": [
        #                                 (
        #                                     0,
        #                                     0,
        #                                     {
        #                                         "move_id": invoice.id or False,
        #                                         "service_id": line.id or False,
        #                                         # 'account_id': account_id.id or False,
        #                                         "name": line.product_id
        #                                                 and line.product_id.name
        #                                                 or "",
        #                                         "product_id": line.product_id
        #                                                       and line.product_id.id
        #                                                       or False,
        #                                         "quantity": line.qty or 0.0,
        #                                         "product_uom_id": line.uom_id
        #                                                           and line.uom_id.id
        #                                                           or False,
        #                                         "price_unit": line.list_price or 0.0,
        #                                         # 'tax_ids': [(6, 0, line.x_sale_tax.ids)] or [(6, 0, line.product_id.taxes_id.ids)],
        #                                     },
        #                                 )
        #                             ]
        #                         }
        #                     )
        #                     ser_upd_vals = {"invoice_id": invoice.id or False}
        #                     if invoice.invoice_line_ids:
        #                         print("wwwwwwwwwwwwwwwwwwwwwwwwwww")
        #                         inv_l_id = invoice.invoice_line_ids.search(
        #                             [
        #                                 ("service_id", "=", line.id),
        #                                 ("id", "in", invoice.invoice_line_ids.ids),
        #                             ],
        #                             limit=1,
        #                         )
        #                         ser_upd_vals.update(
        #                             {"inv_line_id": inv_l_id and inv_l_id.id or False}
        #                         )
        #                     line.write(ser_upd_vals)

