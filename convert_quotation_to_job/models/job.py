from datetime import datetime
from odoo import api, fields, models
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT, DEFAULT_SERVER_DATE_FORMAT, misc, ustr


class Job(models.Model):
    _inherit = "freight.operation"

    main_id = fields.Many2one('sale.order', string='Sale Order', store=True)
    incoterm=fields.Many2one('account.incoterms',String='Incoterm')
    # sale_fright_id = fields.Many2one('freight.operation', string='Sale ID', store=True)

class JobSevice(models.Model):
    _inherit = "operation.service"

    main_service_id = fields.Many2one('sale.order.line', string='Sale Order Line', store=True)

class JobConsignment(models.Model):
    _inherit = "freight.operation.line"

    main_freight_id = fields.Many2one('x_consignment', string='Consignment', store=True)


class SaleJob(models.Model):
    _inherit = "sale.order"

    fright_direction = fields.Selection(
        [("import", "Import"), ("export", "Export")],
        string="Direction",
        default="import",
    )
    fright_transport = fields.Selection(
        [("land", "Land"), ("ocean", "Ocean"), ("air", "Air")],
        default="land",
        string="Transport",
    )
    fright_ocean_shipping = fields.Selection(
        [("fcl", "FCL"), ("lcl", "LCL")],
        string="Ocean Shipping",
        help="""FCL: Full Container Load.
        LCL: Less Container Load.""",
    )
    fright_land_shipping = fields.Selection(
        [("ftl", "FTL"), ("ltc", "LTL")],
        string="Land Shipping",
        help="""FTL: Full Truckload.LTL: Less Then Truckload.""",
    )
    # par_id = fields.Many2one('res.partner', string='Maintenance Incharge', store=True)

    job_count = fields.Integer('Job Count', compute='_compute_Job_count')
    def _compute_Job_count(self):
        obj = self.env['freight.operation']
        for serv in self:
            cnt = obj.search_count([
                ('main_id', '=', serv.id)])
            if cnt != 0:
                print("hii")
                serv['job_count'] = cnt
            else:
                print("hello")
                serv['job_count'] = 0

    # @api.model
    # def default_get(self, default_fields):
    #     res = super(SaleJob, self).default_get(default_fields)
    #     data = self.env['sale.order'].browse(self._context.get('active_ids', []))
    #     update = []
    #     for record in data.order_line:
    #         update.append((0, 0, {
    #             'product_id': record.product_id.id,
    #             # 'product_uom': record.product_uom.id,
    #             # 'order_id': record.order_id.id,
    #             # 'name': record.name,
    #             # 'product_qty': record.product_uom_qty,
    #             # 'price_unit': record.price_unit,
    #             # 'product_subtotal': record.price_subtotal,
    #         }))
    #     res.update({'new_order_line_ids': update,
    #                 'partner_id': data.partner_id.id, })
    #     return res
    def action_create_job(self):
        print("111111111111111111111111111111111111111111")
        self.ensure_one()
        res = self.env['freight.operation'].browse(self._context.get('main_id', []))
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
                'consignee_id': self.partner_id.id,
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


