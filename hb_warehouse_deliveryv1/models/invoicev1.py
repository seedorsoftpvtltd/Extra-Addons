from dateutil import parser
from odoo import api, models, fields, _
from datetime import datetime, date
from odoo.exceptions import AccessError, UserError, ValidationError


class Warehouseinv(models.Model):
    _inherit = 'warehouse.order'

    inv_meth = fields.Selection(string="Invoice Method",
                                selection=[('cbm', 'CBM'), ('pallet', 'Pallet'), ('weight', 'Weight'),
                                           ('carton_units', 'Carton/Units'), ('square', 'Square Units')])
    agreement_id = fields.Many2one('agreement', string="Agreement")


# class accmoveline(models.Model):
#    _inherit = 'account.move.line'

#    start_date = fields.Datetime('Start Dte')
#    end_date = fields.Datetime('End Dte')


class StockpickingInhINV(models.Model):
    _inherit = 'stock.picking'

    quantt = fields.Float(string='Quant', compute='_quantt_calculate')

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

    def create_invoice_from_pickingg(self):
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

            if sched_mnth == crnt_mnth:
                print('ifff')
                for pic in picking_id.move_ids_without_package:
                    pic.start_date = picking_id.scheduled_date
                    print(pic.start_date, 'pic.start_date')
                    pic.end_date = last_day
                    print(pic.end_date, 'pic.end_date')
                    pic.x_days = abs((pic.end_date - pic.start_date).days)
                    print(pic.x_days, 'pic.x_days')
            else:
                print('elseee')
                for pic in picking_id.move_ids_without_package:
                    pic.start_date = first_day
                    print(pic.start_date, 'pic.start_date')
                    pic.end_date = last_day
                    print(pic.end_date, 'pic.end_date')
                    pic.x_days = abs((pic.end_date - pic.start_date).days)

            # for movee in picking_id.move_ids_without_package:
            #     # movee.x_days = self.x_days
            #     if movee.inv_meth == 'weight':
            #         movee['quantt'] = float(movee.x_weight_inv) * float(picking_id.noofdays)
            #     if movee.inv_meth == 'cbm':
            #         movee['quantt'] = float(movee.x_cbm) * float(picking_id.noofdays)
            #     if movee.inv_meth == 'pallet':
            #         movee['quantt'] = float(self.count) * float(picking_id.noofdays)
            #     if movee.inv_meth == 'carton_units':
            #         movee['quantt'] = float(movee.quantity_done) * float(picking_id.noofdays)
            #     if movee.inv_meth == 'square':
            #         movee['quantt'] = float(movee.quantity_done) * float(picking_id.noofdays)
            #     if not movee.inv_meth:
            #         movee['quantt'] = 1
            current_user = self.env.uid

            if picking_id.picking_type_id.code == 'outgoing':
                customer_journal_id = picking_id.env['ir.config_parameter'].sudo().get_param(
                    'stock_move_invoice.customer_journal_id') or False
                if not customer_journal_id:
                    raise UserError(_("Please configure the journal from settings"))
                invoice_line_list = []
                #                valss = self._construct_valuesstorage()
                #                invoice_line_list.append(valss)
                #                print(invoice_line_list)
                weight = 0
                cbm = 0
                pallet = 0
                carton = 0
                square = 0
                noninvoice = 0
                # for move_ids in picking_id.move_ids_without_package:
                #     if move_ids.inv_meth == 'weight' and weight == 0:
                #         valss = self._construct_valuesweight()
                #         invoice_line_list.append(valss)
                #         weight = 1
                #     if move_ids.inv_meth == 'cbm' and cbm == 0:
                #         # valss = self._construct_valuescbm()
                #         valss = self._construct_valuescbmstorage()
                #         invoice_line_list.append(valss)
                #         cbm = 1
                #     if move_ids.inv_meth == 'pallet' and pallet == 0:
                #         valss = self._construct_valuespallet()
                #         invoice_line_list.append(valss)
                #         pallet = 1
                #     if move_ids.inv_meth == 'carton_units' and carton == 0:
                #         valss = self._construct_valuescarton()
                #         invoice_line_list.append(valss)
                #         carton = 1
                #     if move_ids.inv_meth == 'square' and square == 0:
                #         valss = self._construct_valuessquare()
                #         invoice_line_list.append(valss)
                #         carton = 1
                #     if not move_ids.inv_meth and noninvoice == 0:
                #         valss = self._construct_valuesstorage()
                #         invoice_line_list.append(valss)
                #         noninvoice = 1
                for temp in picking_id.agreement_id.charge_lines:
                    if temp.product_id.categ_id.name != 'Storage Charge':
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

                # -------------- Except Storage ------------- #
                for move_ids_without_package in picking_id.move_ids_without_package:
                    if move_ids_without_package.inv_meth == 'cbm':
                        print('cbm')
                        # quantt_tot += float(move_ids_without_package.volume)
                        move_ids_without_package['quantt'] = move_ids_without_package.x_volume * move_ids_without_package.noofdays
                    if move_ids_without_package.inv_meth == 'pallet':
                        print('pallet')
                        # quantt_tot += move_ids_without_package.count
                        move_ids_without_package['quantt'] = float(move_ids_without_package.count) * float(move_ids_without_package.noofdays)
                    if move_ids_without_package.inv_meth == 'carton_units':
                        print('carton')
                        # quantt_tot += float(move_ids_without_package.quantity_done)
                        move_ids_without_package['quantt'] = move_ids_without_package.quantity_done * move_ids_without_package.noofdays
                    if move_ids_without_package.inv_meth == 'weight':
                        print('weight')
                        # quantt_tot += float(move_ids_without_package.x_weight)
                        move_ids_without_package['quantt'] = move_ids_without_package.x_weight * move_ids_without_package.noofdays
                    if move_ids_without_package.inv_meth == 'square':
                        print('square')
                        # quantt_tot += float(move_ids_without_package.x_length * move_ids_without_package.x_breadth)
                        move_ids_without_package['quantt'] = move_ids_without_package.x_length * move_ids_without_package.x_breadth * move_ids_without_package.noofdays
                    if not move_ids_without_package.inv_meth:
                        # quantt_tot += float(move_ids_without_package.noofdays)
                        move_ids_without_package['quantt'] = move_ids_without_package.noofdays
                    agreement_id = picking_id.agreement_id.id
                    print(agreement_id, 'agreement_id')
                    agreement_charges = self.env['agreement.charges'].search(['&',('product_id.categ_id','=','Storage Charge'), ('agreement_id','=',agreement_id)])
                    print(agreement_charges, 'agreement_charges')
                    vals = (0, 0, {
                        'name': 'storage charge of' + ' ' + move_ids_without_package.name,
                        # 'product_id': move_ids_without_package.product_id.id,
                        # 'price_unit': move_ids_without_package.product_id.lst_price,
                        'product_id' : agreement_charges.product_id.id,
                        'price_unit':agreement_charges.list_price * move_ids_without_package.quantt,
                        'account_id': move_ids_without_package.product_id.property_account_income_id.id if move_ids_without_package.product_id.property_account_income_id
                        else move_ids_without_package.product_id.categ_id.property_account_income_categ_id.id,
                        #                        'tax_ids': [(6, 0, [picking_id.company_id.account_sale_tax_id.id])],
                        #                        'quantity': move_ids_without_package.quantity_done,
                        'start_date': move_ids_without_package.start_date,
                        'end_date': move_ids_without_package.end_date,
                        'x_days': move_ids_without_package.x_days,
                        # 'storage_fee': move_ids_without_package.storage_fee,
                        'quantity': move_ids_without_package.quantity_done,
                        # 'quantity': picking_id.quantt,
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
                    # 'invoice_type': 'storage',

                })
                return invoice

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

            # for movee in picking_id.move_ids_without_package:
            #     # movee.x_days = self.x_days
            #     if movee.inv_meth == 'weight':
            #         movee['quantt'] = float(movee.x_weight_inv) * float(picking_id.noofdays)
            #     if movee.inv_meth == 'cbm':
            #         movee['quantt'] = float(movee.x_cbm) * float(picking_id.noofdays)
            #     if movee.inv_meth == 'pallet':
            #         movee['quantt'] = float(self.count) * float(picking_id.noofdays)
            #     if movee.inv_meth == 'carton_units':
            #         movee['quantt'] = float(movee.quantity_done) * float(picking_id.noofdays)
            #     if not movee.inv_meth:
            #         movee['quantt'] = 1
            current_user = self.env.uid

            if picking_id.picking_type_id.code == 'outgoing':
                customer_journal_id = picking_id.env['ir.config_parameter'].sudo().get_param(
                    'stock_move_invoice.customer_journal_id') or False
                if not customer_journal_id:
                    raise UserError(_("Please configure the journal from settings"))
                invoice_line_list = []
                #                valss = self._construct_valuesstorage()
                #                invoice_line_list.append(valss)
                #                print(invoice_line_list)
                weight = 0
                cbm = 0
                pallet = 0
                carton = 0
                noninvoice = 0
                # for move_ids in picking_id.move_ids_without_package:
                #     if move_ids.inv_meth == 'weight' and weight == 0:
                #         valss = self._construct_valuesweight()
                #         invoice_line_list.append(valss)
                #         weight = 1
                #     if move_ids.inv_meth == 'cbm' and cbm == 0:
                #         # valss = self._construct_valuescbm()
                #         valss = self._construct_valuescbmstorage()
                #         invoice_line_list.append(valss)
                #         cbm = 1
                #     if move_ids.inv_meth == 'pallet' and pallet == 0:
                #         valss = self._construct_valuespallet()
                #         invoice_line_list.append(valss)
                #         pallet = 1
                #     if move_ids.inv_meth == 'carton_units' and carton == 0:
                #         valss = self._construct_valuescarton()
                #         invoice_line_list.append(valss)
                #         carton = 1
                #     if not move_ids.inv_meth and noninvoice == 0:
                #         valss = self._construct_valuesstorage()
                #         invoice_line_list.append(valss)
                #         noninvoice = 1
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
                        'start_date': move_ids_without_package.start_date,
                        'end_date': move_ids_without_package.end_date,
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

                })
                return invoice

