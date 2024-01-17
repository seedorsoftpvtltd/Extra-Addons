from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class CreatePatientWizard(models.TransientModel):
    _name = "create.invoice.wizard"
    _description = "Create Invoice Wizard"

    # isinvoice = fields.Boolean(string="Is Invoice", )
    # isbill = fields.Boolean(string="Is Bill", )

    service_ids = fields.One2many(
        "job.invoice.wizard", "new_line_id", string="Services"
    )
    partner_id = fields.Many2one('res.partner', string='Vendor')
    customer_id = fields.Many2one('res.partner', string='Vendor')
    isinvoice = fields.Boolean(string="Select Invoice")
    product_id = fields.Many2one('product.product',String='Product')
    consignee_id = fields.Many2one("res.partner", string="Consignee")
    operation_id = fields.Many2one("freight.operation", "Freight Operation")
    routes_ids = fields.One2many("operation.route", "operation_id", string="Routes")
    link_id=fields.Many2one('operation.service',string='Link')
    triger = fields.Boolean('trigger', )
    invoice = fields.Boolean('invoice')
    qty = fields.Float(String='Quantity', readonly=True)
    list_price =fields.Float(String='Sale Price', readonly=True)

    # invoice_line_ids = fields.One2many('account.move.line', 'move_id', string='Invoice lines',
    #                                    copy=False, readonly=True,
    #                                    domain=[('exclude_from_invoice_tab', '=', False)],
    #                                    states={'draft': [('readonly', False)]})

    @api.model
    def default_get(self, default_fields):
        res = super(CreatePatientWizard, self).default_get(default_fields)
        data = self.env['freight.operation'].browse(self._context.get('active_ids', []))
        update = []

        for record in data.service_ids:
            if record.isinvoice == False:

                update.append((0, 0, {
                    'vendor_id': record.vendor_id.id,
                    'isinvoice': record.isinvoice,
                    'customer_id':record.customer_id.id,
                    'product_id': record.product_id.id,
                    'qty': record.qty,
                    'list_price': record.list_price,
                }))
        res.update({'service_ids': update})
        return res

    # @api.depends('triger')
    # def compute_service_ids(self):
    #     data = self.env['freight.operation'].browse(self._context.get('active_ids', []))
    #     print(data.service_ids)
    #     if data.service_ids:
    #         self.service_ids = data.service_ids
    #     else:
    #         self.service_ids = data.service_ids
    #         raise ValidationError('service is empty')
    #
    # def action_invoice_inh(self):
    #     data = self.env['freight.operation'].browse(self._context.get('active_ids', []))
    #
    #     # Update the isinvoice field to True for selected services
    #     data.service_ids.filtered(lambda r: r.isinvoice and not r.isinvoice).write({'isinvoice': True})
    #
    #     # Retrieve the updated selected_service_ids
    #     selected_service_ids = data.service_ids.filtered(lambda r: r.isinvoice and r.isinvoice).ids
    #
    #     print(selected_service_ids, 'selected_service_ids')
    #     print(data, 'fo11111111111')
    #
    #     # Perform your desired actions with the selected service IDs
    #     data.action_invoice_inh(selected_service_ids)
    # def action_invoice_inh(self):
    #     data = self.env['freight.operation'].browse(self._context.get('active_ids', []))
    #     selected_service_ids = self.env['operation.service'].search([('isinvoice', '=', True)]).ids
    #
    #     print(selected_service_ids, 'selected_service_ids')
    #     print(data, 'fo11111111111')
    #
    #     # Perform your desired actions with the selected service IDs
    #     if selected_service_ids:
    #         data.action_invoice_inh(selected_service_ids)
    #     else:
    #         # Perform alternative actions when no selected service IDs
    #         # For example, display a message or perform a default action
    #         print("No selected service IDs")

    def action_invoice_inh(self):
        service = []
        ids=[]
        updated_service_ids = []
        data = self.env['freight.operation'].browse(self._context.get('active_ids', []))
        for rec in self.service_ids:
                service.append(rec.isinvoice)

        # if True not in service:
        #     # Display validation message or raise an exception
        #     raise ValidationError("Please select any of the above services to generate invoice")
        for line in range(0, len(data.service_ids)):
            if data.service_ids[line].isinvoice == False:
                ids.append(data.service_ids[line])

        for recc in range(0, len(ids)):

                ids[recc].update({'isinvoice': service[recc]})
        # for line in range(0, len(data.service_ids)):
        #     # data.service_ids[line].update({'isinvoice': service[line]})
        #     updated_service_ids.append(data.service_ids[line].id)
        #     print('data')
        #     print(service[line],'service[line]1')
        #
        data.action_invoice_inh1()



        # inv = data.service_ids[line].update({'isinvoice': service[line]})
        # print(inv,'inv')
        # if inv.isinvoice == True:
        #     print(inv.isinvoice,'inv.isinvoice')

        # invo =  data.service_ids[line].isinvoice
        # if data.service_ids[line].isinvoice == True:
        #     print(data.service_ids[line].isinvoice, 'invo1')
        # print(invo,'invo')
        # Perform your desired actions with the selected service IDs

    # def action_invoice_inh(self):
    #     data = self.env['freight.operation'].browse(self._context.get('active_ids', []))
    #
    #     print(data,'fo11111111111')
    #     data.action_invoice_inh()


