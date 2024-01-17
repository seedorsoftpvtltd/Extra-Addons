from dateutil import parser
from odoo import api, models, fields, _
from datetime import datetime, date
from odoo.exceptions import AccessError, UserError, ValidationError

class AccmoveInh(models.Model):
    _inherit = "account.move"

   # invoice_type = fields.Char(string="Invoice Type")
    invoice_type = fields.Selection([('reception', 'Reception Invoice'), ('delivery', 'Delivery Invoice'), ('storage', 'Storage Invoice')], string="Invoice Type")

class StockpickingInh(models.Model):
    _inherit = 'stock.picking'

    date = fields.Datetime(string="Date")
    noofdays = fields.Integer(string="No of Days")
    returnpick = fields.Char(string="Return", compute='_returnpick')
    start_date = fields.Datetime(string="Start Date")
    end_date = fields.Datetime(string="End Date")
    count = fields.Char(string="Count", compute="_countt")

    @api.onchange('move_line_ids_without_package')
    def _countt(self):
        for rec in self:
             rec.count = len(rec.move_line_ids_without_package.mapped('loc'))

           # rec.count = len(rec.move_line_ids_without_package.search([('inv_meth','=','pallet')]).mapped('location_dest_id'))
     #   for rec in self.search([('inv_meth', '=', 'pallet')]):

      #      rec.count = len(rec.move_line_ids_without_package.mapped('location_id'))


    @api.depends('origin')
    def _returnpick(self):
        for rec in self:
            if rec.origin:
                if len(rec.origin) > 1:
                    rec['returnpick'] = rec.origin[:11]
                    print(rec.returnpick)
                else:
                    rec['returnpick'] = 0
            else:
                rec['returnpick'] = 0

    @api.constrains('date', 'scheduled_date')
    def duration(self):
        for rec in self:
            if rec.returnpick == 'Delivery of':
                 rec['noofdays'] = abs((rec.date - rec.scheduled_date).days)
                # d1 = datetime.strftime(self.date, '%Y-%m-%d %H:%M:%S')
                # d2 = datetime.strftime(self.scheduled_date, '%Y-%m-%d %H:%M:%S')
                # dat = abs((d2-d1).days)
#                 d1 = datetime.strptime(str(self.date), '%Y-%m-%d %H:%M:%S')
#                 d2 = datetime.strptime(str(self.scheduled_date), '%Y-%m-%d %H:%M:%S')
#                 da = d2-d1
#                 dat = str(da.days)
#                 rec['noofdays'] = dat

    def _construct_valuesreception(self):
        cbm_total = 0
        storage_tot = 0
        quantt_tot = 0
        for cbm in self.move_ids_without_package:
            cbm_total += float(cbm.x_cbm)
            storage_tot += float(cbm.storage_fee)
            if not cbm.inv_meth:
                quantt_tot = 1
            else:
                quantt_tot += float(cbm.quantt)
            # cbm['cbm_tot'] = cbm_total
        print(cbm_total)
        print(storage_tot)
        product = self.env['product.product'].search([('name', '=', 'reception service')])
        vals = [0, 0, {
            'name': product.name,
            'product_id': product.id,
            'quantity': quantt_tot,
            'price_unit': product.list_price,
            'x_cbm': cbm_total,
            'storage_fee': storage_tot,
        }]
        return vals
    
    def _construct_valuesdelivery(self):
        cbm_total = 0
        storage_tot = 0
        quantt_tot = 0
        for cbm in self.move_ids_without_package:
            cbm_total += float(cbm.x_cbm)
            storage_tot += float(cbm.storage_fee)
            if not cbm.inv_meth:
                quantt_tot = 1
            else:
                quantt_tot += float(cbm.quantt)
            # cbm['cbm_tot'] = cbm_total
        print(cbm_total)
        print(storage_tot)
        product = self.env['product.product'].search([('name', '=', 'delivery service')])
        vals = [0, 0, {
            'name': product.name,
            'product_id': product.id,
            'quantity': quantt_tot,
            'price_unit': product.list_price,
            'x_cbm': cbm_total,
            'storage_fee': storage_tot,
        }]
        return vals
    
    def _construct_valuesstorage(self):
        cbm_total = 0
        storage_tot = 0
        quantt_tot = 0
        for cbm in self.move_ids_without_package:
            cbm_total += float(cbm.x_cbm)
            storage_tot += float(cbm.storage_fee)
            if not cbm.inv_meth:
                quantt_tot = self.noofdays
            else:
                quantt_tot += float(cbm.quantt) * float(self.noofdays)
            # cbm['cbm_tot'] = cbm_total
        print(cbm_total)
        print(storage_tot)
        product = self.env['product.product'].search([('name', '=', 'storage service')])
        vals = [0, 0, {
            'name': product.name,
            'product_id': product.id,
            'quantity': quantt_tot,
            'price_unit': product.list_price,
            'x_cbm': cbm_total,
            'storage_fee': storage_tot,
        }]
        return vals


    def _construct_valuescbm(self):
        cbm_total = 0
        storage_tot = 0
        quantt_tot = 0
