from odoo import api, models, fields, _
from odoo.exceptions import AccessError, UserError, ValidationError


class ReportWizard(models.TransientModel):
    _inherit = 'reportt.wizardd'

    start_date = fields.Date('Start Date', default=fields.Date.today)
    end_date = fields.Date('End Date', default=fields.Date.today)
    company_id = fields.Many2one('res.company', string='Company', required=True, default=lambda self: self.env.company)

    def view_stock_movement(self):
        # filtered_move_lines = self.env['stock.move.line'].search([('owner_id', '=', self.partner_id.id)])
        # related_products = filtered_move_lines.mapped('product_id')
        if self.start_date and not self.end_date:
            raise ValidationError(_("Please fill in the End Date"))
        elif not self.start_date and self.end_date:
            raise ValidationError(_("Please fill in the Start Date"))
        if self.start_date and self.end_date and not self.partner_id and not self.product_id:
            domain = [('x_trans_date', '>=', self.start_date),
                      ('x_trans_date', '<=', self.end_date), ('picking_code', 'in', ['incoming', 'outgoing']),
                      ('product_id.x_medium.name', '=', 'Warehouse'), ('company_id.id', '=', self.company_id.id),
                      ('state', '=', 'done'),
                      ]
        elif self.start_date and self.end_date and self.partner_id and not self.product_id:
            domain = [('x_trans_date', '>=', self.start_date),
                      ('x_trans_date', '<=', self.end_date), ('owner_id', '=', self.partner_id.id),
                      ('picking_code', 'in', ['incoming', 'outgoing']),
                      ('product_id.x_medium.name', '=', 'Warehouse'), ('company_id.id', '=', self.company_id.id),('state', '=', 'done'),
                      ]
        elif self.start_date and self.end_date and not self.partner_id and self.product_id:
            id = []
            for prod in self.product_id:
                id.append(prod.id)
            domain = [('x_trans_date', '>=', self.start_date),
                      ('x_trans_date', '<=', self.end_date),
                      ('picking_code', 'in', ['incoming', 'outgoing']),
                      ('product_id.x_medium.name', '=', 'Warehouse'), ('product_id', 'in', id),('state', '=', 'done'),
                      ('company_id.id', '=', self.company_id.id),
                      ]
        elif self.start_date and self.end_date and self.partner_id and self.product_id:
            id = []
            for prod in self.product_id:
                id.append(prod.id)
            domain = [('x_trans_date', '>=', self.start_date),
                      ('x_trans_date', '<=', self.end_date),
                      ('owner_id', '=', self.partner_id.id),
                      ('picking_code', 'in', ['incoming', 'outgoing']),
                      ('product_id.x_medium.name', '=', 'Warehouse'), ('product_id', 'in', id),('state', '=', 'done'),
                      ('company_id.id', '=', self.company_id.id),
                      ]
        elif not self.start_date and not self.end_date and not self.partner_id and self.product_id:
            id = []
            for prod in self.product_id:
                id.append(prod.id)
            domain = [
                ('picking_code', 'in', ['incoming', 'outgoing']),
                ('product_id.x_medium.name', '=', 'Warehouse'), ('product_id', 'in', id), ('company_id.id', '=', self.company_id.id),('state', '=', 'done'),
            ]
        elif not self.start_date and not self.end_date and self.partner_id and not self.product_id:
            domain = [('owner_id', '=', self.partner_id.id),
                      ('picking_code', 'in', ['incoming', 'outgoing']),
                      ('product_id.x_medium.name', '=', 'Warehouse'), ('company_id.id', '=', self.company_id.id),('state', '=', 'done'),
                      ]
        elif not self.start_date and not self.end_date and self.partner_id and self.product_id:
            id = []
            for prod in self.product_id:
                id.append(prod.id)
            domain = [
                ('owner_id', '=', self.partner_id.id),
                ('picking_code', 'in', ['incoming', 'outgoing']),
                ('product_id.x_medium.name', '=', 'Warehouse'), ('product_id', 'in', id),
                ('company_id.id', '=', self.company_id.id),('state', '=', 'done'),
            ]
        else:
            domain = [
                ('picking_code', 'in', ['incoming', 'outgoing']),
                ('product_id.x_medium.name', '=', 'Warehouse'),
                ('company_id.id', '=', self.company_id.id),('state', '=', 'done'),
            ]

        return {
            'type': 'ir.actions.act_window',
            'name': _('Stock Movement Report'),
            'res_model': 'stock.move.line',
            'view_mode': 'tree',
            'limit': 80,
            'search_view_id': self.env.ref('stock.view_move_line_tree').id,
            'domain': domain,
        }

    def action_xlsx(self):
        print(self.start_date, self.end_date)
        if self.start_date and not self.end_date:
            raise ValidationError(_("Please fill in the End Date"))
        elif not self.start_date and self.end_date:
            raise ValidationError(_("Please fill in the Start Date"))
        else:
            return self.env.ref('stock_movement_report_view.movement_report_xlsx').report_action(self)

    def overall_report_method(self):
        move_line = self.env['stock.move.line'].search([('company_id.id', '=', self.company_id.id),
                                                        ('picking_code', 'in', ['incoming', 'outgoing']),
                                                        ('product_id.x_medium.name', '=', 'Warehouse'),('state', '=', 'done'),
                                                        ], order='x_trans_date desc')

        if move_line:
            values = move_line.read(["x_war", "x_ccode", "owner_id", "product_id", "x_name", "barcode", "x_hs",
                                     "x_cntr_code", "x_tno", "container_no", "x_trans_type", "origin", "x_trans_date",
                                     "x_trans_no", "loc_code", "x_uom", "x_qty", "x_vol", "total_gw", "x_namee",
                                     "pallet",
                                     "x_ref_date", "x_ref_no", "x_bill", "lot_id",
                                     "production_date",
                                     "expiry_date", "x_coo", "batchno", "item_boe", "total_nw", "picking_code"])
            for i in range(0, len(values)):
                if values[i]["x_bill"]:
                    if values[i]["picking_code"] == "outgoing":
                        values[i]["x_bill"] = values[i]["x_bill"]
                    else:
                        values[i]["x_bill"] = ""

                if values[i]["x_ref_no"]:
                    if values[i]["picking_code"] == "outgoing":
                        values[i]["x_ref_no"] = values[i]["x_ref_no"]
                    else:
                        values[i]["x_ref_no"] = ""

                if values[i]["x_ref_date"]:
                    if values[i]["picking_code"] == "outgoing":
                        values[i]["x_ref_date"] = values[i]["x_ref_date"]
                    else:
                        values[i]["x_ref_date"] = ""

                if values[i]["product_id"]:
                    values[i]["product_id"] = values[i]["product_id"][1]
                if values[i]["owner_id"]:
                    values[i]["owner_id"] = values[i]["owner_id"][1]
                if values[i]["loc_code"]:
                    values[i]["loc_code"] = values[i]["loc_code"][1]
                if values[i]["x_uom"]:
                    values[i]["x_uom"] = values[i]["x_uom"][1]
                if values[i]["pallet"]:
                    values[i]["pallet"] = values[i]["pallet"][1]
                if values[i]["lot_id"]:
                    values[i]["lot_id"] = values[i]["lot_id"][1]
                if values[i]["x_coo"]:
                    values[i]["x_coo"] = values[i]["x_coo"][1]
                if values[i]["x_trans_date"]:
                    values[i]["x_trans_date"] = values[i]["x_trans_date"].strftime("%d-%m-%Y")
                if values[i]["x_ref_date"]:
                    values[i]["x_ref_date"] = values[i]["x_ref_date"].strftime("%d-%m-%Y")
                if values[i]["production_date"]:
                    values[i]["production_date"] = values[i]["production_date"].strftime("%d-%m-%Y")
                if values[i]["expiry_date"]:
                    values[i]["expiry_date"] = values[i]["expiry_date"].strftime("%d-%m-%Y")
        else:
            values = []
        return values

    def report_date_filter(self, options):
        move_line = self.env['stock.move.line'].search([('x_trans_date', '>=', options.start_date),
                                                        ('x_trans_date', '<=', options.end_date),
                                                        ('company_id.id', '=', self.company_id.id),
                                                        ('picking_code', 'in', ['incoming', 'outgoing']),
                                                        ('product_id.x_medium.name', '=', 'Warehouse'),('state', '=', 'done'),
                                                        ], order='x_trans_date desc')
        if move_line:
            values = move_line.read(["x_war", "x_ccode", "owner_id", "product_id", "x_name", "barcode", "x_hs",
                                     "x_cntr_code", "x_tno", "container_no", "x_trans_type", "origin", "x_trans_date",
                                     "x_trans_no", "loc_code", "x_uom", "x_qty", "x_vol", "total_gw", "x_namee",
                                     "pallet",
                                     "x_ref_date", "x_ref_no", "x_bill", "lot_id",
                                     "production_date",
                                     "expiry_date", "x_coo", "batchno", "item_boe", "total_nw"])
            for i in range(0, len(values)):
                if values[i]["product_id"]:
                    values[i]["product_id"] = values[i]["product_id"][1]
                if values[i]["owner_id"]:
                    values[i]["owner_id"] = values[i]["owner_id"][1]
                if values[i]["loc_code"]:
                    values[i]["loc_code"] = values[i]["loc_code"][1]
                if values[i]["x_uom"]:
                    values[i]["x_uom"] = values[i]["x_uom"][1]
                if values[i]["pallet"]:
                    values[i]["pallet"] = values[i]["pallet"][1]
                if values[i]["lot_id"]:
                    values[i]["lot_id"] = values[i]["lot_id"][1]
                if values[i]["x_coo"]:
                    values[i]["x_coo"] = values[i]["x_coo"][1]
                if values[i]["x_trans_date"]:
                    values[i]["x_trans_date"] = values[i]["x_trans_date"].strftime("%d-%m-%Y")
                if values[i]["x_ref_date"]:
                    values[i]["x_ref_date"] = values[i]["x_ref_date"].strftime("%d-%m-%Y")
                if values[i]["production_date"]:
                    values[i]["production_date"] = values[i]["production_date"].strftime("%d-%m-%Y")
                if values[i]["expiry_date"]:
                    values[i]["expiry_date"] = values[i]["expiry_date"].strftime("%d-%m-%Y")
        else:
            values = []
        return values

    def report_customer_filter(self, options):
        move_line = self.env['stock.move.line'].search([('x_trans_date', '>=', options.start_date),
                                                        ('x_trans_date', '<=', options.end_date),
                                                        ('owner_id', '=', self.partner_id.id),
                                                        ('company_id.id', '=', self.company_id.id),
                                                        ('picking_code', 'in', ['incoming', 'outgoing']),
                                                        ('product_id.x_medium.name', '=', 'Warehouse'),('state', '=', 'done'),
                                                        ], order='x_trans_date desc')
        if move_line:
            values = move_line.read(["x_war", "x_ccode", "owner_id", "product_id", "x_name", "barcode", "x_hs",
                                     "x_cntr_code", "x_tno", "container_no", "x_trans_type", "origin", "x_trans_date",
                                     "x_trans_no", "loc_code", "x_uom", "x_qty", "x_vol", "total_gw", "x_namee",
                                     "pallet",
                                     "x_ref_date", "x_ref_no", "x_bill", "lot_id",
                                     "production_date",
                                     "expiry_date", "x_coo", "batchno", "item_boe", "total_nw"])
            for i in range(0, len(values)):
                if values[i]["product_id"]:
                    values[i]["product_id"] = values[i]["product_id"][1]
                if values[i]["owner_id"]:
                    values[i]["owner_id"] = values[i]["owner_id"][1]
                if values[i]["loc_code"]:
                    values[i]["loc_code"] = values[i]["loc_code"][1]
                if values[i]["x_uom"]:
                    values[i]["x_uom"] = values[i]["x_uom"][1]
                if values[i]["pallet"]:
                    values[i]["pallet"] = values[i]["pallet"][1]
                if values[i]["lot_id"]:
                    values[i]["lot_id"] = values[i]["lot_id"][1]
                if values[i]["x_coo"]:
                    values[i]["x_coo"] = values[i]["x_coo"][1]
                if values[i]["x_trans_date"]:
                    values[i]["x_trans_date"] = values[i]["x_trans_date"].strftime("%d-%m-%Y")
                if values[i]["x_ref_date"]:
                    values[i]["x_ref_date"] = values[i]["x_ref_date"].strftime("%d-%m-%Y")
                if values[i]["production_date"]:
                    values[i]["production_date"] = values[i]["production_date"].strftime("%d-%m-%Y")
                if values[i]["expiry_date"]:
                    values[i]["expiry_date"] = values[i]["expiry_date"].strftime("%d-%m-%Y")
        else:
            values = []
        return values

    def report_product_filter(self, options):
        move_line = self.env['stock.move.line'].search([('x_trans_date', '>=', options.start_date),
                                                        ('x_trans_date', '<=', options.end_date),
                                                        ('product_id.id', 'in', options.product_id.ids),
                                                        ('company_id.id', '=', self.company_id.id),
                                                        ('picking_code', 'in', ['incoming', 'outgoing']),
                                                        ('product_id.x_medium.name', '=', 'Warehouse'),('state', '=', 'done'),
                                                        ], order='x_trans_date desc')
        if move_line:
            values = move_line.read(["x_war", "x_ccode", "owner_id", "product_id", "x_name", "barcode", "x_hs",
                                     "x_cntr_code", "x_tno", "container_no", "x_trans_type", "origin", "x_trans_date",
                                     "x_trans_no", "loc_code", "x_uom", "x_qty", "x_vol", "total_gw", "x_namee",
                                     "pallet",
                                     "x_ref_date", "x_ref_no", "x_bill", "lot_id",
                                     "production_date",
                                     "expiry_date", "x_coo", "batchno", "item_boe", "total_nw"])
            for i in range(0, len(values)):
                if values[i]["product_id"]:
                    values[i]["product_id"] = values[i]["product_id"][1]
                if values[i]["owner_id"]:
                    values[i]["owner_id"] = values[i]["owner_id"][1]
                if values[i]["loc_code"]:
                    values[i]["loc_code"] = values[i]["loc_code"][1]
                if values[i]["x_uom"]:
                    values[i]["x_uom"] = values[i]["x_uom"][1]
                if values[i]["pallet"]:
                    values[i]["pallet"] = values[i]["pallet"][1]
                if values[i]["lot_id"]:
                    values[i]["lot_id"] = values[i]["lot_id"][1]
                if values[i]["x_coo"]:
                    values[i]["x_coo"] = values[i]["x_coo"][1]
                if values[i]["x_trans_date"]:
                    values[i]["x_trans_date"] = values[i]["x_trans_date"].strftime("%d-%m-%Y")
                if values[i]["x_ref_date"]:
                    values[i]["x_ref_date"] = values[i]["x_ref_date"].strftime("%d-%m-%Y")
                if values[i]["production_date"]:
                    values[i]["production_date"] = values[i]["production_date"].strftime("%d-%m-%Y")
                if values[i]["expiry_date"]:
                    values[i]["expiry_date"] = values[i]["expiry_date"].strftime("%d-%m-%Y")
        else:
            values = []
        return values

    def report_all(self, options):
        move_line = self.env['stock.move.line'].search([('x_trans_date', '>=', options.start_date),
                                                        ('x_trans_date', '<=', options.end_date),
                                                        ('owner_id', '=', self.partner_id.id),
                                                        ('product_id.id', 'in', options.product_id.ids),
                                                        ('company_id.id', '=', self.company_id.id),
                                                        ('picking_code', 'in', ['incoming', 'outgoing']),
                                                        ('product_id.x_medium.name', '=', 'Warehouse'),('state', '=', 'done'),
                                                        ], order='x_trans_date desc')
        if move_line:
            values = move_line.read(["x_war", "x_ccode", "owner_id", "product_id", "x_name", "barcode", "x_hs",
                                     "x_cntr_code", "x_tno", "container_no", "x_trans_type", "origin", "x_trans_date",
                                     "x_trans_no", "loc_code", "x_uom", "x_qty", "x_vol", "total_gw", "x_namee",
                                     "pallet",
                                     "x_ref_date", "x_ref_no", "x_bill", "lot_id",
                                     "production_date",
                                     "expiry_date", "x_coo", "batchno", "item_boe", "total_nw"])
            for i in range(0, len(values)):
                if values[i]["product_id"]:
                    values[i]["product_id"] = values[i]["product_id"][1]
                if values[i]["owner_id"]:
                    values[i]["owner_id"] = values[i]["owner_id"][1]
                if values[i]["loc_code"]:
                    values[i]["loc_code"] = values[i]["loc_code"][1]
                if values[i]["x_uom"]:
                    values[i]["x_uom"] = values[i]["x_uom"][1]
                if values[i]["pallet"]:
                    values[i]["pallet"] = values[i]["pallet"][1]
                if values[i]["lot_id"]:
                    values[i]["lot_id"] = values[i]["lot_id"][1]
                if values[i]["x_coo"]:
                    values[i]["x_coo"] = values[i]["x_coo"][1]
                if values[i]["x_trans_date"]:
                    values[i]["x_trans_date"] = values[i]["x_trans_date"].strftime("%d-%m-%Y")
                if values[i]["x_ref_date"]:
                    values[i]["x_ref_date"] = values[i]["x_ref_date"].strftime("%d-%m-%Y")
                if values[i]["production_date"]:
                    values[i]["production_date"] = values[i]["production_date"].strftime("%d-%m-%Y")
                if values[i]["expiry_date"]:
                    values[i]["expiry_date"] = values[i]["expiry_date"].strftime("%d-%m-%Y")
        else:
            values = []
        return values

    def report_move(self, options):
        if options.partner_id and not options.product_id:
            move_line = self.env['stock.move.line'].search([('owner_id', '=', self.partner_id.id),
                                                            ('company_id.id', '=', self.company_id.id),
                                                            ('picking_code', 'in', ['incoming', 'outgoing']),
                                                            ('product_id.x_medium.name', '=', 'Warehouse'),('state', '=', 'done'),
                                                            ], order='x_trans_date desc')
        elif not options.partner_id and options.product_id:
            move_line = self.env['stock.move.line'].search([('product_id.id', 'in', options.product_id.ids),
                                                            ('company_id.id', '=', self.company_id.id),
                                                            ('picking_code', 'in', ['incoming', 'outgoing']),
                                                            ('product_id.x_medium.name', '=', 'Warehouse'),('state', '=', 'done'),
                                                            ], order='x_trans_date desc')
        elif options.partner_id and options.product_id:
            move_line = self.env['stock.move.line'].search([('product_id.id', 'in', options.product_id.ids),
                                                            ('owner_id', '=', self.partner_id.id),
                                                            ('company_id.id', '=', self.company_id.id),
                                                            ('picking_code', 'in', ['incoming', 'outgoing']),
                                                            ('product_id.x_medium.name', '=', 'Warehouse'),('state', '=', 'done'),
                                                            ], order='x_trans_date desc')
        if move_line:
            values = move_line.read(["x_war", "x_ccode", "owner_id", "product_id", "x_name", "barcode", "x_hs",
                                     "x_cntr_code", "x_tno", "container_no", "x_trans_type", "origin", "x_trans_date",
                                     "x_trans_no", "loc_code", "x_uom", "x_qty", "x_vol", "total_gw", "x_namee",
                                     "pallet",
                                     "x_ref_date", "x_ref_no", "x_bill", "lot_id",
                                     "production_date",
                                     "expiry_date", "x_coo", "batchno", "item_boe", "total_nw"])
            for i in range(0, len(values)):
                if values[i]["product_id"]:
                    values[i]["product_id"] = values[i]["product_id"][1]
                if values[i]["owner_id"]:
                    values[i]["owner_id"] = values[i]["owner_id"][1]
                if values[i]["loc_code"]:
                    values[i]["loc_code"] = values[i]["loc_code"][1]
                if values[i]["x_uom"]:
                    values[i]["x_uom"] = values[i]["x_uom"][1]
                if values[i]["pallet"]:
                    values[i]["pallet"] = values[i]["pallet"][1]
                if values[i]["lot_id"]:
                    values[i]["lot_id"] = values[i]["lot_id"][1]
                if values[i]["x_coo"]:
                    values[i]["x_coo"] = values[i]["x_coo"][1]
                if values[i]["x_trans_date"]:
                    values[i]["x_trans_date"] = values[i]["x_trans_date"].strftime("%d-%m-%Y")
                if values[i]["x_ref_date"]:
                    values[i]["x_ref_date"] = values[i]["x_ref_date"].strftime("%d-%m-%Y")
                if values[i]["production_date"]:
                    values[i]["production_date"] = values[i]["production_date"].strftime("%d-%m-%Y")
                if values[i]["expiry_date"]:
                    values[i]["expiry_date"] = values[i]["expiry_date"].strftime("%d-%m-%Y")
        else:
            values = []
        return values

    def get_data(self, options):
        if options.overall_report:
            val = self.overall_report_method()
        elif options.start_date and options.end_date and not self.partner_id and not self.product_id:
            val = self.report_date_filter(options)
        elif options.start_date and options.end_date and self.partner_id and not self.product_id:
            val = self.report_customer_filter(options)
        elif options.start_date and options.end_date and not self.partner_id and self.product_id:
            val = self.report_product_filter(options)
        elif options.start_date and options.end_date and self.partner_id and self.product_id:
            val = self.report_all(options)

        # not start date and end date
        elif not options.start_date and not options.end_date and self.partner_id and self.product_id:
            val = self.report_move(options)
        elif not options.start_date and not options.end_date and not self.partner_id and self.product_id:
            val = self.report_move(options)
        elif not options.start_date and not options.end_date and self.partner_id and not self.product_id:
            val = self.report_move(options)
        else:
            val = []
        return val
