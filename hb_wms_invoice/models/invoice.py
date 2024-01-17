from dateutil import parser
from odoo import api, models, fields, http, _
from datetime import datetime, date, timedelta
from odoo.exceptions import AccessError, UserError, ValidationError
import logging
logger = logging.getLogger(__name__)


class AccountMove(models.Model):
    _inherit = "account.move"

    def consolidate_invoice_lines(self, invoice):
        product_quantities = {}

        for line in invoice.invoice_line_ids:
            product_id = line.product_id.id
            quantity = line.quantity

            if product_id in product_quantities:
                product_quantities[product_id] += quantity
            else:
                product_quantities[product_id] = quantity

        invoice.invoice_line_ids.unlink()
        for product_id, quantity in product_quantities.items():
            product = self.env['product.product'].browse(product_id)
            invoice.invoice_line_ids.create({
                'product_id': product_id,
                'name': product.name,
                'quantity': quantity,
                'price_unit': product.list_price,
                'invoice_id': invoice.id,
            })

        # consolidate_invoice_lines(invoice_id)


    # Assuming you have the invoice object (invoice_id) available, you can call the function like this:
    # consolidate_invoice_lines(invoice_id)


class Partnerforminherit(models.Model):
    _inherit = "res.partner"

    def create_inv_invoice(self):
        for partner in self:
            s = partner.last_inv_date
            e = partner.inv_end_date
            ee = datetime.strptime(str(e), '%Y-%m-%d %H:%M:%S')
            ss = datetime.strptime(str(s), '%Y-%m-%d %H:%M:%S')
            agreement_id = partner.env['agreement'].search([('partner_id', '=', partner.id)])
            storage_charges = partner.env['agreement.charges'].search(
                ['&', ('charge_type', '=', 'storage'), ('agreement_id', '=', agreement_id.id),
                 ('storage_type', '=', False)])
            quantity_dict = {}
            charge_unit_types = []
            for c in storage_charges:
                if c.charge_unit_type:
                    charge_unit_types.append(c.charge_unit_type)
            values_except_custom = list(filter(lambda x: x != 'custom', charge_unit_types))
            print(values_except_custom)
            charge_unit_type = values_except_custom[0]
            print(charge_unit_types, charge_unit_type)
            uoms = []
            for u in storage_charges:
                if u.uom_id:
                    uoms.append(u.uom_id.id)
            print(uoms)
            inven = self.env['product.summary'].search(
                [('partner_id', '=', partner.id), ('quantity', '>', 0), ('storage_product', '=', False)])
            cbm = 0
            weight = 0
            sq = 0
            pallet = 0
            invoice_line_list = []
            summary_lines = []
            tsummary_lines = []

            if uoms:
                for uom in uoms:
                    print('uom---------------------')
                    quantity_dict[uom] = 0
                    for inv in inven:
                        print('inv---------------------', uom, inv.uom_id.id)
                        if uom == inv.uom_id.id:
                            # ###print(inv.in_date, s, 'indate', inv.out_date, e, 'outdate')
                            if inv.in_date != False and inv.out_date != False and e >= inv.in_date >= s and s <= inv.out_date <= e and inv.storage_product == False:
                                quantity_dict[uom] += inv.quantity * inv.duration
                                print(inv.product_id.prod_volume, 'inv.product_id.prod_volume', inv.quantity,
                                      'inv.quantity', )
                                summ = ({
                                    'start_date': inv.in_date,
                                    'end_date': inv.out_date,
                                    'quantity': inv.quantity,
                                    'charge_type': 'storage',
                                    'product_id': inv.product_id.id,
                                    'charge_unit_type': 'custom',
                                })
                                summ_lines = self.env['summary.sheet.lines'].create(summ)
                                if summ_lines.quantity > 0:
                                    summary_lines.append(summ_lines)
                            elif inv.in_date != False and e >= inv.in_date >= s and inv.out_date == False and inv.storage_product == False:
                                duration = (abs((fields.Datetime.to_datetime(e)
                                                 - fields.Datetime.to_datetime(inv.in_date)).days) + 1)
                                quantity_dict[uom] += inv.quantity * duration
                                print(inv.product_id.prod_volume, 'inv.product_id.prod_volume', inv.quantity,
                                      'inv.quantity', )
                                summ = ({
                                    'start_date': inv.in_date,
                                    'end_date': e,
                                    'quantity': inv.quantity,
                                    'charge_type': 'storage',
                                    'product_id': inv.product_id.id,
                                    'charge_unit_type': 'custom',

                                })
                                summ_lines = self.env['summary.sheet.lines'].create(summ)
                                if summ_lines.quantity > 0:
                                    summary_lines.append(summ_lines)
                            elif inv.in_date != False and e >= inv.in_date <= s and s <= inv.out_date <= e and inv.storage_product == False:
                                duration = (abs((fields.Datetime.to_datetime(inv.out_date)
                                                 - fields.Datetime.to_datetime(s)).days) + 1)
                                quantity_dict[uom] += inv.quantity * duration
                                print(inv.product_id.prod_volume, 'inv.product_id.prod_volume', inv.quantity,
                                      'inv.quantity', )
                                summ = ({
                                    'start_date': s,
                                    'end_date': inv.out_date,
                                    'quantity': inv.quantity,
                                    'charge_type': 'storage',
                                    'product_id': inv.product_id.id,
                                    'charge_unit_type': 'custom',

                                })
                                summ_lines = self.env['summary.sheet.lines'].create(summ)
                                if summ_lines.quantity > 0:
                                    summary_lines.append(summ_lines)
                            elif inv.in_date != False and e >= inv.in_date <= s and s <= inv.out_date >= e and inv.storage_product == False:
                                duration = (abs((fields.Datetime.to_datetime(e)
                                                 - fields.Datetime.to_datetime(s)).days) + 1)
                                quantity_dict[uom] += inv.quantity * duration
                                summ = ({
                                    'start_date': s,
                                    'end_date': e,
                                    'quantity': inv.quantity,
                                    'charge_type': 'storage',
                                    'product_id': inv.product_id.id,
                                    'charge_unit_type': 'custom',

                                })
                                summ_lines = self.env['summary.sheet.lines'].create(summ)
                                if summ_lines.quantity > 0:
                                    summary_lines.append(summ_lines)
                            elif inv.in_date != False and inv.out_date != False and e >= inv.in_date >= s and s <= inv.out_date <= e and inv.storage_product == False:
                                ###print(inv.quantity, inv.duration)
                                duration = (abs((fields.Datetime.to_datetime(e)
                                                 - fields.Datetime.to_datetime(inv.in_date)).days) + 1)
                                quantity_dict[uom] += inv.quantity * duration
                                summ = ({
                                    'start_date': inv.in_date,
                                    'end_date': e,
                                    'quantity': inv.quantity,
                                    'charge_type': 'storage',
                                    'product_id': inv.product_id.id,
                                    'charge_unit_type': 'custom',

                                })
                                summ_lines = self.env['summary.sheet.lines'].create(summ)
                                if summ_lines.quantity > 0:
                                    summary_lines.append(summ_lines)
                            elif inv.in_date != False and e >= inv.in_date <= s and inv.out_date == False and inv.storage_product == False:
                                duration = (abs((fields.Datetime.to_datetime(e)
                                                 - fields.Datetime.to_datetime(s)).days) + 1)
                                quantity_dict[uom] += inv.quantity * duration
                                summ = ({
                                    'start_date': s,
                                    'end_date': e,
                                    'quantity': inv.quantity,
                                    'charge_type': 'storage',
                                    'product_id': inv.product_id.id,
                                    'charge_unit_type': 'custom',

                                })
                                summ_lines = self.env['summary.sheet.lines'].create(summ)
                                if summ_lines.quantity > 0:
                                    summary_lines.append(summ_lines)

            else:
                for inv in inven:
                    # ###print(inv.in_date, s, 'indate', inv.out_date, e, 'outdate')
                    if inv.in_date != False and inv.out_date != False and e >= inv.in_date >= s and s <= inv.out_date <= e and inv.storage_product == False:
                        ###print(inv.quantity, inv.duration)
                        # ###print(cbm, weight, sq, pallet, '------0------------cbm, weight, sq, pallet-----------------')
                        cbm += inv.product_id.prod_volume * inv.quantity * inv.duration
                        sq += inv.product_id.prod_sqm * inv.quantity * inv.duration
                        pallet += inv.quantity
                        weight += inv.product_id.weight * inv.quantity * inv.duration
                        print(cbm, 'cbm')
                        print(inv.product_id.prod_volume, 'inv.product_id.prod_volume', inv.quantity,
                              'inv.quantity', )
                        ###print(cbm, weight, sq, pallet, '------11------------cbm, weight, sq, pallet-----------------')
                        summ = ({
                            'start_date': inv.in_date,
                            'end_date': inv.out_date,
                            'quantity': inv.quantity,
                            # 'cbm': cbm,
                            'cbm': inv.product_id.prod_volume,
                            'sqm': inv.product_id.prod_sqm,
                            'pallet': inv.quantity,
                            'weight': inv.product_id.weight,
                            'charge_type': 'storage',
                            'product_id': inv.product_id.id,
                            'charge_unit_type': charge_unit_type,

                        })
                        summ_lines = self.env['summary.sheet.lines'].create(summ)
                        if summ_lines.quantity > 0:
                            summary_lines.append(summ_lines)

                            # ###print(summ_lines, '$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$'
                            #         '$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$'
                            #         'SUM CREATED $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$')
                    elif inv.in_date != False and e >= inv.in_date >= s and inv.out_date == False and inv.storage_product == False:
                        ###print(inv.quantity, inv.duration)
                        duration = (abs((fields.Datetime.to_datetime(e)
                                         - fields.Datetime.to_datetime(inv.in_date)).days) + 1)
                        # ###print(cbm, weight, sq, pallet, '------0------------cbm, weight, sq, pallet-----------------')
                        cbm += inv.product_id.prod_volume * inv.quantity * duration
                        sq += inv.product_id.prod_sqm * inv.quantity * duration
                        pallet += inv.quantity
                        weight += inv.product_id.weight * inv.quantity * duration
                        print(cbm, 'cbm')
                        print(inv.product_id.prod_volume, 'inv.product_id.prod_volume', inv.quantity,
                              'inv.quantity', )
                        ###print(cbm, weight, sq, pallet, '------12------------cbm, weight, sq, pallet-----------------')
                        summ = ({
                            'start_date': inv.in_date,
                            'end_date': e,
                            'quantity': inv.quantity,
                            'cbm': inv.product_id.prod_volume,
                            'sqm': inv.product_id.prod_sqm,
                            'pallet': inv.quantity,
                            'weight': inv.product_id.weight,
                            'charge_type': 'storage',
                            'product_id': inv.product_id.id,
                            'charge_unit_type': charge_unit_type,


                        })
                        summ_lines = self.env['summary.sheet.lines'].create(summ)
                        if summ_lines.quantity > 0:
                            summary_lines.append(summ_lines)
                            # ###print(summ_lines, '$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$'
                            #         '$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$'
                            #         'SUM CREATED $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$')
                    elif inv.in_date != False and e >= inv.in_date <= s and s <= inv.out_date <= e and inv.storage_product == False:
                        ###print(inv.quantity, inv.duration)
                        duration = (abs((fields.Datetime.to_datetime(inv.out_date)
                                         - fields.Datetime.to_datetime(s)).days) + 1)
                        # ###print(cbm, weight, sq, pallet, '------0------------cbm, weight, sq, pallet-----------------')
                        cbm += inv.product_id.prod_volume * inv.quantity * duration
                        sq += inv.product_id.prod_sqm * inv.quantity * duration
                        pallet += inv.quantity
                        weight += inv.product_id.weight * inv.quantity * duration
                        print(cbm, 'cbm')
                        print(inv.product_id.prod_volume, 'inv.product_id.prod_volume', inv.quantity,
                              'inv.quantity', )
                        ###print(cbm, weight, sq, pallet, '------12------------cbm, weight, sq, pallet-----------------')
                        summ = ({
                            'start_date': s,
                            'end_date': inv.out_date,
                            'quantity': inv.quantity,
                            'cbm': inv.product_id.prod_volume,
                            'sqm': inv.product_id.prod_sqm,
                            'pallet': inv.quantity,
                            'weight': inv.product_id.weight,
                            'charge_type': 'storage',
                            'product_id': inv.product_id.id,
                            'charge_unit_type': charge_unit_type,

                        })
                        summ_lines = self.env['summary.sheet.lines'].create(summ)
                        if summ_lines.quantity > 0:
                            summary_lines.append(summ_lines)
                            # ###print(summ_lines, '$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$'
                            #                   '$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$'
                            #                   'SUM CREATED $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$')
                    elif inv.in_date != False and e >= inv.in_date <= s and s <= inv.out_date >= e and inv.storage_product == False:
                        ###print(inv.quantity, inv.duration)
                        duration = (abs((fields.Datetime.to_datetime(e)
                                         - fields.Datetime.to_datetime(s)).days) + 1)
                        # ###print(cbm, weight, sq, pallet, '----ujn--0------------cbm, weight, sq, pallet-----------------')
                        cbm += inv.product_id.prod_volume * inv.quantity * duration
                        sq += inv.product_id.prod_sqm * inv.quantity * duration
                        pallet += inv.quantity
                        weight += inv.product_id.weight * inv.quantity * duration
                        ###print(cbm, weight, sq, pallet, '------12------------cbm, weight, sq, pallet-----------------')
                        summ = ({
                            'start_date': s,
                            'end_date': e,
                            'quantity': inv.quantity,
                            'cbm': inv.product_id.prod_volume,
                            'sqm': inv.product_id.prod_sqm,
                            'pallet': inv.quantity,
                            'weight': inv.product_id.weight,
                            'charge_type': 'storage',
                            'product_id': inv.product_id.id,
                            'charge_unit_type': charge_unit_type,

                        })
                        summ_lines = self.env['summary.sheet.lines'].create(summ)
                        if summ_lines.quantity > 0:
                            summary_lines.append(summ_lines)
                            # ###print(summ_lines, '$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$'
                            #                   '$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$'
                            #                   'SUM CREATED $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$')
                    elif inv.in_date != False and inv.out_date != False and e >= inv.in_date >= s and s <= inv.out_date <= e and inv.storage_product == False:
                        ###print(inv.quantity, inv.duration)
                        duration = (abs((fields.Datetime.to_datetime(e)
                                         - fields.Datetime.to_datetime(inv.in_date)).days) + 1)
                        # ###print(cbm, weight, sq, pallet, '------0------------cbm, weight, sq, pallet-----------------')
                        cbm += inv.product_id.prod_volume * inv.quantity * duration
                        sq += inv.product_id.prod_sqm * inv.quantity * duration
                        pallet += inv.quantity
                        weight += inv.product_id.weight * inv.quantity * duration
                        ###print(cbm, weight, sq, pallet, '------13------------cbm, weight, sq, pallet-----------------')
                        summ = ({
                            'start_date': inv.in_date,
                            'end_date': e,
                            'quantity': inv.quantity,
                            'cbm': inv.product_id.prod_volume,
                            'sqm': inv.product_id.prod_sqm,
                            'pallet': inv.quantity,
                            'weight': inv.product_id.weight,
                            'charge_type': 'storage',
                            'product_id': inv.product_id.id,
                            'charge_unit_type': charge_unit_type,

                        })
                        summ_lines = self.env['summary.sheet.lines'].create(summ)
                        if summ_lines.quantity > 0:
                            summary_lines.append(summ_lines)
                        # ###print(summ_lines, '$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$'
                        #             '$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$'
                        #             'SUM CREATED $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$')
                    elif inv.in_date != False and e >= inv.in_date <= s and inv.out_date == False and inv.storage_product == False:
                        ###print(inv.quantity, inv.duration)
                        duration = (abs((fields.Datetime.to_datetime(e)
                                         - fields.Datetime.to_datetime(s)).days) + 1)
                        # ###print(cbm, weight, sq, pallet, '------0------------cbm, weight, sq, pallet-----------------')
                        cbm += inv.product_id.prod_volume * inv.quantity * duration
                        sq += inv.product_id.prod_sqm * inv.quantity * duration
                        pallet += inv.quantity
                        weight += inv.product_id.weight * inv.quantity * duration
                        ###print(cbm, weight, sq, pallet, '------14------------cbm, weight, sq, pallet-----------------')
                        summ = ({
                            'start_date': s,
                            'end_date': e,
                            'quantity': inv.quantity,
                            'cbm': inv.product_id.prod_volume,
                            'sqm': inv.product_id.prod_sqm,
                            'pallet': inv.quantity,
                            'weight': inv.product_id.weight,
                            'charge_type': 'storage',
                            'product_id': inv.product_id.id,
                            'charge_unit_type': charge_unit_type,

                        })
                        summ_lines = self.env['summary.sheet.lines'].create(summ)
                        if summ_lines.quantity > 0:
                            summary_lines.append(summ_lines)
                        # ###print(summ_lines, '$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$'
                        #             '$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$'
                        #             'SUM CREATED $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$')
            print(quantity_dict, 'quantity_dict')
            ###print(cbm, weight, sq, pallet, '---------3---------cbm, weight, sq, pallet-----------------')
            for temp in storage_charges:
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
                    if temp_line_values['quantity'] > 0:
                        invoice_line_list.append((0, 0, temp_line_values))
                        # ###print(temp_line_values,
                        #   '-------------------------------cbm------------------------------------')

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
                    if temp_line_values['quantity'] > 0:
                        invoice_line_list.append((0, 0, temp_line_values))
                        # ###print(temp_line_values, '---------------------------weight----------------------------')

                if temp.charge_type == 'storage' and temp.charge_unit_type == 'square':
                    temp_line_values = {
                        'product_id': temp.product_id and temp.product_id.id or False,
                        'name': temp.product_id.name or '',
                        'price_unit': temp.list_price or 0.00,
                        'quantity': sq,
                        'currency_id': temp.currency_id.id,
                        'account_id': temp.product_id.property_account_income_id.id if temp.product_id.property_account_income_id
                        else temp.product_id.categ_id.property_account_income_categ_id.id,
                        # 'start_date': move_ids_without_package.start_date,
                        # 'end_date': move_ids_without_package.end_date,

                    }
                    if temp_line_values['quantity'] > 0:
                        invoice_line_list.append((0, 0, temp_line_values))
                        # ###print(temp_line_values, '---------------------------square--------------------------')

                if temp.charge_type == 'storage' and temp.charge_unit_type == 'pallet':
                    temp_line_values = {
                        'product_id': temp.product_id and temp.product_id.id or False,
                        'name': temp.product_id.name or '',
                        'price_unit': temp.list_price or 0.00,
                        'quantity': pallet,
                        'currency_id': temp.currency_id.id,
                        'account_id': temp.product_id.property_account_income_id.id if temp.product_id.property_account_income_id
                        else temp.product_id.categ_id.property_account_income_categ_id.id,
                        # 'start_date': move_ids_without_package.start_date,
                        # 'end_date': move_ids_without_package.end_date,

                    }
                    if temp_line_values['quantity'] > 0:
                        invoice_line_list.append((0, 0, temp_line_values))
                        # ###print(temp_line_values, '------------------------------pallets----------------------')
                if temp.charge_type == 'storage' and temp.charge_unit_type == 'custom':
                    print(uoms, 'uoms')
                    if uoms:
                        for q in uoms:
                            v = temp.uom_id.id
                            value = quantity_dict[v]
                            qty = value
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
                            if temp_line_values['quantity'] > 0:
                                invoice_line_list.append((0, 0, temp_line_values))
                            break
                                # ###print(temp_line_values, '------------------------------pallets----------------------')




            ###IN###
            in_charges = partner.env['agreement.charges'].search(
                ['&', ('charge_type', '=', 'inbound'), ('agreement_id', '=', agreement_id.id)])
            ###print(in_charges, 'in_charges')
            # invoice_line_list = []
            # invoice_line_liststo = []
            for temp in in_charges:
                ###print(temp.storage_type)
                in_pick_cont = self.env['stock.picking'].search_count(
                    [('picking_type_id.code', '=', 'incoming'),
                     ('container', '=', temp.container.id), ('state', '=', 'done'),
                     ('scheduled_date', '>', s), ('partner_id', '=', partner.id),
                     ('product_id.storage_type', '=', False)])
                in_pick_cont_obj = self.env['stock.picking'].search(
                    [('picking_type_id.code', '=', 'incoming'),
                     ('container', '=', temp.container.id), ('state', '=', 'done'),
                     ('scheduled_date', '>', s), ('partner_id', '=', partner.id),
                     ('product_id.storage_type', '=', False)])
                in_cnt1 = []
                for r in in_pick_cont_obj:
                    in_cnt1.append(r.name)
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
                if temp_line_values['quantity'] > 0:
                    invoice_line_list.append((0, 0, temp_line_values))
                    ###print(invoice_line_list, 'invoice_line_list')

                summ = ({
                    'start_date': s,
                    'end_date': e,
                    'container_type': temp.container.id,
                    'ref_no': in_cnt1,
                    'quantity': in_pick_cont,
                    'charge_type': 'inbound',

                    # 'in_ref_no' :

                })
                summ_lines = self.env['summary.sheet.lines'].create(summ)
                if summ_lines.quantity > 0:
                    summary_lines.append(summ_lines)

                # ###print(summ_lines, '$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$'
                #                   '$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$'
                #                   'IN SUM CREATED $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$')

            ###OUT###
            out_charges = partner.env['agreement.charges'].search(
                ['&', ('charge_type', '=', 'outbound'), ('agreement_id', '=', agreement_id.id)])
            ###print(out_charges, 'out_chsrgs')
            for temp in out_charges:
                out_pick_cont = self.env['stock.picking'].search_count(
                    [('picking_type_id.code', '=', 'outgoing'), ('container', '=', temp.container.id),
                     ('scheduled_date', '>', s), ('partner_id', '=', partner.id), ('state', '=', 'done'),
                     ('product_id.storage_type', '=', False)])
                out_pick_cont_obj = self.env['stock.picking'].search(
                    [('picking_type_id.code', '=', 'outgoing'), ('container', '=', temp.container.id),
                     ('scheduled_date', '>', s), ('partner_id', '=', partner.id), ('state', '=', 'done'),
                     ('product_id.storage_type', '=', False)])
                out_cnt1 = []
                for r in out_pick_cont_obj:
                    out_cnt1.append(r.name)
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
                if temp_line_values['quantity'] > 0:
                    invoice_line_list.append((0, 0, temp_line_values))
                    # ###print(invoice_line_list, 'invoice_line_list')
                summ = ({
                    'start_date': s,
                    'end_date': e,
                    'container_type': temp.container.id,
                    'ref_no': out_cnt1,
                    'quantity': out_pick_cont,
                    'charge_type': 'outbound',

                    # 'in_ref_no' :

                })
                summ_lines = self.env['summary.sheet.lines'].create(summ)
                if summ_lines.quantity > 0:
                    summary_lines.append(summ_lines)

                # ###print(summ_lines, '$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$'
                #                   '$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$'
                #                   'OUT SUM CREATED $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$')

            ###VALUEADDED###
            added_charges = partner.env['agreement.charges'].search(
                ['&', ('charge_type', '=', 'value_added'), ('agreement_id', '=', agreement_id.id)])
            print(added_charges, 'valueadded')
            ###print(added_charges, 'valueadded')
            for temp in added_charges:
                print(added_charges, 'valueadded')
                added_pick_count = self.env['stock.picking'].search_count(
                    [('picking_type_id.code', 'in', ['incoming', 'outgoing']),
                     ('added_service', '=', temp.added_service.id), ('scheduled_date', '>', s),
                     ('state', '=', 'done'), ('product_id.storage_type', '=', False)])
                added_pick_count_obj = self.env['stock.picking'].search(
                    [('picking_type_id.code', 'in', ['incoming', 'outgoing']),
                     ('added_service', '=', temp.added_service.id), ('scheduled_date', '>', s),
                     ('state', '=', 'done'), ('product_id.storage_type', '=', False)])
                added_cnt1 = []
                for r in added_pick_count_obj:
                    added_cnt1.append(r.name)
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
                if temp_line_values['quantity'] > 0:
                    invoice_line_list.append((0, 0, temp_line_values))
                    # ###print(invoice_line_list, 'invoice_line_list')
                summ = ({
                    'start_date': s,
                    'end_date': e,
                    'added_service': temp.added_service.id,
                    'ref_no': added_cnt1,
                    'quantity': added_pick_count,
                    'charge_type': 'value_added',
                    # 'in_ref_no' :

                })
                summ_lines = self.env['summary.sheet.lines'].create(summ)
                if summ_lines.quantity > 0:
                    summary_lines.append(summ_lines)

                # ###print(summ_lines, '$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$'
                #                   '$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$'
                #                   'VALUE ADDED SUM CREATED $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$')

            ###INVMANAGEMNET###
            # inv_charges = partner.env['agreement.charges'].search(
            #     ['&', ('charge_type', '=', 'inventory_mgmnt'), ('agreement_id', '=', agreement_id.id)])
            inv_charges = partner.env['agreement.charges'].search(
                ['&', ('charge_type', '=', 'inventory_mgmnt'), ('agreement_id', '=', agreement_id.id)])

            print(inv_charges, 'invcharges')

            if invoice_line_list:
                for temp in inv_charges:
                    added_pick_count = self.env['stock.picking'].search_count(
                        [('picking_type_id.code', 'in', ['incoming', 'outgoing']),
                         ('scheduled_date', '>', s), ('state', '=', 'done')])
                    added_pick_count_obj = self.env['stock.picking'].search(
                        [('picking_type_id.code', 'in', ['incoming', 'outgoing']),
                         ('scheduled_date', '>', s), ('state', '=', 'done')])
                    added_cnt1 = []
                    for r in added_pick_count_obj:
                        added_cnt1.append(r.name)

                    temp_line_values = {
                        'product_id': temp.product_id and temp.product_id.id or False,
                        'name': temp.product_id.name or '',
                        'price_unit': temp.list_price or 0.00,
                        'quantity': added_pick_count,
                        'currency_id': temp.currency_id.id,
                        'account_id': temp.product_id.property_account_income_id.id if temp.product_id.property_account_income_id
                        else temp.product_id.categ_id.property_account_income_categ_id.id,
                    }

                    if temp_line_values['quantity'] > 0:
                        invoice_line_list.append((0, 0, temp_line_values))

                # ###print(summ_lines, '$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$'
                #                   '$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$'
                #                   'INV MGMNT SUM CREATED $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$')

            current_user = self.env.uid
            # ###print(invoice_line_list, 'invoice_line_list')

            if agreement_id and invoice_line_list:
                invoice = partner.env['account.move'].create({
                    'type': 'out_invoice',
                    'invoice_origin': partner.name,
                    'invoice_user_id': current_user,
                    'narration': partner.name,
                    'partner_id': partner.id,
                    'currency_id': partner.env.user.company_id.currency_id.id,
                    # 'journal_id': int(customer_journal_id),
                    'invoice_payment_ref': partner.name,
                    # 'picking_id': picking_id.id,
                    'invoice_line_ids': invoice_line_list,
                    # 'invoice_type': 'storage',
                    'name': '/',

                })
                # invoice.consolidate_invoice_lines(invoice)

                ###print(invoice, 'Invoice Created')
                summary = ({
                    'name': str(s) + '-' + str(e),
                    'partner_id': partner.id,
                    'invoice_id': invoice.id
                })
                summary = self.env['summary.sheet'].create(summary)
                # ###print(summary_lines, 'summary_lines---fffffffffffffffffffffffffffffffffffffffff'
                #                      'ffffffffffffffffffffffffffffffffffffffffffffffffffffffff'
                #                      'ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff'
                #                      'fffffffffffffffffffffffffffffffffffffffffffffffffffffff'
                #                      'ffffffffffffffffffffffffffffffffffffffffffffffffff')
                for lines in summary_lines:
                    # ###print(lines.product_id.storage_type, '+++++++++++++++++++++========++++++++++++++++++++++++++'
                    #                                      '++++++++++++++++++++=a=====lines.product_id.storage_type'
                    #                                      '+++++++++++++++++++++++++++++++++++++++++++++++++++++++=++'
                    #                                      '')
                    lines['sheet_id'] = summary
                    # if not lines.product_id.storage_type:
                    #     lines['sheet_id'] = summary
                if invoice:
                    message = 'Cheers! Your Invoice is Successfully Crafted'
                    return {
                        'type': 'ir.actions.client',
                        'tag': 'display_notification',
                        'params': {
                            'message': message,
                            'type': 'success'  # Use 'warning' for a warning notification
                        }
                    }

            # ---------------------------------Storage Type Based Invoice----------------------------#
            agreement_id = partner.env['agreement'].search([('partner_id', '=', partner.id)])
            ###print(agreement_id, 'agreement_id')
            tstorage_charges = partner.env['agreement.charges'].search(
                ['&', ('charge_type', '=', 'storage'), ('agreement_id', '=', agreement_id.id),
                 ('storage_type', '!=', False)])
            tuoms = []
            tquantity_dict = {}
            for u in tstorage_charges:
                if u.uom_id:
                    tuoms.append(u.uom_id.id)
            print(tuoms)
            tcharge_unit_types = []
            for c in tstorage_charges:
                if c.charge_unit_type:
                    tcharge_unit_types.append(c.charge_unit_type)
            tvalues_except_custom = list(filter(lambda x: x != 'custom', tcharge_unit_types))
            print(tvalues_except_custom)
            tcharge_unit_type = tvalues_except_custom[0]
            print(tcharge_unit_types, tcharge_unit_type)
            ###print(tstorage_charges, 'tstorage_charges')
            tinven = self.env['product.summary'].search(
                [('partner_id', '=', partner.id), ('storage_product', '=', True), ('quantity', '>', 0)])
            ###print(tinven, 'tinven')
            tcbm = 0
            tweight = 0
            tsq = 0
            tpallet = 0
            tinvoice_line_list = []
            if tuoms:
                for uom in tuoms:
                    tquantity_dict[uom] = 0
                    for tinv in tinven:
                        if uom == tinv.uom_id:
                            ###print(tinv.storage_product, 'tinv.storage_product')
                            # ###print(tinv.in_date, s, 'indate', tinv.out_date, e, 'outdate')
                            if tinv.in_date != False and tinv.out_date != False and e >= tinv.in_date >= s and s <= tinv.out_date <= e and tinv.storage_product == True:
                                ###print(tinv.quantity, tinv.duration)
                                # ###print(tcbm, tweight, tsq, tpallet, '------0------------tcbm, tweight, tsq, tpallet-----------------')
                                # tcbm += tinv.product_id.x_vol * tinv.quantity * tinv.duration
                                # tsq += tinv.product_id.x_vol * tinv.quantity * tinv.duration
                                tcbm += tinv.product_id.prod_volume * tinv.quantity * tinv.duration
                                tsq += tinv.product_id.prod_sqm * tinv.quantity * tinv.duration
                                tpallet += tinv.quantity
                                tweight += tinv.product_id.weight * tinv.quantity * tinv.duration
                                tquantity_dict[uom] += tinv.quantity * tinv.duration
                                ###print(tcbm, tweight, tsq, tpallet,
                                # '------11------------tcbm, tweight, tsq, tpallet-----------------')
                                summ = ({
                                    'start_date': tinv.in_date,
                                    'end_date': tinv.out_date,
                                    'quantity': tinv.quantity,
                                    'cbm': tinv.product_id.prod_volume,
                                    'sqm': tinv.product_id.prod_sqm,
                                    'pallet': tinv.quantity,
                                    'weight': tinv.product_id.weight,
                                    'charge_type': 'storage',
                                    'product_id': tinv.product_id.id,
                                })
                                summ_lines = self.env['summary.sheet.lines'].create(summ)
                                if summ_lines.quantity > 0:
                                    tsummary_lines.append(summ_lines)
                                # ###print(summ_lines, '$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$'
                                #             '$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$'
                                #             'SUM CREATED $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$')
                            elif tinv.in_date != False and e >= tinv.in_date >= s and tinv.out_date == False and tinv.storage_product == True:
                                ###print(tinv.quantity, tinv.duration)
                                duration = (abs((fields.Datetime.to_datetime(e)
                                                 - fields.Datetime.to_datetime(tinv.in_date)).days) + 1)
                                # ###print(tcbm, tweight, tsq, tpallet, '------0------------tcbm, tweight, tsq, tpallet-----------------')
                                # tcbm += tinv.product_id.x_vol * tinv.quantity * tinv.duration
                                # tsq += tinv.product_id.x_vol * tinv.quantity * tinv.duration
                                tcbm += tinv.product_id.prod_volume * tinv.quantity * duration
                                tsq += tinv.product_id.prod_sqm * tinv.quantity * duration
                                tpallet += tinv.quantity
                                tweight += tinv.product_id.weight * tinv.quantity * duration
                                ###print(tcbm, tweight, tsq, tpallet,
                                # '------12------------tcbm, tweight, tsq, tpallet-----------------')
                                summ = ({
                                    'start_date': tinv.in_date,
                                    'end_date': e,
                                    'quantity': tinv.quantity,
                                    'cbm': tinv.product_id.prod_volume,
                                    'sqm': tinv.product_id.prod_sqm,
                                    'pallet': tinv.quantity,
                                    'weight': tinv.product_id.weight,
                                    'charge_type': 'storage',
                                    'product_id': tinv.product_id.id,

                                })
                                summ_lines = self.env['summary.sheet.lines'].create(summ)
                                if summ_lines.quantity > 0:
                                    tsummary_lines.append(summ_lines)
                                # ###print(summ_lines, '$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$'
                                #             '$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$'
                                #             'SUM CREATED $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$')
                            # elif tinv.in_date != False and e >= tinv.in_date >= s and s <= tinv.out_date <= e and tinv.storage_product == True:
                            #     ###print(tinv.quantity, tinv.duration)
                            #     duration = abs((fields.Datetime.to_datetime(tinv.out_date)
                            #                     - fields.Datetime.to_datetime(s)).days)
                            #     # ###print(tcbm, tweight, tsq, tpallet, '------0------------tcbm, tweight, tsq, tpallet-----------------')
                            #     # tcbm += tinv.product_id.x_vol * tinv.quantity * tinv.duration
                            #     # tsq += tinv.product_id.x_vol * tinv.quantity * tinv.duration
                            #     tcbm += tinv.product_id.prod_volume * tinv.quantity * duration
                            #     tsq += tinv.product_id.prod_sqm * tinv.quantity * duration
                            #     tpallet += tinv.quantity
                            #     tweight += tinv.product_id.weight * tinv.quantity * duration
                            #     ###print(tcbm, tweight, tsq, tpallet,
                            #           '------13------------tcbm, tweight, tsq, tpallet-----------------')
                            #     summ = ({
                            #         'start_date': s,
                            #         'end_date': tinv.out_date,
                            #         'quantity': tinv.quantity,
                            #         'cbm': cbm,
                            #         'sqm': sq,
                            #         'pallet': pallet,
                            #         'weight': weight,
                            #     })
                            #     summ_lines = self.env['summary.sheet.lines'].create(summ)
                            #     summary_lines.append(summ_lines)
                            #     ###print(summ_lines, '$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$'
                            #                 '$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$'
                            #                 'SUM CREATED $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$')
                            elif tinv.in_date != False and e >= tinv.in_date <= s and s <= tinv.out_date <= e and tinv.storage_product == False:
                                ###print(tinv.quantity, tinv.duration)
                                duration = (abs((fields.Datetime.to_datetime(e)
                                                 - fields.Datetime.to_datetime(tinv.in_date)).days) + 1)
                                # ###print(cbm, weight, sq, pallet, '------0------------cbm, weight, sq, pallet-----------------')
                                # cbm += tinv.product_id.x_vol * tinv.quantity * tinv.duration
                                # sq += tinv.product_id.x_vol * tinv.quantity * tinv.duration
                                tcbm += tinv.product_id.prod_volume * tinv.quantity * duration
                                tsq += tinv.product_id.prod_sqm * tinv.quantity * duration
                                tpallet += tinv.quantity
                                tweight += tinv.product_id.weight * tinv.quantity * duration
                                ###print(tcbm, tweight, tsq, tpallet, '------12------------tcbm, tweight, sq, pallet-----------------')
                                summ = ({
                                    'start_date': tinv.in_date,
                                    'end_date': tinv.out_date,
                                    'quantity': tinv.quantity,
                                    'cbm': tinv.product_id.prod_volume,
                                    'sqm': tinv.product_id.prod_sqm,
                                    'pallet': tinv.quantity,
                                    'weight': tinv.product_id.weight,
                                    'charge_type': 'storage',
                                    'product_id': tinv.product_id.id,
                                })
                                summ_lines = self.env['summary.sheet.lines'].create(summ)
                                if summ_lines.quantity > 0:
                                    tsummary_lines.append(summ_lines)
                            elif tinv.in_date != False and e >= tinv.in_date <= s and s <= tinv.out_date >= e and tinv.storage_product == False:
                                ###print(tinv.quantity, tinv.duration)
                                duration = (abs((fields.Datetime.to_datetime(e)
                                                 - fields.Datetime.to_datetime(s)).days) + 1)
                                # ###print(cbm, weight, sq, pallet, '------0------------cbm, weight, sq, pallet-----------------')
                                # cbm += tinv.product_id.x_vol * tinv.quantity * tinv.duration
                                # sq += tinv.product_id.x_vol * tinv.quantity * tinv.duration
                                tcbm += tinv.product_id.prod_volume * tinv.quantity * duration
                                tsq += tinv.product_id.prod_sqm * tinv.quantity * duration
                                tpallet += tinv.quantity
                                tweight += tinv.product_id.weight * tinv.quantity * duration
                                ###print(tcbm, tweight, tsq, tpallet, '------12------------tcbm, tweight, sq, pallet-----------------')
                                summ = ({
                                    'start_date': s,
                                    'end_date': e,
                                    'quantity': tinv.quantity,
                                    'cbm': tinv.product_id.prod_volume,
                                    'sqm': tinv.product_id.prod_sqm,
                                    'pallet': tinv.quantity,
                                    'weight': tinv.product_id.weight,
                                    'charge_type': 'storage',
                                    'product_id': tinv.product_id.id,
                                })
                                summ_lines = self.env['summary.sheet.lines'].create(summ)
                                if summ_lines.quantity > 0:
                                    tsummary_lines.append(summ_lines)
                            elif tinv.in_date != False and e >= tinv.in_date <= s and tinv.out_date == False and tinv.storage_product == True:
                                ###print(tinv.quantity, tinv.duration)
                                duration = (abs((fields.Datetime.to_datetime(e)
                                                 - fields.Datetime.to_datetime(s)).days) + 1)
                                # ###print(tcbm, tweight, tsq, tpallet, '------0------------tcbm, tweight, tsq, tpallet-----------------')
                                # tcbm += tinv.product_id.x_vol * tinv.quantity * tinv.duration
                                # tsq += tinv.product_id.x_vol * tinv.quantity * tinv.duration
                                tcbm += tinv.product_id.prod_volume * tinv.quantity * duration
                                tsq += tinv.product_id.prod_sqm * tinv.quantity * duration
                                tpallet += tinv.quantity
                                tweight += tinv.product_id.weight * tinv.quantity * duration
                                ###print(tcbm, tweight, tsq, tpallet,
                                # '------14------------tcbm, tweight, tsq, tpallet-----------------')
                                summ = ({
                                    'start_date': s,
                                    'end_date': e,
                                    'quantity': tinv.quantity,
                                    'cbm': tinv.product_id.prod_volume,
                                    'sqm': tinv.product_id.prod_sqm,
                                    'pallet': tinv.quantity,
                                    'weight': tinv.product_id.weight,
                                    'charge_type': 'storage',
                                    'product_id': tinv.product_id.id,
                                })

                                summ_lines = self.env['summary.sheet.lines'].create(summ)
                                if summ_lines.quantity > 0:
                                    tsummary_lines.append(summ_lines)
                                # ###print(summ_lines, '$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$'
                                #             '$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$'
                                #             'SUM CREATED $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$')

            else:
                for tinv in tinven:
                    ###print(tinv.storage_product, 'tinv.storage_product')
                    # ###print(tinv.in_date, s, 'indate', tinv.out_date, e, 'outdate')
                    if tinv.in_date != False and tinv.out_date != False and e >= tinv.in_date >= s and s <= tinv.out_date <= e and tinv.storage_product == True:
                        ###print(tinv.quantity, tinv.duration)
                        # ###print(tcbm, tweight, tsq, tpallet, '------0------------tcbm, tweight, tsq, tpallet-----------------')
                        # tcbm += tinv.product_id.x_vol * tinv.quantity * tinv.duration
                        # tsq += tinv.product_id.x_vol * tinv.quantity * tinv.duration
                        tcbm += tinv.product_id.prod_volume * tinv.quantity * tinv.duration
                        tsq += tinv.product_id.prod_sqm * tinv.quantity * tinv.duration
                        tpallet += tinv.quantity
                        tweight += tinv.product_id.weight * tinv.quantity * tinv.duration
                        ###print(tcbm, tweight, tsq, tpallet,
                        # '------11------------tcbm, tweight, tsq, tpallet-----------------')
                        summ = ({
                            'start_date': tinv.in_date,
                            'end_date': tinv.out_date,
                            'quantity': tinv.quantity,
                            'cbm': tinv.product_id.prod_volume,
                            'sqm': tinv.product_id.prod_sqm,
                            'pallet': tinv.quantity,
                            'weight': tinv.product_id.weight,
                            'charge_type': 'storage',
                            'product_id': tinv.product_id.id,
                            'charge_unit_type': tcharge_unit_type,
                        })
                        summ_lines = self.env['summary.sheet.lines'].create(summ)
                        if summ_lines.quantity > 0:
                            tsummary_lines.append(summ_lines)
                        # ###print(summ_lines, '$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$'
                        #             '$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$'
                        #             'SUM CREATED $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$')
                    elif tinv.in_date != False and e >= tinv.in_date >= s and tinv.out_date == False and tinv.storage_product == True:
                        ###print(tinv.quantity, tinv.duration)
                        duration = (abs((fields.Datetime.to_datetime(e)
                                         - fields.Datetime.to_datetime(tinv.in_date)).days) + 1)
                        # ###print(tcbm, tweight, tsq, tpallet, '------0------------tcbm, tweight, tsq, tpallet-----------------')
                        # tcbm += tinv.product_id.x_vol * tinv.quantity * tinv.duration
                        # tsq += tinv.product_id.x_vol * tinv.quantity * tinv.duration
                        tcbm += tinv.product_id.prod_volume * tinv.quantity * duration
                        tsq += tinv.product_id.prod_sqm * tinv.quantity * duration
                        tpallet += tinv.quantity
                        tweight += tinv.product_id.weight * tinv.quantity * duration
                        ###print(tcbm, tweight, tsq, tpallet,
                        # '------12------------tcbm, tweight, tsq, tpallet-----------------')
                        summ = ({
                            'start_date': tinv.in_date,
                            'end_date': e,
                            'quantity': tinv.quantity,
                            'cbm': tinv.product_id.prod_volume,
                            'sqm': tinv.product_id.prod_sqm,
                            'pallet': tinv.quantity,
                            'weight': tinv.product_id.weight,
                            'charge_type': 'storage',
                            'product_id': tinv.product_id.id,
                            'charge_unit_type': tcharge_unit_type,

                        })
                        summ_lines = self.env['summary.sheet.lines'].create(summ)
                        if summ_lines.quantity > 0:
                            tsummary_lines.append(summ_lines)
                        # ###print(summ_lines, '$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$'
                        #             '$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$'
                        #             'SUM CREATED $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$')
                    # elif tinv.in_date != False and e >= tinv.in_date >= s and s <= tinv.out_date <= e and tinv.storage_product == True:
                    #     ###print(tinv.quantity, tinv.duration)
                    #     duration = abs((fields.Datetime.to_datetime(tinv.out_date)
                    #                     - fields.Datetime.to_datetime(s)).days)
                    #     # ###print(tcbm, tweight, tsq, tpallet, '------0------------tcbm, tweight, tsq, tpallet-----------------')
                    #     # tcbm += tinv.product_id.x_vol * tinv.quantity * tinv.duration
                    #     # tsq += tinv.product_id.x_vol * tinv.quantity * tinv.duration
                    #     tcbm += tinv.product_id.prod_volume * tinv.quantity * duration
                    #     tsq += tinv.product_id.prod_sqm * tinv.quantity * duration
                    #     tpallet += tinv.quantity
                    #     tweight += tinv.product_id.weight * tinv.quantity * duration
                    #     ###print(tcbm, tweight, tsq, tpallet,
                    #           '------13------------tcbm, tweight, tsq, tpallet-----------------')
                    #     summ = ({
                    #         'start_date': s,
                    #         'end_date': tinv.out_date,
                    #         'quantity': tinv.quantity,
                    #         'cbm': cbm,
                    #         'sqm': sq,
                    #         'pallet': pallet,
                    #         'weight': weight,
                    #     })
                    #     summ_lines = self.env['summary.sheet.lines'].create(summ)
                    #     summary_lines.append(summ_lines)
                    #     ###print(summ_lines, '$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$'
                    #                 '$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$'
                    #                 'SUM CREATED $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$')
                    elif tinv.in_date != False and e >= tinv.in_date <= s and s <= tinv.out_date <= e and tinv.storage_product == False:
                        ###print(tinv.quantity, tinv.duration)
                        duration = (abs((fields.Datetime.to_datetime(e)
                                         - fields.Datetime.to_datetime(tinv.in_date)).days) + 1)
                        # ###print(cbm, weight, sq, pallet, '------0------------cbm, weight, sq, pallet-----------------')
                        # cbm += tinv.product_id.x_vol * tinv.quantity * tinv.duration
                        # sq += tinv.product_id.x_vol * tinv.quantity * tinv.duration
                        tcbm += tinv.product_id.prod_volume * tinv.quantity * duration
                        tsq += tinv.product_id.prod_sqm * tinv.quantity * duration
                        tpallet += tinv.quantity
                        tweight += tinv.product_id.weight * tinv.quantity * duration
                        ###print(tcbm, tweight, tsq, tpallet, '------12------------tcbm, tweight, sq, pallet-----------------')
                        summ = ({
                            'start_date': tinv.in_date,
                            'end_date': tinv.out_date,
                            'quantity': tinv.quantity,
                            'cbm': tinv.product_id.prod_volume,
                            'sqm': tinv.product_id.prod_sqm,
                            'pallet': tinv.quantity,
                            'weight': tinv.product_id.weight,
                            'charge_type': 'storage',
                            'product_id': tinv.product_id.id,
                            'charge_unit_type': tcharge_unit_type,

                        })
                        summ_lines = self.env['summary.sheet.lines'].create(summ)
                        if summ_lines.quantity > 0:
                            tsummary_lines.append(summ_lines)
                    elif tinv.in_date != False and e >= tinv.in_date <= s and s <= tinv.out_date >= e and tinv.storage_product == False:
                        ###print(tinv.quantity, tinv.duration)
                        duration = (abs((fields.Datetime.to_datetime(e)
                                         - fields.Datetime.to_datetime(s)).days) + 1)
                        # ###print(cbm, weight, sq, pallet, '------0------------cbm, weight, sq, pallet-----------------')
                        # cbm += tinv.product_id.x_vol * tinv.quantity * tinv.duration
                        # sq += tinv.product_id.x_vol * tinv.quantity * tinv.duration
                        tcbm += tinv.product_id.prod_volume * tinv.quantity * duration
                        tsq += tinv.product_id.prod_sqm * tinv.quantity * duration
                        tpallet += tinv.quantity
                        tweight += tinv.product_id.weight * tinv.quantity * duration
                        ###print(tcbm, tweight, tsq, tpallet, '------12------------tcbm, tweight, sq, pallet-----------------')
                        summ = ({
                            'start_date': s,
                            'end_date': e,
                            'quantity': tinv.quantity,
                            'cbm': tinv.product_id.prod_volume,
                            'sqm': tinv.product_id.prod_sqm,
                            'pallet': tinv.quantity,
                            'weight': tinv.product_id.weight,
                            'charge_type': 'storage',
                            'product_id': tinv.product_id.id,
                            'charge_unit_type': tcharge_unit_type,

                        })
                        summ_lines = self.env['summary.sheet.lines'].create(summ)
                        if summ_lines.quantity > 0:
                            tsummary_lines.append(summ_lines)
                    elif tinv.in_date != False and e >= tinv.in_date <= s and tinv.out_date == False and tinv.storage_product == True:
                        ###print(tinv.quantity, tinv.duration)
                        duration = (abs((fields.Datetime.to_datetime(e)
                                         - fields.Datetime.to_datetime(s)).days) + 1)
                        # ###print(tcbm, tweight, tsq, tpallet, '------0------------tcbm, tweight, tsq, tpallet-----------------')
                        # tcbm += tinv.product_id.x_vol * tinv.quantity * tinv.duration
                        # tsq += tinv.product_id.x_vol * tinv.quantity * tinv.duration
                        tcbm += tinv.product_id.prod_volume * tinv.quantity * duration
                        tsq += tinv.product_id.prod_sqm * tinv.quantity * duration
                        tpallet += tinv.quantity
                        tweight += tinv.product_id.weight * tinv.quantity * duration
                        ###print(tcbm, tweight, tsq, tpallet,
                        # '------14------------tcbm, tweight, tsq, tpallet-----------------')
                        summ = ({
                            'start_date': s,
                            'end_date': e,
                            'quantity': tinv.quantity,
                            'cbm': tinv.product_id.prod_volume,
                            'sqm': tinv.product_id.prod_sqm,
                            'pallet': tinv.quantity,
                            'weight': tinv.product_id.weight,
                            'charge_type': 'storage',
                            'product_id': tinv.product_id.id,
                            'charge_unit_type': tcharge_unit_type,

                        })

                        summ_lines = self.env['summary.sheet.lines'].create(summ)
                        if summ_lines.quantity > 0:
                            tsummary_lines.append(summ_lines)
                        # ###print(summ_lines, '$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$'
                        #             '$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$'
                        #             'SUM CREATED $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$')
                    #     ###print(tcbm, tweight, tsq, tpallet, '------1------------tcbm, tweight, tsq, tpallet-----------------')
                    # ###print(tcbm, tweight, tsq, tpallet, '--------2----------tcbm, tweight, tsq, tpallet-----------------')
            ###print(tcbm, tweight, tsq, tpallet, '---------3---------tcbm, tweight, tsq, tpallet-----------------')
            for temp in tstorage_charges:
                if temp.charge_type == 'storage' and temp.charge_unit_type == 'cbm':
                    temp_line_values = {
                        'product_id': temp.product_id and temp.product_id.id or False,
                        'name': temp.product_id.name or '',
                        'price_unit': temp.list_price or 0.00,
                        'quantity': tcbm,
                        'currency_id': temp.currency_id.id,
                        'account_id': temp.product_id.property_account_income_id.id if temp.product_id.property_account_income_id
                        else temp.product_id.categ_id.property_account_income_categ_id.id,
                        # 'start_date': move_ids_without_package.start_date,
                        # 'end_date': move_ids_without_package.end_date,

                    }
                    if temp_line_values['quantity'] > 0:
                        tinvoice_line_list.append((0, 0, temp_line_values))
                        # ###print(temp_line_values,
                        #   '-------------------------------tcbm------------------------------------')

                if temp.charge_type == 'storage' and temp.charge_unit_type == 'weight':
                    temp_line_values = {
                        'product_id': temp.product_id and temp.product_id.id or False,
                        'name': temp.product_id.name or '',
                        'price_unit': temp.list_price or 0.00,
                        'quantity': tweight,
                        'currency_id': temp.currency_id.id,
                        'account_id': temp.product_id.property_account_income_id.id if temp.product_id.property_account_income_id
                        else temp.product_id.categ_id.property_account_income_categ_id.id,
                        # 'start_date': move_ids_without_package.start_date,
                        # 'end_date': move_ids_without_package.end_date,

                    }
                    if temp_line_values['quantity'] > 0:
                        tinvoice_line_list.append((0, 0, temp_line_values))
                        # ###print(temp_line_values, '---------------------------tw'
                        #                     '`qwweight----------------------------')

                if temp.charge_type == 'storage' and temp.charge_unit_type == 'square':
                    temp_line_values = {
                        'product_id': temp.product_id and temp.product_id.id or False,
                        'name': temp.product_id.name or '',
                        'price_unit': temp.list_price or 0.00,
                        'quantity': tsq,
                        'currency_id': temp.currency_id.id,
                        'account_id': temp.product_id.property_account_income_id.id if temp.product_id.property_account_income_id
                        else temp.product_id.categ_id.property_account_income_categ_id.id,
                        # 'start_date': move_ids_without_package.start_date,
                        # 'end_date': move_ids_without_package.end_date,

                    }
                    if temp_line_values['quantity'] > 0:
                        tinvoice_line_list.append((0, 0, temp_line_values))
                        # ###print(temp_line_values, '---------------------------tsquare--------------------------')

                if temp.charge_type == 'storage' and temp.charge_unit_type == 'pallet':
                    temp_line_values = {
                        'product_id': temp.product_id and temp.product_id.id or False,
                        'name': temp.product_id.name or '',
                        'price_unit': temp.list_price or 0.00,
                        'quantity': tpallet,
                        'currency_id': temp.currency_id.id,
                        'account_id': temp.product_id.property_account_income_id.id if temp.product_id.property_account_income_id
                        else temp.product_id.categ_id.property_account_income_categ_id.id,
                        # 'start_date': move_ids_without_package.start_date,
                        # 'end_date': move_ids_without_package.end_date,

                    }
                    if temp_line_values['quantity'] > 0:
                        tinvoice_line_list.append((0, 0, temp_line_values))
                        # ###print(temp_line_values, '------------------------------tpallets----------------------')
                if temp.charge_type == 'storage' and temp.charge_unit_type == 'custom':
                    print(tuoms, 'uoms')
                    if tuoms:
                        for q in tuoms:
                            v = temp.uom_id.id
                            value = quantity_dict[v]
                            qty = value
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
                            if temp_line_values['quantity'] > 0:
                                invoice_line_list.append((0, 0, temp_line_values))
                                # ###print(temp_line_values, '------------------------------pallets----------------------')


            ###IN###
            in_charges = partner.env['agreement.charges'].search(
                ['&', ('charge_type', '=', 'inbound'), ('agreement_id', '=', agreement_id.id)])
            ###print(in_charges, 'in_charges')
            # tinvoice_line_list = []
            # tinvoice_line_liststo = []
            if tinvoice_line_list:
                for temp in in_charges:
                    ###print(temp.storage_type)
                    in_pick_cont = self.env['stock.picking'].search_count(
                        [('picking_type_id.code', '=', 'incoming'),
                         ('container', '=', temp.container.id), ('state', '=', 'done'),
                         ('scheduled_date', '>', s), ('partner_id', '=', partner.id),
                         ('product_id.storage_type', '=', in_charges.storage_type.id)])
                    in_pick_cont_len = self.env['stock.picking'].search(
                        [('picking_type_id.code', '=', 'incoming'),
                         ('container', '=', temp.container.id), ('state', '=', 'done'),
                         ('scheduled_date', '>', s), ('partner_id', '=', partner.id),
                         ('product_id.storage_type', '=', in_charges.storage_type.id)])
                    in_cnt2 = []
                    for r in in_pick_cont_len:
                        in_cnt2.append(r.name)
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
                    if temp_line_values['quantity'] > 0:
                        tinvoice_line_list.append((0, 0, temp_line_values))
                        # ###print(tinvoice_line_list, 'tinvoice_line_list')
                    summ = ({
                        'start_date': s,
                        'end_date': e,
                        'container_type': temp.container.id,
                        'ref_no': in_cnt2,
                        'quantity': in_pick_cont,
                        'charge_type': 'inbound',

                    })
                    summ_lines = self.env['summary.sheet.lines'].create(summ)
                    if summ_lines.quantity > 0:
                        tsummary_lines.append(summ_lines)
                    #
                    # ###print(summ_lines, '$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$'
                    #                   '$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$'
                    #                   'IN SUM CREATED $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$')

            ###OUT###
            out_charges = partner.env['agreement.charges'].search(
                ['&', ('charge_type', '=', 'outbound'), ('agreement_id', '=', agreement_id.id)])
            ###print(out_charges, 'out_chsrgs')
            if tinvoice_line_list:
                for temp in out_charges:
                    out_pick_cont = self.env['stock.picking'].search_count(
                        [('picking_type_id.code', '=', 'outgoing'), ('container', '=', temp.container.id),
                         ('scheduled_date', '>', s), ('partner_id', '=', partner.id), ('state', '=', 'done'),
                         ('product_id.storage_type', '=', out_charges.storage_type.id)])
                    out_pick_cont_len = self.env['stock.picking'].search(
                        [('picking_type_id.code', '=', 'outgoing'), ('container', '=', temp.container.id),
                         ('scheduled_date', '>', s), ('partner_id', '=', partner.id), ('state', '=', 'done'),
                         ('product_id.storage_type', '=', out_charges.storage_type.id)])
                    out_cnt2 = []
                    for r in out_pick_cont_len:
                        out_cnt2.append(r.name)
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
                    if temp_line_values['quantity'] > 0:
                        tinvoice_line_list.append((0, 0, temp_line_values))
                        # ###print(tinvoice_line_list, 'tinvoice_line_list')
                    summ = ({
                        'start_date': s,
                        'end_date': e,
                        'container_type': temp.container.id,
                        'ref_no': out_cnt2,
                        'quantity': out_pick_cont,
                        'charge_type': 'outbound',

                    })
                    summ_lines = self.env['summary.sheet.lines'].create(summ)
                    if summ_lines.quantity > 0:
                        tsummary_lines.append(summ_lines)

                    # ###print(summ_lines, '$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$'
                    #                   '$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$'
                    #                   'OUT SUM CREATED $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$')

            ###VALUEADDED###
            added_charges = partner.env['agreement.charges'].search(
                ['&', ('charge_type', '=', 'value_added'), ('agreement_id', '=', agreement_id.id)])
            ###print(added_charges, 'valueadded')
            if tinvoice_line_list:
                for temp in added_charges:
                    added_pick_count = self.env['stock.picking'].search_count(
                        [('picking_type_id.code', '!=', 'internal'),
                         ('added_service', '=', temp.added_service.id), ('scheduled_date', '>', s),
                         ('state', '=', 'done'), ('product_id.storage_type', '!=', added_charges.storage_type.id)])
                    added_pick_count_len = self.env['stock.picking'].search(
                        [('picking_type_id.code', '!=', 'internal'),
                         ('added_service', '=', temp.added_service.id), ('scheduled_date', '>', s),
                         ('state', '=', 'done'), ('product_id.storage_type', '=', added_charges.storage_type.id)])
                    add_cnt2 = []
                    for r in added_pick_count_len:
                        add_cnt2.append(r.name)
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
                    if temp_line_values['quantity'] > 0:
                        tinvoice_line_list.append((0, 0, temp_line_values))
                        # ###print(tinvoice_line_list, 'tinvoice_line_list')
                    summ = ({
                        'start_date': s,
                        'end_date': e,
                        'added_service': temp.added_service.id,
                        'ref_no': add_cnt2,
                        'quantity': added_pick_count,
                        'charge_type': 'value_added',

                    })
                    summ_lines = self.env['summary.sheet.lines'].create(summ)
                    if summ_lines.quantity > 0:
                        tsummary_lines.append(summ_lines)

                    # ###print(summ_lines, '$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$'
                    #                   '$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$'
                    #                   'VALUE ADDED SUM CREATED $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$')

            ###INVMANAGEMNET###
            inv_charges = partner.env['agreement.charges'].search(
                ['&', ('charge_type', '=', 'inventory_mgmnt'), ('agreement_id', '=', agreement_id.id)])
            ###print(added_charges, 'invcharges')
            if tinvoice_line_list:
                for temp in inv_charges:
                    added_pick_count = self.env['stock.picking'].search_count(
                        [('picking_type_id.code', '!=', 'internal'),
                         ('scheduled_date', '>', s), ('state', '=', 'done')])
                    added_pick_count_len = self.env['stock.picking'].search(
                        [('picking_type_id.code', '!=', 'internal'),
                         ('scheduled_date', '>', s), ('state', '=', 'done')])
                    add_cnt2 = []
                    for r in added_pick_count_len:
                        add_cnt2.append(r.name)
                    # added_pick_count = len(added_pick_count_len)
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
                    if temp_line_values['quantity'] > 0:
                        tinvoice_line_list.append((0, 0, temp_line_values))
                    summ = ({
                        'start_date': s,
                        'end_date': e,
                        'added_service': temp.added_service.id,
                        'ref_no': add_cnt2,
                        'quantity': added_pick_count,
                        'charge_type': 'inventory_mgmnt',

                    })
                    summ_lines = self.env['summary.sheet.lines'].create(summ)
                    if summ_lines.quantity > 0:
                        tsummary_lines.append(summ_lines)

                    # ###print(summ_lines, '$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$'
                    #                   '$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$'
                    #                   'INV MGMNT SERVICE SUM CREATED $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$')

            current_user = self.env.uid
            ###print(tinvoice_line_list, 'tinvoice_line_list')

            if agreement_id and tinvoice_line_list:
                tinvoice = partner.env['account.move'].create({
                    'type': 'out_invoice',
                    'invoice_origin': partner.name,
                    'invoice_user_id': current_user,
                    'narration': partner.name,
                    'partner_id': partner.id,
                    'currency_id': partner.env.user.company_id.currency_id.id,
                    # 'journal_id': int(customer_journal_id),
                    'invoice_payment_ref': partner.name,
                    # 'picking_id': picking_id.id,
                    'invoice_line_ids': tinvoice_line_list,
                    # 'invoice_type': 'storage',
                    'name': '/',

                })
                # tinvoice.consolidate_invoice_lines(tinvoice)

                ###print(invoice, tinvoice_line_list, 'TInvoice Created')
                tsummary = ({
                    'name': str(s) + '-' + str(e) + '-' + 'Temperature Control',
                    'partner_id': partner.id,
                    'invoice_id': tinvoice.id
                })
                tsummary = self.env['summary.sheet'].create(tsummary)
                # ###print(tsummary_lines, 'tsummary_linesummary_lines---fffffffffffffffffffffffffffffffffffffffff'
                #                      'ffffffffffffffffffffffffffffffffffffffffffffffffffffffff'
                #                      'ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff'
                #                      'fffffffffffffffffffffffffffffffffffffffffffffffffffffff'
                #                      'ffffffffffffffffffffffffffffffffffffffffffffffffff')
                for lines in tsummary_lines:
                    lines['sheet_id'] = tsummary
                if tinvoice:
                    message = 'Cheers! Your Invoice is Successfully Crafted'
                    return {
                        'type': 'ir.actions.client',
                        'tag': 'display_notification',
                        'params': {
                            'message': message,
                            'type': 'success'  # Use 'warning' for a warning notification
                        }
                    }
                    # if lines.product_id.storage_type:
                    #     lines['sheet_id'] = tsummary

    def create_in_invoice(self):
        for partner in self:
            s = partner.last_inv_date
            e = partner.inv_end_date
            picking_id = self.env['stock.picking'].search(
                [('picking_type_id.code', '=', 'incoming'), ('partner_id', '=', partner.id),
                 ('scheduled_date', '>=', s)])
            invoice_line_list = []
            for picking in picking_id:
                print('1')
                if s <= picking.scheduled_date <= e:
                    print('2', picking.service_id)
                    for pick in picking.service_id:
                        print('3', picking.service_id)
                        vals = (0, 0, {
                            'name': pick.product_id.name,
                            'product_id': pick.product_id.id,
                            'price_unit': pick.qty,
                            'account_id': pick.product_id.property_account_income_id.id if pick.product_id.property_account_income_id
                            else pick.product_id.categ_id.property_account_income_categ_id.id,
                            # 'tax_ids': [(6, 0, [pick.taxes_id.id])] ,
                            'quantity': pick.price,

                            # 'quantity': move_ids_without_package.quantt if move_ids_without_package.inv_meth else 1,
                            # 'x_cbm': picking.x_cbm,
                            # 'start_date': picking.scheduled_date,
                            # 'end_date': picking.date_done,

                        })
                        invoice_line_list.append(vals)
                        print(invoice_line_list)
            current_user = self.env.uid
            invoice = picking_id.env['account.move'].create({
                'type': 'out_invoice',
                'invoice_origin': partner.name,
                'invoice_user_id': current_user,
                'narration': partner.name,
                'partner_id': partner.id,
                'currency_id': self.env.user.company_id.currency_id.id,
                # 'journal_id': int(vendor_journal_id),
                'invoice_payment_ref': partner.name,
                # 'picking_id': picking.id,
                'invoice_line_ids': invoice_line_list,
                # 'invoice_type': 'reception',

            })
            # return invoice

    def create_out_invoice(self):
        for partner in self:
            s = partner.last_inv_date
            e = partner.inv_end_date
            picking_id = self.env['stock.picking'].search(
                [('picking_type_id.code', '=', 'outgoing'), ('partner_id', '=', partner.id),
                 ('scheduled_date', '>=', s)])
            invoice_line_list = []
            for picking in picking_id:
                if s <= picking.scheduled_date <= e:
                    for pick in picking.service_id:
                        vals = (0, 0, {
                            'name': pick.product_id.name,
                            'product_id': pick.product_id.id,
                            'price_unit': pick.qty,
                            'account_id': pick.product_id.property_account_income_id.id if pick.product_id.property_account_income_id
                            else pick.product_id.categ_id.property_account_income_categ_id.id,
                            # 'tax_ids': [(6, 0, [pick.taxes_id.id])],
                            'quantity': pick.price,

                            # 'quantity': move_ids_without_package.quantt if move_ids_without_package.inv_meth else 1,
                            # 'x_cbm': picking.x_cbm,
                            # 'start_date': picking.scheduled_date,
                            # 'end_date': picking.date_done,

                        })
                        invoice_line_list.append(vals)
                        ###print(invoice_line_list)
            current_user = self.env.uid
            invoice = partner.env['account.move'].create({
                'type': 'out_invoice',
                'invoice_origin': partner.name,
                'invoice_user_id': current_user,
                'narration': partner.name,
                'partner_id': partner.id,
                'currency_id': partner.env.user.company_id.currency_id.id,
                # 'journal_id': int(vendor_journal_id),
                'invoice_payment_ref': partner.name,
                # 'picking_id': partner.id,
                'invoice_line_ids': invoice_line_list,
                # 'invoice_type': 'reception',

            })
            # invoice.consolidate_invoice_lines(invoice)

            # return invoice


    def create_inv_invoice_core(self):
        for partner in self:
            s = partner.last_inv_date
            e = partner.inv_end_date
            ee = datetime.strptime(str(e), '%Y-%m-%d %H:%M:%S')
            ss = datetime.strptime(str(s), '%Y-%m-%d %H:%M:%S')
            agreement_id = partner.env['agreement'].search([('partner_id', '=', partner.id)])
            ag = self.env['product.summary'].search([])
            ag._storage_product()
            storage_charges = partner.env['agreement.charges'].search(
                ['&', ('charge_type', '=', 'storage'), ('agreement_id', '=', agreement_id.id),
                 ('storage_type', '=', False)])
            quantity_dict = {}
            charge_unit_types = []
            for c in storage_charges:
                if c.charge_unit_type:
                    charge_unit_types.append(c.charge_unit_type)
                    print(charge_unit_types,
                                '------------------------------------if-----------------------------------------')
            values_except_custom = list(filter(lambda x: x != 'custom', charge_unit_types))
            print(charge_unit_types,
                        '-----------------------------------------------------------------------------')
            print(values_except_custom, '-----------------------------------------------------------------------------')
            print(values_except_custom)
            # charge_unit_type = values_except_custom[0]
            charge_unit_type = values_except_custom[0] if values_except_custom else False
            print(charge_unit_types, charge_unit_type)

            print(charge_unit_types, charge_unit_type)
            uoms = []
            for u in storage_charges:
                if u.uom_id:
                    uoms.append(u.uom_id.id)
            print(uoms)
            inven = self.env['product.summary'].search(
                [('partner_id', '=', partner.id), ('quantity', '>', 0), ('storage_product', '=', False)])
            cbm = 0
            weight = 0
            sq = 0
            pallet = 0
            invoice_line_list = []
            summary_lines = []
            tsummary_lines = []

            if uoms:
                for uom in uoms:
                    print('uom---------------------')
                    quantity_dict[uom] = 0
                    for inv in inven:
                        print('inv---------------------')
                        if uom == inv.uom_id.id:
                            # ###print(inv.in_date, s, 'indate', inv.out_date, e, 'outdate')
                            if inv.in_date != False and inv.out_date != False and e >= inv.in_date >= s and s <= inv.out_date <= e and inv.storage_product == False:
                                quantity_dict[uom] += inv.quantity * inv.duration
                                print(inv.product_id.prod_volume, 'inv.product_id.prod_volume', inv.quantity,
                                      'inv.quantity', )
                                summ = ({
                                    'start_date': inv.in_date,
                                    'end_date': inv.out_date,
                                    'quantity': inv.quantity,
                                    'charge_type': 'storage',
                                    'product_id': inv.product_id.id,
                                    'charge_unit_type': 'custom',
                                })
                                summ_lines = self.env['summary.sheet.lines'].create(summ)
                                if summ_lines.quantity > 0:
                                    summary_lines.append(summ_lines)
                            elif inv.in_date != False and e >= inv.in_date >= s and inv.out_date == False and inv.storage_product == False:
                                duration = (abs((fields.Datetime.to_datetime(e)
                                                 - fields.Datetime.to_datetime(inv.in_date)).days) + 1)
                                quantity_dict[uom] += inv.quantity * duration
                                print(inv.product_id.prod_volume, 'inv.product_id.prod_volume', inv.quantity,
                                      'inv.quantity', )
                                summ = ({
                                    'start_date': inv.in_date,
                                    'end_date': e,
                                    'quantity': inv.quantity,
                                    'charge_type': 'storage',
                                    'product_id': inv.product_id.id,
                                    'charge_unit_type': 'custom',

                                })
                                summ_lines = self.env['summary.sheet.lines'].create(summ)
                                if summ_lines.quantity > 0:
                                    summary_lines.append(summ_lines)
                            elif inv.in_date != False and e >= inv.in_date <= s and s <= inv.out_date <= e and inv.storage_product == False:
                                duration = (abs((fields.Datetime.to_datetime(inv.out_date)
                                                 - fields.Datetime.to_datetime(s)).days) + 1)
                                quantity_dict[uom] += inv.quantity * duration
                                print(inv.product_id.prod_volume, 'inv.product_id.prod_volume', inv.quantity,
                                      'inv.quantity', )
                                summ = ({
                                    'start_date': s,
                                    'end_date': inv.out_date,
                                    'quantity': inv.quantity,
                                    'charge_type': 'storage',
                                    'product_id': inv.product_id.id,
                                    'charge_unit_type': 'custom',

                                })
                                summ_lines = self.env['summary.sheet.lines'].create(summ)
                                if summ_lines.quantity > 0:
                                    summary_lines.append(summ_lines)
                            elif inv.in_date != False and e >= inv.in_date <= s and s <= inv.out_date >= e and inv.storage_product == False:
                                duration = (abs((fields.Datetime.to_datetime(e)
                                                 - fields.Datetime.to_datetime(s)).days) + 1)
                                quantity_dict[uom] += inv.quantity * duration
                                summ = ({
                                    'start_date': s,
                                    'end_date': e,
                                    'quantity': inv.quantity,
                                    'charge_type': 'storage',
                                    'product_id': inv.product_id.id,
                                    'charge_unit_type': 'custom',

                                })
                                summ_lines = self.env['summary.sheet.lines'].create(summ)
                                if summ_lines.quantity > 0:
                                    summary_lines.append(summ_lines)
                            elif inv.in_date != False and inv.out_date != False and e >= inv.in_date >= s and s <= inv.out_date <= e and inv.storage_product == False:
                                ###print(inv.quantity, inv.duration)
                                duration = (abs((fields.Datetime.to_datetime(e)
                                                 - fields.Datetime.to_datetime(inv.in_date)).days) + 1)
                                quantity_dict[uom] += inv.quantity * duration
                                summ = ({
                                    'start_date': inv.in_date,
                                    'end_date': e,
                                    'quantity': inv.quantity,
                                    'charge_type': 'storage',
                                    'product_id': inv.product_id.id,
                                    'charge_unit_type': 'custom',

                                })
                                summ_lines = self.env['summary.sheet.lines'].create(summ)
                                if summ_lines.quantity > 0:
                                    summary_lines.append(summ_lines)
                            elif inv.in_date != False and e >= inv.in_date <= s and inv.out_date == False and inv.storage_product == False:
                                duration = (abs((fields.Datetime.to_datetime(e)
                                                 - fields.Datetime.to_datetime(s)).days) + 1)
                                quantity_dict[uom] += inv.quantity * duration
                                summ = ({
                                    'start_date': s,
                                    'end_date': e,
                                    'quantity': inv.quantity,
                                    'charge_type': 'storage',
                                    'product_id': inv.product_id.id,
                                    'charge_unit_type': 'custom',

                                })
                                summ_lines = self.env['summary.sheet.lines'].create(summ)
                                if summ_lines.quantity > 0:
                                    summary_lines.append(summ_lines)
                    continue
            else:
                for inv in inven:
                    # ###print(inv.in_date, s, 'indate', inv.out_date, e, 'outdate')
                    if inv.in_date != False and inv.out_date != False and e >= inv.in_date >= s and s <= inv.out_date <= e and inv.storage_product == False:
                        ###print(inv.quantity, inv.duration)
                        # ###print(cbm, weight, sq, pallet, '------0------------cbm, weight, sq, pallet-----------------')
                        cbm += inv.product_id.prod_volume * inv.quantity * inv.duration
                        sq += inv.product_id.prod_sqm * inv.quantity * inv.duration
                        pallet += inv.quantity
                        weight += inv.product_id.weight * inv.quantity * inv.duration
                        print(cbm, 'cbm')
                        print(inv.product_id.prod_volume, 'inv.product_id.prod_volume', inv.quantity,
                              'inv.quantity', )
                        ###print(cbm, weight, sq, pallet, '------11------------cbm, weight, sq, pallet-----------------')
                        summ = ({
                            'start_date': inv.in_date,
                            'end_date': inv.out_date,
                            'quantity': inv.quantity,
                            # 'cbm': cbm,
                            'cbm': inv.product_id.prod_volume,
                            'sqm': inv.product_id.prod_sqm,
                            'pallet': inv.quantity,
                            'weight': inv.product_id.weight,
                            'charge_type': 'storage',
                            'product_id': inv.product_id.id,
                            'charge_unit_type': charge_unit_type,

                        })
                        summ_lines = self.env['summary.sheet.lines'].create(summ)
                        if summ_lines.quantity > 0:
                            summary_lines.append(summ_lines)

                            # ###print(summ_lines, '$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$'
                            #         '$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$'
                            #         'SUM CREATED $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$')
                    elif inv.in_date != False and e >= inv.in_date >= s and inv.out_date == False and inv.storage_product == False:
                        ###print(inv.quantity, inv.duration)
                        duration = (abs((fields.Datetime.to_datetime(e)
                                         - fields.Datetime.to_datetime(inv.in_date)).days) + 1)
                        # ###print(cbm, weight, sq, pallet, '------0------------cbm, weight, sq, pallet-----------------')
                        cbm += inv.product_id.prod_volume * inv.quantity * duration
                        sq += inv.product_id.prod_sqm * inv.quantity * duration
                        pallet += inv.quantity
                        weight += inv.product_id.weight * inv.quantity * duration
                        print(cbm, 'cbm')
                        print(inv.product_id.prod_volume, 'inv.product_id.prod_volume', inv.quantity,
                              'inv.quantity', )
                        ###print(cbm, weight, sq, pallet, '------12------------cbm, weight, sq, pallet-----------------')
                        summ = ({
                            'start_date': inv.in_date,
                            'end_date': e,
                            'quantity': inv.quantity,
                            'cbm': inv.product_id.prod_volume,
                            'sqm': inv.product_id.prod_sqm,
                            'pallet': inv.quantity,
                            'weight': inv.product_id.weight,
                            'charge_type': 'storage',
                            'product_id': inv.product_id.id,
                            'charge_unit_type': charge_unit_type,


                        })
                        summ_lines = self.env['summary.sheet.lines'].create(summ)
                        if summ_lines.quantity > 0:
                            summary_lines.append(summ_lines)
                            # ###print(summ_lines, '$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$'
                            #         '$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$'
                            #         'SUM CREATED $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$')
                    elif inv.in_date != False and e >= inv.in_date <= s and s <= inv.out_date <= e and inv.storage_product == False:
                        ###print(inv.quantity, inv.duration)
                        duration = (abs((fields.Datetime.to_datetime(inv.out_date)
                                         - fields.Datetime.to_datetime(s)).days) + 1)
                        # ###print(cbm, weight, sq, pallet, '------0------------cbm, weight, sq, pallet-----------------')
                        cbm += inv.product_id.prod_volume * inv.quantity * duration
                        sq += inv.product_id.prod_sqm * inv.quantity * duration
                        pallet += inv.quantity
                        weight += inv.product_id.weight * inv.quantity * duration
                        print(cbm, 'cbm')
                        print(inv.product_id.prod_volume, 'inv.product_id.prod_volume', inv.quantity,
                              'inv.quantity', )
                        ###print(cbm, weight, sq, pallet, '------12------------cbm, weight, sq, pallet-----------------')
                        summ = ({
                            'start_date': s,
                            'end_date': inv.out_date,
                            'quantity': inv.quantity,
                            'cbm': inv.product_id.prod_volume,
                            'sqm': inv.product_id.prod_sqm,
                            'pallet': inv.quantity,
                            'weight': inv.product_id.weight,
                            'charge_type': 'storage',
                            'product_id': inv.product_id.id,
                            'charge_unit_type': charge_unit_type,

                        })
                        summ_lines = self.env['summary.sheet.lines'].create(summ)
                        if summ_lines.quantity > 0:
                            summary_lines.append(summ_lines)
                            # ###print(summ_lines, '$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$'
                            #                   '$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$'
                            #                   'SUM CREATED $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$')
                    elif inv.in_date != False and e >= inv.in_date <= s and s <= inv.out_date >= e and inv.storage_product == False:
                        ###print(inv.quantity, inv.duration)
                        duration = (abs((fields.Datetime.to_datetime(e)
                                         - fields.Datetime.to_datetime(s)).days) + 1)
                        # ###print(cbm, weight, sq, pallet, '----ujn--0------------cbm, weight, sq, pallet-----------------')
                        cbm += inv.product_id.prod_volume * inv.quantity * duration
                        sq += inv.product_id.prod_sqm * inv.quantity * duration
                        pallet += inv.quantity
                        weight += inv.product_id.weight * inv.quantity * duration
                        ###print(cbm, weight, sq, pallet, '------12------------cbm, weight, sq, pallet-----------------')
                        summ = ({
                            'start_date': s,
                            'end_date': e,
                            'quantity': inv.quantity,
                            'cbm': inv.product_id.prod_volume,
                            'sqm': inv.product_id.prod_sqm,
                            'pallet': inv.quantity,
                            'weight': inv.product_id.weight,
                            'charge_type': 'storage',
                            'product_id': inv.product_id.id,
                            'charge_unit_type': charge_unit_type,

                        })
                        summ_lines = self.env['summary.sheet.lines'].create(summ)
                        if summ_lines.quantity > 0:
                            summary_lines.append(summ_lines)
                            # ###print(summ_lines, '$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$'
                            #                   '$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$'
                            #                   'SUM CREATED $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$')
                    elif inv.in_date != False and inv.out_date != False and e >= inv.in_date >= s and s <= inv.out_date <= e and inv.storage_product == False:
                        ###print(inv.quantity, inv.duration)
                        duration = (abs((fields.Datetime.to_datetime(e)
                                         - fields.Datetime.to_datetime(inv.in_date)).days) + 1)
                        # ###print(cbm, weight, sq, pallet, '------0------------cbm, weight, sq, pallet-----------------')
                        cbm += inv.product_id.prod_volume * inv.quantity * duration
                        sq += inv.product_id.prod_sqm * inv.quantity * duration
                        pallet += inv.quantity
                        weight += inv.product_id.weight * inv.quantity * duration
                        ###print(cbm, weight, sq, pallet, '------13------------cbm, weight, sq, pallet-----------------')
                        summ = ({
                            'start_date': inv.in_date,
                            'end_date': e,
                            'quantity': inv.quantity,
                            'cbm': inv.product_id.prod_volume,
                            'sqm': inv.product_id.prod_sqm,
                            'pallet': inv.quantity,
                            'weight': inv.product_id.weight,
                            'charge_type': 'storage',
                            'product_id': inv.product_id.id,
                            'charge_unit_type': charge_unit_type,

                        })
                        summ_lines = self.env['summary.sheet.lines'].create(summ)
                        if summ_lines.quantity > 0:
                            summary_lines.append(summ_lines)
                        # ###print(summ_lines, '$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$'
                        #             '$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$'
                        #             'SUM CREATED $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$')
                    elif inv.in_date != False and e >= inv.in_date <= s and inv.out_date == False and inv.storage_product == False:
                        ###print(inv.quantity, inv.duration)
                        duration = (abs((fields.Datetime.to_datetime(e)
                                         - fields.Datetime.to_datetime(s)).days) + 1)
                        # ###print(cbm, weight, sq, pallet, '------0------------cbm, weight, sq, pallet-----------------')
                        cbm += inv.product_id.prod_volume * inv.quantity * duration
                        sq += inv.product_id.prod_sqm * inv.quantity * duration
                        pallet += inv.quantity
                        weight += inv.product_id.weight * inv.quantity * duration
                        ###print(cbm, weight, sq, pallet, '------14------------cbm, weight, sq, pallet-----------------')
                        summ = ({
                            'start_date': s,
                            'end_date': e,
                            'quantity': inv.quantity,
                            'cbm': inv.product_id.prod_volume,
                            'sqm': inv.product_id.prod_sqm,
                            'pallet': inv.quantity,
                            'weight': inv.product_id.weight,
                            'charge_type': 'storage',
                            'product_id': inv.product_id.id,
                            'charge_unit_type': charge_unit_type,

                        })
                        summ_lines = self.env['summary.sheet.lines'].create(summ)
                        if summ_lines.quantity > 0:
                            summary_lines.append(summ_lines)
                        # ###print(summ_lines, '$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$'
                        #             '$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$'
                        #             'SUM CREATED $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$')
            print(quantity_dict, 'quantity_dict')
            ###print(cbm, weight, sq, pallet, '---------3---------cbm, weight, sq, pallet-----------------')
            for temp in storage_charges:
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
                    if temp_line_values['quantity'] > 0:
                        invoice_line_list.append((0, 0, temp_line_values))
                        # ###print(temp_line_values,
                        #   '-------------------------------cbm------------------------------------')

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
                    if temp_line_values['quantity'] > 0:
                        invoice_line_list.append((0, 0, temp_line_values))
                        # ###print(temp_line_values, '---------------------------weight----------------------------')

                if temp.charge_type == 'storage' and temp.charge_unit_type == 'square':
                    temp_line_values = {
                        'product_id': temp.product_id and temp.product_id.id or False,
                        'name': temp.product_id.name or '',
                        'price_unit': temp.list_price or 0.00,
                        'quantity': sq,
                        'currency_id': temp.currency_id.id,
                        'account_id': temp.product_id.property_account_income_id.id if temp.product_id.property_account_income_id
                        else temp.product_id.categ_id.property_account_income_categ_id.id,
                        # 'start_date': move_ids_without_package.start_date,
                        # 'end_date': move_ids_without_package.end_date,

                    }
                    if temp_line_values['quantity'] > 0:
                        invoice_line_list.append((0, 0, temp_line_values))
                        # ###print(temp_line_values, '---------------------------square--------------------------')

                if temp.charge_type == 'storage' and temp.charge_unit_type == 'pallet':
                    temp_line_values = {
                        'product_id': temp.product_id and temp.product_id.id or False,
                        'name': temp.product_id.name or '',
                        'price_unit': temp.list_price or 0.00,
                        'quantity': pallet,
                        'currency_id': temp.currency_id.id,
                        'account_id': temp.product_id.property_account_income_id.id if temp.product_id.property_account_income_id
                        else temp.product_id.categ_id.property_account_income_categ_id.id,
                        # 'start_date': move_ids_without_package.start_date,
                        # 'end_date': move_ids_without_package.end_date,

                    }
                    if temp_line_values['quantity'] > 0:
                        invoice_line_list.append((0, 0, temp_line_values))
                        # ###print(temp_line_values, '------------------------------pallets----------------------')
                if temp.charge_type == 'storage' and temp.charge_unit_type == 'custom':
                    print(uoms, 'uoms')
                    if uoms:
                        for q in uoms:
                            v = temp.uom_id.id
                            value = quantity_dict[v]
                            qty = value
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
                            if temp_line_values['quantity'] > 0:
                                invoice_line_list.append((0, 0, temp_line_values))
                            break
            picking_id = self.env['stock.picking'].search(
                [('picking_type_id.code', '=', 'incoming'), ('partner_id', '=', partner.id),
                 ('scheduled_date', '>=', s)])
            for picking in picking_id:
                print('1')
                if s <= picking.scheduled_date <= e:
                    print('2', picking.service_id)
                    for pick in picking.service_id:
                        print('3', picking.service_id)
                        vals = (0, 0, {
                            'name': pick.product_id.name,
                            'product_id': pick.product_id.id,
                            'price_unit': pick.qty,
                            'account_id': pick.product_id.property_account_income_id.id if pick.product_id.property_account_income_id
                            else pick.product_id.categ_id.property_account_income_categ_id.id,
                            # 'tax_ids': [(6, 0, [pick.taxes_id.id])],
                            'quantity': pick.price,

                            # 'quantity': move_ids_without_package.quantt if move_ids_without_package.inv_meth else 1,
                            # 'x_cbm': picking.x_cbm,
                            # 'start_date': picking.scheduled_date,
                            # 'end_date': picking.date_done,

                        })
                        invoice_line_list.append(vals)
                        summ = ({
                            'start_date': s,
                            'end_date': e,
                            # 'container_type': temp.container.id,
                            'ref_no': picking.name,
                            'quantity': pick.qty,
                            # 'charge_type': 'inbound',
                            # 'in_ref_no' :

                        })
                        summ_lines = self.env['summary.sheet.lines'].create(summ)
                        if summ_lines.quantity > 0:
                            summary_lines.append(summ_lines)

            picking_id = self.env['stock.picking'].search(
                [('picking_type_id.code', '=', 'outgoing'), ('partner_id', '=', partner.id),
                 ('scheduled_date', '>=', s)])
            for picking in picking_id:
                if s <= picking.scheduled_date <= e:
                    for pick in picking.service_id:
                        vals = (0, 0, {
                            'name': pick.product_id.name,
                            'product_id': pick.product_id.id,
                            'price_unit': pick.qty,
                            'account_id': pick.product_id.property_account_income_id.id if pick.product_id.property_account_income_id
                            else pick.product_id.categ_id.property_account_income_categ_id.id,
                            # 'tax_ids': [(6, 0, [pick.taxes_id.id])],
                            'quantity': pick.price,

                            # 'quantity': move_ids_without_package.quantt if move_ids_without_package.inv_meth else 1,
                            # 'x_cbm': picking.x_cbm,
                            # 'start_date': picking.scheduled_date,
                            # 'end_date': picking.date_done,

                        })
                        invoice_line_list.append(vals)
                        summ = ({
                            'start_date': s,
                            'end_date': e,
                            # 'container_type': temp.container.id,
                            'ref_no': picking.name,
                            'quantity': pick.qty,
                            # 'charge_type': 'outbound',

                            # 'in_ref_no' :

                        })
                        summ_lines = self.env['summary.sheet.lines'].create(summ)
                        if summ_lines.quantity > 0:
                            summary_lines.append(summ_lines)


            current_user = self.env.uid
            # ###print(invoice_line_list, 'invoice_line_list')

            if agreement_id and invoice_line_list:
                invoice = partner.env['account.move'].create({
                    'type': 'out_invoice',
                    'invoice_origin': partner.name,
                    'invoice_user_id': current_user,
                    'narration': partner.name,
                    'partner_id': partner.id,
                    'currency_id': partner.env.user.company_id.currency_id.id,
                    # 'journal_id': int(customer_journal_id),
                    'invoice_payment_ref': partner.name,
                    # 'picking_id': picking_id.id,
                    'invoice_line_ids': invoice_line_list,
                    # 'invoice_type': 'storage',
                    'name': '/',

                })
                # invoice.consolidate_invoice_lines(invoice)

                ###print(invoice, 'Invoice Created')
                summary = ({
                    'name': str(s) + '-' + str(e),
                    'partner_id': partner.id,
                    'invoice_id': invoice.id
                })
                summary = self.env['summary.sheet'].create(summary)
                # ###print(summary_lines, 'summary_lines---fffffffffffffffffffffffffffffffffffffffff'
                #                      'ffffffffffffffffffffffffffffffffffffffffffffffffffffffff'
                #                      'ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff'
                #                      'fffffffffffffffffffffffffffffffffffffffffffffffffffffff'
                #                      'ffffffffffffffffffffffffffffffffffffffffffffffffff')
                for lines in summary_lines:
                    # ###print(lines.product_id.storage_type, '+++++++++++++++++++++========++++++++++++++++++++++++++'
                    #                                      '++++++++++++++++++++=a=====lines.product_id.storage_type'
                    #                                      '+++++++++++++++++++++++++++++++++++++++++++++++++++++++=++'
                    #                                      '')
                    lines['sheet_id'] = summary
                    # if not lines.product_id.storage_type:
                    #     lines['sheet_id'] = summary
                if invoice:
                    message = 'Cheers! Your Invoice is Successfully Crafted'
                    # return {
                    #     'type': 'ir.actions.client',
                    #     'tag': 'display_notification',
                    #     'params': {
                    #         'message': message,
                    #         'type': 'success'  # Use 'warning' for a warning notification
                    #     }
                    # }

            # ---------------------------------Storage Type Based Invoice----------------------------#
            agreement_id = partner.env['agreement'].search([('partner_id', '=', partner.id)])
            ###print(agreement_id, 'agreement_id')
            tstorage_charges = partner.env['agreement.charges'].search(
                ['&', ('charge_type', '=', 'storage'), ('agreement_id', '=', agreement_id.id),
                 ('storage_type', '!=', False)])
            tuoms = []
            tquantity_dict = {}
            for u in tstorage_charges:
                if u.uom_id:
                    tuoms.append(u.uom_id.id)
            print(tuoms, 'tuoms')
            tcharge_unit_types = []
            for c in tstorage_charges:
                if c.charge_unit_type:
                    print('-------------------if-------------------------')
                    tcharge_unit_types.append(c.charge_unit_type)
            tvalues_except_custom = list(filter(lambda x: x != 'custom', tcharge_unit_types))
            print(tvalues_except_custom)
            tcharge_unit_type = tvalues_except_custom[0] if tvalues_except_custom else False
            print(tcharge_unit_types, tcharge_unit_type)
            ###print(tstorage_charges, 'tstorage_charges')
            tinven = self.env['product.summary'].search(
                [('partner_id', '=', partner.id), ('storage_product', '=', True), ('quantity', '>', 0)])
            print(tinven, tcharge_unit_type, '--------------------------------tinven-----------------tcharge_unit_type----------------------------')

            ###print(tinven, 'tinven')
            tcbm = 0
            tweight = 0
            tsq = 0
            tpallet = 0
            tinvoice_line_list = []
            if tuoms:
                for uom in tuoms:
                    tquantity_dict[uom] = 0
                    for tinv in tinven:
                        print(uom, tinv.uom_id, '@@@@@@')
                        if uom == tinv.uom_id.id:
                            print('@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@')
                            ###print(tinv.storage_product, 'tinv.storage_product')
                            # ###print(tinv.in_date, s, 'indate', tinv.out_date, e, 'outdate')
                            if tinv.in_date != False and tinv.out_date != False and e >= tinv.in_date >= s and s <= tinv.out_date <= e and tinv.storage_product == True:
                                ###print(tinv.quantity, tinv.duration)
                                # ###print(tcbm, tweight, tsq, tpallet, '------0------------tcbm, tweight, tsq, tpallet-----------------')
                                # tcbm += tinv.product_id.x_vol * tinv.quantity * tinv.duration
                                # tsq += tinv.product_id.x_vol * tinv.quantity * tinv.duration
                                tcbm += tinv.product_id.prod_volume * tinv.quantity * tinv.duration
                                tsq += tinv.product_id.prod_sqm * tinv.quantity * tinv.duration
                                tpallet += tinv.quantity
                                tweight += tinv.product_id.weight * tinv.quantity * tinv.duration
                                tquantity_dict[uom] += tinv.quantity * tinv.duration
                                ###print(tcbm, tweight, tsq, tpallet,
                                # '------11------------tcbm, tweight, tsq, tpallet-----------------')
                                summ = ({
                                    'start_date': tinv.in_date,
                                    'end_date': tinv.out_date,
                                    'quantity': tinv.quantity,
                                    'cbm': tinv.product_id.prod_volume,
                                    'sqm': tinv.product_id.prod_sqm,
                                    'pallet': tinv.quantity,
                                    'weight': tinv.product_id.weight,
                                    'charge_type': 'storage',
                                    'product_id': tinv.product_id.id,
                                    'charge_unit_type': 'custom',
                                })
                                summ_lines = self.env['summary.sheet.lines'].create(summ)
                                if summ_lines.quantity > 0:
                                    tsummary_lines.append(summ_lines)
                                # ###print(summ_lines, '$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$'
                                #             '$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$'
                                #             'SUM CREATED $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$')
                            elif tinv.in_date != False and e >= tinv.in_date >= s and tinv.out_date == False and tinv.storage_product == True:
                                ###print(tinv.quantity, tinv.duration)
                                duration = (abs((fields.Datetime.to_datetime(e)
                                                 - fields.Datetime.to_datetime(tinv.in_date)).days) + 1)
                                # ###print(tcbm, tweight, tsq, tpallet, '------0------------tcbm, tweight, tsq, tpallet-----------------')
                                # tcbm += tinv.product_id.x_vol * tinv.quantity * tinv.duration
                                # tsq += tinv.product_id.x_vol * tinv.quantity * tinv.duration
                                tcbm += tinv.product_id.prod_volume * tinv.quantity * duration
                                tsq += tinv.product_id.prod_sqm * tinv.quantity * duration
                                tpallet += tinv.quantity
                                tweight += tinv.product_id.weight * tinv.quantity * duration
                                tquantity_dict[uom] += tinv.quantity * tinv.duration

                                ###print(tcbm, tweight, tsq, tpallet,
                                # '------12------------tcbm, tweight, tsq, tpallet-----------------')
                                summ = ({
                                    'start_date': tinv.in_date,
                                    'end_date': e,
                                    'quantity': tinv.quantity,
                                    'cbm': tinv.product_id.prod_volume,
                                    'sqm': tinv.product_id.prod_sqm,
                                    'pallet': tinv.quantity,
                                    'weight': tinv.product_id.weight,
                                    'charge_type': 'storage',
                                    'product_id': tinv.product_id.id,
                                    'charge_unit_type': 'custom',

                                })
                                summ_lines = self.env['summary.sheet.lines'].create(summ)
                                if summ_lines.quantity > 0:
                                    tsummary_lines.append(summ_lines)
                                # ###print(summ_lines, '$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$'
                                #             '$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$'
                                #             'SUM CREATED $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$')
                            # elif tinv.in_date != False and e >= tinv.in_date >= s and s <= tinv.out_date <= e and tinv.storage_product == True:
                            #     ###print(tinv.quantity, tinv.duration)
                            #     duration = abs((fields.Datetime.to_datetime(tinv.out_date)
                            #                     - fields.Datetime.to_datetime(s)).days)
                            #     # ###print(tcbm, tweight, tsq, tpallet, '------0------------tcbm, tweight, tsq, tpallet-----------------')
                            #     # tcbm += tinv.product_id.x_vol * tinv.quantity * tinv.duration
                            #     # tsq += tinv.product_id.x_vol * tinv.quantity * tinv.duration
                            #     tcbm += tinv.product_id.prod_volume * tinv.quantity * duration
                            #     tsq += tinv.product_id.prod_sqm * tinv.quantity * duration
                            #     tpallet += tinv.quantity
                            #     tweight += tinv.product_id.weight * tinv.quantity * duration
                            #     ###print(tcbm, tweight, tsq, tpallet,
                            #           '------13------------tcbm, tweight, tsq, tpallet-----------------')
                            #     summ = ({
                            #         'start_date': s,
                            #         'end_date': tinv.out_date,
                            #         'quantity': tinv.quantity,
                            #         'cbm': cbm,
                            #         'sqm': sq,
                            #         'pallet': pallet,
                            #         'weight': weight,
                            #     })
                            #     summ_lines = self.env['summary.sheet.lines'].create(summ)
                            #     summary_lines.append(summ_lines)
                            #     ###print(summ_lines, '$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$'
                            #                 '$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$'
                            #                 'SUM CREATED $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$')
                            elif tinv.in_date != False and e >= tinv.in_date <= s and s <= tinv.out_date <= e and tinv.storage_product == False:
                                ###print(tinv.quantity, tinv.duration)
                                duration = (abs((fields.Datetime.to_datetime(e)
                                                 - fields.Datetime.to_datetime(tinv.in_date)).days) + 1)
                                # ###print(cbm, weight, sq, pallet, '------0------------cbm, weight, sq, pallet-----------------')
                                # cbm += tinv.product_id.x_vol * tinv.quantity * tinv.duration
                                # sq += tinv.product_id.x_vol * tinv.quantity * tinv.duration
                                tcbm += tinv.product_id.prod_volume * tinv.quantity * duration
                                tsq += tinv.product_id.prod_sqm * tinv.quantity * duration
                                tpallet += tinv.quantity
                                tweight += tinv.product_id.weight * tinv.quantity * duration
                                tquantity_dict[uom] += tinv.quantity * tinv.duration

                                ###print(tcbm, tweight, tsq, tpallet, '------12------------tcbm, tweight, sq, pallet-----------------')
                                summ = ({
                                    'start_date': tinv.in_date,
                                    'end_date': tinv.out_date,
                                    'quantity': tinv.quantity,
                                    'cbm': tinv.product_id.prod_volume,
                                    'sqm': tinv.product_id.prod_sqm,
                                    'pallet': tinv.quantity,
                                    'weight': tinv.product_id.weight,
                                    'charge_type': 'storage',
                                    'product_id': tinv.product_id.id,
                                    'charge_unit_type': 'custom',

                                })
                                summ_lines = self.env['summary.sheet.lines'].create(summ)
                                if summ_lines.quantity > 0:
                                    tsummary_lines.append(summ_lines)
                            elif tinv.in_date != False and e >= tinv.in_date <= s and s <= tinv.out_date >= e and tinv.storage_product == False:
                                ###print(tinv.quantity, tinv.duration)
                                duration = (abs((fields.Datetime.to_datetime(e)
                                                 - fields.Datetime.to_datetime(s)).days) + 1)
                                # ###print(cbm, weight, sq, pallet, '------0------------cbm, weight, sq, pallet-----------------')
                                # cbm += tinv.product_id.x_vol * tinv.quantity * tinv.duration
                                # sq += tinv.product_id.x_vol * tinv.quantity * tinv.duration
                                tcbm += tinv.product_id.prod_volume * tinv.quantity * duration
                                tsq += tinv.product_id.prod_sqm * tinv.quantity * duration
                                tpallet += tinv.quantity
                                tweight += tinv.product_id.weight * tinv.quantity * duration
                                tquantity_dict[uom] += tinv.quantity * tinv.duration

                                ###print(tcbm, tweight, tsq, tpallet, '------12------------tcbm, tweight, sq, pallet-----------------')
                                summ = ({
                                    'start_date': s,
                                    'end_date': e,
                                    'quantity': tinv.quantity,
                                    'cbm': tinv.product_id.prod_volume,
                                    'sqm': tinv.product_id.prod_sqm,
                                    'pallet': tinv.quantity,
                                    'weight': tinv.product_id.weight,
                                    'charge_type': 'storage',
                                    'product_id': tinv.product_id.id,
                                    'charge_unit_type': 'custom',

                                })
                                summ_lines = self.env['summary.sheet.lines'].create(summ)
                                if summ_lines.quantity > 0:
                                    tsummary_lines.append(summ_lines)
                            elif tinv.in_date != False and e >= tinv.in_date <= s and tinv.out_date == False and tinv.storage_product == True:
                                ###print(tinv.quantity, tinv.duration)
                                duration = (abs((fields.Datetime.to_datetime(e)
                                                 - fields.Datetime.to_datetime(s)).days) + 1)
                                # ###print(tcbm, tweight, tsq, tpallet, '------0------------tcbm, tweight, tsq, tpallet-----------------')
                                # tcbm += tinv.product_id.x_vol * tinv.quantity * tinv.duration
                                # tsq += tinv.product_id.x_vol * tinv.quantity * tinv.duration
                                tcbm += tinv.product_id.prod_volume * tinv.quantity * duration
                                tsq += tinv.product_id.prod_sqm * tinv.quantity * duration
                                tpallet += tinv.quantity
                                tweight += tinv.product_id.weight * tinv.quantity * duration
                                tquantity_dict[uom] += tinv.quantity * tinv.duration

                                ###print(tcbm, tweight, tsq, tpallet,
                                # '------14------------tcbm, tweight, tsq, tpallet-----------------')
                                summ = ({
                                    'start_date': s,
                                    'end_date': e,
                                    'quantity': tinv.quantity,
                                    'cbm': tinv.product_id.prod_volume,
                                    'sqm': tinv.product_id.prod_sqm,
                                    'pallet': tinv.quantity,
                                    'weight': tinv.product_id.weight,
                                    'charge_type': 'storage',
                                    'product_id': tinv.product_id.id,
                                    'charge_unit_type': 'custom',

                                })

                                summ_lines = self.env['summary.sheet.lines'].create(summ)
                                if summ_lines.quantity > 0:
                                    tsummary_lines.append(summ_lines)
                                # ###print(summ_lines, '$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$'
                                #             '$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$'
                                #             'SUM CREATED $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$')
                        print('++++++++++++++++++++++=tquantity_dict[uom]+++++++++++++++++++++++++', tquantity_dict[uom])

            else:
                for tinv in tinven:
                    print(tcharge_unit_type, '---------------------tcharge_unit_type-------------')
                    ###print(tinv.storage_product, 'tinv.storage_product')
                    # ###print(tinv.in_date, s, 'indate', tinv.out_date, e, 'outdate')
                    if tinv.in_date != False and tinv.out_date != False and e >= tinv.in_date >= s and s <= tinv.out_date <= e and tinv.storage_product == True:
                        ###print(tinv.quantity, tinv.duration)
                        # ###print(tcbm, tweight, tsq, tpallet, '------0------------tcbm, tweight, tsq, tpallet-----------------')
                        # tcbm += tinv.product_id.x_vol * tinv.quantity * tinv.duration
                        # tsq += tinv.product_id.x_vol * tinv.quantity * tinv.duration
                        tcbm += tinv.product_id.prod_volume * tinv.quantity * tinv.duration
                        tsq += tinv.product_id.prod_sqm * tinv.quantity * tinv.duration
                        tpallet += tinv.quantity
                        tweight += tinv.product_id.weight * tinv.quantity * tinv.duration
                        ###print(tcbm, tweight, tsq, tpallet,
                        # '------11------------tcbm, tweight, tsq, tpallet-----------------')
                        summ = ({
                            'start_date': tinv.in_date,
                            'end_date': tinv.out_date,
                            'quantity': tinv.quantity,
                            'cbm': tinv.product_id.prod_volume,
                            'sqm': tinv.product_id.prod_sqm,
                            'pallet': tinv.quantity,
                            'weight': tinv.product_id.weight,
                            'charge_type': 'storage',
                            'product_id': tinv.product_id.id,
                            'charge_unit_type': tcharge_unit_type,
                        })
                        summ_lines = self.env['summary.sheet.lines'].create(summ)
                        if summ_lines.quantity > 0:
                            tsummary_lines.append(summ_lines)
                        # ###print(summ_lines, '$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$'
                        #             '$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$'
                        #             'SUM CREATED $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$')
                    elif tinv.in_date != False and e >= tinv.in_date >= s and tinv.out_date == False and tinv.storage_product == True:
                        ###print(tinv.quantity, tinv.duration)
                        duration = (abs((fields.Datetime.to_datetime(e)
                                         - fields.Datetime.to_datetime(tinv.in_date)).days) + 1)
                        # ###print(tcbm, tweight, tsq, tpallet, '------0------------tcbm, tweight, tsq, tpallet-----------------')
                        # tcbm += tinv.product_id.x_vol * tinv.quantity * tinv.duration
                        # tsq += tinv.product_id.x_vol * tinv.quantity * tinv.duration
                        tcbm += tinv.product_id.prod_volume * tinv.quantity * duration
                        tsq += tinv.product_id.prod_sqm * tinv.quantity * duration
                        tpallet += tinv.quantity
                        tweight += tinv.product_id.weight * tinv.quantity * duration
                        ###print(tcbm, tweight, tsq, tpallet,
                        # '------12------------tcbm, tweight, tsq, tpallet-----------------')
                        summ = ({
                            'start_date': tinv.in_date,
                            'end_date': e,
                            'quantity': tinv.quantity,
                            'cbm': tinv.product_id.prod_volume,
                            'sqm': tinv.product_id.prod_sqm,
                            'pallet': tinv.quantity,
                            'weight': tinv.product_id.weight,
                            'charge_type': 'storage',
                            'product_id': tinv.product_id.id,
                            'charge_unit_type': tcharge_unit_type,

                        })
                        summ_lines = self.env['summary.sheet.lines'].create(summ)
                        if summ_lines.quantity > 0:
                            tsummary_lines.append(summ_lines)
                        # ###print(summ_lines, '$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$'
                        #             '$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$'
                        #             'SUM CREATED $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$')
                    # elif tinv.in_date != False and e >= tinv.in_date >= s and s <= tinv.out_date <= e and tinv.storage_product == True:
                    #     ###print(tinv.quantity, tinv.duration)
                    #     duration = abs((fields.Datetime.to_datetime(tinv.out_date)
                    #                     - fields.Datetime.to_datetime(s)).days)
                    #     # ###print(tcbm, tweight, tsq, tpallet, '------0------------tcbm, tweight, tsq, tpallet-----------------')
                    #     # tcbm += tinv.product_id.x_vol * tinv.quantity * tinv.duration
                    #     # tsq += tinv.product_id.x_vol * tinv.quantity * tinv.duration
                    #     tcbm += tinv.product_id.prod_volume * tinv.quantity * duration
                    #     tsq += tinv.product_id.prod_sqm * tinv.quantity * duration
                    #     tpallet += tinv.quantity
                    #     tweight += tinv.product_id.weight * tinv.quantity * duration
                    #     ###print(tcbm, tweight, tsq, tpallet,
                    #           '------13------------tcbm, tweight, tsq, tpallet-----------------')
                    #     summ = ({
                    #         'start_date': s,
                    #         'end_date': tinv.out_date,
                    #         'quantity': tinv.quantity,
                    #         'cbm': cbm,
                    #         'sqm': sq,
                    #         'pallet': pallet,
                    #         'weight': weight,
                    #     })
                    #     summ_lines = self.env['summary.sheet.lines'].create(summ)
                    #     summary_lines.append(summ_lines)
                    #     ###print(summ_lines, '$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$'
                    #                 '$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$'
                    #                 'SUM CREATED $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$')
                    elif tinv.in_date != False and e >= tinv.in_date <= s and s <= tinv.out_date <= e and tinv.storage_product == False:
                        ###print(tinv.quantity, tinv.duration)
                        duration = (abs((fields.Datetime.to_datetime(e)
                                         - fields.Datetime.to_datetime(tinv.in_date)).days) + 1)
                        # ###print(cbm, weight, sq, pallet, '------0------------cbm, weight, sq, pallet-----------------')
                        # cbm += tinv.product_id.x_vol * tinv.quantity * tinv.duration
                        # sq += tinv.product_id.x_vol * tinv.quantity * tinv.duration
                        tcbm += tinv.product_id.prod_volume * tinv.quantity * duration
                        tsq += tinv.product_id.prod_sqm * tinv.quantity * duration
                        tpallet += tinv.quantity
                        tweight += tinv.product_id.weight * tinv.quantity * duration
                        ###print(tcbm, tweight, tsq, tpallet, '------12------------tcbm, tweight, sq, pallet-----------------')
                        summ = ({
                            'start_date': tinv.in_date,
                            'end_date': tinv.out_date,
                            'quantity': tinv.quantity,
                            'cbm': tinv.product_id.prod_volume,
                            'sqm': tinv.product_id.prod_sqm,
                            'pallet': tinv.quantity,
                            'weight': tinv.product_id.weight,
                            'charge_type': 'storage',
                            'product_id': tinv.product_id.id,
                            'charge_unit_type': tcharge_unit_type,

                        })
                        summ_lines = self.env['summary.sheet.lines'].create(summ)
                        if summ_lines.quantity > 0:
                            tsummary_lines.append(summ_lines)
                    elif tinv.in_date != False and e >= tinv.in_date <= s and s <= tinv.out_date >= e and tinv.storage_product == False:
                        ###print(tinv.quantity, tinv.duration)
                        duration = (abs((fields.Datetime.to_datetime(e)
                                         - fields.Datetime.to_datetime(s)).days) + 1)
                        # ###print(cbm, weight, sq, pallet, '------0------------cbm, weight, sq, pallet-----------------')
                        # cbm += tinv.product_id.x_vol * tinv.quantity * tinv.duration
                        # sq += tinv.product_id.x_vol * tinv.quantity * tinv.duration
                        tcbm += tinv.product_id.prod_volume * tinv.quantity * duration
                        tsq += tinv.product_id.prod_sqm * tinv.quantity * duration
                        tpallet += tinv.quantity
                        tweight += tinv.product_id.weight * tinv.quantity * duration
                        ###print(tcbm, tweight, tsq, tpallet, '------12------------tcbm, tweight, sq, pallet-----------------')
                        summ = ({
                            'start_date': s,
                            'end_date': e,
                            'quantity': tinv.quantity,
                            'cbm': tinv.product_id.prod_volume,
                            'sqm': tinv.product_id.prod_sqm,
                            'pallet': tinv.quantity,
                            'weight': tinv.product_id.weight,
                            'charge_type': 'storage',
                            'product_id': tinv.product_id.id,
                            'charge_unit_type': tcharge_unit_type,

                        })
                        summ_lines = self.env['summary.sheet.lines'].create(summ)
                        if summ_lines.quantity > 0:
                            tsummary_lines.append(summ_lines)
                    elif tinv.in_date != False and e >= tinv.in_date <= s and tinv.out_date == False and tinv.storage_product == True:
                        ###print(tinv.quantity, tinv.duration)
                        duration = (abs((fields.Datetime.to_datetime(e)
                                         - fields.Datetime.to_datetime(s)).days) + 1)
                        # ###print(tcbm, tweight, tsq, tpallet, '------0------------tcbm, tweight, tsq, tpallet-----------------')
                        # tcbm += tinv.product_id.x_vol * tinv.quantity * tinv.duration
                        # tsq += tinv.product_id.x_vol * tinv.quantity * tinv.duration
                        tcbm += tinv.product_id.prod_volume * tinv.quantity * duration
                        tsq += tinv.product_id.prod_sqm * tinv.quantity * duration
                        tpallet += tinv.quantity
                        tweight += tinv.product_id.weight * tinv.quantity * duration
                        ###print(tcbm, tweight, tsq, tpallet,
                        # '------14------------tcbm, tweight, tsq, tpallet-----------------')
                        summ = ({
                            'start_date': s,
                            'end_date': e,
                            'quantity': tinv.quantity,
                            'cbm': tinv.product_id.prod_volume,
                            'sqm': tinv.product_id.prod_sqm,
                            'pallet': tinv.quantity,
                            'weight': tinv.product_id.weight,
                            'charge_type': 'storage',
                            'product_id': tinv.product_id.id,
                            'charge_unit_type': tcharge_unit_type,

                        })

                        summ_lines = self.env['summary.sheet.lines'].create(summ)
                        if summ_lines.quantity > 0:
                            tsummary_lines.append(summ_lines)
                        # ###print(summ_lines, '$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$'
                        #             '$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$'
                        #             'SUM CREATED $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$')
                    #     ###print(tcbm, tweight, tsq, tpallet, '------1------------tcbm, tweight, tsq, tpallet-----------------')
                    # ###print(tcbm, tweight, tsq, tpallet, '--------2----------tcbm, tweight, tsq, tpallet-----------------')
            ###print(tcbm, tweight, tsq, tpallet, '---------3---------tcbm, tweight, tsq, tpallet-----------------')
            for temp in tstorage_charges:
                if temp.charge_type == 'storage' and temp.charge_unit_type == 'cbm':
                    temp_line_values = {
                        'product_id': temp.product_id and temp.product_id.id or False,
                        'name': temp.product_id.name or '',
                        'price_unit': temp.list_price or 0.00,
                        'quantity': tcbm,
                        'currency_id': temp.currency_id.id,
                        'account_id': temp.product_id.property_account_income_id.id if temp.product_id.property_account_income_id
                        else temp.product_id.categ_id.property_account_income_categ_id.id,
                        # 'start_date': move_ids_without_package.start_date,
                        # 'end_date': move_ids_without_package.end_date,

                    }
                    if temp_line_values['quantity'] > 0:
                        tinvoice_line_list.append((0, 0, temp_line_values))
                        # ###print(temp_line_values,
                        #   '-------------------------------tcbm------------------------------------')

                if temp.charge_type == 'storage' and temp.charge_unit_type == 'weight':
                    temp_line_values = {
                        'product_id': temp.product_id and temp.product_id.id or False,
                        'name': temp.product_id.name or '',
                        'price_unit': temp.list_price or 0.00,
                        'quantity': tweight,
                        'currency_id': temp.currency_id.id,
                        'account_id': temp.product_id.property_account_income_id.id if temp.product_id.property_account_income_id
                        else temp.product_id.categ_id.property_account_income_categ_id.id,
                        # 'start_date': move_ids_without_package.start_date,
                        # 'end_date': move_ids_without_package.end_date,

                    }
                    if temp_line_values['quantity'] > 0:
                        tinvoice_line_list.append((0, 0, temp_line_values))
                        # ###print(temp_line_values, '---------------------------tw'
                        #                     '`qwweight----------------------------')

                if temp.charge_type == 'storage' and temp.charge_unit_type == 'square':
                    temp_line_values = {
                        'product_id': temp.product_id and temp.product_id.id or False,
                        'name': temp.product_id.name or '',
                        'price_unit': temp.list_price or 0.00,
                        'quantity': tsq,
                        'currency_id': temp.currency_id.id,
                        'account_id': temp.product_id.property_account_income_id.id if temp.product_id.property_account_income_id
                        else temp.product_id.categ_id.property_account_income_categ_id.id,
                        # 'start_date': move_ids_without_package.start_date,
                        # 'end_date': move_ids_without_package.end_date,

                    }
                    if temp_line_values['quantity'] > 0:
                        tinvoice_line_list.append((0, 0, temp_line_values))
                        # ###print(temp_line_values, '---------------------------tsquare--------------------------')

                if temp.charge_type == 'storage' and temp.charge_unit_type == 'pallet':
                    temp_line_values = {
                        'product_id': temp.product_id and temp.product_id.id or False,
                        'name': temp.product_id.name or '',
                        'price_unit': temp.list_price or 0.00,
                        'quantity': tpallet,
                        'currency_id': temp.currency_id.id,
                        'account_id': temp.product_id.property_account_income_id.id if temp.product_id.property_account_income_id
                        else temp.product_id.categ_id.property_account_income_categ_id.id,
                        # 'start_date': move_ids_without_package.start_date,
                        # 'end_date': move_ids_without_package.end_date,

                    }
                    if temp_line_values['quantity'] > 0:
                        tinvoice_line_list.append((0, 0, temp_line_values))
                        # ###print(temp_line_values, '------------------------------tpallets----------------------')
                if temp.charge_type == 'storage' and temp.charge_unit_type == 'custom':
                    print(tuoms, 'uoms')
                    if tuoms:
                        for q in tuoms:
                            v = temp.uom_id.id
                            print(tquantity_dict, '-----------------tquantity_dict---------------------')
                            value = tquantity_dict[v]
                            qty = value
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
                            if temp_line_values['quantity'] > 0:
                                tinvoice_line_list.append((0, 0, temp_line_values))
                                # ###print(temp_line_values, '------------------------------pallets----------------------')


            ###IN###
            in_charges = partner.env['agreement.charges'].search(
                ['&', ('charge_type', '=', 'inbound'), ('agreement_id', '=', agreement_id.id)])
            ###print(in_charges, 'in_charges')
            # tinvoice_line_list = []
            # tinvoice_line_liststo = []
            if tinvoice_line_list:
                for temp in in_charges:
                    ###print(temp.storage_type)
                    in_pick_cont = self.env['stock.picking'].search_count(
                        [('picking_type_id.code', '=', 'incoming'),
                         ('container', '=', temp.container.id), ('state', '=', 'done'),
                         ('scheduled_date', '>', s), ('partner_id', '=', partner.id),
                         ('product_id.storage_type', '=', in_charges.storage_type.id)])
                    in_pick_cont_len = self.env['stock.picking'].search(
                        [('picking_type_id.code', '=', 'incoming'),
                         ('container', '=', temp.container.id), ('state', '=', 'done'),
                         ('scheduled_date', '>', s), ('partner_id', '=', partner.id),
                         ('product_id.storage_type', '=', in_charges.storage_type.id)])
                    in_cnt2 = []
                    for r in in_pick_cont_len:
                        in_cnt2.append(r.name)
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
                    if temp_line_values['quantity'] > 0:
                        tinvoice_line_list.append((0, 0, temp_line_values))
                        # ###print(tinvoice_line_list, 'tinvoice_line_list')
                    summ = ({
                        'start_date': s,
                        'end_date': e,
                        'container_type': temp.container.id,
                        'ref_no': in_cnt2,
                        'quantity': in_pick_cont,
                        'charge_type': 'inbound',

                    })
                    summ_lines = self.env['summary.sheet.lines'].create(summ)
                    if summ_lines.quantity > 0:
                        tsummary_lines.append(summ_lines)
                    #
                    # ###print(summ_lines, '$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$'
                    #                   '$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$'
                    #                   'IN SUM CREATED $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$')

            ###OUT###
            out_charges = partner.env['agreement.charges'].search(
                ['&', ('charge_type', '=', 'outbound'), ('agreement_id', '=', agreement_id.id)])
            ###print(out_charges, 'out_chsrgs')
            if tinvoice_line_list:
                for temp in out_charges:
                    out_pick_cont = self.env['stock.picking'].search_count(
                        [('picking_type_id.code', '=', 'outgoing'), ('container', '=', temp.container.id),
                         ('scheduled_date', '>', s), ('partner_id', '=', partner.id), ('state', '=', 'done'),
                         ('product_id.storage_type', '=', out_charges.storage_type.id)])
                    out_pick_cont_len = self.env['stock.picking'].search(
                        [('picking_type_id.code', '=', 'outgoing'), ('container', '=', temp.container.id),
                         ('scheduled_date', '>', s), ('partner_id', '=', partner.id), ('state', '=', 'done'),
                         ('product_id.storage_type', '=', out_charges.storage_type.id)])
                    out_cnt2 = []
                    for r in out_pick_cont_len:
                        out_cnt2.append(r.name)
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
                    if temp_line_values['quantity'] > 0:
                        tinvoice_line_list.append((0, 0, temp_line_values))
                        # ###print(tinvoice_line_list, 'tinvoice_line_list')
                    summ = ({
                        'start_date': s,
                        'end_date': e,
                        'container_type': temp.container.id,
                        'ref_no': out_cnt2,
                        'quantity': out_pick_cont,
                        'charge_type': 'outbound',

                    })
                    summ_lines = self.env['summary.sheet.lines'].create(summ)
                    if summ_lines.quantity > 0:
                        tsummary_lines.append(summ_lines)

                    # ###print(summ_lines, '$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$'
                    #                   '$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$'
                    #                   'OUT SUM CREATED $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$')

            ###VALUEADDED###
            added_charges = partner.env['agreement.charges'].search(
                ['&', ('charge_type', '=', 'value_added'), ('agreement_id', '=', agreement_id.id)])
            ###print(added_charges, 'valueadded')
            if tinvoice_line_list:
                for temp in added_charges:
                    added_pick_count = self.env['stock.picking'].search_count(
                        [('picking_type_id.code', '!=', 'internal'),
                         ('added_service', '=', temp.added_service.id), ('scheduled_date', '>', s),
                         ('state', '=', 'done'), ('product_id.storage_type', '!=', added_charges.storage_type.id)])
                    added_pick_count_len = self.env['stock.picking'].search(
                        [('picking_type_id.code', '!=', 'internal'),
                         ('added_service', '=', temp.added_service.id), ('scheduled_date', '>', s),
                         ('state', '=', 'done'), ('product_id.storage_type', '=', added_charges.storage_type.id)])
                    add_cnt2 = []
                    for r in added_pick_count_len:
                        add_cnt2.append(r.name)
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
                    if temp_line_values['quantity'] > 0:
                        tinvoice_line_list.append((0, 0, temp_line_values))
                        # ###print(tinvoice_line_list, 'tinvoice_line_list')
                    summ = ({
                        'start_date': s,
                        'end_date': e,
                        'added_service': temp.added_service.id,
                        'ref_no': add_cnt2,
                        'quantity': added_pick_count,
                        'charge_type': 'value_added',

                    })
                    summ_lines = self.env['summary.sheet.lines'].create(summ)
                    if summ_lines.quantity > 0:
                        tsummary_lines.append(summ_lines)

                    # ###print(summ_lines, '$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$'
                    #                   '$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$'
                    #                   'VALUE ADDED SUM CREATED $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$')

            ###INVMANAGEMNET###
            inv_charges = partner.env['agreement.charges'].search(
                ['&', ('charge_type', '=', 'inventory_mgmnt'), ('agreement_id', '=', agreement_id.id)])
            ###print(added_charges, 'invcharges')
            if tinvoice_line_list:
                for temp in inv_charges:
                    added_pick_count = self.env['stock.picking'].search_count(
                        [('picking_type_id.code', '!=', 'internal'),
                         ('scheduled_date', '>', s), ('state', '=', 'done')])
                    added_pick_count_len = self.env['stock.picking'].search(
                        [('picking_type_id.code', '!=', 'internal'),
                         ('scheduled_date', '>', s), ('state', '=', 'done')])
                    add_cnt2 = []
                    for r in added_pick_count_len:
                        add_cnt2.append(r.name)
                    # added_pick_count = len(added_pick_count_len)
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
                    if temp_line_values['quantity'] > 0:
                        tinvoice_line_list.append((0, 0, temp_line_values))
                    summ = ({
                        'start_date': s,
                        'end_date': e,
                        'added_service': temp.added_service.id,
                        'ref_no': add_cnt2,
                        'quantity': added_pick_count,
                        'charge_type': 'inventory_mgmnt',

                    })
                    summ_lines = self.env['summary.sheet.lines'].create(summ)
                    if summ_lines.quantity > 0:
                        tsummary_lines.append(summ_lines)

                    # ###print(summ_lines, '$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$'
                    #                   '$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$'
                    #                   'INV MGMNT SERVICE SUM CREATED $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$')

            current_user = self.env.uid
            print(tinvoice_line_list, 'tinvoice_line_list')

            if agreement_id and tinvoice_line_list:
                tinvoice = partner.env['account.move'].create({
                    'type': 'out_invoice',
                    'invoice_origin': partner.name,
                    'invoice_user_id': current_user,
                    'narration': partner.name,
                    'partner_id': partner.id,
                    'currency_id': partner.env.user.company_id.currency_id.id,
                    # 'journal_id': int(customer_journal_id),
                    'invoice_payment_ref': partner.name,
                    # 'picking_id': picking_id.id,
                    'invoice_line_ids': tinvoice_line_list,
                    # 'invoice_type': 'storage',
                    'name': '/',

                })
                # tinvoice.consolidate_invoice_lines(tinvoice)

                ###print(invoice, tinvoice_line_list, 'TInvoice Created')
                tsummary = ({
                    'name': str(s) + '-' + str(e) + '-' + 'Temperature Control',
                    'partner_id': partner.id,
                    'invoice_id': tinvoice.id
                })
                tsummary = self.env['summary.sheet'].create(tsummary)
                # ###print(tsummary_lines, 'tsummary_linesummary_lines---fffffffffffffffffffffffffffffffffffffffff'
                #                      'ffffffffffffffffffffffffffffffffffffffffffffffffffffffff'
                #                      'ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff'
                #                      'fffffffffffffffffffffffffffffffffffffffffffffffffffffff'
                #                      'ffffffffffffffffffffffffffffffffffffffffffffffffff')
                for lines in tsummary_lines:
                    lines['sheet_id'] = tsummary
                if tinvoice:
                    message = 'Cheers! Your Invoice is Successfully Crafted'
                    return {
                        'type': 'ir.actions.client',
                        'tag': 'display_notification',
                        'params': {
                            'message': message,
                            'type': 'success'  # Use 'warning' for a warning notification
                        }
                    }
                    # if lines.product_id.storage_type:
                    #     lines['sheet_id'] = tsummary