#        invoices = self.env['stock.move'].search([('inv_meth', '=', 'cbm')])
#        for cbm in invoices:
#            cbm_total += float(cbm.x_cbm)
#            storage_tot += float(cbm.storage_fee)
#            quantt_tot += float(cbm.quantt)

            # cbm['cbm_tot'] = cbm_total
#        print(cbm_total)
#        print(storage_tot)
        for rec in self.move_ids_without_package:
 #           invoices = rec.move_ids_without_package
            if rec.inv_meth == 'cbm':
#                for cbm in invoices:
                    cbm_total += float(rec.x_cbm)
                    storage_tot += float(rec.storage_fee)
                    quantt_tot += float(rec.quantt)
 
        product = self.env['product.product'].search([('name', '=', 'service cbm')])
        vals = [0, 0, {
            'name': product.name,
            'product_id': product.id,
            'quantity': quantt_tot,
            'price_unit': product.lst_price,
            'x_cbm' : cbm_total,
            'storage_fee' : storage_tot,

        }]
        return vals
    def _construct_valuespallet(self):
        cbm_total = 0
        storage_tot = 0
        quantt_tot = 0
        pallet = 0
#        invoices = self.env['stock.move'].search([('inv_meth', '=', 'pallet')])
#        for cbm in invoices:
#            cbm_total += float(cbm.x_cbm)
#            storage_tot += float(cbm.storage_fee)
#            quantt_tot += float(cbm.quantt)

            # cbm['cbm_tot'] = cbm_total
#        print(cbm_total)
#        print(storage_tot)
        for rec in self.move_ids_without_package:
#            invoices = rec.move_ids_without_package
            if rec.inv_meth == 'pallet':
#                for cbm in invoices:
                cbm_total += float(rec.x_cbm)
                storage_tot += float(rec.storage_fee)
                quantt_tot += float(rec.quantt)
 

        product = self.env['product.product'].search([('name', '=', 'service pallet')])
        vals = [0, 0, {
            'name': product.name,
            'product_id': product.id,
            'quantity': self.count,
            'price_unit': product.lst_price,
#            'x_cbm' : cbm_total,
            'storage_fee' : storage_tot,

        }]
        return vals

    def _construct_valuescarton(self):
        cbm_total = 0
        storage_tot = 0
        quantt_tot = 0
#        invoices = self.env['stock.move'].search([('inv_meth', '=', 'carton_units')])
#        for cbm in invoices:
#            cbm_total += float(cbm.x_cbm)
#            storage_tot += float(cbm.storage_fee)
#            quantt_tot += float(cbm.quantt)

            # cbm['cbm_tot'] = cbm_total
#        print(cbm_total)
#        print(storage_tot)
        for rec in self.move_ids_without_package:
     #       invoices = rec.move_ids_without_package
            if rec.inv_meth == 'carton_units':
     #           for cbm in invoices:
                cbm_total += float(rec.x_cbm)
                storage_tot += float(rec.storage_fee)
                quantt_tot += float(rec.quantt)


        product = self.env['product.product'].search([('name', '=', 'service carton')])

        vals = [0, 0, {
            'name': product.name,
            'product_id': product.id,
            'quantity': quantt_tot,
            'price_unit': product.lst_price,
            'x_cbm' : cbm_total,
            'storage_fee' : storage_tot,

        }]
        return vals
    def _construct_valuesweight(self):
        cbm_total = 0
        storage_tot = 0
        quantt_tot = 0
#        invoices = self.env['stock.move'].search([('inv_meth', '=', 'weight')])
#        for cbm in invoices:
#            cbm_total += float(cbm.x_cbm)
#            storage_tot += float(cbm.storage_fee)
#            quantt_tot += float(cbm.quantt)

            # cbm['cbm_tot'] = cbm_total
        for rec in self.move_ids_without_package:
    #        invoices = rec.move_ids_without_package
            if rec.inv_meth == 'weight':
