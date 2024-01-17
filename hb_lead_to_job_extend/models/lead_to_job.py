from odoo import api, fields, models,_
from odoo.exceptions import ValidationError, UserError
import logging


_logger = logging.getLogger(__name__)

class LeadJob(models.Model):
    _inherit='crm.lead'

    x_consignee=fields.Many2one('res.partner', string='Consignee')


class Sale_Estimate_Job(models.Model):
    _inherit = "sale.estimate.job"

    x_consignee = fields.Many2one('res.partner', string='Consignee')


class SaleOrder(models.Model):
    _inherit='sale.order'

    x_consignee= fields.Many2one('res.partner', string='Consignee')


    def action_create_job(self):
        print("111111111111111111111111111111111111111111")
        self.ensure_one()
        res = self.env['freight.operation'].browse(self._context.get('main_id', []))
        job_rec = self.env['freight.operation'].search([('main_id', '=', self.id)])
        for rec in job_rec:
            _logger.warning(
                '--------------------------->>>>>>>>>>>>>recccccccccccccccccccccccjobbbbbbbbbbbbbbbbbbbbbbbbbbb')
            if rec.state != 'cancel':
                _logger.warning('--------------------------->>>>>>>>>>>>>jobbbbbbbbbbbbbbbbbbbbbbbbbbb')
                raise ValidationError(_("You cannot create a new job as there is an active job in progress. "
                                        "Please ensure the existing job is in a 'cancelled' state before creating a new job record"))
        # data = self.env['sale.order'].browse([])
        # print(data)
        service = []
        for record in self.order_line:
            service.append((0, 0, {
                'product_id': record.product_id.id,
                # 'order_id': record.order_id.id,
                #'name': record.name,
                'qty': record.product_uom_qty,
                'uom_id':record.product_uom.id,
                'list_price': record.price_unit,
                'cost_price': record.cost_price,
                # 'product_subtotal': record.price_subtotal,
                'vendor_id' : record.vendor_id.id,
                'main_service_id':record.id,
            }))
        print(service)

        update = []
        if self.fright_transport == 'land':
            for record in self.x_consignment_id:
                update.append((0, 0, {
                    'x_truck': record.x_truck.id,
                    'product_id': record.x_description.id,
                    'exp_gross_weight': record.x_grossweight,
                    'exp_vol': record.x_volume,
                    'billing_on': record.x_billing_on,
                    'main_freight_id': record.id,
                }))
            print(update)
            val = []
        else:
            for record in self.x_consignment_id:
                update.append((0, 0, {
                    'container_id': record.x_container.id,
                    'product_id': record.x_description.id,
                    'exp_gross_weight': record.x_grossweight,
                    'exp_vol': record.x_volume,
                    'billing_on': record.x_billing_on,
                    'main_freight_id': record.id,
                }))
            print(update)
            val = []



        # update_road = []
        # for record in self.x_consignment_road:
        #     update_road.append((0, 0, {
        #         'x_truck': record.x_truck.id,
        #         'x_typee': record.x_typee.id,
        #         'product_id': record.x_description.id,
        #         'exp_gross_weight': record.x_grossweight,
        #         'exp_vol': record.x_volume,
        #         'billing_on': record.x_billing_on,
        #         'main_freight_id': record.id,
        #     }))
        # print(update_road)
        # val = []

        for rec in self:
            val.append([0, 0, {
                'partner_id': rec.partner_id,
            }])
            res.create({
                'customer_id': self.partner_id.id,
                # # 'date_order': str(td_date),
                'consignee_id': self.x_consignee.id,
                'operation_line_ids': update,
                'direction': self.fright_direction,
                'transport': self.fright_transport,
                'ocean_shipping': self.fright_ocean_shipping,
                'land_shipping': self.fright_land_shipping,
                'main_id': self.id,
                'incoterm': self.incoterm.id,
                'service_ids': service,

            })

            # if rec.fright_transport == 'land':
            #     res.create({
            #         'customer_id': self.partner_id.id,
            #         # # 'date_order': str(td_date),
            #         'consignee_id': self.partner_id.id,
            #         'operation_line_ids': update_road,
            #         'direction': self.fright_direction,
            #         'transport': self.fright_transport,
            #         'ocean_shipping': self.fright_ocean_shipping,
            #         'land_shipping': self.fright_land_shipping,
            #         'main_id': self.id,
            #         'incoterm': self.incoterm.id,
            #         'service_ids': service,
            #
            #     })
            # else:



        return res





class crm_estimate(models.Model):

    _inherit='crm.lead'

    def action_create_estimate_from_crm(self):
        print('pppppppppppppppppppppppppppp')
        val=[]
        res=self.env['sale.estimate.job'].browse(self._context.get('estim_id', []))
        # sale_pricelist = self.partner_id.property_product_pricelist
        print(res)
        # for rec in self:
        #     val.append([0, 0, {
        #         'partner_id': rec.partner_id.id,
        #
        #     }])
        res.create({
            'partner_id': self.partner_id.id,
            'pricelist_id': self.partner_id.property_product_pricelist.id,
            'estim_id':self.id,
            'lead_ref':self.code,
            'x_consignee':self.x_consignee.id
        })

class SaleEstimateJob(models.Model):
    _inherit = "sale.estimate.job"


    # @api.multi
    def estimate_to_quotation(self):
        quo_obj = self.env['sale.order']
        quo_line_obj = self.env['sale.order.line']
        for rec in self:
            vals = {
                'partner_id': rec.partner_id.id,
                'origin': rec.number,
                # 'project_id':rec.analytic_id.id
                'analytic_account_id': rec.analytic_id.id,
                'estim_sale_link': rec.id,
                'x_consignee': rec.x_consignee.id
            }
            quotation = quo_obj.create(vals)
            rec._prepare_quotation_line(quotation)
            rec.quotation_id = quotation.id
        rec.state = 'quotesend'


class FreightOperationExtend(models.Model):
    _inherit = "freight.operation"

    @api.onchange("customer_id")
    def _onchange_customer_id(self):
    # """Onchange to set the consignee_id."""
          print('hello')


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
                        "partner_id": operation.customer_id.id or False,
                        "invoice_date": fields.Date.context_today(self),
                        "x_consignee1": operation.consignee_id.id or False,
                        "x_shipper_ref_no": operation.x_shipmentno or False,
                        "x_note": operation.x_remarks or False,
                        "x_master": operation.x_mbl_no or False,
                        "x_final": operation.discharg_port_id.id or False,
                        "x_clientrefno": operation.x_clientrefno or False,
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
                                                'tax_ids': [(6, 0, line.x_sale_tax.ids)],
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


class Goods_Stock_Stage(models.Model):
    _inherit='stock.picking'


    custom_state= fields.Char(compute="_compute_state_label" , String="Stage", readonly=True)


    @api.depends('state')
    def _compute_state_label(self):
        for rec in self:
            if rec.state == 'assigned' and rec.picking_type_id.id  == 3:
                rec.custom_state = 'Pick list to initiate'
            elif rec.state == 'waiting' and rec.picking_type_id.id  == 2:
                rec.custom_state = 'Delivery to initiate'
            elif rec.state == 'done' and rec.picking_type_id.id  == 3:
                rec.custom_state = 'Pick list Completed'
            elif rec.state == 'done' and rec.picking_type_id.id == 2:
                rec.custom_state = 'Delivery completed'
            else:
                rec.custom_state = 'Draft'
