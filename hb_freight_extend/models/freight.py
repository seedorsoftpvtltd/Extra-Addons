from datetime import datetime
from odoo import _, api, fields, models
from odoo.exceptions import UserError
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT as DTF


class FreightOperationserviceExtend(models.Model):
    _inherit = "operation.service"

    reimbursable = fields.Boolean(string="Is Reimbursable")
    x_job_type = fields.Many2one('utm.medium', related='operation_id.x_job_type')
    job_type = fields.Char('Job Typee', compute='_job_type', store="True")

    @api.depends('x_job_type')
    def _job_type(self):
        for rec in self:
            if rec.x_job_type:
                rec['job_type'] = rec.x_job_type.name
            else:
                rec['job_type'] = 'no'
            print(rec.job_type, '------rec.job_type------services')


class ProdproductExtend(models.Model):
    _inherit = "product.template"

    job_type = fields.Char('Job Typee', compute='_job_type', store="True")
    job_type_parent = fields.Char('Jobb Typee', compute='_job_type', store="True")

    @api.depends('categ_id')
    def _job_type(self):
        for rec in self:
            if rec.categ_id:
                rec['job_type'] = rec.categ_id.name
            else:
                rec['job_type'] = ''
            print(rec.job_type, '------rec.job_type------product')
        for recc in self:
            if recc.categ_id.parent_id:
                recc['job_type_parent'] = recc.categ_id.parent_id.name
            else:
                recc['job_type_parent'] = ''


class ShippingOperationReportExtend(models.Model):
    _inherit = "shipping.operation.report"

    transport = fields.Selection(
        [("land", "Land"), ("ocean", "Ocean"), ("air", "Air"), ("customs_clearance", "Customs Clearance"),
         ("cross_trade", "Cross Trade"), ("local_transport", "Local Transport"), ("local_services", "Local Services"),
          ],
        default="land",
        string="Transport",
    )
    direction = fields.Selection(
        [("import", "Import"), ("export", "Export"), ("cross_trade", "Cross Trade"),
         ("local_services", "Local Services"), ("control_move", "Control Move"), ("local_move", "Local Move")],
        string="Direction",
        default="import",
    )


class SOExtend(models.Model):
    _inherit = "sale.order"

    fright_transport = fields.Selection(
        [("land", "Land"), ("ocean", "Ocean"), ("air", "Air"), ("customs_clearance", "Customs Clearance"),
         ("cross_trade", "Cross Trade"), ("local_transport", "Local Transport"), ("local_services", "Local Services"),
          ],
        default="land",
        string="Transport",
    )
    fright_direction = fields.Selection(
        [("import", "Import"), ("export", "Export"), ("cross_trade", "Cross Trade"),
         ("local_services", "Local Services"), ("control_move", "Control Move"), ("local_move", "Local Move")],
        string="Direction",
        default="import",
    )


class SOLineExtend(models.Model):
    _inherit = "sale.order.line"

    vendor_id = fields.Many2one('res.partner', string="Vendor")
    cost_price = fields.Float(string="Cost Price")


class OperationRouteExtend(models.Model):
    _inherit = "operation.route"

    transport = fields.Selection(
        [("land", "Land"), ("ocean", "Ocean"), ("air", "Air"), ("customs_clearance", "Customs Clearance"),
         ("cross_trade", "Cross Trade"), ("local_transport", "Local Transport"), ("local_services", "Local Services"),
          ],
        default="land",
        string="Transport",
    )


class FreightVesselsExtend(models.Model):
    _inherit = "freight.vessels"

    transport = fields.Selection(
        [("land", "Land"), ("ocean", "Ocean"), ("air", "Air"), ("customs_clearance", "Customs Clearance"),
         ("cross_trade", "Cross Trade"), ("local_transport", "Local Transport"), ("local_services", "Local Services"),
          ],
        default="land",
        string="Transport",
    )


class FreightOperationLineExtend(models.Model):
    _inherit = "freight.operation.line"

    billing_on = fields.Selection(
        [("weight", "Weight"), ("volume", "Volume"), ("lumpsum", "Lump Sum")],
        string="Billing On",
        default="weight",
    )