#                for cbm in invoices:
                cbm_total += float(rec.x_cbm)
                storage_tot += float(rec.storage_fee)
                quantt_tot += float(rec.quantt)

        product = self.env['product.product'].search([('name', '=', 'service weight')])
        vals = [0, 0, {
            'name': product.name,
            'product_id': product.id,
            'quantity': quantt_tot,
            'price_unit': product.lst_price,
#            'x_cbm' : cbm_total,
            'storage_fee' : storage_tot,

        }]
        return vals

    def _construct_valuescbmstorage(self):
        pack = self.move_line_ids_without_package.search([('inv_meth','=','cbm')]).mapped('location_id.x_pallet')
        print(pack,'pack')
        tot = 0
        for rec in pack:
            vol = rec.dimension
            print(vol)
            tot += int(vol)
        print(tot)
        cbm_total = 0
        storage_tot = 0
        quantt_tot = 0
#        invoices = self.env['stock.move'].search([('inv_meth', '=', 'cbm')])
#        for cbm in invoices:
 #           cbm_total += float(cbm.x_cbm)
 #           storage_tot += float(cbm.storage_fee)
 #           quantt_tot += float(cbm.quantt)

            # cbm['cbm_tot'] = cbm_total
        for rec in self.move_ids_without_package:
    #        invoices = rec.move_ids_without_package
            if rec.inv_meth == 'cbm':
              #  for cbm in invoices:
                cbm_total += float(rec.x_cbm)
                storage_tot += float(rec.storage_fee)
                quantt_tot += float(rec.quantt)
        qty = float(tot) * float(self.noofdays)
        product = self.env['product.product'].search([('name', '=', 'service cbm')])
        vals = [0, 0, {
            'name': product.name,
            'product_id': product.id,
            'quantity': qty,
            'price_unit': product.lst_price,
            'x_cbm': cbm_total,
            'storage_fee': storage_tot,

        }]
        return vals


    def create_invoiceinv(self):
        self.create_inv()
        for picking_id in self:
            for movee in picking_id.move_ids_without_package:
                if movee.inv_meth == 'weight':
                    movee['quantt'] = movee.x_weight_inv
                if movee.inv_meth == 'cbm':
                    movee['quantt'] = movee.x_cbm
                if movee.inv_meth == 'pallet':
                    movee['quantt'] = self.count
                if movee.inv_meth == 'carton_units':
                    movee['quantt'] = movee.quantity_done
                if not movee.inv_meth:
                    movee['quantt'] = 1

            current_user = self.env.uid
            if picking_id.picking_type_id.code == 'outgoing':
                customer_journal_id = picking_id.env['ir.config_parameter'].sudo().get_param(
                    'stock_move_invoice.customer_journal_id') or False
                if not customer_journal_id:
                    raise UserError(_("Please configure the journal from settings"))
                invoice_line_list = []
#                valss = self._construct_valuesdelivery()
#                invoice_line_list.append(valss)
#                print(invoice_line_list)
                weight = 0
                cbm = 0
                pallet = 0
                carton = 0
                noninvoice = 0
                for move_ids in picking_id.move_ids_without_package:
                    if move_ids.inv_meth == 'weight' and weight == 0:
                        valss = self._construct_valuesweight()
                        invoice_line_list.append(valss)
                        weight = 1
                    if move_ids.inv_meth == 'cbm' and cbm == 0:
                        valss = self._construct_valuescbmstorage()
                        invoice_line_list.append(valss)
                        cbm = 1
                    if move_ids.inv_meth == 'pallet' and pallet == 0:
                        valss = self._construct_valuespallet()
                        invoice_line_list.append(valss)
                        pallet = 1
                    if move_ids.inv_meth == 'carton_units' and carton == 0:
                        valss = self._construct_valuescarton()
                        invoice_line_list.append(valss)
                        carton = 1
                    if not move_ids.inv_meth and noninvoice == 0:
                        valss = self._construct_valuesdelivery()
                        invoice_line_list.append(valss)
                        noninvoice = 1
                for move_ids_without_package in picking_id.move_ids_without_package:
                    vals = (0, 0, {
                        'name': move_ids_without_package.description_picking,
                        'product_id': move_ids_without_package.product_id.id,
                        'price_unit': 0,
                        'account_id': move_ids_without_package.product_id.property_account_income_id.id if move_ids_without_package.product_id.property_account_income_id
                        else move_ids_without_package.product_id.categ_id.property_account_income_categ_id.id,
                        #                        'tax_ids': [(6, 0, [picking_id.company_id.account_sale_tax_id.id])],
                        'quantity': 0 ,
                        #'quantity' : move_ids_without_package.quantt if move_ids_without_package.inv_meth else 1,
                        'x_cbm': move_ids_without_package.x_cbm,
                        'start_date':picking_id.scheduled_date,
                        'end_date':picking_id.date_done,
                    })
