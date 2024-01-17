from dateutil import parser
from odoo import api, models, fields, _
from datetime import datetime, date, timedelta
from odoo.exceptions import AccessError, UserError, ValidationError


class Warehouseinv(models.Model):
    _inherit = 'warehouse.order'

    inv_meth = fields.Selection(string="Invoice Method",
                                selection=[('cbm', 'CBM'), ('pallet', 'Pallet'), ('weight', 'Weight'),
                                           ('carton_units', 'Carton/Units'), ('square', 'Square Units')])
    agreement_id = fields.Many2one('agreement', string="Agreement", compute='_agreement')
    storage_type = fields.Selection(string="Storage Type",
                                    selection=[('hazardous', 'Hazardous Storage'),
                                               ('non_hazardous', 'Non  Hazardous Storage')])
    x_eta = fields.Datetime(string="ETA")
    x_vol = fields.Float(string="Volume")
    x_wt = fields.Float(string="Weight")
    container = fields.Many2one('freight.container', string="Container ID")
    container_qty = fields.Float(sttring="No of Containers")
    container_no = fields.Char(string="Container No")

    def _agreement(self):
        for rec in self:
            agree = self.env['agreement'].search([('partner_id', '=', rec.partner_id.id)])
            rec['agreement_id'] = agree.id
            charge_type = ''
            # for temp in agree.charge_lines:
            #     print('temp.product_id', temp.product_id)
            #     if temp.charge_type == 'storage':
            #         charge_type = temp.charge_unit_type
            # rec['inv_meth'] = charge_type
            # print(rec.inv_meth, 'inv meth...................')


class accmoveline(models.Model):
    _inherit = 'account.move.line'

    x_cbm = fields.Float(string="CBM")
    x_weight = fields.Float(string="Weight")
    uom_type = fields.Selection(string="Storage Type",
                                selection=[('weight', 'Weight'),
                                           ('cbm', 'Cbm')], default='cbm')

    # @api.onchange('uom_type')
    # def _onchange_inv(self):
    #     if self.uom_type == 'cbm':
    #         self['quantity'] = self.x_cbm * self.quantity
    #     if self.uom_type == 'weight':
    #         self['quantity'] = (self.x_weight / 167) * self.quantity


#    start_date = fields.Datetime('Start Dte')
#    end_date = fields.Datetime('End Dte')


