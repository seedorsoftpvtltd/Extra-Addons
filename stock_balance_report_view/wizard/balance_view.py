from odoo import models, fields, api, _


class ReportWizard(models.TransientModel):
    _inherit = 'report.wizard.quant'

    ason_date = fields.Date('Inventory Date', default=fields.Date.today)
    company_id = fields.Many2one('res.company', string='Company', required=True, default=lambda self: self.env.company)

    def action_xlsx(self):
        """ Button function for Xlsx """
        return self.env.ref(
            'stock_balance_report_view.balance_report_xlsx').report_action(self)

    def overall_report_method(self, options):
        quant = self.env['stock.quant'].search([('company_id.id', '=', self.company_id.id),
                                                ('create_date', '<=', options.ason_date),
                                                ("on_hand", "=", True), ('product_id.x_medium.name', '=', 'Warehouse'),
                                                ('quantity', '>', 0), ('location_id.usage', '=', 'internal')],
                                               order='sche_date desc')

        if quant:
            quant_fields = quant.read(["x_loc_code", "x_war_code", "x_war_name", "x_asn", "x_ccode",
                                       "x_cname", "x_sku_code", "x_sku_name", "x_hs", "in_date",
                                       "x_grn", "x_boe", "package_id", "location_id", "x_ltype",
                                       "lot_id", "x_barcode", "x_uom", "x_currency", "quantity",
                                       "total_gw", "x_volume", "x_ex", "value_goods", "x_batchno", "x_prod",
                                       "x_exp", "x_coo", "x_stype", "x_container_no", "x_sarea",
                                       "sche_date", "putaway_zone", "x_tno", "item_boe", "total_nw"])

            for i in range(0, len(quant_fields)):
                if quant_fields[i]["in_date"]:
                    quant_fields[i]["in_date"] = quant_fields[i]["in_date"].strftime("%d-%m-%Y")
                if quant_fields[i]["x_prod"]:
                    quant_fields[i]["x_prod"] = quant_fields[i]["x_prod"].strftime("%d-%m-%Y")
                if quant_fields[i]["x_exp"]:
                    quant_fields[i]["x_exp"] = quant_fields[i]["x_exp"].strftime("%d-%m-%Y")
                if quant_fields[i]["sche_date"]:
                    quant_fields[i]["sche_date"] = quant_fields[i]["sche_date"].strftime("%d-%m-%Y")
                if quant_fields[i]["location_id"]:
                    quant_fields[i]["location_id"] = quant_fields[i]["location_id"][1]
                if quant_fields[i]["x_currency"]:
                    quant_fields[i]["x_currency"] = quant_fields[i]["x_currency"][1]
                if quant_fields[i]["x_uom"]:
                    quant_fields[i]["x_uom"] = quant_fields[i]["x_uom"][1]
                if quant_fields[i]["lot_id"]:
                    quant_fields[i]["lot_id"] = quant_fields[i]["lot_id"][1]
                if quant_fields[i]["package_id"]:
                    quant_fields[i]["package_id"] = quant_fields[i]["package_id"][1]
                if quant_fields[i]["x_ltype"]:
                    vt = []
                    for j in quant_fields[i]["x_ltype"]:
                        ltype = self.env['stock.location.storage.type'].browse(j)
                        vt.append(ltype.name)
                    result = ','.join(vt)
                    quant_fields[i]["x_ltype"] = result
                if quant_fields[i]["x_sarea"]:
                    st = []
                    for k in quant_fields[i]["x_sarea"]:
                        sarea = self.env['stock.location.tag'].browse(k)
                        st.append(sarea.name)
                    result1 = ','.join(st)
                    quant_fields[i]["x_sarea"] = result1
                if quant_fields[i]["x_stype"]:
                    quant_fields[i]["x_stype"] = quant_fields[i]["x_stype"][1]

            return quant_fields

    def report_partner(self, options):
        if options.partner_id:
            part = []
            for y in options.partner_id:
                part.append(y.name)
        quant = self.env['stock.quant'].search([('company_id.id', '=', self.company_id.id),
                                                ('create_date', '<=', options.ason_date),
                                                ('x_cname', 'in', part),
                                                ("on_hand", "=", True), ('product_id.x_medium.name', '=', 'Warehouse'),
                                                ('quantity', '>', 0), ('location_id.usage', '=', 'internal')], order='sche_date desc')
        if quant:
            quant_fields = quant.read(["x_loc_code", "x_war_code", "x_war_name", "x_asn", "x_ccode",
                                       "x_cname", "x_sku_code", "x_sku_name", "x_hs", "in_date",
                                       "x_grn", "x_boe", "package_id", "location_id", "x_ltype",
                                       "lot_id", "x_barcode", "x_uom", "x_currency", "quantity",
                                       "total_gw", "x_volume", "x_ex", "value_goods", "x_batchno", "x_prod",
                                       "x_exp", "x_coo", "x_stype", "x_container_no", "x_sarea",
                                       "sche_date", "putaway_zone", "x_tno", "item_boe", "total_nw"])

            for i in range(0, len(quant_fields)):
                if quant_fields[i]["in_date"]:
                    quant_fields[i]["in_date"] = quant_fields[i]["in_date"].strftime("%d-%m-%Y")
                if quant_fields[i]["x_prod"]:
                    quant_fields[i]["x_prod"] = quant_fields[i]["x_prod"].strftime("%d-%m-%Y")
                if quant_fields[i]["x_exp"]:
                    quant_fields[i]["x_exp"] = quant_fields[i]["x_exp"].strftime("%d-%m-%Y")
                if quant_fields[i]["sche_date"]:
                    quant_fields[i]["sche_date"] = quant_fields[i]["sche_date"].strftime("%d-%m-%Y")
                if quant_fields[i]["location_id"]:
                    quant_fields[i]["location_id"] = quant_fields[i]["location_id"][1]
                if quant_fields[i]["x_currency"]:
                    quant_fields[i]["x_currency"] = quant_fields[i]["x_currency"][1]
                if quant_fields[i]["x_uom"]:
                    quant_fields[i]["x_uom"] = quant_fields[i]["x_uom"][1]
                if quant_fields[i]["lot_id"]:
                    quant_fields[i]["lot_id"] = quant_fields[i]["lot_id"][1]
                if quant_fields[i]["package_id"]:
                    quant_fields[i]["package_id"] = quant_fields[i]["package_id"][1]
                if quant_fields[i]["x_ltype"]:
                    vt = []
                    for j in quant_fields[i]["x_ltype"]:
                        sarea = self.env['stock.location.storage.type'].browse(j)
                        vt.append(sarea.name)
                    result = ','.join(vt)
                    quant_fields[i]["x_ltype"] = result
                if quant_fields[i]["x_sarea"]:
                    st = []
                    for k in quant_fields[i]["x_sarea"]:
                        sarea = self.env['stock.location.tag'].browse(k)
                        st.append(sarea.name)
                    result1 = ','.join(st)
                    quant_fields[i]["x_sarea"] = result1
                if quant_fields[i]["x_stype"]:
                    quant_fields[i]["x_stype"] = quant_fields[i]["x_stype"][1]
            return quant_fields

    def report_product(self, options):
        if options.product_id:
            prod = []
            for y in options.product_id:
                prod.append(y.name)
        quant = self.env['stock.quant'].search([('company_id.id', '=', self.company_id.id),
                                                ('create_date', '<=', options.ason_date),
                                                ('x_sku_code', 'in', prod),
                                                ("on_hand", "=", True), ('product_id.x_medium.name', '=', 'Warehouse'),
                                                ('quantity', '>', 0), ('location_id.usage', '=', 'internal')], order='sche_date desc')

        if quant:
            quant_fields = quant.read(["x_loc_code", "x_war_code", "x_war_name", "x_asn", "x_ccode",
                                       "x_cname", "x_sku_code", "x_sku_name", "x_hs", "in_date",
                                       "x_grn", "x_boe", "package_id", "location_id", "x_ltype",
                                       "lot_id", "x_barcode", "x_uom", "x_currency", "quantity",
                                       "total_gw", "x_volume", "x_ex", "value_goods", "x_batchno", "x_prod",
                                       "x_exp", "x_coo", "x_stype", "x_container_no", "x_sarea",
                                       "sche_date", "putaway_zone", "x_tno", "item_boe", "total_nw"])

            for i in range(0, len(quant_fields)):
                if quant_fields[i]["in_date"]:
                    quant_fields[i]["in_date"] = quant_fields[i]["in_date"].strftime("%d-%m-%Y")
                if quant_fields[i]["x_prod"]:
                    quant_fields[i]["x_prod"] = quant_fields[i]["x_prod"].strftime("%d-%m-%Y")
                if quant_fields[i]["x_exp"]:
                    quant_fields[i]["x_exp"] = quant_fields[i]["x_exp"].strftime("%d-%m-%Y")
                if quant_fields[i]["sche_date"]:
                    quant_fields[i]["sche_date"] = quant_fields[i]["sche_date"].strftime("%d-%m-%Y")

                # Many2one
                if quant_fields[i]["location_id"]:
                    quant_fields[i]["location_id"] = quant_fields[i]["location_id"][1]
                if quant_fields[i]["x_currency"]:
                    quant_fields[i]["x_currency"] = quant_fields[i]["x_currency"][1]
                if quant_fields[i]["x_uom"]:
                    quant_fields[i]["x_uom"] = quant_fields[i]["x_uom"][1]
                if quant_fields[i]["lot_id"]:
                    quant_fields[i]["lot_id"] = quant_fields[i]["lot_id"][1]
                if quant_fields[i]["package_id"]:
                    quant_fields[i]["package_id"] = quant_fields[i]["package_id"][1]

                # Many2many
                if quant_fields[i]["x_ltype"]:
                    vt = []
                    for j in quant_fields[i]["x_ltype"]:
                        sarea = self.env['stock.location.storage.type'].browse(j)
                        vt.append(sarea.name)
                    result = ','.join(vt)
                    quant_fields[i]["x_ltype"] = result
                if quant_fields[i]["x_sarea"]:
                    st = []
                    for k in quant_fields[i]["x_sarea"]:
                        sarea = self.env['stock.location.tag'].browse(k)
                        st.append(sarea.name)
                    result1 = ','.join(st)
                    quant_fields[i]["x_sarea"] = result1
                if quant_fields[i]["x_stype"]:
                    quant_fields[i]["x_stype"] = quant_fields[i]["x_stype"][1]
            return quant_fields

    def report_all_filter(self, options):
        if options.product_id:
            prod = []
            for y in options.product_id:
                prod.append(y.name)

        if options.partner_id:
            part = []
            for y in options.partner_id:
                part.append(y.name)
        quant = self.env['stock.quant'].search([('company_id.id', '=', self.company_id.id),
                                                ('create_date', '<=', options.ason_date),
                                                ('x_cname', 'in', part),
                                                ('x_sku_code', 'in', prod),
                                                ("on_hand", "=", True), ('product_id.x_medium.name', '=', 'Warehouse'),
                                                ('quantity', '>', 0), ('location_id.usage', '=', 'internal')], order='sche_date desc')

        if quant:
            quant_fields = quant.read(["x_loc_code", "x_war_code", "x_war_name", "x_asn", "x_ccode",
                                       "x_cname", "x_sku_code", "x_sku_name", "x_hs", "in_date",
                                       "x_grn", "x_boe", "package_id", "location_id", "x_ltype",
                                       "lot_id", "x_barcode", "x_uom", "x_currency", "quantity",
                                       "total_gw", "x_volume", "x_ex", "value_goods", "x_batchno", "x_prod",
                                       "x_exp", "x_coo", "x_stype", "x_container_no", "x_sarea",
                                       "sche_date", "putaway_zone", "x_tno", "item_boe", "total_nw"])

            for i in range(0, len(quant_fields)):
                if quant_fields[i]["in_date"]:
                    quant_fields[i]["in_date"] = quant_fields[i]["in_date"].strftime("%d-%m-%Y")
                if quant_fields[i]["x_prod"]:
                    quant_fields[i]["x_prod"] = quant_fields[i]["x_prod"].strftime("%d-%m-%Y")
                if quant_fields[i]["x_exp"]:
                    quant_fields[i]["x_exp"] = quant_fields[i]["x_exp"].strftime("%d-%m-%Y")
                if quant_fields[i]["sche_date"]:
                    quant_fields[i]["sche_date"] = quant_fields[i]["sche_date"].strftime("%d-%m-%Y")

                if quant_fields[i]["package_id"]:
                    quant_fields[i]["package_id"] = quant_fields[i]["package_id"][1]
                if quant_fields[i]["location_id"]:
                    quant_fields[i]["location_id"] = quant_fields[i]["location_id"][1]
                if quant_fields[i]["x_currency"]:
                    quant_fields[i]["x_currency"] = quant_fields[i]["x_currency"][1]
                if quant_fields[i]["x_uom"]:
                    quant_fields[i]["x_uom"] = quant_fields[i]["x_uom"][1]
                if quant_fields[i]["lot_id"]:
                    quant_fields[i]["lot_id"] = quant_fields[i]["lot_id"][1]
                if quant_fields[i]["x_ltype"]:
                    vt = []
                    for j in quant_fields[i]["x_ltype"]:
                        sarea = self.env['stock.location.storage.type'].browse(j)
                        vt.append(sarea.name)
                    result = ','.join(vt)
                    quant_fields[i]["x_ltype"] = result
                if quant_fields[i]["x_sarea"]:
                    st = []
                    for k in quant_fields[i]["x_sarea"]:
                        sarea = self.env['stock.location.tag'].browse(k)
                        st.append(sarea.name)
                    result1 = ','.join(st)
                    quant_fields[i]["x_sarea"] = result1
                if quant_fields[i]["x_stype"]:
                    quant_fields[i]["x_stype"] = quant_fields[i]["x_stype"][1]
            return quant_fields

    def report_balance(self, options):
        if options.product_id and not options.partner_id:
            prod = []
            for y in options.product_id:
                prod.append(y.name)

            quant = self.env['stock.quant'].search([('company_id.id', '=', self.company_id.id),
                                                    ('x_sku_code', 'in', prod),
                                                    ("on_hand", "=", True), ('product_id.x_medium.name', '=', 'Warehouse'),
                                                    ('quantity', '>', 0), ('location_id.usage', '=', 'internal')], order='sche_date desc')

        elif not options.product_id and options.partner_id:
            part = []
            for y in options.partner_id:
                part.append(y.name)

            quant = self.env['stock.quant'].search([('company_id.id', '=', self.company_id.id),
                                                    ('x_cname', 'in', part)], order='sche_date desc')

        elif options.product_id and options.partner_id:
            prod = []
            for y in options.product_id:
                prod.append(y.name)

            part = []
            for y in options.partner_id:
                part.append(y.name)

            quant = self.env['stock.quant'].search([('company_id.id', '=', self.company_id.id),
                                                    ('create_date', '<=', options.ason_date),
                                                    ('x_cname', 'in', part),
                                                    ('x_sku_code', 'in', prod),
                                                    ("on_hand", "=", True), ('product_id.x_medium.name', '=', 'Warehouse'),
                                                    ('quantity', '>', 0), ('location_id.usage', '=', 'internal')], order='sche_date desc')

        if quant:
            quant_fields = quant.read(["x_loc_code", "x_war_code", "x_war_name", "x_asn", "x_ccode",
                                       "x_cname", "x_sku_code", "x_sku_name", "x_hs", "in_date",
                                       "x_grn", "x_boe", "package_id", "location_id", "x_ltype",
                                       "lot_id", "x_barcode", "x_uom", "x_currency", "quantity",
                                       "total_gw", "x_volume", "x_ex", "value_goods", "x_batchno", "x_prod",
                                       "x_exp", "x_coo", "x_stype", "x_container_no", "x_sarea",
                                       "sche_date", "putaway_zone", "x_tno", "item_boe", "total_nw"])

            for i in range(0, len(quant_fields)):
                if quant_fields[i]["in_date"]:
                    quant_fields[i]["in_date"] = quant_fields[i]["in_date"].strftime("%d-%m-%Y")
                if quant_fields[i]["x_prod"]:
                    quant_fields[i]["x_prod"] = quant_fields[i]["x_prod"].strftime("%d-%m-%Y")
                if quant_fields[i]["x_exp"]:
                    quant_fields[i]["x_exp"] = quant_fields[i]["x_exp"].strftime("%d-%m-%Y")
                if quant_fields[i]["sche_date"]:
                    quant_fields[i]["sche_date"] = quant_fields[i]["sche_date"].strftime("%d-%m-%Y")
                if quant_fields[i]["location_id"]:
                    quant_fields[i]["location_id"] = quant_fields[i]["location_id"][1]
                if quant_fields[i]["x_currency"]:
                    quant_fields[i]["x_currency"] = quant_fields[i]["x_currency"][1]
                if quant_fields[i]["x_uom"]:
                    quant_fields[i]["x_uom"] = quant_fields[i]["x_uom"][1]
                if quant_fields[i]["lot_id"]:
                    quant_fields[i]["lot_id"] = quant_fields[i]["lot_id"][1]
                if quant_fields[i]["package_id"]:
                    quant_fields[i]["package_id"] = quant_fields[i]["package_id"][1]
                if quant_fields[i]["x_ltype"]:
                    vt = []
                    for j in quant_fields[i]["x_ltype"]:
                        sarea = self.env['stock.location.storage.type'].browse(j)
                        vt.append(sarea.name)
                    result = ','.join(vt)
                    quant_fields[i]["x_ltype"] = result
                if quant_fields[i]["x_sarea"]:
                    st = []
                    for k in quant_fields[i]["x_sarea"]:
                        sarea = self.env['stock.location.tag'].browse(k)
                        st.append(sarea.name)
                    result1 = ','.join(st)
                    quant_fields[i]["x_sarea"] = result1
                if quant_fields[i]["x_stype"]:
                    quant_fields[i]["x_stype"] = quant_fields[i]["x_stype"][1]
            return quant_fields

    def get_data(self, options):
        if options.ason_date and not self.partner_id and not self.product_id:
            val = self.overall_report_method(options)
        elif options.ason_date and self.partner_id and not self.product_id:
            val = self.report_partner(options)
        elif options.ason_date and not self.partner_id and self.product_id:
            val = self.report_product(options)
        elif options.ason_date and self.partner_id and self.product_id:
            val = self.report_all_filter(options)

        elif not options.ason_date and self.partner_id and self.product_id:
            val = self.report_balance(options)
        elif not options.ason_date and not self.partner_id and self.product_id:
            val = self.report_balance(options)
        elif not options.ason_date and self.partner_id and not self.product_id:
            val = self.report_balance(options)
        else:
            val = []
        return val