#                    invoice_line_list.append(vals)
#                    print(invoice_line_list)
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
                    'invoice_type':'delivery',

                })
                return invoice

    def create_billinv(self):
        for picking_id in self:
            for movee in picking_id.move_ids_without_package:
                if movee.inv_meth == 'weight':
                    movee['quantt'] = movee.x_weight_inv
                if movee.inv_meth == 'cbm':
                    movee['quantt'] = movee.x_cbm
                if movee.inv_meth == 'pallet':
                    movee['quantt'] = self.count
                if movee.inv_meth == 'carton_units':
                    movee['quantt'] = movee.quantity_done
                if not movee.inv_meth:
                    movee['quantt'] = 1
            current_user = self.env.uid
            if picking_id.picking_type_id.code == 'incoming':
                vendor_journal_id = picking_id.env['ir.config_parameter'].sudo().get_param(
                    'stock_move_invoice.vendor_journal_id') or False
                if not vendor_journal_id:
                    raise UserError(_("Please configure the journal from the settings."))
                invoice_line_list = []
#                valss = self._construct_valuesreception()
#                invoice_line_list.append(valss)
                weight = 0
                cbm = 0
                pallet = 0
                carton = 0
                noninvoice = 0
                for move_ids in picking_id.move_ids_without_package:
                    if move_ids.inv_meth == 'weight' and weight == 0:
                        valss = self._construct_valuesweight()
                        invoice_line_list.append(valss)
                        weight = 1
                    if move_ids.inv_meth == 'cbm' and cbm == 0:
                        valss = self._construct_valuescbm()
                        invoice_line_list.append(valss)
                        cbm = 1
                    if move_ids.inv_meth == 'pallet' and pallet == 0:
                        valss = self._construct_valuespallet()
                        invoice_line_list.append(valss)
                        pallet = 1
                    if move_ids.inv_meth == 'carton_units' and carton == 0:
                        valss = self._construct_valuescarton()
                        invoice_line_list.append(valss)
                        carton = 1
                    if not move_ids.inv_meth and noninvoice == 0:
                        valss = self._construct_valuesreception()
                        invoice_line_list.append(valss)
                        noninvoice = 1
                for move_ids_without_package in picking_id.move_ids_without_package:
                    vals = (0, 0, {
                        'name': move_ids_without_package.description_picking,
                        'product_id': move_ids_without_package.product_id.id,
                        'price_unit': 0,
                        'account_id': move_ids_without_package.product_id.property_account_income_id.id if move_ids_without_package.product_id.property_account_income_id
                        else move_ids_without_package.product_id.categ_id.property_account_income_categ_id.id,
                        #                       'tax_ids': [(6, 0, [picking_id.company_id.account_purchase_tax_id.id])],
                        'quantity': 0,
                        #'quantity': move_ids_without_package.quantt if move_ids_without_package.inv_meth else 1,
                        'x_cbm': move_ids_without_package.x_cbm,
                        'start_date':picking_id.scheduled_date,
                        'end_date':picking_id.date_done,

                     })