class StockpickingInhINV(models.Model):
    _inherit = 'stock.picking'

    quantt = fields.Float(string='Quant', compute='_quantt_calculate')
    storage_type = fields.Selection(string="Storage Type",
                                    selection=[('hazardous', 'Harardous Storage'),
                                               ('non_hazardous', 'Non  Harardous Storage')],
                                    related='warehouse_id.storage_type')
    x_eta = fields.Datetime('ETA', related='warehouse_id.x_eta')
    container = fields.Many2one('freight.container', string="Container ID")
    container_qty = fields.Float(sttring="No of Containers")
    container_no = fields.Char(string="Container No")

    # def _storagetype(self):
    #     for rec in self:
    #         if rec.warehouse_id:
    #             rec['storage_type'] = rec.warehouse_id.storage_type

    def _quantt_calculate(self):
        for record in self:
            quantt_tot = 0
            qty = 0
            # for rec in record.move_ids_without_package:
            #     if rec.inv_meth == 'cbm':
            #         print('cbm')
            #         quantt_tot += float(rec.x_volume)
            #         # rec['quantt'] = quantt_tot
            #     if rec.inv_meth == 'pallet':
            #         print('pallet')
            #         quantt_tot = self.count
            #         # rec['quantt'] = self.count
            #     if rec.inv_meth == 'carton_units':
            #         print('carton')
            #         quantt_tot += float(rec.quantity_done)
            #         # rec['quantt'] = quantt_tot
            #     if rec.inv_meth == 'weight':
            #         print('weight')
            #         quantt_tot += float(rec.x_weight)
            #         # rec['quantt'] = quantt_tot
            #     if rec.inv_meth == 'square':
            #         print('square')
            #         quantt_tot += float(rec.x_length * rec.x_breadth)
            #         # rec['quantt'] = quantt_tot
            #     if not rec.inv_meth:
            #         quantt_tot += float(rec.noofdays)
            #         # rec['quantt'] = quantt_tot
            #         print(quantt_tot)
            record['quantt'] = quantt_tot

        #### OUT ####

    #### CFS INV #####
    def create_cfsinvoice(self):
        for picking_id in self:
            current_user = self.env.uid
            if picking_id.picking_type_id.code != 'internal':
                customer_journal_id = picking_id.env['ir.config_parameter'].sudo().get_param(
                    'stock_move_invoice.customer_journal_id') or False
                if not customer_journal_id:
                    raise UserError(_("Please configure the journal from settings"))
                invoice_line_list = []
                agreement_id = self.env['agreement'].search([('type', '=', 'cfs')])
                # now = datetime.today()
                now = picking_id.scheduled_date
                stoarge_type = picking_id.warehouse_id.storage_type
                eta = picking_id.warehouse_id.x_eta
                if eta == False:
                    raise UserError(_("Please make sure ETA in sub job"))
                dur = abs((eta - now).days)
                print(dur, 'duration', eta, 'eta')
                # raise UserError(_(dur))

                for temp in agreement_id.charge_lines_new:
                    if temp.charge_type == 'fixed' and temp.charge_unit_type == 'cbm' and temp.storage_type == stoarge_type:
                        if picking_id.warehouse_id.x_wt / 1000 <= picking_id.warehouse_id.x_vol:
                            meass = picking_id.warehouse_id.x_vol
                            if meass <= 1:
                                meas = 1
                            else:
                                meas = meass
                            uom = 'cbm'
                            print(uom, 'uom', meas, 'meas')
                        else:
                            meass = picking_id.warehouse_id.x_wt / 1000
                            if meass <= 1:
                                meas = 1
                            else:
                                meas = meass
                            uom = 'weight'
                            print(uom, 'uom', meas, 'meas')

                        temp_line_values = {
                            'product_id': temp.product_id and temp.product_id.id or False,
                            'name': temp.product_id.name or '',
                            'price_unit': temp.list_price or 0.00,
                            'quantity': meas,
                            'currency_id': temp.currency_id.id,
                            # 'x_cbm': picking_id.warehouse_id.x_vol,
                            # 'x_weight': picking_id.warehouse_id.x_wt,
                            'account_id': temp.product_id.property_account_income_id.id if temp.product_id.property_account_income_id
                             else temp.product_id.categ_id.property_account_income_categ_id.id,
                            'tax_ids': [(6, 0, temp.product_id.taxes_id.ids)],
                            # 'start_date': move_ids_without_package.start_date,
                            # 'end_date': move_ids_without_package.end_date,

                        }
                        invoice_line_list.append((0, 0, temp_line_values))
                for temp in agreement_id.charge_lines_new:
                    if temp.charge_type == 'fixed' and temp.charge_unit_type == 'cbm' and temp.storage_type == False:
                        if picking_id.warehouse_id.x_wt / 1000 <= picking_id.warehouse_id.x_vol:
                            meass = picking_id.warehouse_id.x_vol
                            if meass <= 1:
                                meas = 1
                            else:
                                meas = meass
                            uom = 'cbm'
                            print(uom, 'uom', meas, 'meas')
                        else:
                            meass = picking_id.warehouse_id.x_wt / 1000
                            if meass <= 1:
                                meas = 1
                            else:
                                meas = meass
                            uom = 'weight'
                            print(uom, 'uom', meas, 'meas')
                        temp_line_values = {
                            'product_id': temp.product_id and temp.product_id.id or False,
                            'name': temp.product_id.name or '',
                            'price_unit': temp.list_price or 0.00,
                            'quantity': meas,
                            'currency_id': temp.currency_id.id,
                            # 'x_cbm': picking_id.warehouse_id.x_vol,
                            # 'x_weight': picking_id.warehouse_id.x_wt,
                            'account_id': temp.product_id.property_account_income_id.id if temp.product_id.property_account_income_id
                             else temp.product_id.categ_id.property_account_income_categ_id.id,
                            'tax_ids': [(6, 0, temp.product_id.taxes_id.ids)],
                            # 'start_date': move_ids_without_package.start_date,
                            # 'end_date': move_ids_without_package.end_date,

                        }
                        invoice_line_list.append((0, 0, temp_line_values))
                for temp in agreement_id.charge_lines_new:
                    if temp.charge_type == 'fixed' and temp.charge_unit_type == 'shipment' and temp.storage_type == stoarge_type:
                        temp_line_values = {
                            'product_id': temp.product_id and temp.product_id.id or False,
                            'name': temp.product_id.name or '',
                            'price_unit': temp.list_price or 0.00,
                            'quantity': 1,
                            'currency_id': temp.currency_id.id,
                            'account_id': temp.product_id.property_account_income_id.id if temp.product_id.property_account_income_id
                            else temp.product_id.categ_id.property_account_income_categ_id.id,
                            'tax_ids': [(6, 0, temp.product_id.taxes_id.ids)],
                            # 'start_date': move_ids_without_package.start_date,
                            # 'end_date': move_ids_without_package.end_date,

                        }
                        invoice_line_list.append((0, 0, temp_line_values))
                for temp in agreement_id.charge_lines_new:
                    if temp.charge_type == 'fixed' and temp.charge_unit_type == 'shipment' and temp.storage_type == False:
                        temp_line_values = {
                            'product_id': temp.product_id and temp.product_id.id or False,
                            'name': temp.product_id.name or '',
                            'price_unit': temp.list_price or 0.00,
                            'quantity': 1,
                            'currency_id': temp.currency_id.id,
                            'account_id': temp.product_id.property_account_income_id.id if temp.product_id.property_account_income_id
                            else temp.product_id.categ_id.property_account_income_categ_id.id,
                            'tax_ids': [(6, 0, temp.product_id.taxes_id.ids)],
                            # 'start_date': move_ids_without_package.start_date,
                            # 'end_date': move_ids_without_package.end_date,

                        }
                        invoice_line_list.append((0, 0, temp_line_values))
                for temp in agreement_id.charge_lines_new:
                    print(dur, '5555555555555', temp.fromm)
                    if picking_id.warehouse_id.x_wt / 1000 <= picking_id.warehouse_id.x_vol :
                        meass = picking_id.warehouse_id.x_vol
                        if meass <= 1:
                            meas = 1
                        else:
                            meas = meass
                        uom = 'cbm'
                        print(uom, 'uom', meas, 'meas')
                    else:
                        meass = picking_id.warehouse_id.x_wt / 1000
                        if meass <= 1:
                            meas = 1
                        else:
                            meas = meass
                        uom = 'weight'
                        print(uom, 'uom', meas, 'meas')
                    if temp.charge_type == 'storage' and temp.storage_type == stoarge_type:
                        print(dur, 'storageeeeeeeeee', temp.fromm)
                        if int(dur) >= temp.fromm:
                            if int(dur) >= temp.to and temp.to != False:
                                print('startttttttttttttttttttttttttt',abs(temp.to - temp.fromm),'-----',  meas, temp.to, temp.fromm, '-----', meas * (abs(temp.to - temp.fromm) +1))
                                # raise UserError(_(meas))
                                temp_line_values = {
                                    'product_id': temp.product_id and temp.product_id.id or False,
                                    'name': temp.product_id.name or '',
                                    'price_unit': temp.list_price or 0.00,
                                    'quantity': meas * (abs(temp.to - temp.fromm) +1),
                                    'currency_id': temp.currency_id.id,
                                    'x_cbm': picking_id.warehouse_id.x_vol,
                                    'x_weight': picking_id.warehouse_id.x_wt / 1000,
                                    'uom_type': uom,
                                    'account_id': temp.product_id.property_account_income_id.id if temp.product_id.property_account_income_id
                                    else temp.product_id.categ_id.property_account_income_categ_id.id,
                                    'tax_ids': [(6, 0, temp.product_id.taxes_id.ids)],
                                    # 'start_date': move_ids_without_package.start_date,
                                    # 'end_date': move_ids_without_package.end_date,

                                }
                                invoice_line_list.append((0, 0, temp_line_values))
                            else:
                                print('startttttttttttttttttttttttttt=======================================', abs(dur - temp.fromm),'-----',  meas, temp.to, temp.fromm, '-----', meas * (abs(dur - temp.fromm) +1))
                                # raise UserError(_(meas))

                                temp_line_values = {
                                    'product_id': temp.product_id and temp.product_id.id or False,
                                    'name': temp.product_id.name or '',
                                    'price_unit': temp.list_price or 0.00,
                                    'quantity': meas * (abs(dur - temp.fromm) + 1),
                                    'currency_id': temp.currency_id.id,
                                    'x_cbm': picking_id.warehouse_id.x_vol,
                                    'x_weight': picking_id.warehouse_id.x_wt / 1000,
                                    'uom_type': uom,
                                    'account_id': temp.product_id.property_account_income_id.id if temp.product_id.property_account_income_id
                                    else temp.product_id.categ_id.property_account_income_categ_id.id,
                                    'tax_ids': [(6, 0, temp.product_id.taxes_id.ids)],
                                    # 'start_date': move_ids_without_package.start_date,
                                    # 'end_date': move_ids_without_package.end_date,

                                }
                                invoice_line_list.append((0, 0, temp_line_values))
                print(invoice_line_list)
                # raise UserError(_(invoice_line_list))

                invoice = picking_id.env['account.move'].create({
                    'type': 'out_invoice',
                    'invoice_origin': picking_id.name,
                    'invoice_user_id': current_user,
                    'narration': picking_id.name,
                    'partner_id': picking_id.partner_id.id,
                    'currency_id': picking_id.env.user.company_id.currency_id.id,
                    'journal_id': int(customer_journal_id),
                    'invoice_payment_ref': picking_id.name,
                    'picking_id': picking_id.id,
                    'invoice_line_ids': invoice_line_list,
                    # 'invoice_type': 'delivery',
                    'invoice_date': datetime.today(),

                })
                return invoice

    #### IN ####
    def create_billinv(self):
        for picking_id in self:
            current_user = self.env.uid
            if picking_id.picking_type_id.code == 'incoming':
                customer_journal_id = picking_id.env['ir.config_parameter'].sudo().get_param(
                    'stock_move_invoice.customer_journal_id') or False
                if not customer_journal_id:
                    raise UserError(_("Please configure the journal from settings"))
                # vendor_journal_id = picking_id.env['ir.config_parameter'].sudo().get_param(
                #     'stock_move_invoice.vendor_journal_id') or False
                # if not vendor_journal_id:
                #     raise UserError(_("Please configure the journal from the settings."))
                invoice_line_list = []
                agreement_id = self.env['agreement'].search([('partner_id', '=', self.partner_id.id)])
                print('agreement irukkkkkkkkkkkkkkkkkkkkkkkkkkk')
                for temp in agreement_id.charge_lines:
                    print('temp.product_id', temp.product_id, 'agreement irukkkkkkkkkkkkkk')
                    if temp.charge_type == 'inbound':
                        print('invvvvvvvvvvv')
                        if temp.container == picking_id.container:
                            print('vanthennn')
                            temp_line_values = {
                                'product_id': temp.product_id and temp.product_id.id or False,
                                'name': temp.product_id.name or '',
                                'price_unit': temp.list_price or 0.00,
                                'quantity': '1',
                                'currency_id': temp.currency_id.id,
                                'account_id': temp.product_id.property_account_income_id.id if temp.product_id.property_account_income_id
                                else temp.product_id.categ_id.property_account_income_categ_id.id,
                                # 'start_date': move_ids_without_package.start_date,
                                # 'end_date': move_ids_without_package.end_date,

                            }
                            invoice_line_list.append((0, 0, temp_line_values))

                invoice = picking_id.env['account.move'].create({
                    'type': 'out_invoice',
                    'invoice_origin': picking_id.name,
                    'invoice_user_id': current_user,
                    'narration': picking_id.name,
                    'partner_id': picking_id.partner_id.id,
                    'currency_id': picking_id.env.user.company_id.currency_id.id,
                    'journal_id': int(customer_journal_id),
                    'invoice_payment_ref': picking_id.name,
                    'picking_id': picking_id.id,
                    'invoice_line_ids': invoice_line_list,
                    'invoice_type': 'reception',
                    'name': '/',

                })
                return invoice

    def create_billinvnew(self):
        for picking_id in self:
            current_user = self.env.uid
            if picking_id.picking_type_id.code == 'incoming':
                customer_journal_id = picking_id.env['ir.config_parameter'].sudo().get_param(
                    'stock_move_invoice.customer_journal_id') or False
                if not customer_journal_id:
                    raise UserError(_("Please configure the journal from settings"))
                # vendor_journal_id = picking_id.env['ir.config_parameter'].sudo().get_param(
                #     'stock_move_invoice.vendor_journal_id') or False
                # if not vendor_journal_id:
                #     raise UserError(_("Please configure the journal from the settings."))
                invoice_line_list = []
                agreement_id = self.env['agreement'].search([('partner_id', '=', self.partner_id.id)])
                print('agreement irukkkkkkkkkkkkkkkkkkkkkkkkkkk')
                for temp in agreement_id.charge_lines:
                    print('temp.product_id', temp.product_id, 'agreement irukkkkkkkkkkkkkk')
                    if temp.charge_type == 'inbound':
                        print('invvvvvvvvvvv')
                        if temp.container == picking_id.container:
                            print('vanthennn')
                            temp_line_values = {
                                'product_id': temp.product_id and temp.product_id.id or False,
                                'name': temp.product_id.name or '',
                                'price_unit': temp.list_price or 0.00,
                                'quantity': '1',
                                'currency_id': temp.currency_id.id,
                                'account_id': temp.product_id.property_account_income_id.id if temp.product_id.property_account_income_id
                                else temp.product_id.categ_id.property_account_income_categ_id.id,
                                # 'start_date': move_ids_without_package.start_date,
                                # 'end_date': move_ids_without_package.end_date,

                            }
                            invoice_line_list.append((0, 0, temp_line_values))

                invoice = picking_id.env['account.move'].create({
                    'type': 'out_invoice',
                    'invoice_origin': picking_id.name,
                    'invoice_user_id': current_user,
                    'narration': picking_id.name,
                    'partner_id': picking_id.partner_id.id,
                    'currency_id': picking_id.env.user.company_id.currency_id.id,
                    'journal_id': int(customer_journal_id),
                    'invoice_payment_ref': picking_id.name,
                    'picking_id': picking_id.id,
                    'invoice_line_ids': invoice_line_list,
                    'invoice_type': 'reception',
                    'name': '/',

                })
                return invoice

    #### OUT ####
    def create_invoiceinv(self):
        for picking_id in self:
            current_user = self.env.uid
            if picking_id.picking_type_id.code == 'outgoing':
                customer_journal_id = picking_id.env['ir.config_parameter'].sudo().get_param(
                    'stock_move_invoice.customer_journal_id') or False
                if not customer_journal_id:
                    raise UserError(_("Please configure the journal from settings"))
                invoice_line_list = []
                agreement_id = self.env['agreement'].search([('partner_id', '=', self.partner_id.id)])

                for temp in agreement_id.charge_lines:
                    if temp.charge_type == 'outbound':
                        if temp.container == picking_id.container:
                            temp_line_values = {
                                'product_id': temp.product_id and temp.product_id.id or False,
                                'name': temp.product_id.name or '',
                                'price_unit': temp.list_price or 0.00,
                                'quantity': '1',
                                'currency_id': temp.currency_id.id,
                                'account_id': temp.product_id.property_account_income_id.id if temp.product_id.property_account_income_id
                                else temp.product_id.categ_id.property_account_income_categ_id.id,
                                # 'start_date': move_ids_without_package.start_date,
                                # 'end_date': move_ids_without_package.end_date,

                            }
                            invoice_line_list.append((0, 0, temp_line_values))

                invoice = picking_id.env['account.move'].create({
                    'type': 'out_invoice',
                    'invoice_origin': picking_id.name,
                    'invoice_user_id': current_user,
                    'narration': picking_id.name,
                    'partner_id': picking_id.partner_id.id,
                    'currency_id': picking_id.env.user.company_id.currency_id.id,
                    'journal_id': int(customer_journal_id),
                    'invoice_payment_ref': picking_id.name,
                    'picking_id': picking_id.id,
                    'invoice_line_ids': invoice_line_list,
                    'invoice_type': 'delivery',
                    'name': '/',

                })
                return invoice

    def trig_inv_month(self):
        print("[[[[[[[[[[[[]]]]]]]]]]]]")

        for res in self.env['stock.picking'].search([('state', '=', 'done')]):
            if res.picking_type_id.code == 'incoming':
                print("::::::::::::::::::::::::::::::::::::::::::::::::")
                res.create_invoice_from_pickingg()

    def create_invoice_from_pickingg(self):
        print('-------------Storage Invoice Running--------------')
        stock_orders = self.env['stock.picking'].search([('state', '=', 'done')])
        partners = [order.partner_id.id for order in stock_orders]
        for picking_id in self:
            # if (len(set(partners)) == 1):
            print(picking_id, 'picking_id')
            crnt_mnth = date.today().month
            sched_mnth = picking_id.scheduled_date.month
            print(crnt_mnth)
            today = datetime.today().date()
            first_da = today.replace(day=1)
            first_day = datetime.strptime(str(first_da), '%Y-%m-%d').strftime('%Y-%m-%d %H:%M:%S')
            print(first_da)
            print(first_day, 'first_day')
            last_da = today
            last_day = datetime.strptime(str(last_da), '%Y-%m-%d').strftime('%Y-%m-%d %H:%M:%S')
            print(last_da)
            print(last_day, 'last_day')
            print(picking_id.date_done, "picking_id.date_done")
            print('-------------Storage Invoice Running--------------')
            for pic in picking_id.move_ids_without_package:
                pic.start_date = first_day
                print(pic.start_date, 'pic.start_date')
                pic.end_date = last_day
                print(pic.end_date, 'pic.end_date')
                pic.x_days = str((pic.end_date - pic.start_date).days)

            current_user = self.env.uid
            if picking_id.picking_type_id.code == 'incoming':
                customer_journal_id = picking_id.env['ir.config_parameter'].sudo().get_param(
                    'stock_move_invoice.customer_journal_id') or False
                if not customer_journal_id:
                    raise UserError(_("Please configure the journal from settings"))
                invoice_line_list = []

                for move_ids_without_package in picking_id.move_ids_without_package:
                    if move_ids_without_package.product_id.free_qty > 0:
                        if move_ids_without_package.inv_meth == 'cbm':
                            print('cbm')
                            # quantt_tot += float(move_ids_without_package.volume)
                            move_ids_without_package[
                                'quantt'] = move_ids_without_package.x_volume * move_ids_without_package.noofdays
                        if move_ids_without_package.inv_meth == 'pallet':
                            print('pallet')
                            # quantt_tot += move_ids_without_package.count
                            move_ids_without_package['quantt'] = float(move_ids_without_package.count) * float(
                                move_ids_without_package.noofdays)
                        if move_ids_without_package.inv_meth == 'carton_units':
                            print('carton')
                            # quantt_tot += float(move_ids_without_package.quantity_done)
                            move_ids_without_package[
                                'quantt'] = move_ids_without_package.quantity_done * move_ids_without_package.noofdays
                        if move_ids_without_package.inv_meth == 'weight':
                            print('weight')
                            # quantt_tot += float(move_ids_without_package.x_weight)
                            move_ids_without_package[
                                'quantt'] = move_ids_without_package.x_weight * move_ids_without_package.noofdays
                        if move_ids_without_package.inv_meth == 'square':
                            print('square')
                            # quantt_tot += float(move_ids_without_package.x_length * move_ids_without_package.x_breadth)
                            move_ids_without_package[
                                'quantt'] = move_ids_without_package.x_length * move_ids_without_package.x_breadth * move_ids_without_package.noofdays
                        if not move_ids_without_package.inv_meth:
                            # quantt_tot += float(move_ids_without_package.noofdays)
                            move_ids_without_package[
                                'quantt'] = move_ids_without_package.quantity_done * move_ids_without_package.noofdays

                        # agreement_id = picking_id.agreement_id.id
                        agreement_id = self.env['agreement'].search([('partner_id', '=', self.partner_id.id)])
                        print(agreement_id, 'agreement_id')
                        agreement_charges = self.env['agreement.charges'].search(
                            ['&', ('charge_type', '=', 'storage'), ('agreement_id', '=', agreement_id.id)])
                        print(agreement_charges, 'agreement_charges')
                        for temp in agreement_id.charge_lines:
                            print(temp.charge_type, 'temp.charge_typ')
                            if temp.charge_type == 'storage':
                                temp_line_values = {
                                    'product_id': temp.product_id and temp.product_id.id or False,
                                    'name': temp.product_id.name or '',
                                    'price_unit': temp.list_price or 0.00,
                                    'quantity': '1',
                                    'currency_id': temp.currency_id.id,
                                    'account_id': temp.product_id.property_account_income_id.id if temp.product_id.property_account_income_id
                                    else temp.product_id.categ_id.property_account_income_categ_id.id,
                                    # 'start_date': move_ids_without_package.start_date,
                                    # 'end_date': move_ids_without_package.end_date,

                                }
                                invoice_line_list.append((0, 0, temp_line_values))
                        invoice = picking_id.env['account.move'].create({
                            'type': 'out_invoice',
                            'invoice_origin': picking_id.name,
                            'invoice_user_id': current_user,
                            'narration': picking_id.name,
                            'partner_id': picking_id.partner_id.id,
                            'currency_id': picking_id.env.user.company_id.currency_id.id,
                            'journal_id': int(customer_journal_id),
                            'invoice_payment_ref': picking_id.name,
                            'picking_id': picking_id.id,
                            'invoice_line_ids': invoice_line_list,
                            # 'invoice_type': 'storage',
                            'name': '/',

                        })
                        return invoice

        # for picking_id in self:
        #     print(picking_id, 'picking_id')
        #     crnt_mnth = date.today().month
        #     sched_mnth = picking_id.scheduled_date.month
        #     print(crnt_mnth)
        #     today = datetime.today().date()
        #     first_da = today.replace(day=1)
        #     first_day = datetime.strptime(str(first_da), '%Y-%m-%d').strftime('%Y-%m-%d %H:%M:%S')
        #     print(first_da)
        #     print(first_day, 'first_day')
        #     last_da = today
        #     last_day = datetime.strptime(str(last_da), '%Y-%m-%d').strftime('%Y-%m-%d %H:%M:%S')
        #     print(last_da)
        #     print(last_day, 'last_day')
        #     print(picking_id.date_done, "picking_id.date_done")
        #     print('-------------Storage Invoice Running--------------')
        #
        #     if sched_mnth == crnt_mnth:
        #         print('ifff')
        #         for pic in picking_id.move_ids_without_package:
        #             pic.start_date = picking_id.scheduled_date
        #             print(pic.start_date, 'pic.start_date')
        #             pic.end_date = last_day
        #             print(pic.end_date, 'pic.end_date')
        #             pic.x_days = str((pic.end_date - pic.start_date).days)
        #             print(pic.x_days, 'pic.x_days')
        #     else:
        #         print('elseee')
        #         for pic in picking_id.move_ids_without_package:
        #             pic.start_date = first_day
        #             print(pic.start_date, 'pic.start_date')
        #             pic.end_date = last_day
        #             print(pic.end_date, 'pic.end_date')
        #             pic.x_days = str((pic.end_date - pic.start_date).days)
        #
        #     current_user = self.env.uid
        #
        #     if picking_id.picking_type_id.code == 'incoming':
        #         customer_journal_id = picking_id.env['ir.config_parameter'].sudo().get_param(
        #             'stock_move_invoice.customer_journal_id') or False
        #         if not customer_journal_id:
        #             raise UserError(_("Please configure the journal from settings"))
        #         quantt = 0
        #         for mov in picking_id.move_ids_without_package:
        #             quantt += mov['quantt']
        #         print(quantt, 'quantt')
        #         invoice_line_list = []
        #
        #         for temp in picking_id.agreement_id.charge_lines:
        #             if temp.product_id.categ_id.name == 'Storage Charge':
        #                 temp_line_values = {
        #                     'product_id': temp.product_id and temp.product_id.id or False,
        #                     'name': temp.product_id.name or '',
        #                     'price_unit': temp.list_price or 0.00,
        #                     'quantity': '1',
        #                     'currency_id': temp.currency_id.id,
        #                     'account_id': temp.product_id.property_account_income_id.id if temp.product_id.property_account_income_id
        #                     else temp.product_id.categ_id.property_account_income_categ_id.id,
        #                     # 'start_date': move_ids_without_package.start_date,
        #                     # 'end_date': move_ids_without_package.end_date,
        #
        #                 }
        #                 invoice_line_list.append((0, 0, temp_line_values))
        #
        #         # -------------- Except Storage ------------- #
        #
        #         for move_ids_without_package in picking_id.move_ids_without_package:
        #             if move_ids_without_package.inv_meth == 'cbm':
        #                 print('cbm')
        #                 # quantt_tot += float(move_ids_without_package.volume)
        #                 move_ids_without_package[
        #                     'quantt'] = move_ids_without_package.x_volume * move_ids_without_package.noofdays
        #             if move_ids_without_package.inv_meth == 'pallet':
        #                 print('pallet')
        #                 # quantt_tot += move_ids_without_package.count
        #                 move_ids_without_package['quantt'] = float(move_ids_without_package.count) * float(
        #                     move_ids_without_package.noofdays)
        #             if move_ids_without_package.inv_meth == 'carton_units':
        #                 print('carton')
        #                 # quantt_tot += float(move_ids_without_package.quantity_done)
        #                 move_ids_without_package[
        #                     'quantt'] = move_ids_without_package.quantity_done * move_ids_without_package.noofdays
        #             if move_ids_without_package.inv_meth == 'weight':
        #                 print('weight')
        #                 # quantt_tot += float(move_ids_without_package.x_weight)
        #                 move_ids_without_package[
        #                     'quantt'] = move_ids_without_package.x_weight * move_ids_without_package.noofdays
        #             if move_ids_without_package.inv_meth == 'square':
        #                 print('square')
        #                 # quantt_tot += float(move_ids_without_package.x_length * move_ids_without_package.x_breadth)
        #                 move_ids_without_package[
        #                     'quantt'] = move_ids_without_package.x_length * move_ids_without_package.x_breadth * move_ids_without_package.noofdays
        #             if not move_ids_without_package.inv_meth:
        #                 # quantt_tot += float(move_ids_without_package.noofdays)
        #                 move_ids_without_package['quantt'] = move_ids_without_package.noofdays
        #
        #             agreement_id = picking_id.agreement_id.id
        #             print(agreement_id, 'agreement_id')
        #             agreement_charges = self.env['agreement.charges'].search(
        #                 ['&', ('product_id.categ_id', '=', 'Storage Charge'), ('agreement_id', '=', agreement_id)])
        #             print(agreement_charges, 'agreement_charges')
        #
        #             for temp in picking_id.agreement_id.charge_lines:
        #                 if temp.product_id.categ_id.name == 'Storage Charge':
        #                     temp_line_values = {
        #                         'product_id': temp.product_id and temp.product_id.id or False,
        #                         'name': temp.product_id.name or '',
        #                         'price_unit': temp.list_price or 0.00,
        #                         'quantity': '1',
        #                         'currency_id': temp.currency_id.id,
        #                         'account_id': temp.product_id.property_account_income_id.id if temp.product_id.property_account_income_id
        #                         else temp.product_id.categ_id.property_account_income_categ_id.id,
        #                         # 'start_date': move_ids_without_package.start_date,
        #                         # 'end_date': move_ids_without_package.end_date,
        #
        #                     }
        #                     invoice_line_list.append((0, 0, temp_line_values))
        #
        #             # vals = (0, 0, {
        #             #     'name': 'storage charge of' + ' ' + move_ids_without_package.name,
        #             #     # 'product_id': move_ids_without_package.product_id.id,
        #             #     # 'price_unit': move_ids_without_package.product_id.lst_price,
        #             #     'product_id' : agreement_charges.product_id.id,
        #             #     'price_unit':agreement_charges.list_price * move_ids_without_package.quantt,
        #             #     'account_id': move_ids_without_package.product_id.property_account_income_id.id if move_ids_without_package.product_id.property_account_income_id
        #             #     else move_ids_without_package.product_id.categ_id.property_account_income_categ_id.id,
        #             #     #                        'tax_ids': [(6, 0, [picking_id.company_id.account_sale_tax_id.id])],
        #             #     #                        'quantity': move_ids_without_package.quantity_done,
        #             #     # 'start_date': move_ids_without_package.start_date,
        #             #     # 'end_date': move_ids_without_package.end_date,
        #             #     'x_days': move_ids_without_package.x_days,
        #             #     # 'storage_fee': move_ids_without_package.storage_fee,
        #             #     'quantity': move_ids_without_package.quantity_done,
        #             #     # 'quantity': picking_id.quantt,
        #             #     # 'x_cbm': move_ids_without_package.x_cbm,
        #             #     #                        'start_date':picking_id.scheduled_date,
        #             #     #                        'end_date':picking_id.date,
        #             # })
        #             # invoice_line_list.append(vals)
        #             # print(invoice_line_list)
        #         invoice = picking_id.env['account.move'].create({
        #             'type': 'out_invoice',
        #             'invoice_origin': picking_id.name,
        #             'invoice_user_id': current_user,
        #             'narration': picking_id.name,
        #             'partner_id': picking_id.partner_id.id,
        #             'currency_id': picking_id.env.user.company_id.currency_id.id,
        #             'journal_id': int(customer_journal_id),
        #             'invoice_payment_ref': picking_id.name,
        #             'picking_id': picking_id.id,
        #             'invoice_line_ids': invoice_line_list,
        #             # 'invoice_type': 'storage',
        #
        #         })
        #         return invoice

    def create_invoice_from_picking(self):
        for picking_id in self:
            print(picking_id, 'picking_id')
            crnt_mnth = date.today().month
            sched_mnth = picking_id.scheduled_date.month
            print(crnt_mnth)
            today = datetime.today().date()
            first_da = today.replace(day=1)
            first_day = datetime.strptime(str(first_da), '%Y-%m-%d').strftime('%Y-%m-%d %H:%M:%S')
            print(first_da)
            print(first_day, 'first_day')
            last_da = today
            last_day = datetime.strptime(str(last_da), '%Y-%m-%d').strftime('%Y-%m-%d %H:%M:%S')
            print(last_da)
            print(last_day, 'last_day')
            print(picking_id.date_done, "picking_id.date_done")
            # for pic in picking_id.move_ids_without_package:
            #     pic.start_date = picking_id.scheduled_date
            #     print(pic.start_date, 'pic.start_date')
            #     pic.end_date = last_day
            #     print(pic.end_date, 'pic.end_date')
            #     pic.x_days = str((pic.end_date - pic.start_date).days)
            #     print(pic.x_days, 'pic.x_days')
            #

            if sched_mnth == crnt_mnth:
                print('ifff')
                for pic in picking_id.move_ids_without_package:
                    pic.start_date = picking_id.scheduled_date
                    print(pic.start_date, 'pic.start_date')
                    pic.end_date = last_day
                    print(pic.end_date, 'pic.end_date')
                    pic.x_days = str((pic.end_date - pic.start_date).days)
                    print(pic.x_days, 'pic.x_days')
            else:
                print('elseee')
                for pic in picking_id.move_ids_without_package:
                    pic.start_date = first_day
                    print(pic.start_date, 'pic.start_date')
                    pic.end_date = last_day
                    print(pic.end_date, 'pic.end_date')
                    pic.x_days = str((pic.end_date - pic.start_date).days)

            current_user = self.env.uid

            if picking_id.picking_type_id.code == 'outgoing':
                customer_journal_id = picking_id.env['ir.config_parameter'].sudo().get_param(
                    'stock_move_invoice.customer_journal_id') or False
                if not customer_journal_id:
                    raise UserError(_("Please configure the journal from settings"))
                invoice_line_list = []

                for temp in picking_id.charge_lines:
                    temp_line_values = {
                        'product_id': temp.product_id and temp.product_id.id or False,
                        'name': temp.product_id.name or '',
                        'price_unit': temp.product_id.list_price or 0.00,
                        'quantity': temp.qty,
                        'currency_id': temp.currency_id.id,
                        'account_id': temp.product_id.property_account_income_id.id if temp.product_id.property_account_income_id
                        else temp.product_id.categ_id.property_account_income_categ_id.id,
                    }
                    invoice_line_list.append((0, 0, temp_line_values))

                for move_ids_without_package in picking_id.move_ids_without_package:
                    vals = (0, 0, {
                        'name': move_ids_without_package.description_picking,
                        'product_id': move_ids_without_package.product_id.id,
                        'price_unit': move_ids_without_package.product_id.lst_price,
                        'account_id': move_ids_without_package.product_id.property_account_income_id.id if move_ids_without_package.product_id.property_account_income_id
                        else move_ids_without_package.product_id.categ_id.property_account_income_categ_id.id,
                        #                        'tax_ids': [(6, 0, [picking_id.company_id.account_sale_tax_id.id])],
                        #                        'quantity': move_ids_without_package.quantity_done,
                        # 'start_date': move_ids_without_package.start_date,
                        # 'end_date': move_ids_without_package.end_date,
                        'x_days': move_ids_without_package.x_days,
                        'storage_fee': move_ids_without_package.storage_fee,
                        'quantity': 0,
                        # 'x_cbm': move_ids_without_package.x_cbm,
                        #                        'start_date':picking_id.scheduled_date,
                        #                        'end_date':picking_id.date,
                    })
                    invoice_line_list.append(vals)
                    print(invoice_line_list)
                invoice = picking_id.env['account.move'].create({
                    'type': 'out_invoice',
                    'invoice_origin': picking_id.name,
                    'invoice_user_id': current_user,
                    'narration': picking_id.name,
                    'partner_id': picking_id.partner_id.id,
                    'currency_id': picking_id.env.user.company_id.currency_id.id,
                    'journal_id': int(customer_journal_id),
                    'invoice_payment_ref': picking_id.name,
                    'picking_id': picking_id.id,
                    'invoice_line_ids': invoice_line_list,
                    'invoice_type': 'storage',
                    'name': '/',

                })
                return invoice


