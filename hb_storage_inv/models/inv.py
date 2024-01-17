from dateutil import parser
from odoo import api, models, fields, _
from datetime import datetime, date, timedelta
from odoo.exceptions import AccessError, UserError, ValidationError


class Partnerforminh(models.Model):
    _inherit = "res.partner"

    # last_inv_date = fields.Datetime(string='Last invoice date')
    # inv_end_date = fields.Datetime(string='End Date')

    def trig_inv_monthh1(self):
        print("[[[[[[[[[[[[]]]]]]]]]]]]")
        partner = self.env['res.partner'].search([])
        partner.create_invoice_from_pickinggg1()
        # raise UserError(_("Server is too busy right now. Please wait... "))

    def trig_inv_mon(self):
        print("[[[[[[[[[[[[]]]]]]]]]]]]")
        partner = self.env['res.partner'].search([])
        # partner.create_invoice_from_pickinggg1()
        raise UserError(_("Server is too busy right now. Please wait... "))

    def create_invoice_from_pickinggg1(self):
        for rec in self:
#            if rec.last_inv_date < rec.final_inv_date:
#                raise UserError (_("Invoice has been Generated already for this customer!"))
            s = rec.last_inv_date
            e = rec.inv_end_date
            agreement_id = rec.env['agreement'].search([('partner_id', '=', rec.id)])
            print(agreement_id, 'agreement_id')
            ###IN###
            in_charges = rec.env['agreement.charges'].search(
                ['&', ('charge_type', '=', 'inbound'), ('agreement_id', '=', agreement_id.id)])
            print(in_charges, 'agreement_charges')
            invoice_line_list = []
            invoice_line_liststo = []
            for temp in in_charges:
                if temp.storage_type == False:
                    in_pick_cont = self.env['stock.picking'].search_count([('picking_type_id.code', '=', 'incoming'),
                                                                           ('container', '=', temp.container.id),
                                                                           ('scheduled_date', '>', s), ('partner_id','=',rec.id)])
                    # qty = pick.search_count([('container','=',temp.container.id)])
                    temp_line_values = {
                        'product_id': temp.product_id and temp.product_id.id or False,
                        'name': temp.product_id.name or '',
                        'price_unit': temp.list_price or 0.00,
                        'quantity': in_pick_cont,
                        'currency_id': temp.currency_id.id,
                        'account_id': temp.product_id.property_account_income_id.id if temp.product_id.property_account_income_id
                        else temp.product_id.categ_id.property_account_income_categ_id.id,
                        # 'start_date': move_ids_without_package.start_date,
                        # 'end_date': move_ids_without_package.end_date,

                    }
                    invoice_line_list.append((0, 0, temp_line_values))
            for temp in in_charges:

                if temp.storage_type != False:
                    in_pick_cont_sto = self.env['stock.picking'].search_count(
                        [('picking_type_id.code', '=', 'incoming'),
                         ('container', '=', temp.container.id), ('scheduled_date', '>', s), ('partner_id','=',rec.id),
                         ('product_id.storage_type', '=', temp.storage_type.id)])
                    # qty = pick.search_count([('container','=',temp.container.id)])
                    temp_line_valuessto = {
                        'product_id': temp.product_id and temp.product_id.id or False,
                        'name': temp.product_id.name or '',
                        'price_unit': temp.list_price or 0.00,
                        'quantity': in_pick_cont_sto,
                        'currency_id': temp.currency_id.id,
                        'account_id': temp.product_id.property_account_income_id.id if temp.product_id.property_account_income_id
                        else temp.product_id.categ_id.property_account_income_categ_id.id,
                        # 'start_date': move_ids_without_package.start_date,
                        # 'end_date': move_ids_without_package.end_date,

                    }
                    invoice_line_liststo.append((0, 0, temp_line_valuessto))

                # print(invoice_line_list, 'invoice_line_list')
            ###OUT###
            out_charges = rec.env['agreement.charges'].search(
                ['&', ('charge_type', '=', 'outbound'), ('agreement_id', '=', agreement_id.id)])
            print(out_charges, 'agreement_charges')
            for temp in out_charges:
                if temp.storage_type == False:
                    out_pick_cont = self.env['stock.picking'].search_count(
                        [('picking_type_id.code', '=', 'outgoing'), ('container', '=', temp.container.id),
                         ('scheduled_date', '>', s),  ('partner_id','=',rec.id)])
                    # qty = pick.search_count([('container','=',temp.container.id)])
                    temp_line_values = {
                        'product_id': temp.product_id and temp.product_id.id or False,
                        'name': temp.product_id.name or '',
                        'price_unit': temp.list_price or 0.00,
                        'quantity': out_pick_cont,
                        'currency_id': temp.currency_id.id,
                        'account_id': temp.product_id.property_account_income_id.id if temp.product_id.property_account_income_id
                        else temp.product_id.categ_id.property_account_income_categ_id.id,
                        # 'start_date': move_ids_without_package.start_date,
                        # 'end_date': move_ids_without_package.end_date,

                    }
                    invoice_line_list.append((0, 0, temp_line_values))
                    # print(invoice_line_list, 'invoice_line_list')
            for temp in out_charges:
                if temp.storage_type != False:
                    out_pick_cont_sto = self.env['stock.picking'].search_count(
                        [('picking_type_id.code', '=', 'outgoing'), ('container', '=', temp.container.id),
                         ('scheduled_date', '>', s), ('product_id.storage_type', '=', temp.storage_type.id),  ('partner_id','=',rec.id)])
                    # qty = pick.search_count([('container','=',temp.container.id)])
                    temp_line_valuessto = {
                        'product_id': temp.product_id and temp.product_id.id or False,
                        'name': temp.product_id.name or '',
                        'price_unit': temp.list_price or 0.00,
                        'quantity': out_pick_cont_sto,
                        'currency_id': temp.currency_id.id,
                        'account_id': temp.product_id.property_account_income_id.id if temp.product_id.property_account_income_id
                        else temp.product_id.categ_id.property_account_income_categ_id.id,
                        # 'start_date': move_ids_without_package.start_date,
                        # 'end_date': move_ids_without_package.end_date,

                    }
                    invoice_line_liststo.append((0, 0, temp_line_valuessto))
                    # print(invoice_line_list, 'invoice_line_list')

            ###VALUEADDED###
            added_charges = rec.env['agreement.charges'].search(
                ['&', ('charge_type', '=', 'value_added'), ('agreement_id', '=', agreement_id.id),  ('partner_id','=',rec.id)])
            print(added_charges, 'agreement_charges')
            for temp in added_charges:
                added_pick_count = self.env['stock.picking'].search_count(
                    [('picking_type_id.code', 'in', ['incoming', 'outgoing']),
                     ('added_service', '=', temp.added_service.id), ('scheduled_date', '>', s)])
                # qty = pick.search_count([('container','=',temp.container.id)])
                temp_line_values = {
                    'product_id': temp.product_id and temp.product_id.id or False,
                    'name': temp.product_id.name or '',
                    'price_unit': temp.list_price or 0.00,
                    'quantity': added_pick_count,
                    'currency_id': temp.currency_id.id,
                    'account_id': temp.product_id.property_account_income_id.id if temp.product_id.property_account_income_id
                    else temp.product_id.categ_id.property_account_income_categ_id.id,
                    # 'start_date': move_ids_without_package.start_date,
                    # 'end_date': move_ids_without_package.end_date,

                }
                invoice_line_list.append((0, 0, temp_line_values))
                # print(invoice_line_list, 'invoice_line_list')

                ###INVMANAGEMNET###
                added_charges = rec.env['agreement.charges'].search(
                    ['&', ('charge_type', '=', 'inventory_mgmnt'), ('agreement_id', '=', agreement_id.id),
                     ('partner_id', '=', rec.id)])
                print(added_charges, 'agreement_charges')
                for temp in added_charges:
                    added_pick_count = self.env['stock.picking'].search_count(
                        [('picking_type_id.code', 'in', ['incoming', 'outgoing']),
                         ('scheduled_date', '>', s)])
                    # qty = pick.search_count([('container','=',temp.container.id)])
                    temp_line_values = {
                        'product_id': temp.product_id and temp.product_id.id or False,
                        'name': temp.product_id.name or '',
                        'price_unit': temp.list_price or 0.00,
                        'quantity': 1,
                        'currency_id': temp.currency_id.id,
                        'account_id': temp.product_id.property_account_income_id.id if temp.product_id.property_account_income_id
                        else temp.product_id.categ_id.property_account_income_categ_id.id,
                        # 'start_date': move_ids_without_package.start_date,
                        # 'end_date': move_ids_without_package.end_date,

                    }
                    invoice_line_list.append((0, 0, temp_line_values))

            ###STORAGE###
            storage_charges = rec.env['agreement.charges'].search(
                ['&', ('charge_type', '=', 'storage'), ('agreement_id', '=', agreement_id.id),
                 ('storage_type', '=', False)])
            print(storage_charges, 'agreement_charges', added_charges.storage_type.id)
            quants = self.env['stock.quant'].search(
                [('owner_id', '=', rec.id), ('location_id.usage', 'in', ['internal', 'transit']),
                 # ('in_date', '>=', s),
                 ('quantity', '>', 0)
                 ])
            quantsss = self.env['stock.quant'].search(
                [('owner_id', '=', rec.id), ('location_id.usage', 'in', ['internal', 'transit']),
                 # ('in_date', '>=', s),
                 ('quantity', '>', 0), ('product_id.storage_type','!=',False)
                 ])
            quantityy = 0
            pallets = 0
            cbmm = 0
            weightt = 0
            squaree = 0
            for quant in quants:
                print(quant, rec.id, quant.quantity, quant.location_id.usage, '------------quant--------------')
                prod_moves = self.env['stock.move.line'].search(
                    [('lot_id', '=', quant.lot_id.id), ('picking_code', '=', 'incoming'), ('start_date', '>=', s),
                     ('state', '=', 'done')])
                quantityy += quant.quantity
                print(quantityy, 'quantityy')
                # pallett = (prod_moves.mapped('result_package_id')).id
                # print(pallett, 'pallett')
                # if pallet:
                #     pallet = len(pallett)
                # else:
                #     pallet = 0
                quantity = 0
                cbm = 0
                weight = 0
                square = 0
                squantity = 0
                pallet = 0
                for pmoves in prod_moves:
                    ee = datetime.strptime(str(e), '%Y-%m-%d %H:%M:%S')
                    ss = datetime.strptime(str(s), '%Y-%m-%d %H:%M:%S')
                    fduration = (abs(ee - ss)).days
                    durtion = (abs(ee - pmoves.start_date)).days
                    if durtion < fduration:
                        durr = durtion
                    else:
                        durr = fduration
                    if durr < 1:
                        dur = 1
                    else:
                        dur = durr

                    if pmoves.picking_code != 'outgoing' and not pmoves.product_id.storage_type:
                        print(dur, quantityy, '-------------------dur, quantityy---------------move lines')
                        cbm += pmoves.move_id.x_volume * quantityy
                        quantity += pmoves.qty_done * quantityy
                        weight += pmoves.move_id.x_weight * quantityy
                        square += (pmoves.move_id.x_length * pmoves.move_id.x_breadth)  * quantityy
                        pallet += quantityy
                cbmm += cbm * dur
                weightt += weight * dur
                squaree += square * dur
                pallets = pallet * dur
            print(cbmm, weightt, squaree, pallets, '-------------------------cbmm, weightt, squaree, pallets,-------------------------')
            for temp in storage_charges:
                if temp.charge_type == 'storage' and temp.charge_unit_type == 'cbm':
                    temp_line_values = {
                        'product_id': temp.product_id and temp.product_id.id or False,
                        'name': temp.product_id.name or '',
                        'price_unit': temp.list_price or 0.00,
                        'quantity': cbmm,
                        'currency_id': temp.currency_id.id,
                        'account_id': temp.product_id.property_account_income_id.id if temp.product_id.property_account_income_id
                        else temp.product_id.categ_id.property_account_income_categ_id.id,
                        # 'start_date': move_ids_without_package.start_date,
                        # 'end_date': move_ids_without_package.end_date,

                    }
                    invoice_line_list.append((0, 0, temp_line_values))
                    print(temp_line_values, '-------------------------------cbm------------------------------------')

                if temp.charge_type == 'storage' and temp.charge_unit_type == 'weight':
                    temp_line_values = {
                        'product_id': temp.product_id and temp.product_id.id or False,
                        'name': temp.product_id.name or '',
                        'price_unit': temp.list_price or 0.00,
                        'quantity': weightt,
                        'currency_id': temp.currency_id.id,
                        'account_id': temp.product_id.property_account_income_id.id if temp.product_id.property_account_income_id
                        else temp.product_id.categ_id.property_account_income_categ_id.id,
                        # 'start_date': move_ids_without_package.start_date,
                        # 'end_date': move_ids_without_package.end_date,

                    }
                    invoice_line_list.append((0, 0, temp_line_values))
                    print(temp_line_values, '---------------------------weight----------------------------')

                if temp.charge_type == 'storage' and temp.charge_unit_type == 'square':
                    temp_line_values = {
                        'product_id': temp.product_id and temp.product_id.id or False,
                        'name': temp.product_id.name or '',
                        'price_unit': temp.list_price or 0.00,
                        'quantity': squaree,
                        'currency_id': temp.currency_id.id,
                        'account_id': temp.product_id.property_account_income_id.id if temp.product_id.property_account_income_id
                        else temp.product_id.categ_id.property_account_income_categ_id.id,
                        # 'start_date': move_ids_without_package.start_date,
                        # 'end_date': move_ids_without_package.end_date,

                    }
                    invoice_line_list.append((0, 0, temp_line_values))
                    print(temp_line_values, '---------------------------square--------------------------')

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
                    print(temp_line_values, '------------------------------pallets----------------------')

            ###TEMPSTORAGE###
            tstorage_charges = rec.env['agreement.charges'].search(
                ['&', ('charge_type', '=', 'storage'), ('agreement_id', '=', agreement_id.id),
                 ('storage_type', '!=', False)])
            print(tstorage_charges, 'tstorage_charges')
            for temp in tstorage_charges:
                print('hhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhh')
                temps = self.env['storage.type'].search([('id', '=', temp.storage_type.id)])
                # for stot in temps:
                quantityy = 0
                pallets = 0
                cbmm = 0
                weightt = 0
                squaree = 0
                for quant in quantsss:
                    print(quant, rec.id, quant.quantity, quant.location_id.usage, '------------quant1--------------')

                    prod_moves = self.env['stock.move.line'].search(
                        [('lot_id', '=', quant.lot_id.id), ('picking_code', '=', 'incoming'),
                         # ('start_date', '>=', s),
                         # ('quantity', '>', 0),
                         ('state', '=', 'done'), ('')])
                    ee = datetime.strptime(str(e), '%Y-%m-%d %H:%M:%S')
                    ss = datetime.strptime(str(s), '%Y-%m-%d %H:%M:%S')
                    quantity = 0
                    cbm = 0
                    weight = 0
                    square = 0
                    pallet = 0
                    for pmoves in prod_moves:
                        fduration = (abs(ee - ss)).days
                        durtion = (abs(ee - pmoves.start_date)).days
                        if durtion < fduration:
                            durr = durtion
                        else:
                            durr = fduration
                        if durr < 1:
                            dur = 1
                        else:
                            dur = durr
                        quantityy += quant.quantity

                        if pmoves.picking_code != 'outgoing' and pmoves.product_id.storage_type:
                            print(dur, quantityy, '~~~~~~~~~~~~~~~~~~~~~~~dur, quantityy,~~~~~~~~~~~~~~~~~~~~~~~~~~~' )
                            cbm += pmoves.move_id.x_volume * quantityy
                            quantity += pmoves.qty_done * quantityy
                            weight += pmoves.move_id.x_weight * quantityy
                            square += (pmoves.move_id.x_length * pmoves.move_id.x_breadth)* quantityy
                            pallet += 1 * quantityy
                            print(cbm, weight, square, '~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~cbm, weight, square~~~~~~~~~~~~~~~~~~~~~~')
                    cbmm += cbm * dur
                    weightt += weight * dur
                    squaree += square * dur
                    pallets = pallet * dur
                print(cbmm, weightt, squaree, '~~~~~~~~~~~~~~~~~~~~~~~~cbmm, weightt, squaree~~~~~~~~~~~~~~~~~~~~~~~')
                for temp in tstorage_charges:
                    print('jjjjjjjjjjjjjjjjjjjjjjjjjj')
                    if temp.charge_type == 'storage' and temp.charge_unit_type == 'cbm':
                        print('iiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiii')
                        temp_line_valuessto = {
                            'product_id': temp.product_id and temp.product_id.id or False,
                            'name': temp.product_id.name or '',
                            'price_unit': temp.list_price or 0.00,
                            'quantity': cbmm,
                            'currency_id': temp.currency_id.id,
                            'account_id': temp.product_id.property_account_income_id.id if temp.product_id.property_account_income_id
                            else temp.product_id.categ_id.property_account_income_categ_id.id,
                            # 'start_date': move_ids_without_package.start_date,
                            # 'end_date': move_ids_without_package.end_date,

                        }
                        invoice_line_liststo.append((0, 0, temp_line_valuessto))
                        print(temp_line_valuessto, '~~~~~~~~~~~~~~~~~~~~~~~~~~`cbm~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')

                    if temp.charge_type == 'storage' and temp.charge_unit_type == 'weight':
                        temp_line_valuessto = {
                            'product_id': temp.product_id and temp.product_id.id or False,
                            'name': temp.product_id.name or '',
                            'price_unit': temp.list_price or 0.00,
                            'quantity': weightt,
                            'currency_id': temp.currency_id.id,
                            'account_id': temp.product_id.property_account_income_id.id if temp.product_id.property_account_income_id
                            else temp.product_id.categ_id.property_account_income_categ_id.id,
                            # 'start_date': move_ids_without_package.start_date,
                            # 'end_date': move_ids_without_package.end_date,

                        }
                        invoice_line_liststo.append((0, 0, temp_line_valuessto))
                        print(temp_line_valuessto, '~~~~~~~~~~~~~~~~~~~~~~~weight~~~~~~~~~~~~~~~~~~~~~~')

                    if temp.charge_type == 'storage' and temp.charge_unit_type == 'square':
                        temp_line_valuessto = {
                            'product_id': temp.product_id and temp.product_id.id or False,
                            'name': temp.product_id.name or '',
                            'price_unit': temp.list_price or 0.00,
                            'quantity': squaree,
                            'currency_id': temp.currency_id.id,
                            'account_id': temp.product_id.property_account_income_id.id if temp.product_id.property_account_income_id
                            else temp.product_id.categ_id.property_account_income_categ_id.id,
                            # 'start_date': move_ids_without_package.start_date,
                            # 'end_date': move_ids_without_package.end_date,

                        }
                        invoice_line_liststo.append((0, 0, temp_line_valuessto))
                        print(temp_line_valuessto, '~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~square~~~~~~~~~~~~~~~~~~~~')

                    if temp.charge_type == 'storage' and temp.charge_unit_type == 'pallet':
                        temp_line_valuessto = {
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
                        invoice_line_liststo.append((0, 0, temp_line_valuessto))
                        print(temp_line_valuessto, '~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~pallets~~~~~~~~~~~~~~~~~~~~~~~~')

            current_user = self.env.uid
            if agreement_id and invoice_line_list:
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
                print(invoice,invoice_line_list, 'Invoice Created')
                # rec['final_inv_date'] = rec.inv_end_date
            if agreement_id and invoice_line_liststo:
                invoicee = rec.env['account.move'].create({
                    'type': 'out_invoice',
                    'invoice_origin': rec.name,
                    'invoice_user_id': current_user,
                    'narration': rec.name,
                    'partner_id': rec.id,
                    'currency_id': rec.env.user.company_id.currency_id.id,
                    # 'journal_id': int(customer_journal_id),
                    'invoice_payment_ref': rec.name,
                    # 'picking_id': picking_id.id,
                    'invoice_line_ids': invoice_line_liststo,
                    # 'invoice_type': 'storage',
                    'name': '/',

                })

                print(invoicee, invoice_line_liststo, 'Invoiceesto Created')
                # rec['final_inv_date'] = rec.inv_end_date

                # rec.inv_gen_date()
                # return invoice

    def create_invoice_from_pickinggg11(self):
        for rec in self:
            print('-------------Storage Invoice Running--------------')
            quants = self.env['stock.quant'].search([('owner_id', '=', rec.id), ('location_id.usage', '=', 'internal')])
            quantityy = 0
            pallet = 0
            cbmm = 0
            weightt = 0
            squaree = 0
            agreement_id = rec.env['agreement'].search([('partner_id', '=', rec.id)])
            print(agreement_id, 'agreement_id')
            agreement_charges = rec.env['agreement.charges'].search(
                ['&', ('charge_type', '=', 'storage'), ('agreement_id', '=', agreement_id.id)])
            print(agreement_charges, 'agreement_charges')
            for quant in quants:
                print(quant, rec.id, quant.inventory_quantity, quant.quantity, quant.location_id.usage, 'quant')
                prod_moves = self.env['stock.move.line'].search(
                    [('lot_id', '=', quant.lot_id.id), ('picking_code', '!=', 'outcoming')])
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
                squantity = 0
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
                    test_durr = abs(datetime.today() - pmoves.start_date).days
                    if test_durr == 0:
                        test_dur = 1
                    else:
                        test_dur = test_durr
                    fixed_dur = abs(today - begin_day).days
                    print(test_dur, 'test_dur', 'fixed_dur', fixed_dur)
                    print('-------------Storage Invoice Running--------------')
                    if test_dur <= fixed_dur:
                        dur = test_dur
                    else:
                        dur = fixed_dur
                    print(prod_moves.lot_id.name, 'lottttttttttt', quantityy, dur)
                    if pmoves.picking_code != 'outgoing' and not pmoves.product_id.storage_type:
                        print(
                            '&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&')
                        cbm += pmoves.move_id.x_volume * dur * quantityy
                        quantity += pmoves.qty_done * dur * quantityy
                        weight += pmoves.move_id.x_weight * dur * quantityy
                        square += (pmoves.move_id.x_length * pmoves.move_id.x_breadth) * dur * quantityy
                        pallet += 0 * dur * quantityy
                    print(cbm, quantity, weight, square, pallet, '%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%')
                print(cbm, quantity, weight, square, pallet, '%%%%%%%%%%555555555555555555555555555%%%%%%%')

                cbmm += cbm
                weightt += weight
                squaree += square
                pallets = pallet

            print(cbmm, weightt, squaree, '##############################################')

            invoice_line_list = []
            for temp in agreement_id.charge_lines.search([('agreement_id', '=', agreement_id.id)]):
                print(temp.charge_type, 'temp.charge_typ')
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

                for quant in quants:
                    prod_moves = self.env['stock.move.line'].search(
                        [('lot_id', '=', quant.lot_id.id), ('picking_code', '!=', 'outcoming')])
                    print(prod_moves, 'prod_moves')
                    # if temp.charge_type == 'storage' and temp.storage_charge == '':
                    ##############storage###########################
                    if temp.charge_type == 'storage' and temp.charge_unit_type == 'cbm':
                        temp_line_values = {
                            'product_id': temp.product_id and temp.product_id.id or False,
                            'name': temp.product_id.name or '',
                            'price_unit': temp.list_price or 0.00,
                            'quantity': cbmm,
                            'currency_id': temp.currency_id.id,
                            'account_id': temp.product_id.property_account_income_id.id if temp.product_id.property_account_income_id
                            else temp.product_id.categ_id.property_account_income_categ_id.id,
                            # 'start_date': move_ids_without_package.start_date,
                            # 'end_date': move_ids_without_package.end_date,

                        }
                        invoice_line_list.append((0, 0, temp_line_values))
                        print(temp_line_values, 'mmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmm')
                        break
                    if temp.charge_type == 'storage' and temp.charge_unit_type == 'weight':
                        temp_line_values = {
                            'product_id': temp.product_id and temp.product_id.id or False,
                            'name': temp.product_id.name or '',
                            'price_unit': temp.list_price or 0.00,
                            'quantity': weightt,
                            'currency_id': temp.currency_id.id,
                            'account_id': temp.product_id.property_account_income_id.id if temp.product_id.property_account_income_id
                            else temp.product_id.categ_id.property_account_income_categ_id.id,
                            # 'start_date': move_ids_without_package.start_date,
                            # 'end_date': move_ids_without_package.end_date,

                        }
                        invoice_line_list.append((0, 0, temp_line_values))
                        print(temp_line_values, 'mmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmm')
                        break
                    if temp.charge_type == 'storage' and temp.charge_unit_type == 'square':
                        temp_line_values = {
                            'product_id': temp.product_id and temp.product_id.id or False,
                            'name': temp.product_id.name or '',
                            'price_unit': temp.list_price or 0.00,
                            'quantity': squaree,
                            'currency_id': temp.currency_id.id,
                            'account_id': temp.product_id.property_account_income_id.id if temp.product_id.property_account_income_id
                            else temp.product_id.categ_id.property_account_income_categ_id.id,
                            # 'start_date': move_ids_without_package.start_date,
                            # 'end_date': move_ids_without_package.end_date,

                        }
                        invoice_line_list.append((0, 0, temp_line_values))
                        print(temp_line_values, 'mmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmm')
                        break
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
                        print(temp_line_values, 'mmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmm')
                        break

                    ###########Temperature control###################
                    if temp.charge_type == 'storage' and temp.charge_unit_type == 'cbm' and temp.storage_type:
                        bla = 0
                        for prod in prod_moves.search([('product_id.storage_type', '=', temp.storage_type.id)]):
                            print(prod, prod.picking_id, prod.start_date, datetime.today())
                            print(prod.picking_id, 'apdyaaaaaaaaaaaaaaaaaa')
                            test_durr = abs(datetime.today() - prod.start_date).days
                            print(prod.picking_id)
                            print(prod.picking_id)
                            if test_durr == 0:
                                test_dur = 1
                            else:
                                test_dur = test_durr
                            fixed_dur = abs(today - begin_day).days
                            print(test_dur, 'test_dur', 'fixed_dur', fixed_dur)
                            print('-------------Storage Invoice Running--------------')
                            if test_dur <= fixed_dur:
                                dur = test_dur
                            else:
                                dur = fixed_dur
                            print('prod-------------------------------------------', prod.product_id.storage_type,
                                  temp.storage_type)
                            if prod.product_id.storage_type == temp.storage_type:
                                print('prodif-------------------------------------------', prod.picking_id, prod)
                                bla += prod.move_id.x_volume * dur * quantityy
                                print(bla, prod.move_id.x_volume, dur, quantityy, 'ding')
                        temp_line_values = {
                            'product_id': temp.product_id and temp.product_id.id or False,
                            'name': temp.product_id.name or '',
                            'price_unit': temp.list_price or 0.00,
                            'quantity': bla,
                            'currency_id': temp.currency_id.id,
                            'account_id': temp.product_id.property_account_income_id.id if temp.product_id.property_account_income_id
                            else temp.product_id.categ_id.property_account_income_categ_id.id,
                            # 'start_date': move_ids_without_package.start_date,
                            # 'end_date': move_ids_without_package.end_date,

                        }
                        invoice_line_list.append((0, 0, temp_line_values))
                        print(temp_line_values, 'ssssssssssssssssssssssssssssssssssssss')
                        break

                    if temp.charge_type == 'storage' and temp.charge_unit_type == 'weight' and temp.storage_type:
                        bla = 0
                        for prod in prod_moves.search([('product_id.storage_type', '=', temp.storage_type.id)]):
                            print(prod.picking_id, 'apdyaaaaaaaaaaaaaaaaaa')
                            test_durr = abs(datetime.today() - prod.start_date).days
                            print(prod.picking_id)
                            print(prod.picking_id)
                            if test_durr == 0:
                                test_dur = 1
                            else:
                                test_dur = test_durr
                            fixed_dur = abs(today - begin_day).days
                            print(test_dur, 'test_dur', 'fixed_dur', fixed_dur)
                            print('-------------Storage Invoice Running--------------')
                            if test_dur <= fixed_dur:
                                dur = test_dur
                            else:
                                dur = fixed_dur
                            print('prod-------------------------------------------', prod.product_id.storage_type,
                                  temp.storage_type)
                            if prod.product_id.storage_type == temp.storage_type:
                                print('prodif-------------------------------------------', prod.picking_id, prod)
                                bla += prod.qty_done * dur * quantityy

                        temp_line_values = {
                            'product_id': temp.product_id and temp.product_id.id or False,
                            'name': temp.product_id.name or '',
                            'price_unit': temp.list_price or 0.00,
                            'quantity': bla,
                            'currency_id': temp.currency_id.id,
                            'account_id': temp.product_id.property_account_income_id.id if temp.product_id.property_account_income_id
                            else temp.product_id.categ_id.property_account_income_categ_id.id,
                            # 'start_date': move_ids_without_package.start_date,
                            # 'end_date': move_ids_without_package.end_date,

                        }
                        invoice_line_list.append((0, 0, temp_line_values))
                        print(temp_line_values, 'ssssssssssssssssssssssssssssssssssssss')
                        break
                    if temp.charge_type == 'storage' and temp.charge_unit_type == 'square' and temp.storage_type:
                        bla = 0
                        for prod in prod_moves.search([('product_id.storage_type', '=', temp.storage_type.id)]):
                            print(prod.picking_id, 'apdyaaaaaaaaaaaaaaaaaa')
                            print(prod.picking_id, 'apdyaaaaaaaaaaaaaaaaaa')
                            test_durr = abs(datetime.today() - prod.start_date).days
                            print(prod.picking_id)
                            print(prod.picking_id)
                            print(prod.picking_id)
                            if test_durr == 0:
                                test_dur = 1
                            else:
                                test_dur = test_durr
                            fixed_dur = abs(today - begin_day).days
                            print(test_dur, 'test_dur', 'fixed_dur', fixed_dur)
                            print('-------------Storage Invoice Running--------------')
                            if test_dur <= fixed_dur:
                                dur = test_dur
                            else:
                                dur = fixed_dur
                            print('prod-------------------------------------------', prod.product_id.storage_type,
                                  temp.storage_type)
                            if prod.product_id.storage_type == temp.storage_type:
                                print('prodif-------------------------------------------', prod.picking_id, prod)
                                bla += (prod.move_id.x_length * prod.move_id.x_breadth) * dur * quantityy

                        temp_line_values = {
                            'product_id': temp.product_id and temp.product_id.id or False,
                            'name': temp.product_id.name or '',
                            'price_unit': temp.list_price or 0.00,
                            'quantity': bla,
                            'currency_id': temp.currency_id.id,
                            'account_id': temp.product_id.property_account_income_id.id if temp.product_id.property_account_income_id
                            else temp.product_id.categ_id.property_account_income_categ_id.id,
                            # 'start_date': move_ids_without_package.start_date,
                            # 'end_date': move_ids_without_package.end_date,

                        }
                        invoice_line_list.append((0, 0, temp_line_values))
                        print(temp_line_values, 'ssssssssssssssssssssssssssssssssssssss')
                        break
                    if temp.charge_type == 'storage' and temp.charge_unit_type == 'pallet' and temp.storage_type:
                        bla = 0
                        for prod in prod_moves.search([('product_id.storage_type', '=', temp.storage_type.id)]):
                            print(prod.picking_id, 'apdyaaaaaaaaaaaaaaaaaa')
                            test_durr = abs(datetime.today() - prod.start_date).days
                            print(prod.picking_id)
                            print(prod.picking_id)
                            if test_durr == 0:
                                test_dur = 1
                            else:
                                test_dur = test_durr
                            fixed_dur = abs(today - begin_day).days
                            print(test_dur, 'test_dur', 'fixed_dur', fixed_dur)
                            print('-------------Storage Invoice Running--------------')
                            if test_dur <= fixed_dur:
                                dur = test_dur
                            else:
                                dur = fixed_dur
                            print('prod-------------------------------------------', prod.product_id.storage_type,
                                  temp.storage_type)
                            if prod.product_id.storage_type == temp.storage_type:
                                print('prodif-------------------------------------------', prod.picking_id, prod)
                                bla += 0 * dur * quantityy
                                print(bla, prod.move_id.x_volume, dur, quantityy, 'ding')
                        temp_line_values = {
                            'product_id': temp.product_id and temp.product_id.id or False,
                            'name': temp.product_id.name or '',
                            'price_unit': temp.list_price or 0.00,
                            'quantity': bla,
                            'currency_id': temp.currency_id.id,
                            'account_id': temp.product_id.property_account_income_id.id if temp.product_id.property_account_income_id
                            else temp.product_id.categ_id.property_account_income_categ_id.id,
                            # 'start_date': move_ids_without_package.start_date,
                            # 'end_date': move_ids_without_package.end_date,

                        }
                        invoice_line_list.append((0, 0, temp_line_values))
                        print(temp_line_values, 'ssssssssssssssssssssssssssssssssssssss')
                        break

            pick = self.env['stock.picking'].search([('partner_id', '=', rec.id), ('state', '=', 'done')])
            for temp in agreement_id.charge_lines:
                if temp.charge_type == 'inbound':
                    for picking_id in pick:
                        print('temp.product_id', temp.product_id, 'agreement irukkkkkkkkkkkkkk')
                        print(
                            '----------------------------------------------------------temp-------------------------------------',
                            temp.charge_type)
                        qty = pick.search_count([('container', '=', temp.container.id)])
                        print(qty)
                        temp_line_values = {
                            'product_id': temp.product_id and temp.product_id.id or False,
                            'name': temp.product_id.name or '',
                            'price_unit': temp.list_price or 0.00,
                            'quantity': qty,
                            'currency_id': temp.currency_id.id,
                            'account_id': temp.product_id.property_account_income_id.id if temp.product_id.property_account_income_id
                            else temp.product_id.categ_id.property_account_income_categ_id.id,
                            # 'start_date': move_ids_without_package.start_date,
                            # 'end_date': move_ids_without_package.end_date,

                        }
                        invoice_line_list.append((0, 0, temp_line_values))
                        print(temp_line_values, temp)
                        break

                if temp.charge_type == 'outbound':
                    for picking_id in pick:
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
                            break

                if temp.charge_type == 'value_added':
                    for picking_id in pick:
                        if temp.added_service == picking_id.added_service:
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
                            break

                    # break
                # break
            # break

            # if temp.charge_type == 'value_added':
            #     print('invvvvvvvvvvv')
            #     if temp.added_service == picking_id.added_service:
            #         print('vanthennn')
            #         temp_line_values = {
            #             'product_id': temp.product_id and temp.product_id.id or False,
            #             'name': temp.product_id.name or '',
            #             'price_unit': temp.list_price or 0.00,
            #             'quantity': '1',
            #             'currency_id': temp.currency_id.id,
            #             'account_id': temp.product_id.property_account_income_id.id if temp.product_id.property_account_income_id
            #             else temp.product_id.categ_id.property_account_income_categ_id.id,
            #             # 'start_date': move_ids_without_package.start_date,
            #             # 'end_date': move_ids_without_package.end_date,
            #
            #         }
            #         invoice_line_list.append((0, 0, temp_line_values))

            print(invoice_line_list, 'invoice_line_list')
            current_user = self.env.uid
            if agreement_id and invoice_line_list:
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
                    # 'name': '/',

                })
                print(invoice, 'Invoice Created')
                # return invoice


class StockpickingInhINVinh(models.Model):
    _inherit = 'stock.picking'

    ###### IN INVOICE ##########
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
                        if temp.charge_type == 'value_added':
                            print('invvvvvvvvvvv')
                            if temp.added_service == picking_id.added_service:
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

    ###### Out Invoice #########
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
                    if temp.charge_type == 'value_added':
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
