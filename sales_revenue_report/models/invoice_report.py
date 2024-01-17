from odoo import api, fields, models

class Freightin(models.Model):
    _inherit = 'freight.operation'
    x_rpd_department = fields.Char(compute='_full_department_name', string='Department')

    x_rpd_sale= fields.Float(compute='_sale_calculation', string="Sale",digits=(12,3))
    x_rpd_cost= fields.Float(compute='_cost_calculation', string="Cost",digits=(12,3))
    x_rpd_gp= fields.Float(compute='_gp_calculation', string="GP", digits=(12,3))
    x_service_type=fields.Char(compute='_service_type_fu', string="Service Type")
    #x_bayan_no=fields.Char(string='bayan no')

    # x_rpd_service_type=fields.Selection(compute='_service_type', string='Service type')
    # x_rpd_invoice_user_id = fields.Many2one('account.move', related="invoice_id.invoice_user_id")
    # x_rpd_partner_id=fields.Many2one('account.move', related="invoice_id.partner_id")


    def _full_department_name(self):
        for rec in self:
            name = rec.transport + " " + rec.direction
            print(name)
            rec.x_rpd_department = name

    def _service_type_fu(self):
        for rec in self:
            if rec.transport == 'ocean' or rec.transport == 'air':
                value = rec.ocean_shipping
                rec['x_service_type']= value
            else:
                value = rec.land_shipping
                rec ['x_service_type'] = value


    def _sale_calculation(self):
        amountcash = self.env['operation.service'].read_group([('operation_id','!=',False)], fields=['x_sale_total', 'operation_id'], groupby=['operation_id'])
        print('.........>>>>>>>', amountcash)
        if not amountcash:
            pass
        else:
            for records in amountcash:
                print('>>>>>>>>>>>>>>>>>>>',records)
                payrec = records.get('operation_id')[0]
                invoicerec = self.browse(payrec)
                invoicerec.x_rpd_sale = records['x_sale_total']
                self -= invoicerec
            self.x_rpd_sale = 0


    def _cost_calculation(self):
        amountcash = self.env['operation.service'].read_group([('operation_id','!=',False)], fields=['x_cost_total', 'operation_id'], groupby=['operation_id'])
        print('.........>>>>>>>', amountcash)
        if not amountcash:
            pass
        else:
            for records in amountcash:
                payrec = records.get('operation_id')[0]
                invoicerec = self.browse(payrec)
                invoicerec.x_rpd_cost = records['x_cost_total']
                self -= invoicerec
            self.x_rpd_sale = 0


    def _gp_calculation(self):
        for rec in self:
            print('>>>>>>>>>>>>>>',rec.x_rpd_sale)
            value = rec.x_rpd_sale - rec.x_rpd_cost
            print('>>>>>>>>>>>>>>>',value)
            rec.x_rpd_gp = value



class accounting(models.Model):
    _inherit = 'account.move'
    #sales person revenue report
    x_rpd_department = fields.Char(string="Department", related='operation_id.x_rpd_department')
    x_rpd_job_date=fields.Datetime(String="Job date" , related='operation_id.order_date')

    #shipment update report
    x_rpd_date=fields.Date(string="ETD" , related='operation_id.x_date')
    x_rpd_pod=fields.Many2one(string="POD",related='operation_id.discharg_port_id')
    x_rpd_pol=fields.Many2one(string="POL", related='operation_id.loading_port_id')
    x_rpd_bayan=fields.Char(string="Bayan No", related='operation_id.x_bayan_no')
    x_rpd_hbl = fields.Char(string="HAWB HBL", related='operation_id.x_hbl_no')
    x_rpd_mbl = fields.Char(string="MAWB MBL", related='operation_id.x_mbl_no')
    x_rpd_clientref=fields.Char(string="Client LPO No",related='operation_id.x_clientrefno')
    x_rpd_eta = fields.Date(string="ETA", related='operation_id.x_eta')
    x_rpd_quotation_no = fields.Char(string="SLS Quotation No", related='operation_id.main_id.name')
    x_rpd_refno = fields.Char(string="Reference No", related='operation_id.main_id.client_order_ref')
    x_rpd_mot= fields.Selection(string="Mode of Transpotation", related='operation_id.transport')
    x_rpd_land_type = fields.Selection(string="Service Type", related='operation_id.land_shipping')
    x_rpd_ocean_type = fields.Selection(string="Service Type", related='operation_id.ocean_shipping')
    x_rpd_sale_total=fields.Float(string="Sale Total" , related='operation_id.x_rpd_sale', digits=(12,3))
    x_rpd_cost_total = fields.Float(string="Cost Total", related='operation_id.x_rpd_cost', digits=(12,3))
    x_rpd_gp_total = fields.Float(string="GP Total", related='operation_id.x_rpd_gp', digits=(12,3))
    x_rpd_service_type= fields.Char(string="Service Type",related='operation_id.x_service_type')