#                    invoice_line_list.append(vals)
#                print(invoice_line_list)
                invoice = picking_id.env['account.move'].create({
                    'type': 'out_invoice',
                    'invoice_origin': picking_id.name,
                    'invoice_user_id': current_user,
                    'narration': picking_id.name,
                    'partner_id': picking_id.partner_id.id,
                    'currency_id': picking_id.env.user.company_id.currency_id.id,
                    'journal_id': int(vendor_journal_id),
                    'invoice_payment_ref': picking_id.name,
                    'picking_id': picking_id.id,
                    'invoice_line_ids': invoice_line_list,
                    'invoice_type':'reception',

                })
                return invoice

    #  @api.model
    def trig_inv_month(self):
        print("[[[[[[[[[[[[]]]]]]]]]]]]")
        for res in self.env['stock.picking'].search([('state', '=', 'done')]):
            print("::::::::::::::::::::::::::::::::::::::::::::::::")
            res.create_inv()

    # @api.model
    def create_inv(self):
        for picking_id in self:
            print("picking idddddddddddddddddd")
            print(picking_id)
            crnt_mnth = date.today().month
            print(crnt_mnth)
            today = datetime.today().date()
            first_da = today.replace(day=1)
            first_day = datetime.strptime(str(first_da), '%Y-%m-%d').strftime('%Y-%m-%d %H:%M:%S')
            print(first_da)
            print(first_day)
            last_da = today
            last_day = datetime.strptime(str(last_da), '%Y-%m-%d').strftime('%Y-%m-%d %H:%M:%S')
            print(last_da)
            print(last_day)
            print(picking_id.date_done, "fffffffffffffffff")

            if picking_id.scheduled_date < parser.parse(first_day):
                for pic in picking_id.move_ids_without_package:
                    pic.start_date = first_day
                    print(pic.start_date)
                    pic.end_date = last_day
                    print(pic.end_date)
                    pic.x_days = str((pic.end_date - pic.start_date).days)
                    print(pic.x_days)
            else:
                for pic in picking_id.move_ids_without_package:
                    pic.start_date = picking_id.date_done
                    print(pic.start_date)
                    pic.end_date = last_day
                    print(pic.end_date)
                    pic.x_days = str((pic.end_date - pic.start_date).days)
            
            for movee in picking_id.move_ids_without_package:
               # movee.x_days = self.x_days
                if movee.inv_meth == 'weight':
                    movee['quantt'] = float(movee.x_weight_inv) * float(picking_id.noofdays)
                if movee.inv_meth == 'cbm':
                    movee['quantt'] = float(movee.x_cbm) * float(picking_id.noofdays)
                if movee.inv_meth == 'pallet':
                    movee['quantt'] = float(self.count) * float(picking_id.noofdays)
                if movee.inv_meth == 'carton_units':
                    movee['quantt'] = float(movee.quantity_done) * float(picking_id.noofdays)
                if not movee.inv_meth:
                    movee['quantt'] = 1
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
                for move_ids in picking_id.move_ids_without_package:
                    if move_ids.inv_meth == 'weight' and weight == 0:
                        valss = self._construct_valuesweight()
                        invoice_line_list.append(valss)
                        weight = 1
                    if move_ids.inv_meth == 'cbm' and cbm == 0:
                        #valss = self._construct_valuescbm()
                        valss = self._construct_valuescbmstorage()
                        invoice_line_list.append(valss)
                        cbm = 1
                    if move_ids.inv_meth == 'pallet' and pallet == 0:
                        valss = self._construct_valuespallet()
                        invoice_line_list.append(valss)
                        pallet = 1
                    if move_ids.inv_meth == 'carton_units' and carton == 0:
                        valss = self._construct_valuescarton()
                        invoice_line_list.append(valss)
                        carton = 1
                    if not move_ids.inv_meth and noninvoice == 0:
                        valss = self._construct_valuesstorage()
                        invoice_line_list.append(valss)
                        noninvoice = 1
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
                        'x_cbm': move_ids_without_package.x_cbm,
#                        'start_date':picking_id.scheduled_date,
#                        'end_date':picking_id.date,
                    })
#                    invoice_line_list.append(vals)
#                print(invoice_line_list)
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
                    'invoice_type':'storage',

                })
                return invoice

    @api.constrains('date_done')
    def storage_chrg(self):
        for rec in self.env['stock.picking'].search([('returnpick', '=', 'Delivery of')]):
            print("storage chrgggggggggggggggggggggggggggggggggggggggggggggggg")
            today = datetime.today().date()
            first_da = today.replace(day=1)
            first_day = datetime.strptime(str(first_da), '%Y-%m-%d').strftime('%Y-%m-%d %H:%M:%S')
            if rec.date_done:
                if rec.date_done > parser.parse(first_day):
                    for pic in rec.move_ids_without_package:
                        pic.start_date = rec.date_done
                        print(pic.start_date)
                        pic.end_date = today
                        pic.x_days = (pic.end_date - pic.start_date).days

                else:
                    for pic in rec.move_ids_without_package:
                        pic.start_date = first_day
                        print(pic.start_date)
                        pic.end_date = today
                        pic.x_days = (pic.end_date - pic.start_date).days