class FreightOperationExtend(models.Model):
    _inherit = "freight.operation"

    x_job_type = fields.Many2one('utm.medium', readonly=False)
    ocean_shipping = fields.Selection(
        [("fcl", "FCL"), ("lcl", "LCL")],
        string="Ocean Shipping",
        help="""FCL: Full Container Load.
            LCL: Less Container Load.""",
    )
    transport = fields.Selection(
        [("land", "Land"), ("ocean", "Ocean"), ("air", "Air"), ("customs_clearance", "Customs Clearance"),
         ("cross_trade", "Cross Trade"), ("local_transport", "Local Transport"), ("local_services", "Local Services"),
          ],
        default="land",
        string="Transport",
    )
    direction = fields.Selection(
        [("import", "Import"), ("export", "Export"), ("cross_trade", "Cross Trade"),
         ("local_services", "Local Services")],
        string="Direction",
        default="import",
    )

    # loading_port_id = fields.Many2one("freight.port", string="Loading Port")
    # discharg_port_id = fields.Many2one("freight.port", string="Discharging Port")

    @api.model
    def create(self, vals):
        res = super(FreightOperationExtend, self).create(vals)
        if self.main_id:
            self['x_job_type'] = self.main_id.medium_id.id
            self['loading_port_id'] = self.main_id.x_origin.id
            self['discharg_port_id'] = self.main_id.x_finaldestination.id
        return res

    def write(self, vals):
        res = super(FreightOperationExtend, self).write(vals)
        if 'main_id' in vals:
            for rec in self:
                rec.x_job_type = rec.main_id.medium_id.id
                rec.loading_port_id = rec.main_id.x_origin.id
                rec.discharg_port_id = rec.main_id.x_finaldestination.id

        return res

    @api.constrains('main_id')
    def _jobtype(self):
        for rec in self:
            if rec.main_id:
                rec['x_job_type'] = rec.main_id.medium_id.id
                rec['loading_port_id'] = rec.main_id.x_origin.id
                rec['discharg_port_id'] = rec.main_id.x_finaldestination.id

            # else:
            #     rec['x_job_type'] = ''

    def action_invoice_inh(self):
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
                        operation.consignee_id and operation.consignee_id.id or False,
                    ),
                ],
                limit=1,
            )
            done_line = operation.operation_line_ids.mapped("invoice_id")
            done_services = operation.service_ids.mapped("invoice_id")
            if len(done_line) < len(operation.operation_line_ids) or len(
                    done_services
            ) < len(operation.service_ids):
                if not invoice:
                    inv_val = {
                        "operation_id": operation.id or False,
                        "type": "out_invoice",
                        "state": "draft",
                        "partner_id": operation.consignee_id.id or False,
                        "invoice_date": fields.Date.context_today(self),
                        # "x_clientrefno": operation.x_clientrefno or False,
                    }
                    invoice = inv_obj.create(inv_val)
                operation.write({"invoice_id": invoice.id})
                for line in operation.service_ids:
                    if line.reimbursable == False:
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
                                                "price_unit": line.list_price or 0.0,
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

    #                for line in operation.operation_line_ids:
    #                    if not line.invoice_id and not line.inv_line_id:
    #                        qty = 0.0
    #                        if line.billing_on == "volume":
    #                            qty = line.exp_vol or 0.0
    #                        elif line.billing_on == "weight":
    #                            qty = line.exp_gross_weight or 0.0
    #                        invoice.write(
    #                            {
    #                                "invoice_line_ids": [
    #                                    (
    #                                        0,
    #                                        0,
    #                                        {
    #                                            "move_id": invoice.id or False,
    #                                            "name": line.product_id
    #                                                    and line.product_id.name
    #                                                    or "",
    #                                            "product_id": line.product_id
    #                                                          and line.product_id.id
    #                                                          or False,
    #                                            "quantity": qty,
    #                                            "product_uom_id": line.product_id
    #                                                              and line.product_id.uom_id
    #                                                              and line.product_id.uom_id.id
    #                                                              or "",
    #                                            "price_unit": line.price or 0.0,
    #                                        },
    #                                    )
    #                                ]
    #                            }
    #                        )
    #                        ser_upd_vals = {"invoice_id": invoice.id or False}
    #                        if invoice.invoice_line_ids:
    #                            inv_l_id = invoice.invoice_line_ids.search(
    #                                [
    #                                    ("service_id", "=", line.id),
    #                                    ("id", "in", invoice.invoice_line_ids.ids),
    #                                ],
    #                                limit=1,
    #                           )
    #                           ser_upd_vals.update(
    #                               {"inv_line_id": inv_l_id and inv_l_id.id or False}
    #                           )
    #                       line.write(ser_upd_vals)

    @api.constrains("operation_line_ids")
    def _check_container_capacity(self):
        for operation in self:
            for line in operation.operation_line_ids:
                containers = operation.operation_line_ids.filtered(
                    lambda rec: rec.container_id.id == line.container_id.id
                )
                order_weight = order_volume = 0.0
                # for container in containers:
                #     order_weight += container.exp_gross_weight or 0.0
                #     order_volume += container.exp_vol or 0.0
                # if order_weight > line.container_id.weight:
                #    raise UserError(
                #         _(
                #             "%s Container's Weight Capacity is %s! \n \
                #     You planned more weight then container capacity!!"
                #         )
                #         % (line.container_id.name, line.container_id.weight)
                #     )

                # if order_volume > line.container_id.volume:
                #     raise UserError(
                #         _(
                #             "%s Container's Volume Capacity is %s! \n \
                #     You planned more volume then container capacity!!"
                #         )
                #         % (line.container_id.name, line.container_id.volume)
                #     )

    def action_confirm(self):
        """Action Confirm Method."""
        seq_obj = self.env["ir.sequence"]
        for operation in self:
            operation_vals = {}
            for line in operation.operation_line_ids:
                if line.exp_vol > line.container_id.volume:
                    print("hello")
            if not operation.name:
                operation_vals.update(
                    {"name": seq_obj.next_by_code("freight.operation.direct")}
                )
            route_val = {
                "route_operation": "main_carrige",
                "source_location": operation.loading_port_id
                                   and operation.loading_port_id.id
                                   or False,
                "dest_location": operation.discharg_port_id
                                 and operation.discharg_port_id.id
                                 or False,
                "transport": operation.transport,
            }
            operation_vals.update(
                {"state": "confirm", "routes_ids": [(0, 0, route_val)]}
            )
            operation.write(operation_vals)
            containers = operation.operation_line_ids.mapped("container_id")
            if containers:
                containers.write({"state": "reserve"})
            services = operation.mapped("routes_ids").mapped("service_ids")
            if services:
                services.write({"operation_id": operation.id})