class Partnerform(models.Model):
    _inherit = 'res.partner'

    def trig_inv_monthh(self):
        print("[[[[[[[[[[[[]]]]]]]]]]]]")
        partner = self.env['res.partner'].search([])
        partner.create_invoice_from_pickinggg()
        # raise UserError(_("Server is too busy right now. Please wait... "))

    def create_invoice_from_pickinggg(self):
        for rec in self:
            print('-------------Storage Invoice Running--------------')
            quants = self.env['stock.quant'].search(
                [('owner_id', '=', rec.id), ('location_id.usage', '=', 'internal')])
            quantityy = 0
            pallet = 0
            cbm = 0
            weight = 0
            square = 0

            for quant in quants:
                print(quant, rec.id, quant.inventory_quantity, quant.quantity,  quant.location_id.usage, 'quant')
                prod_moves = self.env['stock.move.line'].search([('lot_id','=',quant.lot_id.id),('picking_code','!=','outcoming')])
                print(prod_moves, 'prod_moves')
                quantityy += quant.quantity
                print(quantityy, 'quantityy')
                pallett = (prod_moves.mapped('result_package_id')).id
                print(pallett, 'pallett')
                if pallet:
                    pallet = len(pallett)
                else:
                    pallet = 0
                quantity = 0
                cbm = 0
                weight = 0
                square = 0
                # dur = 0
                for pmoves in prod_moves:
                        today = datetime.today().date()
                        first_da = today.replace(day=1)
                        first_day = datetime.strptime(str(first_da), '%Y-%m-%d').strftime('%Y-%m-%d %H:%M:%S')
                        last_mo = first_da - timedelta(days=1)
                        # last_month = datetime.strptime((last_mo), '%Y-%m-%d').strftime('%Y-%m-%d %H:%M:%S')
                        begin_day = last_mo.replace(day=26)
                        print(begin_day, 'begin_day')
                        last_da = today
                        last_day = datetime.strptime(str(last_da), '%Y-%m-%d').strftime('%Y-%m-%d %H:%M:%S')
                        print(last_day, 'last_day')
                        test_dur = abs(datetime.today() - pmoves.picking_id.scheduled_date).days
                        fixed_dur = abs(today - begin_day).days
                        print(test_dur, 'test_dur', 'fixed_dur' , fixed_dur)
                        print('-------------Storage Invoice Running--------------')
                        if test_dur <= fixed_dur:
                            dur = test_dur
                        else:
                            dur = fixed_dur
                        print(prod_moves.lot_id.name, 'lottttttttttt', quantityy, dur)
                        if pmoves.picking_code != 'outgoing':
                            cbm += pmoves.move_id.x_volume * dur * quantityy
                            quantity += pmoves.qty_done * dur * quantityy
                            weight += pmoves.move_id.x_weight * dur * quantityy
                            square += (pmoves.move_id.x_length * pmoves.move_id.x_breadth) * dur * quantityy
                            pallet += 0 * dur * quantityy

                print(quantity)
                print(cbm)
                print(weight)
                print(square)
            cbm += cbm
            weight += weight
            square += square
            pallets = pallet

            agreement_id = rec.env['agreement'].search([('partner_id', '=', rec.id)])
            print(agreement_id, 'agreement_id')
            agreement_charges = rec.env['agreement.charges'].search(
                ['&', ('charge_type', '=', 'storage'), ('agreement_id', '=', agreement_id.id)])
            print(agreement_charges, 'agreement_charges')
            invoice_line_list = []
            for temp in agreement_id.charge_lines:
                print(temp.charge_type, 'temp.charge_typ')
                if temp.charge_type == 'storage' and temp.charge_unit_type == 'cbm':
                    temp_line_values = {
                        'product_id': temp.product_id and temp.product_id.id or False,
                        'name': temp.product_id.name or '',
                        'price_unit': temp.list_price or 0.00,
                        'quantity': cbm,
                        'currency_id': temp.currency_id.id,
                        'account_id': temp.product_id.property_account_income_id.id if temp.product_id.property_account_income_id
                        else temp.product_id.categ_id.property_account_income_categ_id.id,
                        # 'start_date': move_ids_without_package.start_date,
                        # 'end_date': move_ids_without_package.end_date,

                    }
                    invoice_line_list.append((0, 0, temp_line_values))
                if temp.charge_type == 'storage' and temp.charge_unit_type == 'weight':
                    temp_line_values = {
                        'product_id': temp.product_id and temp.product_id.id or False,
                        'name': temp.product_id.name or '',
                        'price_unit': temp.list_price or 0.00,
                        'quantity': weight,
                        'currency_id': temp.currency_id.id,
                        'account_id': temp.product_id.property_account_income_id.id if temp.product_id.property_account_income_id
                        else temp.product_id.categ_id.property_account_income_categ_id.id,
                        # 'start_date': move_ids_without_package.start_date,
                        # 'end_date': move_ids_without_package.end_date,

                    }
                    invoice_line_list.append((0, 0, temp_line_values))
                if temp.charge_type == 'storage' and temp.charge_unit_type == 'square':
                    temp_line_values = {
                        'product_id': temp.product_id and temp.product_id.id or False,
                        'name': temp.product_id.name or '',
                        'price_unit': temp.list_price or 0.00,
                        'quantity': square,
                        'currency_id': temp.currency_id.id,
                        'account_id': temp.product_id.property_account_income_id.id if temp.product_id.property_account_income_id
                        else temp.product_id.categ_id.property_account_income_categ_id.id,
                        # 'start_date': move_ids_without_package.start_date,
                        # 'end_date': move_ids_without_package.end_date,

                    }
                    invoice_line_list.append((0, 0, temp_line_values))
                if temp.charge_type == 'storage' and temp.charge_unit_type == 'pallet':
                    temp_line_values = {
                        'product_id': temp.product_id and temp.product_id.id or False,
                        'name': temp.product_id.name or '',
                        'price_unit': temp.list_price or 0.00,
                        'quantity': pallets,
                        'currency_id': temp.currency_id.id,
                        'account_id': temp.product_id.property_account_income_id.id if temp.product_id.property_account_income_id
                        else temp.product_id.categ_id.property_account_income_categ_id.id,
                        # 'start_date': move_ids_without_package.start_date,
                        # 'end_date': move_ids_without_package.end_date,

                    }
                    invoice_line_list.append((0, 0, temp_line_values))

            print(invoice_line_list, 'invoice_line_list')
            current_user = self.env.uid
            if agreement_id:
                invoice = rec.env['account.move'].create({
                    'type': 'out_invoice',
                    'invoice_origin': rec.name,
                    'invoice_user_id': current_user,
                    'narration': rec.name,
                    'partner_id': rec.id,
                    'currency_id': rec.env.user.company_id.currency_id.id,
                    # 'journal_id': int(customer_journal_id),
                    'invoice_payment_ref': rec.name,
                    # 'picking_id': picking_id.id,
                    'invoice_line_ids': invoice_line_list,
                    # 'invoice_type': 'storage',
                    'name': '/',

                })
                print(invoice, 'Invoice Created')
                # return invoice







        # stock_orders = self.env['stock.picking'].search([('state', '=', 'done')])
        # # partners = [order.partner_id.id for order in stock_orders]
        # for picking_id in stock_orders:
        #     # if (len(set(partners)) == 1):
        #     print(picking_id, 'picking_id')
        #     crnt_mnth = date.today().month
        #     sched_mnth = picking_id.scheduled_date.month
        #     print(crnt_mnth)
        #     today = datetime.today().date()
        #     first_da = today.replace(day=1)
        #     first_day = datetime.strptime(str(first_da), '%Y-%m-%d').strftime('%Y-%m-%d %H:%M:%S')
        #     print(first_da)
        #     print(first_day, 'first_day')
        #     last_da = today
        #     last_day = datetime.strptime(str(last_da), '%Y-%m-%d').strftime('%Y-%m-%d %H:%M:%S')
        #     print(last_da)
        #     print(last_day, 'last_day')
        #     print(picking_id.date_done, "picking_id.date_done")
        #     print('-------------Storage Invoice Running--------------')
        #     for pic in picking_id.move_ids_without_package:
        #         pic.start_date = first_day
        #         print(pic.start_date, 'pic.start_date')
        #         pic.end_date = last_day
        #         print(pic.end_date, 'pic.end_date')
        #         pic.x_days = str((pic.end_date - pic.start_date).days)
        #
        #     current_user = self.env.uid
        #     if picking_id.picking_type_id.code == 'incoming':
        #         customer_journal_id = picking_id.env['ir.config_parameter'].sudo().get_param(
        #             'stock_move_invoice.customer_journal_id') or False
        #         if not customer_journal_id:
        #             raise UserError(_("Please configure the journal from settings"))
        #         invoice_line_list = []
        #
        #         for move_ids_without_package in picking_id.move_ids_without_package:
        #             if move_ids_without_package.product_id.free_qty > 0:
        #                 if move_ids_without_package.inv_meth == 'cbm':
        #                     print('cbm')
        #                     # quantt_tot += float(move_ids_without_package.volume)
        #                     move_ids_without_package[
        #                         'quantt'] = move_ids_without_package.x_volume * move_ids_without_package.noofdays
        #                 if move_ids_without_package.inv_meth == 'pallet':
        #                     print('pallet')
        #                     # quantt_tot += move_ids_without_package.count
        #                     move_ids_without_package['quantt'] = float(move_ids_without_package.count) * float(
        #                         move_ids_without_package.noofdays)
        #                 if move_ids_without_package.inv_meth == 'carton_units':
        #                     print('carton')
        #                     # quantt_tot += float(move_ids_without_package.quantity_done)
        #                     move_ids_without_package[
        #                         'quantt'] = move_ids_without_package.quantity_done * move_ids_without_package.noofdays
        #                 if move_ids_without_package.inv_meth == 'weight':
        #                     print('weight')
        #                     # quantt_tot += float(move_ids_without_package.x_weight)
        #                     move_ids_without_package[
        #                         'quantt'] = move_ids_without_package.x_weight * move_ids_without_package.noofdays
        #                 if move_ids_without_package.inv_meth == 'square':
        #                     print('square')
        #                     # quantt_tot += float(move_ids_without_package.x_length * move_ids_without_package.x_breadth)
        #                     move_ids_without_package[
        #                         'quantt'] = move_ids_without_package.x_length * move_ids_without_package.x_breadth * move_ids_without_package.noofdays
        #                 if not move_ids_without_package.inv_meth:
        #                     # quantt_tot += float(move_ids_without_package.noofdays)
        #                     move_ids_without_package[
        #                         'quantt'] = move_ids_without_package.quantity_done * move_ids_without_package.noofdays
        #
        #                 # agreement_id = picking_id.agreement_id.id
        #         agreement_id = self.env['agreement'].search([('partner_id', '=', self.id)])
        #         print(agreement_id, 'agreement_id')
        #         agreement_charges = self.env['agreement.charges'].search(
        #             ['&', ('charge_type', '=', 'storage'), ('agreement_id', '=', agreement_id.id)])
        #         print(agreement_charges, 'agreement_charges')
        #         for temp in agreement_id.charge_lines:
        #             print(temp.charge_type, 'temp.charge_typ')
        #             if temp.charge_type == 'storage':
        #                 temp_line_values = {
        #                     'product_id': temp.product_id and temp.product_id.id or False,
        #                     'name': temp.product_id.name or '',
        #                     'price_unit': temp.list_price or 0.00,
        #                     'quantity': '1',
        #                     'currency_id': temp.currency_id.id,
        #                     'account_id': temp.product_id.property_account_income_id.id if temp.product_id.property_account_income_id
        #                     else temp.product_id.categ_id.property_account_income_categ_id.id,
        #                     # 'start_date': move_ids_without_package.start_date,
        #                     # 'end_date': move_ids_without_package.end_date,
        #
        #                 }
        #                 invoice_line_list.append((0, 0, temp_line_values))
        #         print(invoice_line_list, 'invoice_line_list')
        #         invoice = picking_id.env['account.move'].create({
        #             'type': 'out_invoice',
        #             'invoice_origin': picking_id.name,
        #             'invoice_user_id': current_user,
        #             'narration': picking_id.name,
        #             'partner_id': picking_id.id,
        #             'currency_id': picking_id.env.user.company_id.currency_id.id,
        #             'journal_id': int(customer_journal_id),
        #             'invoice_payment_ref': picking_id.name,
        #             'picking_id': picking_id.id,
        #             'invoice_line_ids': invoice_line_list,
        #             # 'invoice_type': 'storage',
        #
        #         })
        #         print(invoice, 'Invoice Created')
        #         return invoice