class JobInvoice(models.TransientModel):
    _name = 'job.invoice.wizard'

    new_line_id = fields.Many2one('create.invoice.wizard')

    vendor_id = fields.Many2one('res.partner', string="Vendor",readonly=True)
    isinvoice = fields.Boolean(string="Is Invoice")
    customer_id=fields.Many2one('res.partner', string="Customer",readonly=True)
    product_id = fields.Many2one('product.product', String='Service',readonly=True)
    qty = fields.Float(String='Quantity', readonly=True)
    list_price =fields.Float(String='Sale Price', readonly=True)

class FreighOp(models.Model):
    _inherit='freight.operation'


    def action_invoice_inh1(self):
        inv_obj = self.env["account.move"]
        # inv_line_obj = self.env['account.move.line']
        for operation in self:

            services = operation.mapped("routes_ids").mapped("service_ids")
            services.write({"operation_id": operation.id})
            invoice = inv_obj.search(
                [
                    ("operation_id", "=", operation.id),
                    ("type", "=", "out_invoice"),
                    ("state", "=", "draft"),
                    (
                        "partner_id",
                        "=",
                        operation.customer_id and operation.customer_id.id or False,
                    ),
                ],
                limit=1,
            )
            done_line = operation.operation_line_ids.mapped("invoice_id")
            done_services = operation.service_ids.mapped("invoice_id")
            if len(done_line) < len(operation.operation_line_ids) or len(
                    done_services
            ) < len(operation.service_ids):
                # if not invoice:
                #     print("eeeeeeeeeeeeeeeeeeeeeeeeeeee")
                inv_val = {
                        "operation_id": operation.id or False,
                        "type": "out_invoice",
                        "state": "draft",
                        "partner_id": operation.customer_id.id or False,
                        "invoice_date": fields.Date.context_today(self),
                        # "x_clientrefno": operation.x_clientrefno or False,
                    }
                invoice = inv_obj.create(inv_val)

                operation.write({"invoice_id": invoice.id})
                for line in operation.service_ids:
                    if line.reimbursable == False and line.isinvoice == True:
                        if not line.invoice_id and not line.inv_line_id:

                            # we did the below code to update inv line id
                            # in service, other wise we can do that by
                            # creating common vals
                            invoice.write(
                                {
                                    "invoice_line_ids": [
                                        (
                                            0,
                                            0,
                                            {
                                                "move_id": invoice.id or False,
                                                "service_id": line.id or False,
                                                # 'account_id': account_id.id or False,
                                                "name": line.product_id
                                                        and line.product_id.name
                                                        or "",
                                                "product_id": line.product_id
                                                              and line.product_id.id
                                                              or False,
                                                "quantity": line.qty or 0.0,
                                                "product_uom_id": line.uom_id
                                                                  and line.uom_id.id
                                                                  or False,
                                                "price_unit": line.x_list_price or 0.0,
                                                'tax_ids': [(6, 0, line.x_sale_tax.ids)] or [(6, 0, line.product_id.taxes_id.ids)],
                                            },
                                        )
                                    ]
                                }
                            )
                            ser_upd_vals = {"invoice_id": invoice.id or False}
                            if invoice.invoice_line_ids:

                                inv_l_id = invoice.invoice_line_ids.search(
                                    [
                                        ("service_id", "=", line.id),
                                        ("id", "in", invoice.invoice_line_ids.ids),
                                    ],
                                    limit=1,
                                )
                                ser_upd_vals.update(
                                    {"inv_line_id": inv_l_id and inv_l_id.id or False}
                                )
                            line.write(ser_upd_vals)

