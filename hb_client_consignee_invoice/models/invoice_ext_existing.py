from dateutil import parser
from odoo import api, models, fields, http, _
from datetime import datetime, date, timedelta
from odoo.exceptions import AccessError, UserError, ValidationError
import logging

logger = logging.getLogger(__name__)


class Partnerforminherit(models.Model):
    _inherit = "res.partner"

    def create_inv_invoice_coreeexist(self):
        invoice_type = self.env['ir.config_parameter'].sudo().get_param(
            'hb_wms_invoice_v1.invoice_type')
        if invoice_type == 'con':
            return self.create_inv_invoice_core_consolidatedexist()
        elif invoice_type == 'sep':
            return self.create_inv_invoice_core_seperateexist()
        else:
            raise ValidationError(_('Please configure the Invoice Type from the Settings'))

    def create_inv_invoice_core_consolidatedexist(self):
        invoices = []
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
            charge_unit_types = {}
            for c in storage_charges:
                chrg = c['charge_unit_type']['name']
                sto = c['storage_uom']
                charge_unit_types[chrg] = sto

            # charge_unit_types = []
            # for c in storage_charges:
            #     if c.charge_unit_type:
            #         charge_unit_types.append(c.charge_unit_type.name)
            # values_except_UOM = list(filter(lambda x: x != 'UOM', charge_unit_types))
            values_except_UOM = {chrg: sto for chrg, sto in charge_unit_types.items() if chrg != 'UOM' and
                                 chrg in ['CBM', 'Pallet', 'Square Units', 'Weight']}
            other_values = {chrg: sto for chrg, sto in charge_unit_types.items() if chrg not in
                            ['CBM', 'Pallet', 'Square Units', 'Weight', 'UOM']}

            # charge_unit_type = values_except_UOM[0]
            # charge_unit_type = values_except_UOM[0] if values_except_UOM else False
            uoms = {}
            for u in storage_charges:
                if u.uom_id:
                    uom = u['uom_id']['id']
                    unit = u['storage_uom']
                    uoms[uom] = unit
            inven = self.env['product.summary'].search(
                [('partner_id', '=', partner.id), ('storage_product', '=', False),('gen_seperate_inv','=',False)])

            invoice_line_list = []
            summary_lines = []
            tsummary_lines = []

            if uoms:
                for uom, unit in uoms.items():
                    quantity_dict[uom] = 0
                    for inv in inven:
                        UOM = self.env['charge.types'].search([('name', '=', 'UOM')])
                        if uom == inv.uom_id.id:
                            if inv.charge_unit_type.name == 'UOM' and inv.in_date != False and inv.out_date != False and e >= inv.in_date >= s and s <= inv.out_date <= e and inv.storage_product == False:

                                if unit == 'month':
                                    quantity_dict[uom] += inv.out_qty if inv.out_qty > 0 else inv.quantity
                                else:
                                    quantity_dict[
                                        uom] += inv.out_qty if inv.out_qty > 0 else inv.quantity * inv.duration

                                summ = ({
                                    'start_date': inv.in_date,
                                    'end_date': inv.out_date,
                                    'quantity': inv.out_qty if inv.out_qty > 0 else inv.quantity,
                                    'charge_type': 'storage',
                                    'product_id': inv.product_id.id,
                                    'charge_unit_type': UOM[0].id,
                                })
                                summ_lines = self.env['summary.sheet.lines'].create(summ)
                                if summ_lines.quantity > 0:
                                    summary_lines.append(summ_lines)
                            elif inv.charge_unit_type.name == 'UOM' and inv.in_date != False and e >= inv.in_date >= s and inv.out_date == False and inv.storage_product == False:
                                duration = (abs((fields.Datetime.to_datetime(e).date()
                                                 - fields.Datetime.to_datetime(inv.in_date).date()).days) + 1)
                                if unit == 'month':
                                    quantity_dict[uom] += inv.out_qty if inv.out_qty > 0 else inv.quantity
                                else:
                                    quantity_dict[uom] += inv.out_qty if inv.out_qty > 0 else inv.quantity * duration
                                # quantity_dict[uom] += inv.out_qty if inv.out_qty > 0 else inv.quantity * duration
                                summ = ({
                                    'start_date': inv.in_date,
                                    'end_date': e,
                                    'quantity': inv.out_qty if inv.out_qty > 0 else inv.quantity,
                                    'charge_type': 'storage',
                                    'product_id': inv.product_id.id,
                                    'charge_unit_type': UOM[0].id,

                                })
                                summ_lines = self.env['summary.sheet.lines'].create(summ)
                                if summ_lines.quantity > 0:
                                    summary_lines.append(summ_lines)
                            elif inv.charge_unit_type.name == 'UOM' and inv.in_date != False and inv.out_date != False and e >= inv.in_date <= s and s <= inv.out_date <= e and inv.storage_product == False:
                                duration = (abs((fields.Datetime.to_datetime(inv.out_date).date()
                                                 - fields.Datetime.to_datetime(s).date()).days) + 1)
                                # quantity_dict[uom] += inv.out_qty if inv.out_qty > 0 else inv.quantity * duration
                                if unit == 'month':
                                    quantity_dict[uom] += inv.out_qty if inv.out_qty > 0 else inv.quantity
                                else:
                                    quantity_dict[uom] += inv.out_qty if inv.out_qty > 0 else inv.quantity * duration
                                summ = ({
                                    'start_date': s,
                                    'end_date': inv.out_date,
                                    'quantity': inv.out_qty if inv.out_qty > 0 else inv.quantity,
                                    'charge_type': 'storage',
                                    'product_id': inv.product_id.id,
                                    'charge_unit_type': UOM[0].id,

                                })
                                summ_lines = self.env['summary.sheet.lines'].create(summ)
                                if summ_lines.quantity > 0:
                                    summary_lines.append(summ_lines)
                            elif inv.charge_unit_type.name == 'UOM' and inv.in_date != False and inv.out_date != False and e >= inv.in_date <= s and s <= inv.out_date >= e and inv.storage_product == False:
                                duration = (abs((fields.Datetime.to_datetime(e).date()
                                                 - fields.Datetime.to_datetime(s).date()).days) + 1)
                                # quantity_dict[uom] += inv.out_qty if inv.out_qty > 0 else inv.quantity * duration
                                if unit == 'month':
                                    quantity_dict[uom] += inv.out_qty if inv.out_qty > 0 else inv.quantity
                                else:
                                    quantity_dict[uom] += inv.out_qty if inv.out_qty > 0 else inv.quantity * duration
                                summ = ({
                                    'start_date': s,
                                    'end_date': e,
                                    'quantity': inv.out_qty if inv.out_qty > 0 else inv.quantity,
                                    'charge_type': 'storage',
                                    'product_id': inv.product_id.id,
                                    'charge_unit_type': UOM[0].id,

                                })
                                summ_lines = self.env['summary.sheet.lines'].create(summ)
                                if summ_lines.quantity > 0:
                                    summary_lines.append(summ_lines)
                            elif inv.charge_unit_type.name == 'UOM' and inv.in_date != False and inv.out_date != False and inv.out_date != False and e >= inv.in_date >= s and s <= inv.out_date <= e and inv.storage_product == False:
                                duration = (abs((fields.Datetime.to_datetime(e).date()
                                                 - fields.Datetime.to_datetime(inv.in_date).date()).days) + 1)
                                # quantity_dict[uom] += inv.out_qty if inv.out_qty > 0 else inv.quantity * duration
                                if unit == 'month':
                                    quantity_dict[uom] += inv.out_qty if inv.out_qty > 0 else inv.quantity
                                else:
                                    quantity_dict[uom] += inv.out_qty if inv.out_qty > 0 else inv.quantity * duration
                                summ = ({
                                    'start_date': inv.in_date,
                                    'end_date': e,
                                    'quantity': inv.out_qty if inv.out_qty > 0 else inv.quantity,
                                    'charge_type': 'storage',
                                    'product_id': inv.product_id.id,
                                    'charge_unit_type': UOM[0].id,

                                })
                                summ_lines = self.env['summary.sheet.lines'].create(summ)
                                if summ_lines.quantity > 0:
                                    summary_lines.append(summ_lines)
                            elif inv.charge_unit_type.name == 'UOM' and inv.in_date != False and e >= inv.in_date <= s and inv.out_date == False and inv.storage_product == False:
                                duration = (abs((fields.Datetime.to_datetime(e).date()
                                                 - fields.Datetime.to_datetime(s).date()).days) + 1)
                                # quantity_dict[uom] += inv.out_qty if inv.out_qty > 0 else inv.quantity * duration
                                if unit == 'month':
                                    quantity_dict[uom] += inv.out_qty if inv.out_qty > 0 else inv.quantity
                                else:
                                    quantity_dict[uom] += inv.out_qty if inv.out_qty > 0 else inv.quantity * duration
                                summ = ({
                                    'start_date': s,
                                    'end_date': e,
                                    'quantity': inv.out_qty if inv.out_qty > 0 else inv.quantity,
                                    'charge_type': 'storage',
                                    'product_id': inv.product_id.id,
                                    'charge_unit_type': UOM[0].id,

                                })
                                summ_lines = self.env['summary.sheet.lines'].create(summ)
                                if summ_lines.quantity > 0:
                                    summary_lines.append(summ_lines)
                            elif inv.charge_unit_type.name == 'UOM' and inv.out_date != False and inv.in_date != False and e >= inv.in_date >= s and s <= inv.out_date >= e and inv.storage_product == False:
                                duration = (abs((fields.Datetime.to_datetime(e).date()
                                                 - fields.Datetime.to_datetime(inv.in_date).date()).days) + 1)
                                if unit == 'month':
                                    quantity_dict[uom] += inv.out_qty if inv.out_qty > 0 else inv.quantity
                                else:
                                    quantity_dict[uom] += inv.out_qty if inv.out_qty > 0 else inv.quantity * duration
                                summ = ({
                                    'start_date': s,
                                    'end_date': e,
                                    'quantity': inv.out_qty if inv.out_qty > 0 else inv.quantity,
                                    'charge_type': 'storage',
                                    'product_id': inv.product_id.id,
                                    'charge_unit_type': UOM[0].id,

                                })
                                summ_lines = self.env['summary.sheet.lines'].create(summ)
                                if summ_lines.quantity > 0:
                                    summary_lines.append(summ_lines)
                    continue
                for temp in storage_charges:
                    if temp.charge_type == 'storage' and temp.charge_unit_type.name == 'UOM':
                        if uoms:
                            for q in uoms:
                                v = temp.uom_id.id
                                value = quantity_dict[v]
                                qty = value
                                temp_line_values = {
                                    'product_id': temp.product_id and temp.product_id.id or False,
                                    'name': temp.product_id.name or '',
                                    'price_unit': temp.list_price or 0.00,
                                    'quantity': qty,
                                    'currency_id': temp.currency_id.id,
                                    'tax_ids': [(6, 0, [temp.tax_id.id])] if temp.tax_id else False,
                                    'account_id': temp.product_id.property_account_income_id.id if temp.product_id.property_account_income_id
                                    else temp.product_id.categ_id.property_account_income_categ_id.id,
                                    # 'start_date': move_ids_without_package.start_date,
                                    # 'end_date': move_ids_without_package.end_date,
                                }
                                if temp_line_values['quantity'] > 0:
                                    invoice_line_list.append((0, 0, temp_line_values))
                                break

            if values_except_UOM:
                cbm = 0
                weight = 0
                sq = 0
                pallet = 0
                pallets = []
                types = []

                for values, unit in values_except_UOM.items():
                    chrg_unit_type = self.env['charge.types'].search([('name', '=', values)])
                    for inv in inven:
                        # print(s, 's', e, 'e', inv.in_date, 'in', inv.out_date, 'out', values, 'values',
                        #       inv.charge_unit_type.name, 'inv.charge_unit_type.name', inv.storage_product,
                        #       'inv.storage_product')
                        if values != 'Ppallet':
                            if values == inv.charge_unit_type.name and inv.in_date != False and inv.out_date != False and e >= inv.in_date >= s and s <= inv.out_date <= e and inv.storage_product == False:
                                print(inv.duration, 'dur 1', inv.product_id.prod_volume, inv.out_qty, inv.quantity)
                                if inv.charge_unit_type.name not in types:
                                    types.append(inv.charge_unit_type.name)
                                if unit == 'month':
                                    if values == 'CBM':
                                        cbm += inv.product_id.prod_volume * inv.out_qty if inv.out_qty > 0 else inv.product_id.prod_volume * inv.quantity
                                    if values == 'Square Units':
                                        sq += inv.product_id.prod_sqm * inv.out_qty if inv.out_qty > 0 else inv.product_id.prod_sqm * inv.quantity
                                    if values == 'Pallet':
                                        if inv.pallet_id:
                                            if inv.pallet_id.id not in pallets:
                                                pallets.append(inv.pallet_id.id)
                                        # pallet += 1
                                    if values == 'Weight':
                                        weight += inv.product_id.weight * inv.out_qty if inv.out_qty > 0 else inv.product_id.weight * inv.quantity
                                else:
                                    if values == 'CBM':
                                        cbm += inv.product_id.prod_volume * inv.out_qty * inv.duration if inv.out_qty > 0 else inv.product_id.prod_volume * inv.quantity * inv.duration
                                    if values == 'Square Units':
                                        sq += inv.product_id.prod_sqm * inv.out_qty * inv.duration if inv.out_qty > 0 else inv.product_id.prod_sqm * inv.quantity * inv.duration
                                    # if values == 'Pallet':
                                    #     pallet += 1 * inv.duration
                                    if values == 'Weight':
                                        weight += inv.product_id.weight * inv.out_qty * inv.duration if inv.out_qty > 0 else inv.product_id.weight * inv.quantity * inv.duration

                                summ = ({
                                    'start_date': inv.in_date,
                                    'end_date': inv.out_date,
                                    'quantity': inv.out_qty if inv.out_qty > 0 else inv.quantity,
                                    # 'cbm': cbm,
                                    'cbm': inv.product_id.prod_volume,
                                    'sqm': inv.product_id.prod_sqm,
                                    'pallet': 1,
                                    'weight': inv.product_id.weight,
                                    'charge_type': 'storage',
                                    'product_id': inv.product_id.id,
                                    'charge_unit_type': chrg_unit_type[0].id,

                                })
                                summ_lines = self.env['summary.sheet.lines'].create(summ)
                                # if summ_lines.quantity > 0 and values != 'Pallet' and unit != 'month':
                                #     summary_lines.append(summ_lines)
                                # if summ_lines.quantity > 0 and values == 'Pallet' and unit != 'month':
                                #     summary_lines.append(summ_lines)
                                if summ_lines.quantity > 0:
                                    summary_lines.append(summ_lines)
                            elif values == inv.charge_unit_type.name and inv.in_date != False and e >= inv.in_date >= s and inv.out_date == False and inv.storage_product == False:
                                if inv.charge_unit_type.name not in types:
                                    types.append(inv.charge_unit_type.name)
                                duration = (abs((fields.Datetime.to_datetime(e).date()
                                                 - fields.Datetime.to_datetime(inv.in_date).date()).days) + 1)
                                print(duration, 'dur 2', inv.product_id.prod_volume, inv.out_qty, inv.quantity)
                                if unit == 'month':
                                    if values == 'CBM':
                                        cbm += inv.product_id.prod_volume * inv.out_qty if inv.out_qty > 0 else inv.product_id.prod_volume * inv.quantity
                                    if values == 'Square Units':
                                        sq += inv.product_id.prod_sqm * inv.out_qty if inv.out_qty > 0 else inv.product_id.prod_sqm * inv.quantity
                                    if values == 'Pallet':
                                        if inv.pallet_id:
                                            if inv.pallet_id.id not in pallets:
                                                pallets.append(inv.pallet_id.id)
                                        # pallet += 1
                                    if values == 'Weight':
                                        weight += inv.product_id.weight * inv.out_qty if inv.out_qty > 0 else inv.product_id.weight * inv.quantity
                                else:
                                    if values == 'CBM':
                                        cbm += inv.product_id.prod_volume * inv.out_qty * duration if inv.out_qty > 0 else inv.product_id.prod_volume * inv.quantity * duration
                                    if values == 'Square Units':
                                        sq += inv.product_id.prod_sqm * inv.out_qty * duration if inv.out_qty > 0 else inv.product_id.prod_sqm * inv.quantity * duration
                                    # if values == 'Pallet':
                                    #     pallet += 1 * duration
                                    if values == 'Weight':
                                        weight += inv.product_id.weight * inv.out_qty * duration if inv.out_qty > 0 else inv.product_id.weight * inv.quantity * duration
                                summ = ({
                                    'start_date': inv.in_date,
                                    'end_date': e,
                                    'quantity': inv.out_qty if inv.out_qty > 0 else inv.quantity,
                                    'cbm': inv.product_id.prod_volume,
                                    'sqm': inv.product_id.prod_sqm,
                                    'pallet': 1,
                                    'weight': inv.product_id.weight,
                                    'charge_type': 'storage',
                                    'product_id': inv.product_id.id,
                                    'charge_unit_type': chrg_unit_type[0].id,

                                })
                                summ_lines = self.env['summary.sheet.lines'].create(summ)

                                if summ_lines.quantity > 0:
                                    summary_lines.append(summ_lines)
                            elif values == inv.charge_unit_type.name and inv.in_date != False and inv.out_date != False and e >= inv.in_date <= s and s <= inv.out_date <= e and inv.storage_product == False:
                                if inv.charge_unit_type.name not in types:
                                    types.append(inv.charge_unit_type.name)
                                duration = (abs((fields.Datetime.to_datetime(inv.out_date).date()
                                                 - fields.Datetime.to_datetime(s).date()).days) + 1)
                                print(inv.out_date, s, duration, 'dur 3', inv.product_id.prod_volume, inv.out_qty,
                                      inv.quantity)
                                if unit == 'month':
                                    if values == 'CBM':
                                        cbm += inv.product_id.prod_volume * inv.out_qty if inv.out_qty > 0 else inv.product_id.prod_volume * inv.quantity
                                    if values == 'Square Units':
                                        sq += inv.product_id.prod_sqm * inv.out_qty if inv.out_qty > 0 else inv.product_id.prod_sqm * inv.quantity
                                    if values == 'Pallet':
                                        if inv.pallet_id:
                                            if inv.pallet_id.id not in pallets:
                                                pallets.append(inv.pallet_id.id)
                                        # pallet += 1
                                    if values == 'Weight':
                                        weight += inv.product_id.weight * inv.out_qty if inv.out_qty > 0 else inv.product_id.weight * inv.quantity
                                else:
                                    if values == 'CBM':
                                        cbm += inv.product_id.prod_volume * inv.out_qty * duration if inv.out_qty > 0 else inv.product_id.prod_volume * inv.quantity * duration
                                    if values == 'Square Units':
                                        sq += inv.product_id.prod_sqm * inv.out_qty * duration if inv.out_qty > 0 else inv.product_id.prod_sqm * inv.quantity * duration
                                    # if values == 'Pallet':
                                    #     pallet += 1 * duration
                                    if values == 'Weight':
                                        weight += inv.product_id.weight * inv.out_qty * duration if inv.out_qty > 0 else inv.product_id.weight * inv.quantity * duration
                                summ = ({
                                    'start_date': s,
                                    'end_date': inv.out_date,
                                    'quantity': inv.out_qty if inv.out_qty > 0 else inv.quantity,
                                    'cbm': inv.product_id.prod_volume,
                                    'sqm': inv.product_id.prod_sqm,
                                    'pallet': 1,
                                    'weight': inv.product_id.weight,
                                    'charge_type': 'storage',
                                    'product_id': inv.product_id.id,
                                    'charge_unit_type': chrg_unit_type[0].id,

                                })
                                summ_lines = self.env['summary.sheet.lines'].create(summ)
                                # if summ_lines.quantity > 0 and values != 'Pallet' and unit != 'month':
                                #     summary_lines.append(summ_lines)
                                # if summ_lines.quantity > 0 and values == 'Pallet' and unit != 'month':
                                #     summary_lines.append(summ_lines)
                                if summ_lines.quantity > 0:
                                    summary_lines.append(summ_lines)
                            elif values == inv.charge_unit_type.name and inv.in_date != False and inv.out_date != False and e >= inv.in_date <= s and s <= inv.out_date >= e and inv.storage_product == False:
                                if inv.charge_unit_type.name not in types:
                                    types.append(inv.charge_unit_type.name)
                                duration = (abs((fields.Datetime.to_datetime(e).date()
                                                 - fields.Datetime.to_datetime(s).date()).days) + 1)
                                print(duration, 'dur 4', inv.product_id.prod_volume, inv.out_qty, inv.quantity)
                                if unit == 'month':
                                    if values == 'CBM':
                                        cbm += inv.product_id.prod_volume * inv.out_qty if inv.out_qty > 0 else inv.product_id.prod_volume * inv.quantity
                                    if values == 'Square Units':
                                        sq += inv.product_id.prod_sqm * inv.out_qty if inv.out_qty > 0 else inv.product_id.prod_sqm * inv.quantity
                                    if values == 'Pallet':
                                        if inv.pallet_id:
                                            if inv.pallet_id.id not in pallets:
                                                pallets.append(inv.pallet_id.id)
                                        # pallet += 1
                                    if values == 'Weight':
                                        weight += inv.product_id.weight * inv.out_qty if inv.out_qty > 0 else inv.product_id.weight * inv.quantity
                                else:
                                    if values == 'CBM':
                                        cbm += inv.product_id.prod_volume * inv.out_qty * duration if inv.out_qty > 0 else inv.product_id.prod_volume * inv.quantity * duration
                                    if values == 'Square Units':
                                        sq += inv.product_id.prod_sqm * inv.out_qty * duration if inv.out_qty > 0 else inv.product_id.prod_sqm * inv.quantity * duration
                                    # if values == 'Pallet':
                                    #     pallet += 1 * duration
                                    if values == 'Weight':
                                        weight += inv.product_id.weight * inv.out_qty * duration if inv.out_qty > 0 else inv.product_id.weight * inv.quantity * duration
                                summ = ({
                                    'start_date': s,
                                    'end_date': e,
                                    'quantity': inv.out_qty if inv.out_qty > 0 else inv.quantity,
                                    'cbm': inv.product_id.prod_volume,
                                    'sqm': inv.product_id.prod_sqm,
                                    'pallet': 1,
                                    'weight': inv.product_id.weight,
                                    'charge_type': 'storage',
                                    'product_id': inv.product_id.id,
                                    'charge_unit_type': chrg_unit_type[0].id,

                                })
                                summ_lines = self.env['summary.sheet.lines'].create(summ)
                                # if summ_lines.quantity > 0 and values != 'Pallet' and unit != 'month':
                                #     summary_lines.append(summ_lines)
                                # if summ_lines.quantity > 0 and values == 'Pallet' and unit != 'month':
                                #     summary_lines.append(summ_lines)
                                if summ_lines.quantity > 0:
                                    summary_lines.append(summ_lines)
                            elif values == inv.charge_unit_type.name and inv.in_date != False and inv.out_date != False and e >= inv.in_date >= s and s <= inv.out_date <= e and inv.storage_product == False:
                                if inv.charge_unit_type.name not in types:
                                    types.append(inv.charge_unit_type.name)
                                duration = (abs((fields.Datetime.to_datetime(e).date()
                                                 - fields.Datetime.to_datetime(inv.in_date).date()).days) + 1)
                                print(duration, 'dur 5', inv.product_id.prod_volume, inv.out_qty, inv.quantity)
                                if unit == 'month':
                                    if values == 'CBM':
                                        cbm += inv.product_id.prod_volume * inv.out_qty if inv.out_qty > 0 else inv.product_id.prod_volume * inv.quantity
                                    if values == 'Square Units':
                                        sq += inv.product_id.prod_sqm * inv.out_qty if inv.out_qty > 0 else inv.product_id.prod_sqm * inv.quantity
                                    if values == 'Pallet':
                                        if inv.pallet_id:
                                            if inv.pallet_id.id not in pallets:
                                                pallets.append(inv.pallet_id.id)
                                        # pallet += 1
                                    if values == 'Weight':
                                        weight += inv.product_id.weight * inv.out_qty if inv.out_qty > 0 else inv.product_id.weight * inv.quantity
                                else:
                                    if values == 'CBM':
                                        cbm += inv.product_id.prod_volume * inv.out_qty * duration if inv.out_qty > 0 else inv.product_id.prod_volume * inv.quantity * duration
                                    if values == 'Square Units':
                                        sq += inv.product_id.prod_sqm * inv.out_qty * duration if inv.out_qty > 0 else inv.product_id.prod_sqm * inv.quantity * duration
                                    # if values == 'Pallet':
                                    #     pallet += 1 * duration
                                    if values == 'Weight':
                                        weight += inv.product_id.weight * inv.out_qty * duration if inv.out_qty > 0 else inv.product_id.weight * inv.quantity * duration
                                summ = ({
                                    'start_date': inv.in_date,
                                    'end_date': e,
                                    'quantity': inv.out_qty if inv.out_qty > 0 else inv.quantity,
                                    'cbm': inv.product_id.prod_volume,
                                    'sqm': inv.product_id.prod_sqm,
                                    'pallet': 1,
                                    'weight': inv.product_id.weight,
                                    'charge_type': 'storage',
                                    'product_id': inv.product_id.id,
                                    'charge_unit_type': chrg_unit_type[0].id,

                                })
                                summ_lines = self.env['summary.sheet.lines'].create(summ)
                                # if summ_lines.quantity > 0 and values != 'Pallet' and unit != 'month':
                                #     summary_lines.append(summ_lines)
                                # if summ_lines.quantity > 0 and values == 'Pallet' and unit != 'month':
                                #     summary_lines.append(summ_lines)
                                if summ_lines.quantity > 0:
                                    summary_lines.append(summ_lines)
                            elif values == inv.charge_unit_type.name and inv.in_date != False and e >= inv.in_date <= s and inv.out_date == False and inv.storage_product == False:
                                if inv.charge_unit_type.name not in types:
                                    types.append(inv.charge_unit_type.name)
                                duration = (abs((fields.Datetime.to_datetime(e).date()
                                                 - fields.Datetime.to_datetime(s).date()).days) + 1)
                                print(duration, 'dur 6', inv.product_id.prod_volume, inv.out_qty, inv.quantity)
                                if unit == 'month':
                                    if values == 'CBM':
                                        cbm += inv.product_id.prod_volume * inv.out_qty if inv.out_qty > 0 else inv.product_id.prod_volume * inv.quantity
                                    if values == 'Square Units':
                                        sq += inv.product_id.prod_sqm * inv.out_qty if inv.out_qty > 0 else inv.product_id.prod_sqm * inv.quantity
                                    if values == 'Pallet':
                                        if inv.pallet_id:
                                            if inv.pallet_id.id not in pallets:
                                                pallets.append(inv.pallet_id.id)
                                        # pallet += 1
                                    if values == 'Weight':
                                        weight += inv.product_id.weight * inv.out_qty if inv.out_qty > 0 else inv.product_id.weight * inv.quantity
                                else:
                                    if values == 'CBM':
                                        cbm += inv.product_id.prod_volume * inv.out_qty * duration if inv.out_qty > 0 else inv.product_id.prod_volume * inv.quantity * duration
                                    if values == 'Square Units':
                                        sq += inv.product_id.prod_sqm * inv.out_qty * duration if inv.out_qty > 0 else inv.product_id.prod_sqm * inv.quantity * duration
                                    # if values == 'Pallet':
                                    #     pallet += 1 * duration
                                    if values == 'Weight':
                                        weight += inv.product_id.weight * inv.out_qty * duration if inv.out_qty > 0 else inv.product_id.weight * inv.quantity * duration
                                summ = ({
                                    'start_date': s,
                                    'end_date': e,
                                    'quantity': inv.out_qty if inv.out_qty > 0 else inv.quantity,
                                    'cbm': inv.product_id.prod_volume,
                                    'sqm': inv.product_id.prod_sqm,
                                    'pallet': 1,
                                    'weight': inv.product_id.weight,
                                    'charge_type': 'storage',
                                    'product_id': inv.product_id.id,
                                    'charge_unit_type': chrg_unit_type[0].id,

                                })
                                summ_lines = self.env['summary.sheet.lines'].create(summ)
                                # if summ_lines.quantity > 0 and values != 'Pallet' and unit != 'month':
                                #     summary_lines.append(summ_lines)
                                # if summ_lines.quantity > 0 and values == 'Pallet' and unit != 'month':
                                #     summary_lines.append(summ_lines)
                                if summ_lines.quantity > 0:
                                    summary_lines.append(summ_lines)
                            elif values == inv.charge_unit_type.name and inv.out_date != False and inv.in_date != False and e >= inv.in_date >= s and s <= inv.out_date >= e and inv.storage_product == False:
                                if inv.charge_unit_type.name not in types:
                                    types.append(inv.charge_unit_type.name)
                                duration = (abs((fields.Datetime.to_datetime(e).date()
                                                 - fields.Datetime.to_datetime(inv.in_date).date()).days) + 1)
                                print(duration, 'dur 7', inv.product_id.prod_volume, inv.out_qty, inv.quantity)
                                if unit == 'month':
                                    if values == 'CBM':
                                        cbm += inv.product_id.prod_volume * inv.out_qty if inv.out_qty > 0 else inv.product_id.prod_volume * inv.quantity
                                    if values == 'Square Units':
                                        sq += inv.product_id.prod_sqm * inv.out_qty if inv.out_qty > 0 else inv.product_id.prod_sqm * inv.quantity
                                    if values == 'Pallet':
                                        if inv.pallet_id:
                                            if inv.pallet_id.id not in pallets:
                                                pallets.append(inv.pallet_id.id)
                                        # pallet += 1
                                    if values == 'Weight':
                                        weight += inv.product_id.weight * inv.out_qty if inv.out_qty > 0 else inv.product_id.weight * inv.quantity
                                else:
                                    if values == 'CBM':
                                        cbm += inv.product_id.prod_volume * inv.out_qty * duration if inv.out_qty > 0 else inv.product_id.prod_volume * inv.quantity * duration
                                    if values == 'Square Units':
                                        sq += inv.product_id.prod_sqm * inv.out_qty * duration if inv.out_qty > 0 else inv.product_id.prod_sqm * inv.quantity * duration
                                    # if values == 'Pallet':
                                    #     pallet += 1 * duration
                                    if values == 'Weight':
                                        weight += inv.product_id.weight * inv.out_qty * duration if inv.out_qty > 0 else inv.product_id.weight * inv.quantity * duration
                                summ = ({
                                    'start_date': s,
                                    'end_date': e,
                                    'quantity': inv.out_qty if inv.out_qty > 0 else inv.quantity,
                                    'cbm': inv.product_id.prod_volume,
                                    'sqm': inv.product_id.prod_sqm,
                                    'pallet': 1,
                                    'weight': inv.product_id.weight,
                                    'charge_type': 'storage',
                                    'product_id': inv.product_id.id,
                                    'charge_unit_type': chrg_unit_type[0].id,

                                })
                                summ_lines = self.env['summary.sheet.lines'].create(summ)
                                # if summ_lines.quantity > 0 and values != 'Pallet' and unit != 'month':
                                #     summary_lines.append(summ_lines)
                                # if summ_lines.quantity > 0 and values == 'Pallet' and unit != 'month':
                                #     summary_lines.append(summ_lines)
                                if summ_lines.quantity > 0:
                                    summary_lines.append(summ_lines)

                            # break
                    print(inven, '-------------------inven------------')

                    pals = inven.filtered(lambda inv: inv.charge_unit_type.name == 'Pallet')
                    max = {}
                    for pinv in pals:
                        if values == pinv.charge_unit_type.name and pinv.in_date != False and pinv.out_date != False and e >= pinv.in_date >= s and s <= pinv.out_date <= e and pinv.storage_product == False:
                            print(pinv.duration, '-------dur 1')
                            duration = pinv.duration
                            pinv.duration_inv = duration
                            max[pinv] = {
                                'pallet_id': pinv.pallet_id.id,
                                'duration': duration}
                            # max[pinv] = {'summ': pinv,
                            #              'duration': duration,
                            #              }                                         }

                        elif values == pinv.charge_unit_type.name and pinv.in_date != False and e >= pinv.in_date >= s and pinv.out_date == False and pinv.storage_product == False:
                            if pinv.charge_unit_type.name not in types:
                                types.append(pinv.charge_unit_type.name)
                            duration = (abs((fields.Datetime.to_datetime(e).date()
                                             - fields.Datetime.to_datetime(pinv.in_date).date()).days) + 1)
                            pinv.duration_inv = duration
                            max[pinv] = {
                                'pallet_id': pinv.pallet_id.id,
                                'duration': duration}

                        elif values == pinv.charge_unit_type.name and pinv.in_date != False and pinv.out_date != False and e >= pinv.in_date <= s and s <= pinv.out_date <= e and pinv.storage_product == False:
                            if pinv.charge_unit_type.name not in types:
                                types.append(pinv.charge_unit_type.name)
                            duration = (abs((fields.Datetime.to_datetime(pinv.out_date).date()
                                             - fields.Datetime.to_datetime(s).date()).days) + 1)
                            pinv.duration_inv = duration
                            max[pinv] = {
                                'pallet_id': pinv.pallet_id.id,
                                'duration': duration}


                        elif values == pinv.charge_unit_type.name and pinv.in_date != False and pinv.out_date != False and e >= pinv.in_date <= s and s <= pinv.out_date >= e and pinv.storage_product == False:
                            if pinv.charge_unit_type.name not in types:
                                types.append(pinv.charge_unit_type.name)
                            duration = (abs((fields.Datetime.to_datetime(e).date()
                                             - fields.Datetime.to_datetime(s).date()).days) + 1)
                            pinv.duration_inv = duration
                            max[pinv] = {
                                'pallet_id': pinv.pallet_id.id,
                                'duration': duration}


                        elif values == pinv.charge_unit_type.name and pinv.in_date != False and pinv.out_date != False and e >= pinv.in_date >= s and s <= pinv.out_date <= e and pinv.storage_product == False:
                            if pinv.charge_unit_type.name not in types:
                                types.append(pinv.charge_unit_type.name)
                            duration = (abs((fields.Datetime.to_datetime(e).date()
                                             - fields.Datetime.to_datetime(pinv.in_date).date()).days) + 1)
                            pinv.duration_inv = duration
                            max[pinv] = {
                                'pallet_id': pinv.pallet_id.id,
                                'duration': duration}


                        elif pinv.out_date == False and values == pinv.charge_unit_type.name and pinv.in_date != False and e >= pinv.in_date <= s and pinv.storage_product == False:
                            if pinv.charge_unit_type.name not in types:
                                types.append(pinv.charge_unit_type.name)
                            duration = (abs((fields.Datetime.to_datetime(e).date()
                                             - fields.Datetime.to_datetime(s).date()).days) + 1)
                            pinv.duration_inv = duration
                            max[pinv] = {
                                'pallet_id': pinv.pallet_id.id,
                                'duration': duration}


                        elif pinv.out_date != False and values == pinv.charge_unit_type.name and pinv.in_date != False and pinv.out_date != False and e >= pinv.in_date >= s and s <= pinv.out_date >= e and pinv.storage_product == False:

                            if pinv.charge_unit_type.name not in types:
                                types.append(pinv.charge_unit_type.name)
                            duration = (abs((fields.Datetime.to_datetime(e).date()
                                             - fields.Datetime.to_datetime(pinv.in_date).date()).days) + 1)
                            pinv.duration_inv = duration
                            max[pinv] = {
                                'pallet_id': pinv.pallet_id.id,
                                'duration': duration}

                    print(max, '----------max')
                    MAX = max
                    data_list = [(key, value) for key, value in max.items()]

                    # Sort the list based on pallet_id
                    data_list.sort(key=lambda x: (x[1]['pallet_id'], -x[1]['duration']))

                    # Create a new dictionary to store the sorted and filtered data
                    sorted_data = {}

                    # Iterate through the sorted list and keep the summary records with the highest duration for each unique pallet_id
                    seen_pallets = set()
                    sorted_summ = []
                    for summary, info in data_list:
                        pallet_id = info['pallet_id']
                        duration = info['duration']

                        # If pallet_id is False, skip this entry
                        if pallet_id is False:
                            continue

                        # If pallet_id is not seen before or has a higher duration, add it to the new dictionary
                        if pallet_id not in seen_pallets or duration > sorted_data[pallet_id]['duration']:
                            sorted_data[pallet_id] = {'summary': summary, 'duration': duration}
                            seen_pallets.add(pallet_id)
                            sorted_summ.append(summary)

                    # Print the sorted and filtered data
                    for pallet_id, info in sorted_data.items():
                        print(f'Pallet ID: {pallet_id}, Summary: {info["summary"]}, Duration: {info["duration"]}')
                    print(sorted_summ, 'sorted_summ')
                    for inv in sorted_summ:
                        if values == inv.charge_unit_type.name and inv.in_date != False and inv.out_date != False and e >= inv.in_date >= s and s <= inv.out_date <= e and inv.storage_product == False:
                            print(inv.duration, 'dur 1')
                            duration = inv.duration
                            if inv.charge_unit_type.name not in types:
                                types.append(inv.charge_unit_type.name)
                            if unit == 'day':
                                pallet += duration
                            summ = ({
                                'start_date': inv.in_date,
                                'end_date': inv.out_date,
                                'quantity': inv.out_qty if inv.out_qty > 0 else inv.quantity,
                                'pallet': 1,
                                'charge_type': 'storage',
                                'product_id': inv.product_id.id,
                                'charge_unit_type': chrg_unit_type[0].id,

                            })
                            summ_lines = self.env['summary.sheet.lines'].create(summ)

                            if summ_lines.quantity > 0:
                                summary_lines.append(summ_lines)
                        elif values == inv.charge_unit_type.name and inv.in_date != False and e >= inv.in_date >= s and inv.out_date == False and inv.storage_product == False:
                            if inv.charge_unit_type.name not in types:
                                types.append(inv.charge_unit_type.name)
                            duration = (abs((fields.Datetime.to_datetime(e).date()
                                             - fields.Datetime.to_datetime(inv.in_date).date()).days) + 1)
                            print(duration, 'dur 2')
                            if unit == 'day':
                                pallet += duration
                            summ = ({
                                'start_date': inv.in_date,
                                'end_date': e,
                                'quantity': inv.out_qty if inv.out_qty > 0 else inv.quantity,
                                'pallet': 1,
                                'charge_type': 'storage',
                                'product_id': inv.product_id.id,
                                'charge_unit_type': chrg_unit_type[0].id,

                            })
                            summ_lines = self.env['summary.sheet.lines'].create(summ)

                            if summ_lines.quantity > 0:
                                summary_lines.append(summ_lines)
                        elif values == inv.charge_unit_type.name and inv.in_date != False and inv.out_date != False and e >= inv.in_date <= s and s <= inv.out_date <= e and inv.storage_product == False:
                            if inv.charge_unit_type.name not in types:
                                types.append(inv.charge_unit_type.name)
                            duration = (abs((fields.Datetime.to_datetime(inv.out_date).date()
                                             - fields.Datetime.to_datetime(s).date()).days) + 1)
                            print(inv.out_date, s, duration, 'dur 3')
                            if unit == 'day':
                                pallet += duration
                            summ = ({
                                'start_date': s,
                                'end_date': inv.out_date,
                                'quantity': inv.out_qty if inv.out_qty > 0 else inv.quantity,
                                'pallet': 1,
                                'charge_type': 'storage',
                                'product_id': inv.product_id.id,
                                'charge_unit_type': chrg_unit_type[0].id,

                            })
                            summ_lines = self.env['summary.sheet.lines'].create(summ)

                            if summ_lines.quantity > 0:
                                summary_lines.append(summ_lines)
                        elif values == inv.charge_unit_type.name and inv.in_date != False and inv.out_date != False and e >= inv.in_date <= s and s <= inv.out_date >= e and inv.storage_product == False:
                            if inv.charge_unit_type.name not in types:
                                types.append(inv.charge_unit_type.name)
                            duration = (abs((fields.Datetime.to_datetime(e).date()
                                             - fields.Datetime.to_datetime(s).date()).days) + 1)
                            print(duration, 'dur 4')
                            if unit == 'day':
                                pallet += duration

                            summ = ({
                                'start_date': s,
                                'end_date': e,
                                'quantity': inv.out_qty if inv.out_qty > 0 else inv.quantity,
                                'pallet': 1,
                                'charge_type': 'storage',
                                'product_id': inv.product_id.id,
                                'charge_unit_type': chrg_unit_type[0].id,

                            })
                            summ_lines = self.env['summary.sheet.lines'].create(summ)

                            if summ_lines.quantity > 0:
                                summary_lines.append(summ_lines)
                        elif values == inv.charge_unit_type.name and inv.in_date != False and inv.out_date != False and e >= inv.in_date >= s and s <= inv.out_date <= e and inv.storage_product == False:
                            if inv.charge_unit_type.name not in types:
                                types.append(inv.charge_unit_type.name)
                            duration = (abs((fields.Datetime.to_datetime(e).date()
                                             - fields.Datetime.to_datetime(inv.in_date).date()).days) + 1)
                            print(duration, 'dur 5')
                            if unit == 'day':
                                pallet += duration

                            summ = ({
                                'start_date': inv.in_date,
                                'end_date': e,
                                'quantity': inv.out_qty if inv.out_qty > 0 else inv.quantity,
                                'pallet': 1,
                                'charge_type': 'storage',
                                'product_id': inv.product_id.id,
                                'charge_unit_type': chrg_unit_type[0].id,

                            })
                            summ_lines = self.env['summary.sheet.lines'].create(summ)

                            if summ_lines.quantity > 0:
                                summary_lines.append(summ_lines)
                        elif values == inv.charge_unit_type.name and inv.in_date != False and e >= inv.in_date <= s and inv.out_date == False and inv.storage_product == False:
                            if inv.charge_unit_type.name not in types:
                                types.append(inv.charge_unit_type.name)
                            duration = (abs((fields.Datetime.to_datetime(e).date()
                                             - fields.Datetime.to_datetime(s).date()).days) + 1)
                            print(duration, 'dur 6')
                            if unit == 'day':
                                pallet += duration

                            summ = ({
                                'start_date': s,
                                'end_date': e,
                                'quantity': inv.out_qty if inv.out_qty > 0 else inv.quantity,
                                'pallet': 1,
                                'charge_type': 'storage',
                                'product_id': inv.product_id.id,
                                'charge_unit_type': chrg_unit_type[0].id,

                            })
                            summ_lines = self.env['summary.sheet.lines'].create(summ)

                            if summ_lines.quantity > 0:
                                summary_lines.append(summ_lines)
                        elif values == inv.charge_unit_type.name and inv.out_date != False and inv.in_date != False and e >= inv.in_date >= s and s <= inv.out_date >= e and inv.storage_product == False:
                            if inv.charge_unit_type.name not in types:
                                types.append(inv.charge_unit_type.name)
                            duration = (abs((fields.Datetime.to_datetime(e).date()
                                             - fields.Datetime.to_datetime(inv.in_date).date()).days) + 1)
                            print(duration, 'dur 7')
                            if unit == 'day':
                                pallet += duration

                            summ = ({
                                'start_date': s,
                                'end_date': e,
                                'quantity': inv.out_qty if inv.out_qty > 0 else inv.quantity,
                                'pallet': 1,
                                'charge_type': 'storage',
                                'product_id': inv.product_id.id,
                                'charge_unit_type': chrg_unit_type[0].id,

                            })
                            summ_lines = self.env['summary.sheet.lines'].create(summ)

                            if summ_lines.quantity > 0:
                                summary_lines.append(summ_lines)

                # print(pallet)
                if pallets:
                    pallet_count = len(pallets)
                    chrg_unit_type = self.env['charge.types'].search([('name', '=', 'Pallet')])
                    summ = ({

                        'pallet': pallet_count,
                        # 'weight': inv.product_id.weight,
                        'charge_type': 'storage',
                        # 'product_id': inv.product_id.id,
                        'charge_unit_type': chrg_unit_type[0].id,

                    })
                    summ_lines = self.env['summary.sheet.lines'].create(summ)
                    summary_lines.append(summ_lines)

                else:
                    pallet_count = 0
                print(pallet_count, '---pallet_count--------')
                print(types, '======sto==false====')
                if types:
                    for type in types:
                        print(type, '------------------------------------hb------------type1')
                        for temp in storage_charges:
                            if temp.charge_type == 'storage' and temp.charge_unit_type.name == 'CBM' and temp.charge_unit_type.name == type:
                                temp_line_values = {
                                    'product_id': temp.product_id and temp.product_id.id or False,
                                    'name': temp.product_id.name or '',
                                    'price_unit': temp.list_price or 0.00,
                                    'quantity': cbm,
                                    'currency_id': temp.currency_id.id,
                                    'tax_ids': [(6, 0, [temp.tax_id.id])] if temp.tax_id else False,
                                    'account_id': temp.product_id.property_account_income_id.id if temp.product_id.property_account_income_id
                                    else temp.product_id.categ_id.property_account_income_categ_id.id,
                                    # 'start_date': move_ids_without_package.start_date,
                                    # 'end_date': move_ids_without_package.end_date,

                                }
                                if temp_line_values['quantity'] > 0:
                                    invoice_line_list.append((0, 0, temp_line_values))

                            if temp.charge_type == 'storage' and temp.charge_unit_type.name == 'Weight' and temp.charge_unit_type.name == type:
                                temp_line_values = {
                                    'product_id': temp.product_id and temp.product_id.id or False,
                                    'name': temp.product_id.name or '',
                                    'price_unit': temp.list_price or 0.00,
                                    'quantity': weight,
                                    'currency_id': temp.currency_id.id,
                                    'tax_ids': [(6, 0, [temp.tax_id.id])] if temp.tax_id else False,
                                    'account_id': temp.product_id.property_account_income_id.id if temp.product_id.property_account_income_id
                                    else temp.product_id.categ_id.property_account_income_categ_id.id,
                                    # 'start_date': move_ids_without_package.start_date,
                                    # 'end_date': move_ids_without_package.end_date,

                                }
                                if temp_line_values['quantity'] > 0:
                                    invoice_line_list.append((0, 0, temp_line_values))

                            if temp.charge_type == 'storage' and temp.charge_unit_type.name == 'Square Units' and temp.charge_unit_type.name == type:
                                temp_line_values = {
                                    'product_id': temp.product_id and temp.product_id.id or False,
                                    'name': temp.product_id.name or '',
                                    'price_unit': temp.list_price or 0.00,
                                    'quantity': sq,
                                    'currency_id': temp.currency_id.id,
                                    'tax_ids': [(6, 0, [temp.tax_id.id])] if temp.tax_id else False,
                                    'account_id': temp.product_id.property_account_income_id.id if temp.product_id.property_account_income_id
                                    else temp.product_id.categ_id.property_account_income_categ_id.id,
                                    # 'start_date': move_ids_without_package.start_date,
                                    # 'end_date': move_ids_without_package.end_date,

                                }
                                if temp_line_values['quantity'] > 0:
                                    invoice_line_list.append((0, 0, temp_line_values))

                            if temp.charge_type == 'storage' and temp.charge_unit_type.name == 'Pallet' and temp.charge_unit_type.name == type:
                                temp_line_values = {
                                    'product_id': temp.product_id and temp.product_id.id or False,
                                    'name': temp.product_id.name or '',
                                    'price_unit': temp.list_price or 0.00,
                                    'quantity': pallet if pallet > 0 else pallet_count,
                                    'currency_id': temp.currency_id.id,
                                    'tax_ids': [(6, 0, [temp.tax_id.id])] if temp.tax_id else False,
                                    'account_id': temp.product_id.property_account_income_id.id if temp.product_id.property_account_income_id
                                    else temp.product_id.categ_id.property_account_income_categ_id.id,
                                    # 'start_date': move_ids_without_package.start_date,
                                    # 'end_date': move_ids_without_package.end_date,

                                }
                                if temp_line_values['quantity'] > 0:
                                    invoice_line_list.append((0, 0, temp_line_values))

            if other_values:
                for values, unit in other_values.items():
                    cbm = 0
                    weight = 0
                    sq = 0
                    pallet = 0
                    quo = 0
                    chrg_unit_type = self.env['charge.types'].search([('name', '=', values)])
                    for inv in inven:

                        if values == inv.charge_unit_type.name and inv.in_date != False and inv.out_date != False and e >= inv.in_date >= s and s <= inv.out_date <= e and inv.storage_product == False:
                            if unit == 'month':
                                cbm += inv.product_id.prod_volume * inv.out_qty if inv.out_qty > 0 else inv.quantity
                                sq += inv.product_id.prod_sqm * inv.out_qty if inv.out_qty > 0 else inv.quantity
                                pallet += 1
                                weight += inv.product_id.weight * inv.out_qty if inv.out_qty > 0 else inv.quantity
                                quo += 1
                            else:
                                cbm += inv.product_id.prod_volume * inv.out_qty if inv.out_qty > 0 else inv.quantity * inv.duration
                                sq += inv.product_id.prod_sqm * inv.out_qty if inv.out_qty > 0 else inv.quantity * inv.duration
                                pallet += 1
                                weight += inv.product_id.weight * inv.out_qty if inv.out_qty > 0 else inv.quantity * inv.duration
                                quo += 1 * inv.duration

                            summ = ({
                                'start_date': inv.in_date,
                                'end_date': inv.out_date,
                                'quantity': inv.out_qty if inv.out_qty > 0 else inv.quantity,

                                'other': 1,

                                'charge_type': 'storage',
                                'product_id': inv.product_id.id,
                                'charge_unit_type': chrg_unit_type[0].id,

                            })
                            summ_lines = self.env['summary.sheet.lines'].create(summ)
                            if summ_lines.quantity > 0:
                                summary_lines.append(summ_lines)

                        elif values == inv.charge_unit_type.name and inv.in_date != False and e >= inv.in_date >= s and inv.out_date == False and inv.storage_product == False:

                            duration = (abs((fields.Datetime.to_datetime(e).date()
                                             - fields.Datetime.to_datetime(inv.in_date).date()).days) + 1)
                            if unit == 'month':
                                cbm += inv.product_id.prod_volume * inv.out_qty if inv.out_qty > 0 else inv.quantity
                                sq += inv.product_id.prod_sqm * inv.out_qty if inv.out_qty > 0 else inv.quantity
                                pallet += 1
                                weight += inv.product_id.weight * inv.out_qty if inv.out_qty > 0 else inv.quantity
                                quo += 1
                            else:
                                cbm += inv.product_id.prod_volume * inv.out_qty if inv.out_qty > 0 else inv.quantity * duration
                                sq += inv.product_id.prod_sqm * inv.out_qty if inv.out_qty > 0 else inv.quantity * duration
                                pallet += 1
                                weight += inv.product_id.weight * inv.out_qty if inv.out_qty > 0 else inv.quantity * duration
                                quo += 1 * duration
                            summ = ({
                                'start_date': inv.in_date,
                                'end_date': e,
                                'quantity': inv.out_qty if inv.out_qty > 0 else inv.quantity,
                                'other': 1,
                                'charge_type': 'storage',
                                'product_id': inv.product_id.id,
                                'charge_unit_type': chrg_unit_type[0].id,

                            })
                            summ_lines = self.env['summary.sheet.lines'].create(summ)
                            if summ_lines.quantity > 0:
                                summary_lines.append(summ_lines)
                        elif values == inv.charge_unit_type.name and inv.in_date != False and inv.out_date != False and e >= inv.in_date <= s and s <= inv.out_date <= e and inv.storage_product == False:

                            duration = (abs((fields.Datetime.to_datetime(inv.out_date).date()
                                             - fields.Datetime.to_datetime(s).date()).days) + 1)
                            if unit == 'month':
                                cbm += inv.product_id.prod_volume * inv.out_qty if inv.out_qty > 0 else inv.quantity
                                sq += inv.product_id.prod_sqm * inv.out_qty if inv.out_qty > 0 else inv.quantity
                                pallet += 1
                                weight += inv.product_id.weight * inv.out_qty if inv.out_qty > 0 else inv.quantity
                                quo += 1
                            else:
                                cbm += inv.product_id.prod_volume * inv.out_qty if inv.out_qty > 0 else inv.quantity * duration
                                sq += inv.product_id.prod_sqm * inv.out_qty if inv.out_qty > 0 else inv.quantity * duration
                                pallet += 1
                                weight += inv.product_id.weight * inv.out_qty if inv.out_qty > 0 else inv.quantity * duration
                                quo += 1 * duration
                            summ = ({
                                'start_date': s,
                                'end_date': inv.out_date,
                                'quantity': inv.out_qty if inv.out_qty > 0 else inv.quantity,
                                'other': 1,
                                'charge_type': 'storage',
                                'product_id': inv.product_id.id,
                                'charge_unit_type': chrg_unit_type[0].id,

                            })
                            summ_lines = self.env['summary.sheet.lines'].create(summ)
                            if summ_lines.quantity > 0:
                                summary_lines.append(summ_lines)
                        elif values == inv.charge_unit_type.name and inv.in_date != False and inv.out_date != False and e >= inv.in_date <= s and s <= inv.out_date >= e and inv.storage_product == False:

                            duration = (abs((fields.Datetime.to_datetime(e).date()
                                             - fields.Datetime.to_datetime(s).date()).days) + 1)
                            if unit == 'month':
                                cbm += inv.product_id.prod_volume * inv.out_qty if inv.out_qty > 0 else inv.quantity
                                sq += inv.product_id.prod_sqm * inv.out_qty if inv.out_qty > 0 else inv.quantity
                                pallet += 1
                                weight += inv.product_id.weight * inv.out_qty if inv.out_qty > 0 else inv.quantity
                                quo += 1
                            else:
                                cbm += inv.product_id.prod_volume * inv.out_qty if inv.out_qty > 0 else inv.quantity * duration
                                sq += inv.product_id.prod_sqm * inv.out_qty if inv.out_qty > 0 else inv.quantity * duration
                                pallet += 1
                                weight += inv.product_id.weight * inv.out_qty if inv.out_qty > 0 else inv.quantity * duration
                                quo += 1 * duration
                            summ = ({
                                'start_date': s,
                                'end_date': e,
                                'quantity': inv.out_qty if inv.out_qty > 0 else inv.quantity,
                                'other': 1,
                                'charge_type': 'storage',
                                'product_id': inv.product_id.id,
                                'charge_unit_type': chrg_unit_type[0].id,

                            })
                            summ_lines = self.env['summary.sheet.lines'].create(summ)
                            if summ_lines.quantity > 0:
                                summary_lines.append(summ_lines)
                        elif values == inv.charge_unit_type.name and inv.in_date != False and inv.out_date != False and inv.out_date != False and e >= inv.in_date >= s and s <= inv.out_date <= e and inv.storage_product == False:

                            duration = (abs((fields.Datetime.to_datetime(e).date()
                                             - fields.Datetime.to_datetime(inv.in_date).date()).days) + 1)
                            if unit == 'month':
                                cbm += inv.product_id.prod_volume
                                sq += inv.product_id.prod_sqm
                                pallet += 1
                                weight += inv.product_id.weight
                                quo += 1
                            else:
                                cbm += inv.product_id.prod_volume * inv.out_qty if inv.out_qty > 0 else inv.quantity * duration
                                sq += inv.product_id.prod_sqm * inv.out_qty if inv.out_qty > 0 else inv.quantity * duration
                                pallet += 1
                                weight += inv.product_id.weight * inv.out_qty if inv.out_qty > 0 else inv.quantity * duration
                                quo += 1 * duration
                            summ = ({
                                'start_date': inv.in_date,
                                'end_date': e,
                                'quantity': inv.out_qty if inv.out_qty > 0 else inv.quantity,
                                'other': 1,
                                'charge_type': 'storage',
                                'product_id': inv.product_id.id,
                                'charge_unit_type': chrg_unit_type[0].id,

                            })
                            summ_lines = self.env['summary.sheet.lines'].create(summ)
                            if summ_lines.quantity > 0:
                                summary_lines.append(summ_lines)
                        elif values == inv.charge_unit_type.name and inv.in_date != False and e >= inv.in_date <= s and inv.out_date == False and inv.storage_product == False:

                            duration = (abs((fields.Datetime.to_datetime(e).date()
                                             - fields.Datetime.to_datetime(s).date()).days) + 1)
                            if unit == 'month':
                                cbm += inv.product_id.prod_volume * inv.out_qty if inv.out_qty > 0 else inv.quantity
                                sq += inv.product_id.prod_sqm * inv.out_qty if inv.out_qty > 0 else inv.quantity
                                pallet += 1
                                weight += inv.product_id.weight * inv.out_qty if inv.out_qty > 0 else inv.quantity
                                quo += 1
                            else:
                                cbm += inv.product_id.prod_volume * inv.out_qty if inv.out_qty > 0 else inv.quantity * duration
                                sq += inv.product_id.prod_sqm * inv.out_qty if inv.out_qty > 0 else inv.quantity * duration
                                pallet += 1
                                weight += inv.product_id.weight * inv.out_qty if inv.out_qty > 0 else inv.quantity * duration
                                quo += 1 * duration
                            summ = ({
                                'start_date': s,
                                'end_date': e,
                                'quantity': inv.out_qty if inv.out_qty > 0 else inv.quantity,
                                'other': 1,
                                'charge_type': 'storage',
                                'product_id': inv.product_id.id,
                                'charge_unit_type': chrg_unit_type[0].id,

                            })
                            summ_lines = self.env['summary.sheet.lines'].create(summ)
                            if summ_lines.quantity > 0:
                                summary_lines.append(summ_lines)
                        elif values == inv.charge_unit_type.name and inv.out_date != False and inv.in_date != False and e >= inv.in_date <= s and inv.out_date == False and inv.storage_product == False:

                            duration = (abs((fields.Datetime.to_datetime(e).date()
                                             - fields.Datetime.to_datetime(s).date()).days) + 1)
                            if unit == 'month':
                                cbm += inv.product_id.prod_volume * inv.out_qty if inv.out_qty > 0 else inv.quantity
                                sq += inv.product_id.prod_sqm * inv.out_qty if inv.out_qty > 0 else inv.quantity
                                pallet += 1
                                weight += inv.product_id.weight * inv.out_qty if inv.out_qty > 0 else inv.quantity
                                quo += 1
                            else:
                                cbm += inv.product_id.prod_volume * inv.out_qty if inv.out_qty > 0 else inv.quantity * duration
                                sq += inv.product_id.prod_sqm * inv.out_qty if inv.out_qty > 0 else inv.quantity * duration
                                pallet += 1
                                weight += inv.product_id.weight * inv.out_qty if inv.out_qty > 0 else inv.quantity * duration
                                quo += 1 * duration
                            summ = ({
                                'start_date': s,
                                'end_date': e,
                                'quantity': inv.out_qty if inv.out_qty > 0 else inv.quantity,
                                'other': 1,
                                'charge_type': 'storage',
                                'product_id': inv.product_id.id,
                                'charge_unit_type': chrg_unit_type[0].id,

                            })
                            summ_lines = self.env['summary.sheet.lines'].create(summ)
                            if summ_lines.quantity > 0:
                                summary_lines.append(summ_lines)

                        # break
                    for temp in storage_charges.filtered(
                            lambda inv: inv.charge_unit_type.name == values and inv.agreement_id == agreement_id):
                        if temp.charge_type == 'storage' and temp.charge_unit_type.name == values and not temp.storage_type:
                            temp_line_values = {
                                'product_id': temp.product_id and temp.product_id.id or False,
                                'name': temp.product_id.name or '',
                                'price_unit': temp.list_price or 0.00,
                                'quantity': quo,
                                'currency_id': temp.currency_id.id,
                                'tax_ids': [(6, 0, [temp.tax_id.id])] if temp.tax_id else False,
                                'account_id': temp.product_id.property_account_income_id.id if temp.product_id.property_account_income_id
                                else temp.product_id.categ_id.property_account_income_categ_id.id,

                                # 'start_date': move_ids_without_package.start_date,
                                # 'end_date': move_ids_without_package.end_date,

                            }
                            if temp_line_values['quantity'] > 0:
                                invoice_line_list.append((0, 0, temp_line_values))
                        break

            picking_id_in = self.env['stock.picking'].search(
                [('picking_type_id.code', '=', 'incoming'), ('partner_id', '=', partner.id),
                 ('scheduled_date', '>=', s), ('product_id.storage_type', '=', False)])
            print(picking_id_in, 'picking_id_in')
            in_vals = []
            for picking in picking_id_in:
                if s <= picking.scheduled_date <= e:
                    for pick in picking.service_id:
                        # if pick.product_id
                        vals = (0, 0, {
                            'name': pick.product_id.name,
                            'product_id': pick.product_id.id,
                            'price_unit': pick.price,
                            'account_id': pick.product_id.property_account_income_id.id if pick.product_id.property_account_income_id
                            else pick.product_id.categ_id.property_account_income_categ_id.id,
                            'tax_ids': [(6, 0, [pick.taxes_id.id])] if pick.taxes_id else False,
                            'quantity': pick.qty,

                            # 'quantity': move_ids_without_package.quantt if move_ids_without_package.inv_meth else 1,
                            # 'x_cbm': picking.x_cbm,
                            # 'start_date': picking.scheduled_date,
                            # 'end_date': picking.date_done,

                        })
                        in_vals.append(vals)
                        # invoice_line_list.append(vals)
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
            consolidated_in_data = {}
            for item in in_vals:
                _, _, item_data = item
                product_id = item_data['product_id']
                price_unit = item_data['price_unit']
                quantity = item_data['quantity']

                if product_id in consolidated_in_data:
                    consolidated_in_data[product_id]['price_unit'] += price_unit
                    consolidated_in_data[product_id]['quantity'] += quantity

                else:
                    consolidated_in_data[product_id] = item_data

            consolidated_in_list = [(0, 0, data) for data in consolidated_in_data.values()]
            print(consolidated_in_list, 'consolidated_in_list')
            for c in consolidated_in_list:
                print(c, '------------------------------------------------c-------------------------')
                invoice_line_list.append(c)

            picking_id_out = self.env['stock.picking'].search(
                [('picking_type_id.code', '=', 'outgoing'), ('partner_id', '=', partner.id),
                 ('scheduled_date', '>=', s), ('product_id.storage_type', '=', False)])
            print(picking_id_out, 'picking_id_out')
            out_vals = []
            for picking in picking_id_out:
                if s <= picking.scheduled_date <= e:
                    for pick in picking.service_id:
                        vals = (0, 0, {
                            'name': pick.product_id.name,
                            'product_id': pick.product_id.id,
                            'price_unit': pick.qty,
                            'account_id': pick.product_id.property_account_income_id.id if pick.product_id.property_account_income_id
                            else pick.product_id.categ_id.property_account_income_categ_id.id,
                            'tax_ids': [(6, 0, [pick.taxes_id.id])] if pick.taxes_id else False,
                            'quantity': pick.price,

                            # 'quantity': move_ids_without_package.quantt if move_ids_without_package.inv_meth else 1,
                            # 'x_cbm': picking.x_cbm,
                            # 'start_date': picking.scheduled_date,
                            # 'end_date': picking.date_done,

                        })
                        # invoice_line_list.append(vals)
                        out_vals.append(vals)
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
            consolidated_out_data = {}
            for item in out_vals:
                _, _, item_data = item
                product_id = item_data['product_id']
                price_unit = item_data['price_unit']
                quantity = item_data['quantity']

                if product_id in consolidated_out_data:
                    consolidated_out_data[product_id]['price_unit'] += price_unit
                    consolidated_out_data[product_id]['quantity'] += quantity

                else:
                    consolidated_out_data[product_id] = item_data

            consolidated_out_list = [(0, 0, data) for data in consolidated_out_data.values()]
            print(consolidated_out_list, 'consolidated_out_list')
            for c in consolidated_out_list:
                print(c, '------------------------------------------------c-------------------------')
                invoice_line_list.append(c)

            current_user = self.env.uid

            if agreement_id and invoice_line_list:
                invoice = partner.env['account.move'].create({
                    'type': 'out_invoice',
                    'sto_type': 'warehouse',
                    'start_date_sto': s,
                    'end_date_sto': e,
                    'invoice_origin': partner.name,
                    'invoice_user_id': current_user,
                    'narration': partner.name,
                    'partner_id': partner.id,
                    'currency_id': partner.env.user.company_id.currency_id.id,
                    # 'journal_id': int(UOMer_journal_id),
                    'invoice_payment_ref': partner.name,
                    # 'picking_id': picking_id.id,
                    'invoice_line_ids': invoice_line_list,
                    # 'invoice_type': 'storage',
                    'name': '/',

                })
                invoices.append(invoice.id)
                if invoice:
                    invoice._summary_sheet()
                # invoice.consolidate_invoice_lines(invoice)

                summary = ({
                    'name': str(s) + '-' + str(e),
                    'partner_id': partner.id,
                    'invoice_id': invoice.id
                })
                summary = self.env['summary.sheet'].create(summary)

                for lines in summary_lines:
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
            tstorage_charges = partner.env['agreement.charges'].search(
                ['&', ('charge_type', '=', 'storage'), ('agreement_id', '=', agreement_id.id),
                 ('storage_type', '!=', False)])
            tuoms = {}
            tquantity_dict = {}
            sto_type = []
            for styp in tstorage_charges:
                if styp.storage_type and styp.storage_type.name not in sto_type:
                    sto_type.append(styp.storage_type.name)
            tinvoice_line_list = []
            tser = False
            for sty in sto_type:
                for u in tstorage_charges:
                    if u.uom_id:
                        uom = u['uom_id']['id']
                        unit = u['storage_uom']
                        tuoms[uom] = unit
                tcharge_unit_types = {}
                for c in tstorage_charges:
                    chrg = c['charge_unit_type']['name']
                    sto = c['storage_uom']
                    tcharge_unit_types[chrg] = sto
                tvalues_except_UOM = {chrg: sto for chrg, sto in tcharge_unit_types.items() if chrg != 'UOM'
                                      and chrg in ['CBM', 'Pallet', 'Square Units', 'Weight', 'UOM']}

                tother_values = {chrg: sto for chrg, sto in tcharge_unit_types.items() if chrg not in
                                 ['CBM', 'Pallet', 'Square Units', 'Weight', 'UOM']}
                tinven = self.env['product.summary'].search(
                    [('partner_id', '=', partner.id), ('storage_product', '=', True),('gen_seperate_inv','=',False),
                     ('product_id.storage_type.name', '=', sty)])
                # print(tvalues_except_UOM, tother_values)

                if tuoms:
                    for uom, unit in tuoms.items():
                        tquantity_dict[uom] = 0
                        for tinv in tinven:
                            UOM = self.env['charge.types'].search([('name', '=', 'UOM')])

                            if uom == tinv.uom_id.id:
                                # print(tinv.product_id.storage_type.name, sty,'----------------------')
                                if tinv.product_id.storage_type.name == sty and tinv.charge_unit_type.name == 'UOM' and tinv.in_date != False and tinv.out_date != False and e >= tinv.in_date >= s and s <= tinv.out_date <= e and tinv.storage_product == True:
                                    if unit == 'month':
                                        tquantity_dict[uom] += tinv.out_qty if tinv.out_qty > 0 else tinv.quantity
                                    else:
                                        tquantity_dict[
                                            uom] += tinv.out_qty if tinv.out_qty > 0 else tinv.quantity * tinv.duration
                                    # tquantity_dict[uom] += tinv.out_qty if tinv.out_qty > 0 else tinv.quantity * tinv.duration

                                    summ = ({
                                        'start_date': tinv.in_date,
                                        'end_date': tinv.out_date,
                                        'quantity': tinv.out_qty if tinv.out_qty > 0 else tinv.quantity,
                                        'cbm': tinv.product_id.prod_volume,
                                        'sqm': tinv.product_id.prod_sqm,
                                        'pallet': 0,
                                        'weight': tinv.product_id.weight,
                                        'charge_type': 'storage',
                                        'product_id': tinv.product_id.id,
                                        'charge_unit_type': UOM[0].id,
                                    })
                                    summ_lines = self.env['summary.sheet.lines'].create(summ)
                                    if summ_lines.quantity > 0:
                                        tsummary_lines.append(summ_lines)
                                elif tinv.product_id.storage_type.name == sty and tinv.charge_unit_type.name == 'UOM' and tinv.in_date != False and e >= tinv.in_date >= s and tinv.out_date == False and tinv.storage_product == True:
                                    duration = (abs((fields.Datetime.to_datetime(e).date()
                                                     - fields.Datetime.to_datetime(tinv.in_date).date()).days) + 1)
                                    if unit == 'month':
                                        tquantity_dict[uom] += tinv.out_qty if tinv.out_qty > 0 else tinv.quantity
                                    else:
                                        tquantity_dict[
                                            uom] += tinv.out_qty if tinv.out_qty > 0 else tinv.quantity * duration

                                    summ = ({
                                        'start_date': tinv.in_date,
                                        'end_date': e,
                                        'quantity': tinv.out_qty if tinv.out_qty > 0 else tinv.quantity,
                                        'cbm': tinv.product_id.prod_volume,
                                        'sqm': tinv.product_id.prod_sqm,
                                        'pallet': 0,
                                        'weight': tinv.product_id.weight,
                                        'charge_type': 'storage',
                                        'product_id': tinv.product_id.id,
                                        'charge_unit_type': UOM[0].id,

                                    })
                                    summ_lines = self.env['summary.sheet.lines'].create(summ)
                                    if summ_lines.quantity > 0:
                                        tsummary_lines.append(summ_lines)
                                # elif tinv.in_date != False and e >= tinv.in_date >= s and s <= tinv.out_date <= e and tinv.storage_product == True:
                                #     duration = abs((fields.Datetime.to_datetime(tinv.out_date).date()
                                #                     - fields.Datetime.to_datetime(s).date()).days)
                                #     # tcbm += tinv.product_id.x_vol * tinv.out_qty if tinv.out_qty > 0 else tinv.quantity * tinv.duration
                                #     # tsq += tinv.product_id.x_vol * tinv.out_qty if tinv.out_qty > 0 else tinv.quantity * tinv.duration
                                #     tcbm += tinv.product_id.prod_volume * tinv.out_qty if tinv.out_qty > 0 else tinv.quantity * duration
                                #     tsq += tinv.product_id.prod_sqm * tinv.out_qty if tinv.out_qty > 0 else tinv.quantity * duration
                                #     tpallet += 1
                                #     tweight += tinv.product_id.weight * tinv.out_qty if tinv.out_qty > 0 else tinv.quantity * duration
                                #     summ = ({
                                #         'start_date': s,
                                #         'end_date': tinv.out_date,
                                #         'quantity': tinv.out_qty if tinv.out_qty > 0 else tinv.quantity,
                                #         'cbm': cbm,
                                #         'sqm': sq,
                                #         'pallet': pallet,
                                #         'weight': weight,
                                #     })
                                #     summ_lines = self.env['summary.sheet.lines'].create(summ)
                                #     summary_lines.append(summ_lines)
                                elif tinv.product_id.storage_type.name == sty and tinv.charge_unit_type.name == 'UOM' and tinv.in_date != False and tinv.out_date != False and e >= tinv.in_date <= s and s <= tinv.out_date <= e and tinv.storage_product == True:
                                    duration = (abs((fields.Datetime.to_datetime(e).date()
                                                     - fields.Datetime.to_datetime(tinv.in_date).date()).days) + 1)
                                    if unit == 'month':
                                        tquantity_dict[uom] += tinv.out_qty if tinv.out_qty > 0 else tinv.quantity
                                    else:
                                        tquantity_dict[
                                            uom] += tinv.out_qty if tinv.out_qty > 0 else tinv.quantity * duration
                                    # tquantity_dict[uom] += tinv.out_qty if tinv.out_qty > 0 else tinv.quantity * duration

                                    summ = ({
                                        'start_date': tinv.in_date,
                                        'end_date': tinv.out_date,
                                        'quantity': tinv.out_qty if tinv.out_qty > 0 else tinv.quantity,
                                        'cbm': tinv.product_id.prod_volume,
                                        'sqm': tinv.product_id.prod_sqm,
                                        'pallet': 0,
                                        'weight': tinv.product_id.weight,
                                        'charge_type': 'storage',
                                        'product_id': tinv.product_id.id,
                                        'charge_unit_type': UOM[0].id,

                                    })
                                    summ_lines = self.env['summary.sheet.lines'].create(summ)
                                    if summ_lines.quantity > 0:
                                        tsummary_lines.append(summ_lines)
                                elif tinv.product_id.storage_type.name == sty and tinv.charge_unit_type.name == 'UOM' and tinv.in_date != False and tinv.out_date != False and e >= tinv.in_date <= s and s <= tinv.out_date >= e and tinv.storage_product == True:
                                    duration = (abs((fields.Datetime.to_datetime(e).date()
                                                     - fields.Datetime.to_datetime(s).date()).days) + 1)
                                    if unit == 'month':
                                        tquantity_dict[uom] += tinv.out_qty if tinv.out_qty > 0 else tinv.quantity
                                    else:
                                        tquantity_dict[
                                            uom] += tinv.out_qty if tinv.out_qty > 0 else tinv.quantity * duration

                                    # tquantity_dict[uom] += tinv.out_qty if tinv.out_qty > 0 else tinv.quantity * tinv.duration

                                    summ = ({
                                        'start_date': s,
                                        'end_date': e,
                                        'quantity': tinv.out_qty if tinv.out_qty > 0 else tinv.quantity,
                                        'cbm': tinv.product_id.prod_volume,
                                        'sqm': tinv.product_id.prod_sqm,
                                        'pallet': 0,
                                        'weight': tinv.product_id.weight,
                                        'charge_type': 'storage',
                                        'product_id': tinv.product_id.id,
                                        'charge_unit_type': UOM[0].id,

                                    })
                                    summ_lines = self.env['summary.sheet.lines'].create(summ)
                                    if summ_lines.quantity > 0:
                                        tsummary_lines.append(summ_lines)
                                elif tinv.product_id.storage_type.name == sty and tinv.charge_unit_type.name == 'UOM' and tinv.in_date != False and e >= tinv.in_date <= s and tinv.out_date == False and tinv.storage_product == True:
                                    duration = (abs((fields.Datetime.to_datetime(e).date()
                                                     - fields.Datetime.to_datetime(s).date()).days) + 1)
                                    if unit == 'month':
                                        tquantity_dict[uom] += tinv.out_qty if tinv.out_qty > 0 else tinv.quantity
                                    else:
                                        tquantity_dict[
                                            uom] += tinv.out_qty if tinv.out_qty > 0 else tinv.quantity * duration
                                    # tquantity_dict[uom] += tinv.out_qty if tinv.out_qty > 0 else tinv.quantity * tinv.duration

                                    summ = ({
                                        'start_date': s,
                                        'end_date': e,
                                        'quantity': tinv.out_qty if tinv.out_qty > 0 else tinv.quantity,
                                        'cbm': tinv.product_id.prod_volume,
                                        'sqm': tinv.product_id.prod_sqm,
                                        'pallet': 0,
                                        'weight': tinv.product_id.weight,
                                        'charge_type': 'storage',
                                        'product_id': tinv.product_id.id,
                                        'charge_unit_type': UOM[0].id,

                                    })

                                    summ_lines = self.env['summary.sheet.lines'].create(summ)
                                    if summ_lines.quantity > 0:
                                        tsummary_lines.append(summ_lines)
                                elif tinv.product_id.storage_type.name == sty and tinv.charge_unit_type.name == 'UOM' and tinv.out_date != False and tinv.in_date != False and e >= tinv.in_date >= s and s <= tinv.out_date >= e and tinv.storage_product == True:
                                    duration = (abs((fields.Datetime.to_datetime(e).date()
                                                     - fields.Datetime.to_datetime(tinv.in_date).date()).days) + 1)
                                    if unit == 'month':
                                        tquantity_dict[uom] += tinv.out_qty if tinv.out_qty > 0 else tinv.quantity
                                    else:
                                        tquantity_dict[
                                            uom] += tinv.out_qty if tinv.out_qty > 0 else tinv.quantity * duration
                                    summ = ({
                                        'start_date': s,
                                        'end_date': e,
                                        'quantity': tinv.out_qty if tinv.out_qty > 0 else tinv.quantity,
                                        'charge_type': 'storage',
                                        'product_id': tinv.product_id.id,
                                        'charge_unit_type': UOM[0].id,

                                    })
                                    summ_lines = self.env['summary.sheet.lines'].create(summ)
                                    if summ_lines.quantity > 0:
                                        summary_lines.append(summ_lines)

                    for temp in tstorage_charges.filtered(lambda inv: inv.charge_unit_type.name == 'UOM'):
                        # print(temp.storage_type.name, sty, '----------', temp.charge_unit_type.name , 'UOM', temp.charge_type, 'storage')
                        if temp.charge_type == 'storage' and temp.charge_unit_type.name == 'UOM' and temp.storage_type.name == sty:
                            # print('----------1')
                            if tuoms:
                                # print('----------2')

                                for q in tuoms:
                                    # print('----------3')
                                    v = temp.uom_id.id
                                    value = tquantity_dict[v]
                                    qty = value
                                    # print(qty, 'qty ', '----------3')
                                    temp_line_values = {
                                        'product_id': temp.product_id and temp.product_id.id or False,
                                        'name': temp.product_id.name or '',
                                        'price_unit': temp.list_price or 0.00,
                                        'quantity': qty,
                                        'currency_id': temp.currency_id.id,
                                        'tax_ids': [(6, 0, [temp.tax_id.id])] if temp.tax_id else False,
                                        'account_id': temp.product_id.property_account_income_id.id if temp.product_id.property_account_income_id
                                        else temp.product_id.categ_id.property_account_income_categ_id.id,
                                        # 'start_date': move_ids_without_package.start_date,
                                        # 'end_date': move_ids_without_package.end_date,
                                    }
                                    if temp_line_values['quantity'] > 0:
                                        print('ok')
                                        tinvoice_line_list.append((0, 0, temp_line_values))
                                        # print(tinvoice_line_list, 'tinvoice_line_list')
                if tvalues_except_UOM:
                    tcbm = 0
                    tweight = 0
                    tsq = 0
                    tpallet = 0
                    tpallets = []
                    types = []
                    for values, unit in tvalues_except_UOM.items():
                        tchrg_unit_type = self.env['charge.types'].search([('name', '=', values)])
                        for tinv in tinven:
                            # print(s, 's', e, 'e', tinv.in_date, 'in', tinv.out_date, 'out', values, 'values',
                            #       tinv.charge_unit_type.name, 'tinv.charge_unit_type.name', tinv.storage_product,
                            #       'tinv.storage_product')
                            if values != 'Ppallet':

                                if tinv.product_id.storage_type.name == sty and values == tinv.charge_unit_type.name and tinv.in_date != False and tinv.out_date != False and e >= tinv.in_date >= s and s <= tinv.out_date <= e and tinv.storage_product == True:
                                    print(tinv.duration, 'tdur1')
                                    if tinv.charge_unit_type.name not in types:
                                        types.append(tinv.charge_unit_type.name)
                                    if unit == 'month':
                                        if values == 'CBM':
                                            tcbm += tinv.product_id.prod_volume * tinv.out_qty if tinv.out_qty > 0 else tinv.product_id.prod_volume * tinv.quantity
                                        if values == 'Square Units':
                                            tsq += tinv.product_id.prod_sqm * tinv.out_qty if tinv.out_qty > 0 else tinv.product_id.prod_sqm * tinv.quantity
                                        if values == 'Pallet':
                                            if tinv.pallet_id:
                                                if tinv.pallet_id.id not in tpallets:
                                                    tpallets.append(tinv.pallet_id.id)
                                            # tpallet += 1
                                        if values == 'Weight':
                                            tweight += tinv.product_id.weight * tinv.out_qty if tinv.out_qty > 0 else tinv.product_id.weight * tinv.quantity
                                    else:
                                        if values == 'CBM':
                                            tcbm += tinv.product_id.prod_volume * tinv.out_qty * tinv.duration if tinv.out_qty > 0 else tinv.product_id.prod_volume * tinv.quantity * tinv.duration
                                        if values == 'Square Units':
                                            tsq += tinv.product_id.prod_sqm * tinv.out_qty * tinv.duration if tinv.out_qty > 0 else tinv.product_id.prod_sqm * tinv.quantity * tinv.duration
                                        # if values == 'Pallet':
                                        #     tpallet += 1 * tinv.duration
                                        if values == 'Weight':
                                            tweight += tinv.product_id.weight * tinv.out_qty * tinv.duration if tinv.out_qty > 0 else tinv.product_id.weight * tinv.quantity * tinv.duration
                                    print(tcbm, '-------tcbm1')
                                    summ = ({
                                        'start_date': tinv.in_date,
                                        'end_date': tinv.out_date,
                                        'quantity': tinv.out_qty if tinv.out_qty > 0 else tinv.quantity,
                                        'cbm': tinv.product_id.prod_volume,
                                        'sqm': tinv.product_id.prod_sqm,
                                        'pallet': 1,
                                        'weight': tinv.product_id.weight,
                                        'charge_type': 'storage',
                                        'product_id': tinv.product_id.id,
                                        'charge_unit_type': tchrg_unit_type[0].id,
                                    })
                                    summ_lines = self.env['summary.sheet.lines'].create(summ)
                                    # if summ_lines.quantity > 0 and values != 'Pallet' and unit != 'month':
                                    #     tsummary_lines.append(summ_lines)
                                    # if summ_lines.quantity > 0 and values == 'Pallet' and unit != 'month':
                                    #     tsummary_lines.append(summ_lines)
                                    if summ_lines.quantity > 0:
                                        tsummary_lines.append(summ_lines)
                                elif tinv.product_id.storage_type.name == sty and values == tinv.charge_unit_type.name and tinv.in_date != False and e >= tinv.in_date >= s and tinv.out_date == False and tinv.storage_product == True:
                                    if tinv.charge_unit_type.name not in types:
                                        types.append(tinv.charge_unit_type.name)
                                    duration = (abs((fields.Datetime.to_datetime(e).date()
                                                     - fields.Datetime.to_datetime(tinv.in_date).date()).days) + 1)
                                    print(duration, 'tdur2')
                                    if unit == 'month':
                                        if values == 'CBM':
                                            tcbm += tinv.product_id.prod_volume * tinv.out_qty if tinv.out_qty > 0 else tinv.product_id.prod_volume * tinv.quantity
                                        if values == 'Square Units':
                                            tsq += tinv.product_id.prod_sqm * tinv.out_qty if tinv.out_qty > 0 else tinv.product_id.prod_sqm * tinv.quantity
                                        if values == 'Pallet':
                                            if tinv.pallet_id:
                                                if tinv.pallet_id.id not in tpallets:
                                                    tpallets.append(tinv.pallet_id.id)
                                            # tpallet += 1
                                        if values == 'Weight':
                                            tweight += tinv.product_id.weight * tinv.out_qty if tinv.out_qty > 0 else tinv.product_id.weight * tinv.quantity
                                    else:
                                        if values == 'CBM':
                                            tcbm += tinv.product_id.prod_volume * tinv.out_qty * duration if tinv.out_qty > 0 else tinv.product_id.prod_volume * tinv.quantity * duration
                                        if values == 'Square Units':
                                            tsq += tinv.product_id.prod_sqm * tinv.out_qty * duration if tinv.out_qty > 0 else tinv.product_id.prod_sqm * tinv.quantity * duration
                                        # if values == 'Pallet':
                                        #     tpallet += 1 * duration
                                        if values == 'Weight':
                                            tweight += tinv.product_id.weight * tinv.out_qty * duration if tinv.out_qty > 0 else tinv.product_id.weight * tinv.quantity * duration
                                    print(tcbm, '-------tcbm2')
                                    summ = ({
                                        'start_date': tinv.in_date,
                                        'end_date': e,
                                        'quantity': tinv.out_qty if tinv.out_qty > 0 else tinv.quantity,
                                        'cbm': tinv.product_id.prod_volume,
                                        'sqm': tinv.product_id.prod_sqm,
                                        'pallet': 1,
                                        'weight': tinv.product_id.weight,
                                        'charge_type': 'storage',
                                        'product_id': tinv.product_id.id,
                                        'charge_unit_type': tchrg_unit_type[0].id,

                                    })
                                    summ_lines = self.env['summary.sheet.lines'].create(summ)
                                    # if summ_lines.quantity > 0 and values != 'Pallet' and unit != 'month':
                                    #     tsummary_lines.append(summ_lines)
                                    # if summ_lines.quantity > 0 and values == 'Pallet' and unit != 'month':
                                    #     tsummary_lines.append(summ_lines)
                                    if summ_lines.quantity > 0:
                                        tsummary_lines.append(summ_lines)
                                # elif tinv.in_date != False and e >= tinv.in_date >= s and s <= tinv.out_date <= e and tinv.storage_product == True:
                                #     duration = abs((fields.Datetime.to_datetime(tinv.out_date).date()
                                #                     - fields.Datetime.to_datetime(s).date()).days)
                                #     # tcbm += tinv.product_id.x_vol * tinv.out_qty if tinv.out_qty > 0 else tinv.quantity * tinv.duration
                                #     # tsq += tinv.product_id.x_vol * tinv.out_qty if tinv.out_qty > 0 else tinv.quantity * tinv.duration
                                #     tcbm += tinv.product_id.prod_volume * tinv.out_qty if tinv.out_qty > 0 else tinv.quantity * duration
                                #     tsq += tinv.product_id.prod_sqm * tinv.out_qty if tinv.out_qty > 0 else tinv.quantity * duration
                                #     tpallet += 1
                                #     tweight += tinv.product_id.weight * tinv.out_qty if tinv.out_qty > 0 else tinv.quantity * duration
                                #     summ = ({
                                #         'start_date': s,
                                #         'end_date': tinv.out_date,
                                #         'quantity': tinv.out_qty if tinv.out_qty > 0 else tinv.quantity,
                                #         'cbm': cbm,
                                #         'sqm': sq,
                                #         'pallet': pallet,
                                #         'weight': weight,
                                #     })
                                #     summ_lines = self.env['summary.sheet.lines'].create(summ)
                                #     summary_lines.append(summ_lines)
                                elif tinv.product_id.storage_type.name == sty and values == tinv.charge_unit_type.name and tinv.in_date != False and tinv.out_date != False and e >= tinv.in_date <= s and s <= tinv.out_date <= e and tinv.storage_product == True:
                                    if tinv.charge_unit_type.name not in types:
                                        types.append(tinv.charge_unit_type.name)
                                    duration = (abs((fields.Datetime.to_datetime(tinv.out_date).date()
                                                     - fields.Datetime.to_datetime(s).date()).days) + 1)
                                    # duration = (abs((fields.Datetime.to_datetime(e).date()
                                    #                  - fields.Datetime.to_datetime(tinv.in_date).date()).days) + 1)
                                    print(duration, tinv, 'tdur3')
                                    if unit == 'month':
                                        if values == 'CBM':
                                            tcbm += tinv.product_id.prod_volume * tinv.out_qty if tinv.out_qty > 0 else tinv.product_id.prod_volume * tinv.quantity
                                        if values == 'Square Units':
                                            tsq += tinv.product_id.prod_sqm * tinv.out_qty if tinv.out_qty > 0 else tinv.product_id.prod_sqm * tinv.quantity
                                        if values == 'Pallet':
                                            if tinv.pallet_id:
                                                if tinv.pallet_id.id not in tpallets:
                                                    tpallets.append(tinv.pallet_id.id)
                                            # tpallet += 1
                                        if values == 'Weight':
                                            tweight += tinv.product_id.weight * tinv.out_qty if tinv.out_qty > 0 else tinv.product_id.weight * tinv.quantity
                                    else:
                                        if values == 'CBM':
                                            tcbm += tinv.product_id.prod_volume * tinv.out_qty * duration if tinv.out_qty > 0 else tinv.product_id.prod_volume * tinv.quantity * duration
                                        if values == 'Square Units':
                                            tsq += tinv.product_id.prod_sqm * tinv.out_qty * duration if tinv.out_qty > 0 else tinv.product_id.prod_sqm * tinv.quantity * duration
                                        # if values == 'Pallet':
                                        #     tpallet += 1 * duration
                                        if values == 'Weight':
                                            tweight += tinv.product_id.weight * tinv.out_qty * duration if tinv.out_qty > 0 else tinv.product_id.weight * tinv.quantity * duration
                                    print(tcbm, '-------tcbm3')
                                    summ = ({
                                        'start_date': tinv.in_date,
                                        'end_date': tinv.out_date,
                                        'quantity': tinv.out_qty if tinv.out_qty > 0 else tinv.quantity,
                                        'cbm': tinv.product_id.prod_volume,
                                        'sqm': tinv.product_id.prod_sqm,
                                        'pallet': 1,
                                        'weight': tinv.product_id.weight,
                                        'charge_type': 'storage',
                                        'product_id': tinv.product_id.id,
                                        'charge_unit_type': tchrg_unit_type[0].id,

                                    })
                                    summ_lines = self.env['summary.sheet.lines'].create(summ)
                                    # if summ_lines.quantity > 0 and values != 'Pallet' and unit != 'month':
                                    #     tsummary_lines.append(summ_lines)
                                    # if summ_lines.quantity > 0 and values == 'Pallet' and unit != 'month':
                                    #     tsummary_lines.append(summ_lines)
                                    if summ_lines.quantity > 0:
                                        tsummary_lines.append(summ_lines)
                                elif tinv.product_id.storage_type.name == sty and values == tinv.charge_unit_type.name and tinv.in_date != False and tinv.out_date != False and e >= tinv.in_date <= s and s <= tinv.out_date >= e and tinv.storage_product == True:
                                    if tinv.charge_unit_type.name not in types:
                                        types.append(tinv.charge_unit_type.name)
                                    duration = (abs((fields.Datetime.to_datetime(e).date()
                                                     - fields.Datetime.to_datetime(s).date()).days) + 1)
                                    print(duration, 'tdur4')

                                    if unit == 'month':
                                        if values == 'CBM':
                                            tcbm += tinv.product_id.prod_volume * tinv.out_qty if tinv.out_qty > 0 else tinv.product_id.prod_volume * tinv.quantity
                                        if values == 'Square Units':
                                            tsq += tinv.product_id.prod_sqm * tinv.out_qty if tinv.out_qty > 0 else tinv.product_id.prod_sqm * tinv.quantity
                                        if values == 'Pallet':
                                            if tinv.pallet_id:
                                                if tinv.pallet_id.id not in tpallets:
                                                    tpallets.append(tinv.pallet_id.id)
                                            # tpallet += 1
                                        if values == 'Weight':
                                            tweight += tinv.product_id.weight * tinv.out_qty if tinv.out_qty > 0 else tinv.product_id.weight * tinv.quantity
                                    else:
                                        if values == 'CBM':
                                            tcbm += tinv.product_id.prod_volume * tinv.out_qty * duration if tinv.out_qty > 0 else tinv.product_id.prod_volume * tinv.quantity * duration
                                        if values == 'Square Units':
                                            tsq += tinv.product_id.prod_sqm * tinv.out_qty * duration if tinv.out_qty > 0 else tinv.product_id.prod_sqm * tinv.quantity * duration
                                        # if values == 'Pallet':
                                        #     tpallet += 1 * duration
                                        if values == 'Weight':
                                            tweight += tinv.product_id.weight * tinv.out_qty * duration if tinv.out_qty > 0 else tinv.product_id.weight * tinv.quantity * duration
                                    print(tcbm, '-------tcbm4')
                                    summ = ({
                                        'start_date': s,
                                        'end_date': e,
                                        'quantity': tinv.out_qty if tinv.out_qty > 0 else tinv.quantity,
                                        'cbm': tinv.product_id.prod_volume,
                                        'sqm': tinv.product_id.prod_sqm,
                                        'pallet': 1,
                                        'weight': tinv.product_id.weight,
                                        'charge_type': 'storage',
                                        'product_id': tinv.product_id.id,
                                        'charge_unit_type': tchrg_unit_type[0].id,

                                    })
                                    summ_lines = self.env['summary.sheet.lines'].create(summ)
                                    # if summ_lines.quantity > 0 and values != 'Pallet' and unit != 'month':
                                    #     tsummary_lines.append(summ_lines)
                                    # if summ_lines.quantity > 0 and values == 'Pallet' and unit != 'month':
                                    #     tsummary_lines.append(summ_lines)
                                    if summ_lines.quantity > 0:
                                        tsummary_lines.append(summ_lines)
                                elif tinv.product_id.storage_type.name == sty and values == tinv.charge_unit_type.name and tinv.in_date != False and e >= tinv.in_date <= s and tinv.out_date == False and tinv.storage_product == True:
                                    if tinv.charge_unit_type.name not in types:
                                        types.append(tinv.charge_unit_type.name)
                                    duration = (abs((fields.Datetime.to_datetime(e).date()
                                                     - fields.Datetime.to_datetime(s).date()).days) + 1)
                                    print(duration, tinv, 'tdur5', tinv.quantity, tinv.product_id.prod_volume,
                                          tinv.out_qty)
                                    if unit == 'month':
                                        if values == 'CBM':
                                            tcbm += tinv.product_id.prod_volume * tinv.out_qty if tinv.out_qty > 0 else tinv.product_id.prod_volume * tinv.quantity
                                        if values == 'Square Units':
                                            tsq += tinv.product_id.prod_sqm * tinv.out_qty if tinv.out_qty > 0 else tinv.product_id.prod_sqm * tinv.quantity
                                        if values == 'Pallet':
                                            if tinv.pallet_id:
                                                if tinv.pallet_id.id not in tpallets:
                                                    tpallets.append(tinv.pallet_id.id)
                                            # tpallet += 1
                                        if values == 'Weight':
                                            tweight += tinv.product_id.weight * tinv.out_qty if tinv.out_qty > 0 else tinv.product_id.weight * tinv.quantity
                                    else:
                                        if values == 'CBM':
                                            tcbm += tinv.product_id.prod_volume * tinv.out_qty * duration if tinv.out_qty > 0 else tinv.product_id.prod_volume * tinv.quantity * duration
                                        if values == 'Square Units':
                                            tsq += tinv.product_id.prod_sqm * tinv.out_qty * duration if tinv.out_qty > 0 else tinv.product_id.prod_sqm * tinv.quantity * duration
                                        # if values == 'Pallet':
                                        #     tpallet += 1 * duration
                                        if values == 'Weight':
                                            tweight += tinv.product_id.weight * tinv.out_qty * duration if tinv.out_qty > 0 else tinv.product_id.weight * tinv.quantity * duration
                                    print(tcbm, '-------tcbm5')
                                    summ = ({
                                        'start_date': s,
                                        'end_date': e,
                                        'quantity': tinv.out_qty if tinv.out_qty > 0 else tinv.quantity,
                                        'cbm': tinv.product_id.prod_volume,
                                        'sqm': tinv.product_id.prod_sqm,
                                        'pallet': 1,
                                        'weight': tinv.product_id.weight,
                                        'charge_type': 'storage',
                                        'product_id': tinv.product_id.id,
                                        'charge_unit_type': tchrg_unit_type[0].id,

                                    })

                                    summ_lines = self.env['summary.sheet.lines'].create(summ)
                                    # if summ_lines.quantity > 0 and values != 'Pallet' and unit != 'month':
                                    #     tsummary_lines.append(summ_lines)
                                    # if summ_lines.quantity > 0 and values == 'Pallet' and unit != 'month':
                                    #     tsummary_lines.append(summ_lines)
                                    if summ_lines.quantity > 0:
                                        tsummary_lines.append(summ_lines)
                                elif tinv.product_id.storage_type.name == sty and values == tinv.charge_unit_type.name and tinv.out_date != False and tinv.in_date != False and e >= tinv.in_date >= s and s <= tinv.out_date >= e and tinv.storage_product == True:
                                    if tinv.charge_unit_type.name not in types:
                                        types.append(tinv.charge_unit_type.name)
                                    duration = (abs((fields.Datetime.to_datetime(e).date()
                                                     - fields.Datetime.to_datetime(s).date()).days) + 1)
                                    print(duration, 'tdur5')
                                    if unit == 'month':
                                        if values == 'CBM':
                                            tcbm += tinv.product_id.prod_volume * tinv.out_qty if tinv.out_qty > 0 else tinv.product_id.prod_volume * tinv.quantity
                                        if values == 'Square Units':
                                            tsq += tinv.product_id.prod_sqm * tinv.out_qty if tinv.out_qty > 0 else tinv.product_id.prod_sqm * tinv.quantity
                                        if values == 'Pallet':
                                            if tinv.pallet_id:
                                                if tinv.pallet_id.id not in tpallets:
                                                    tpallets.append(tinv.pallet_id.id)
                                            # tpallet += 1
                                        if values == 'Weight':
                                            tweight += tinv.product_id.weight * tinv.out_qty if tinv.out_qty > 0 else tinv.product_id.weight * tinv.quantity
                                    else:
                                        if values == 'CBM':
                                            tcbm += tinv.product_id.prod_volume * tinv.out_qty * duration if tinv.out_qty > 0 else tinv.product_id.prod_volume * tinv.quantity * duration
                                        if values == 'Square Units':
                                            tsq += tinv.product_id.prod_sqm * tinv.out_qty * duration if tinv.out_qty > 0 else tinv.product_id.prod_sqm * tinv.quantity * duration
                                        # if values == 'Pallet':
                                        #     tpallet += 1 * duration
                                        if values == 'Weight':
                                            tweight += tinv.product_id.weight * tinv.out_qty * duration if tinv.out_qty > 0 else tinv.product_id.weight * tinv.quantity * duration
                                    print(tcbm, '-------tcbm6')
                                    summ = ({
                                        'start_date': s,
                                        'end_date': e,
                                        'quantity': tinv.out_qty if tinv.out_qty > 0 else tinv.quantity,
                                        'cbm': tinv.product_id.prod_volume,
                                        'sqm': tinv.product_id.prod_sqm,
                                        'pallet': 1,
                                        'weight': tinv.product_id.weight,
                                        'charge_type': 'storage',
                                        'product_id': tinv.product_id.id,
                                        'charge_unit_type': tchrg_unit_type[0].id,

                                    })

                                    summ_lines = self.env['summary.sheet.lines'].create(summ)
                                    # if summ_lines.quantity > 0 and values != 'Pallet' and unit != 'month':
                                    #     tsummary_lines.append(summ_lines)
                                    # if summ_lines.quantity > 0 and values == 'Pallet' and unit != 'month':
                                    #     tsummary_lines.append(summ_lines)
                                    if summ_lines.quantity > 0:
                                        tsummary_lines.append(summ_lines)
                        pals = tinven.filtered(lambda
                                                   inv: inv.charge_unit_type.name == 'Pallet' and inv.product_id.storage_type.name == sty)
                        print(pals, '-------------------pals---------------')
                        max = {}
                        for pinv in pals:
                            if values == pinv.charge_unit_type.name and pinv.in_date != False and pinv.out_date != False and e >= pinv.in_date >= s and s <= pinv.out_date <= e and pinv.storage_product == True:
                                print(pinv.duration, '-------dur 1')
                                duration = pinv.duration
                                pinv.duration_inv = duration
                                max[pinv] = {
                                    'pallet_id': pinv.pallet_id.id,
                                    'duration': duration}
                                # max[pinv] = {'summ': pinv,
                                #              'duration': duration,
                                #              }                                         }

                            elif values == pinv.charge_unit_type.name and pinv.in_date != False and e >= pinv.in_date >= s and pinv.out_date == False and pinv.storage_product == True:
                                if pinv.charge_unit_type.name not in types:
                                    types.append(pinv.charge_unit_type.name)
                                duration = (abs((fields.Datetime.to_datetime(e).date()
                                                 - fields.Datetime.to_datetime(pinv.in_date).date()).days) + 1)
                                pinv.duration_inv = duration
                                max[pinv] = {
                                    'pallet_id': pinv.pallet_id.id,
                                    'duration': duration}

                            elif values == pinv.charge_unit_type.name and pinv.in_date != False and pinv.out_date != False and e >= pinv.in_date <= s and s <= pinv.out_date <= e and pinv.storage_product == True:
                                if pinv.charge_unit_type.name not in types:
                                    types.append(pinv.charge_unit_type.name)
                                duration = (abs((fields.Datetime.to_datetime(pinv.out_date).date()
                                                 - fields.Datetime.to_datetime(s).date()).days) + 1)
                                pinv.duration_inv = duration
                                max[pinv] = {
                                    'pallet_id': pinv.pallet_id.id,
                                    'duration': duration}


                            elif values == pinv.charge_unit_type.name and pinv.in_date != False and pinv.out_date != False and e >= pinv.in_date <= s and s <= pinv.out_date >= e and pinv.storage_product == True:
                                if pinv.charge_unit_type.name not in types:
                                    types.append(pinv.charge_unit_type.name)
                                duration = (abs((fields.Datetime.to_datetime(e).date()
                                                 - fields.Datetime.to_datetime(s).date()).days) + 1)
                                pinv.duration_inv = duration
                                max[pinv] = {
                                    'pallet_id': pinv.pallet_id.id,
                                    'duration': duration}


                            elif values == pinv.charge_unit_type.name and pinv.in_date != False and pinv.out_date != False and e >= pinv.in_date >= s and s <= pinv.out_date <= e and pinv.storage_product == True:
                                if pinv.charge_unit_type.name not in types:
                                    types.append(pinv.charge_unit_type.name)
                                duration = (abs((fields.Datetime.to_datetime(e).date()
                                                 - fields.Datetime.to_datetime(pinv.in_date).date()).days) + 1)
                                pinv.duration_inv = duration
                                max[pinv] = {
                                    'pallet_id': pinv.pallet_id.id,
                                    'duration': duration}


                            elif pinv.out_date == False and values == pinv.charge_unit_type.name and pinv.in_date != False and e >= pinv.in_date <= s and pinv.storage_product == True:
                                if pinv.charge_unit_type.name not in types:
                                    types.append(pinv.charge_unit_type.name)
                                duration = (abs((fields.Datetime.to_datetime(e).date()
                                                 - fields.Datetime.to_datetime(s).date()).days) + 1)
                                pinv.duration_inv = duration
                                max[pinv] = {
                                    'pallet_id': pinv.pallet_id.id,
                                    'duration': duration}


                            elif pinv.out_date != False and values == pinv.charge_unit_type.name and pinv.in_date != False and pinv.out_date != False and e >= pinv.in_date >= s and s <= pinv.out_date >= e and pinv.storage_product == True:

                                if pinv.charge_unit_type.name not in types:
                                    types.append(pinv.charge_unit_type.name)
                                duration = (abs((fields.Datetime.to_datetime(e).date()
                                                 - fields.Datetime.to_datetime(pinv.in_date).date()).days) + 1)
                                pinv.duration_inv = duration
                                max[pinv] = {
                                    'pallet_id': pinv.pallet_id.id,
                                    'duration': duration}

                        print(max, '----------max')
                        MAX = max
                        data_list = [(key, value) for key, value in max.items()]

                        # Sort the list based on pallet_id
                        data_list.sort(key=lambda x: (x[1]['pallet_id'], -x[1]['duration']))

                        # Create a new dictionary to store the sorted and filtered data
                        sorted_data = {}

                        # Iterate through the sorted list and keep the summary records with the highest duration for each unique pallet_id
                        seen_pallets = set()
                        sorted_summ = []
                        for summary, info in data_list:
                            pallet_id = info['pallet_id']
                            duration = info['duration']

                            # If pallet_id is False, skip this entry
                            if pallet_id is False:
                                continue

                            # If pallet_id is not seen before or has a higher duration, add it to the new dictionary
                            if pallet_id not in seen_pallets or duration > sorted_data[pallet_id]['duration']:
                                sorted_data[pallet_id] = {'summary': summary, 'duration': duration}
                                seen_pallets.add(pallet_id)
                                sorted_summ.append(summary)

                        # Print the sorted and filtered data
                        for pallet_id, info in sorted_data.items():
                            print(f'Pallet ID: {pallet_id}, Summary: {info["summary"]}, Duration: {info["duration"]}')
                        print(sorted_summ, 'sorted_summ')
                        for inv in sorted_summ:
                            if values == inv.charge_unit_type.name and inv.in_date != False and inv.out_date != False and e >= inv.in_date >= s and s <= inv.out_date <= e and inv.storage_product == True:
                                print(inv.duration, 'dur 1')
                                duration = inv.duration
                                if inv.charge_unit_type.name not in types:
                                    types.append(inv.charge_unit_type.name)
                                if unit == 'day':
                                    tpallet += duration
                                summ = ({
                                    'start_date': inv.in_date,
                                    'end_date': inv.out_date,
                                    'quantity': inv.out_qty if inv.out_qty > 0 else inv.quantity,
                                    'pallet': 1,
                                    'charge_type': 'storage',
                                    'product_id': inv.product_id.id,
                                    'charge_unit_type': tchrg_unit_type[0].id,

                                })
                                summ_lines = self.env['summary.sheet.lines'].create(summ)

                                if summ_lines.quantity > 0:
                                    summary_lines.append(summ_lines)
                            elif values == inv.charge_unit_type.name and inv.in_date != False and e >= inv.in_date >= s and inv.out_date == False and inv.storage_product == True:
                                if inv.charge_unit_type.name not in types:
                                    types.append(inv.charge_unit_type.name)
                                duration = (abs((fields.Datetime.to_datetime(e).date()
                                                 - fields.Datetime.to_datetime(inv.in_date).date()).days) + 1)
                                print(duration, 'dur 2')
                                if unit == 'day':
                                    tpallet += duration
                                summ = ({
                                    'start_date': inv.in_date,
                                    'end_date': e,
                                    'quantity': inv.out_qty if inv.out_qty > 0 else inv.quantity,
                                    'pallet': 1,
                                    'charge_type': 'storage',
                                    'product_id': inv.product_id.id,
                                    'charge_unit_type': tchrg_unit_type[0].id,

                                })
                                summ_lines = self.env['summary.sheet.lines'].create(summ)

                                if summ_lines.quantity > 0:
                                    summary_lines.append(summ_lines)
                            elif values == inv.charge_unit_type.name and inv.in_date != False and inv.out_date != False and e >= inv.in_date <= s and s <= inv.out_date <= e and inv.storage_product == True:
                                if inv.charge_unit_type.name not in types:
                                    types.append(inv.charge_unit_type.name)
                                duration = (abs((fields.Datetime.to_datetime(inv.out_date).date()
                                                 - fields.Datetime.to_datetime(s).date()).days) + 1)
                                print(inv.out_date, s, duration, 'dur 3')
                                if unit == 'day':
                                    tpallet += duration
                                summ = ({
                                    'start_date': s,
                                    'end_date': inv.out_date,
                                    'quantity': inv.out_qty if inv.out_qty > 0 else inv.quantity,
                                    'pallet': 1,
                                    'charge_type': 'storage',
                                    'product_id': inv.product_id.id,
                                    'charge_unit_type': tchrg_unit_type[0].id,

                                })
                                summ_lines = self.env['summary.sheet.lines'].create(summ)

                                if summ_lines.quantity > 0:
                                    summary_lines.append(summ_lines)
                            elif values == inv.charge_unit_type.name and inv.in_date != False and inv.out_date != False and e >= inv.in_date <= s and s <= inv.out_date >= e and inv.storage_product == True:
                                if inv.charge_unit_type.name not in types:
                                    types.append(inv.charge_unit_type.name)
                                duration = (abs((fields.Datetime.to_datetime(e).date()
                                                 - fields.Datetime.to_datetime(s).date()).days) + 1)
                                print(duration, 'dur 4')
                                if unit == 'day':
                                    tpallet += duration

                                summ = ({
                                    'start_date': s,
                                    'end_date': e,
                                    'quantity': inv.out_qty if inv.out_qty > 0 else inv.quantity,
                                    'pallet': 1,
                                    'charge_type': 'storage',
                                    'product_id': inv.product_id.id,
                                    'charge_unit_type': tchrg_unit_type[0].id,

                                })
                                summ_lines = self.env['summary.sheet.lines'].create(summ)

                                if summ_lines.quantity > 0:
                                    summary_lines.append(summ_lines)
                            elif values == inv.charge_unit_type.name and inv.in_date != False and inv.out_date != False and e >= inv.in_date >= s and s <= inv.out_date <= e and inv.storage_product == True:
                                if inv.charge_unit_type.name not in types:
                                    types.append(inv.charge_unit_type.name)
                                duration = (abs((fields.Datetime.to_datetime(e).date()
                                                 - fields.Datetime.to_datetime(inv.in_date).date()).days) + 1)
                                print(duration, 'dur 5')
                                if unit == 'day':
                                    tpallet += duration

                                summ = ({
                                    'start_date': inv.in_date,
                                    'end_date': e,
                                    'quantity': inv.out_qty if inv.out_qty > 0 else inv.quantity,
                                    'pallet': 1,
                                    'charge_type': 'storage',
                                    'product_id': inv.product_id.id,
                                    'charge_unit_type': tchrg_unit_type[0].id,

                                })
                                summ_lines = self.env['summary.sheet.lines'].create(summ)

                                if summ_lines.quantity > 0:
                                    summary_lines.append(summ_lines)
                            elif values == inv.charge_unit_type.name and inv.in_date != False and e >= inv.in_date <= s and inv.out_date == False and inv.storage_product == True:
                                if inv.charge_unit_type.name not in types:
                                    types.append(inv.charge_unit_type.name)
                                duration = (abs((fields.Datetime.to_datetime(e).date()
                                                 - fields.Datetime.to_datetime(s).date()).days) + 1)
                                print(duration, 'dur 6')
                                if unit == 'day':
                                    tpallet += duration

                                summ = ({
                                    'start_date': s,
                                    'end_date': e,
                                    'quantity': inv.out_qty if inv.out_qty > 0 else inv.quantity,
                                    'pallet': 1,
                                    'charge_type': 'storage',
                                    'product_id': inv.product_id.id,
                                    'charge_unit_type': tchrg_unit_type[0].id,

                                })
                                summ_lines = self.env['summary.sheet.lines'].create(summ)

                                if summ_lines.quantity > 0:
                                    summary_lines.append(summ_lines)
                            elif values == inv.charge_unit_type.name and inv.out_date != False and inv.in_date != False and e >= inv.in_date >= s and s <= inv.out_date >= e and inv.storage_product == True:
                                if inv.charge_unit_type.name not in types:
                                    types.append(inv.charge_unit_type.name)
                                duration = (abs((fields.Datetime.to_datetime(e).date()
                                                 - fields.Datetime.to_datetime(inv.in_date).date()).days) + 1)
                                print(duration, 'dur 7')
                                if unit == 'day':
                                    tpallet += duration

                                summ = ({
                                    'start_date': s,
                                    'end_date': e,
                                    'quantity': inv.out_qty if inv.out_qty > 0 else inv.quantity,
                                    'pallet': 1,
                                    'charge_type': 'storage',
                                    'product_id': inv.product_id.id,
                                    'charge_unit_type': tchrg_unit_type[0].id,

                                })
                                summ_lines = self.env['summary.sheet.lines'].create(summ)

                                if summ_lines.quantity > 0:
                                    summary_lines.append(summ_lines)

                    if tpallets:
                        tpallet_count = len(tpallets)
                        tchrg_unit_type = self.env['charge.types'].search([('name', '=', 'Pallet')])
                        summ = ({
                            # 'start_date': inv.in_date,
                            # 'end_date': inv.out_date,
                            # 'quantity': inv.out_qty if inv.out_qty > 0 else inv.quantity,
                            # 'cbm': cbm,
                            # 'cbm': inv.product_id.prod_volume,
                            # 'sqm': inv.product_id.prod_sqm,
                            'pallet': tpallet_count,
                            # 'weight': inv.product_id.weight,
                            'charge_type': 'storage',
                            # 'product_id': inv.product_id.id,
                            'charge_unit_type': tchrg_unit_type[0].id,

                        })
                        summ_lines = self.env['summary.sheet.lines'].create(summ)
                        tsummary_lines.append(summ_lines)
                    else:
                        tpallet_count = 0
                        print(types, '======sto==true====')
                    if types:

                        for type in types:
                            print(type, sty, '------------------------hb-------typesto-----------------')
                            for temp in tstorage_charges.filtered(lambda inv: inv.storage_type.name == sty):
                                # print(temp, temp.charge_unit_type.name, type, '-------------------------temp----------------------')
                                if temp.charge_type == 'storage' and temp.charge_unit_type.name == 'CBM' and temp.charge_unit_type.name == type:
                                    temp_line_values = {
                                        'product_id': temp.product_id and temp.product_id.id or False,
                                        'name': temp.product_id.name or '',
                                        'price_unit': temp.list_price or 0.00,
                                        'quantity': tcbm,
                                        'currency_id': temp.currency_id.id,
                                        'tax_ids': [(6, 0, [temp.tax_id.id])] if temp.tax_id else False,
                                        'account_id': temp.product_id.property_account_income_id.id if temp.product_id.property_account_income_id
                                        else temp.product_id.categ_id.property_account_income_categ_id.id,
                                        # 'start_date': move_ids_without_package.start_date,
                                        # 'end_date': move_ids_without_package.end_date,

                                    }
                                    if temp_line_values['quantity'] > 0:
                                        print(temp_line_values, temp.storage_type.name)
                                        tinvoice_line_list.append((0, 0, temp_line_values))

                                if temp.charge_type == 'storage' and temp.charge_unit_type.name == 'Weight' and temp.charge_unit_type.name == type:
                                    temp_line_values = {
                                        'product_id': temp.product_id and temp.product_id.id or False,
                                        'name': temp.product_id.name or '',
                                        'price_unit': temp.list_price or 0.00,
                                        'quantity': tweight,
                                        'currency_id': temp.currency_id.id,
                                        'tax_ids': [(6, 0, [temp.tax_id.id])] if temp.tax_id else False,
                                        'account_id': temp.product_id.property_account_income_id.id if temp.product_id.property_account_income_id
                                        else temp.product_id.categ_id.property_account_income_categ_id.id,
                                        # 'start_date': move_ids_without_package.start_date,
                                        # 'end_date': move_ids_without_package.end_date,

                                    }
                                    if temp_line_values['quantity'] > 0:
                                        print(temp_line_values, temp.storage_type.name)
                                        tinvoice_line_list.append((0, 0, temp_line_values))

                                if temp.charge_type == 'storage' and temp.charge_unit_type.name == 'Square Units' and temp.charge_unit_type.name == type:
                                    temp_line_values = {
                                        'product_id': temp.product_id and temp.product_id.id or False,
                                        'name': temp.product_id.name or '',
                                        'price_unit': temp.list_price or 0.00,
                                        'quantity': tsq,
                                        'currency_id': temp.currency_id.id,
                                        'tax_ids': [(6, 0, [temp.tax_id.id])] if temp.tax_id else False,
                                        'account_id': temp.product_id.property_account_income_id.id if temp.product_id.property_account_income_id
                                        else temp.product_id.categ_id.property_account_income_categ_id.id,
                                        # 'start_date': move_ids_without_package.start_date,
                                        # 'end_date': move_ids_without_package.end_date,

                                    }
                                    if temp_line_values['quantity'] > 0:
                                        print(temp_line_values, temp.storage_type.name)
                                        tinvoice_line_list.append((0, 0, temp_line_values))

                                if temp.charge_type == 'storage' and temp.charge_unit_type.name == 'Pallet' and temp.charge_unit_type.name == type:
                                    temp_line_values = {
                                        'product_id': temp.product_id and temp.product_id.id or False,
                                        'name': temp.product_id.name or '',
                                        'price_unit': temp.list_price or 0.00,
                                        'quantity': tpallet if tpallet > 0 else tpallet_count,
                                        'currency_id': temp.currency_id.id,
                                        'tax_ids': [(6, 0, [temp.tax_id.id])] if temp.tax_id else False,
                                        'account_id': temp.product_id.property_account_income_id.id if temp.product_id.property_account_income_id
                                        else temp.product_id.categ_id.property_account_income_categ_id.id,
                                        # 'start_date': move_ids_without_package.start_date,
                                        # 'end_date': move_ids_without_package.end_date,

                                    }
                                    if temp_line_values['quantity'] > 0:
                                        print(temp_line_values, temp.storage_type.name)
                                        tinvoice_line_list.append((0, 0, temp_line_values))

                if tother_values:
                    print(tother_values, '---------------tother_values')
                    for values, unit in tother_values.items():
                        tcbm = 0
                        tweight = 0
                        tsq = 0
                        tpallet = 0
                        tquo = 0
                        tchrg_unit_type = self.env['charge.types'].search([('name', '=', values)])
                        print(tinven.charge_unit_type, '----tinven----')
                        for tinv in tinven.filtered(
                                lambda inv: inv.charge_unit_type.name == values and inv.product_id.storage_type.name == sty):
                            if tinv.product_id.storage_type.name == sty and values == tinv.charge_unit_type.name and tinv.in_date != False and tinv.out_date != False and e >= tinv.in_date >= s and s <= tinv.out_date <= e and tinv.storage_product == True:
                                if unit == 'month':
                                    tcbm += tinv.product_id.prod_volume * tinv.out_qty if tinv.out_qty > 0 else tinv.quantity
                                    tsq += tinv.product_id.prod_sqm * tinv.out_qty if tinv.out_qty > 0 else tinv.quantity
                                    tpallet += 1
                                    tweight += tinv.product_id.weight * tinv.out_qty if tinv.out_qty > 0 else tinv.quantity
                                    tquo += 1
                                else:
                                    tcbm += tinv.product_id.prod_volume * tinv.out_qty if tinv.out_qty > 0 else tinv.quantity * tinv.duration
                                    tsq += tinv.product_id.prod_sqm * tinv.out_qty if tinv.out_qty > 0 else tinv.quantity * tinv.duration
                                    tpallet += 1
                                    tweight += tinv.product_id.weight * tinv.out_qty if tinv.out_qty > 0 else tinv.quantity * tinv.duration
                                    tquo += 1 * tinv.duration

                                summ = ({
                                    'start_date': tinv.in_date,
                                    'end_date': tinv.out_date,
                                    'quantity': tinv.out_qty if tinv.out_qty > 0 else tinv.quantity,
                                    'other': 1,
                                    'charge_type': 'storage',
                                    'product_id': tinv.product_id.id,
                                    'charge_unit_type': tchrg_unit_type[0].id,
                                })
                                summ_lines = self.env['summary.sheet.lines'].create(summ)
                                if summ_lines.quantity > 0:
                                    tsummary_lines.append(summ_lines)
                            elif tinv.product_id.storage_type.name == sty and values == tinv.charge_unit_type.name and tinv.in_date != False and e >= tinv.in_date >= s and tinv.out_date == False and tinv.storage_product == True:
                                duration = (abs((fields.Datetime.to_datetime(e).date()
                                                 - fields.Datetime.to_datetime(tinv.in_date).date()).days) + 1)

                                if unit == 'month':
                                    tcbm += tinv.product_id.prod_volume * tinv.out_qty if tinv.out_qty > 0 else tinv.quantity
                                    tsq += tinv.product_id.prod_sqm * tinv.out_qty if tinv.out_qty > 0 else tinv.quantity
                                    tpallet += 1
                                    tweight += tinv.product_id.weight * tinv.out_qty if tinv.out_qty > 0 else tinv.quantity
                                    tquo += 1
                                else:
                                    tcbm += tinv.product_id.prod_volume * tinv.out_qty if tinv.out_qty > 0 else tinv.quantity * duration
                                    tsq += tinv.product_id.prod_sqm * tinv.out_qty if tinv.out_qty > 0 else tinv.quantity * duration
                                    tpallet += 1
                                    tweight += tinv.product_id.weight * tinv.out_qty if tinv.out_qty > 0 else tinv.quantity * duration
                                    tquo += 1 * duration
                                summ = ({
                                    'start_date': tinv.in_date,
                                    'end_date': e,
                                    'quantity': tinv.out_qty if tinv.out_qty > 0 else tinv.quantity,
                                    'other': 1,
                                    'charge_type': 'storage',
                                    'product_id': tinv.product_id.id,
                                    'charge_unit_type': tchrg_unit_type[0].id,

                                })
                                summ_lines = self.env['summary.sheet.lines'].create(summ)
                                if summ_lines.quantity > 0:
                                    tsummary_lines.append(summ_lines)
                            # elif tinv.in_date != False and e >= tinv.in_date >= s and s <= tinv.out_date <= e and tinv.storage_product == True:
                            #     duration = abs((fields.Datetime.to_datetime(tinv.out_date).date()
                            #                     - fields.Datetime.to_datetime(s).date()).days)
                            #     # tcbm += tinv.product_id.x_vol * tinv.out_qty if tinv.out_qty > 0 else tinv.quantity * tinv.duration
                            #     # tsq += tinv.product_id.x_vol * tinv.out_qty if tinv.out_qty > 0 else tinv.quantity * tinv.duration
                            #     tcbm += tinv.product_id.prod_volume * tinv.out_qty if tinv.out_qty > 0 else tinv.quantity * duration
                            #     tsq += tinv.product_id.prod_sqm * tinv.out_qty if tinv.out_qty > 0 else tinv.quantity * duration
                            #     tpallet += 1
                            #     tweight += tinv.product_id.weight * tinv.out_qty if tinv.out_qty > 0 else tinv.quantity * duration
                            #     summ = ({
                            #         'start_date': s,
                            #         'end_date': tinv.out_date,
                            #         'quantity': tinv.out_qty if tinv.out_qty > 0 else tinv.quantity,
                            #         'cbm': cbm,
                            #         'sqm': sq,
                            #         'pallet': pallet,
                            #         'weight': weight,
                            #     })
                            #     summ_lines = self.env['summary.sheet.lines'].create(summ)
                            #     summary_lines.append(summ_lines)
                            elif tinv.product_id.storage_type.name == sty and values == tinv.charge_unit_type.name and tinv.in_date != False and tinv.out_date != False and e >= tinv.in_date <= s and s <= tinv.out_date <= e and tinv.storage_product == True:
                                duration = (abs((fields.Datetime.to_datetime(e).date()
                                                 - fields.Datetime.to_datetime(tinv.in_date).date()).days) + 1)

                                if unit == 'month':
                                    tcbm += tinv.product_id.prod_volume * tinv.out_qty if tinv.out_qty > 0 else tinv.quantity
                                    tsq += tinv.product_id.prod_sqm * tinv.out_qty if tinv.out_qty > 0 else tinv.quantity
                                    tpallet += 1
                                    tweight += tinv.product_id.weight * tinv.out_qty if tinv.out_qty > 0 else tinv.quantity
                                    tquo += 1
                                else:
                                    tcbm += tinv.product_id.prod_volume * tinv.out_qty if tinv.out_qty > 0 else tinv.quantity * duration
                                    tsq += tinv.product_id.prod_sqm * tinv.out_qty if tinv.out_qty > 0 else tinv.quantity * duration
                                    tpallet += 1
                                    tweight += tinv.product_id.weight * tinv.out_qty if tinv.out_qty > 0 else tinv.quantity * duration
                                    tquo += 1 * duration
                                summ = ({
                                    'start_date': tinv.in_date,
                                    'end_date': tinv.out_date,
                                    'quantity': tinv.out_qty if tinv.out_qty > 0 else tinv.quantity,
                                    'other': 1,
                                    'charge_type': 'storage',
                                    'product_id': tinv.product_id.id,
                                    'charge_unit_type': tchrg_unit_type[0].id,

                                })
                                summ_lines = self.env['summary.sheet.lines'].create(summ)
                                if summ_lines.quantity > 0:
                                    tsummary_lines.append(summ_lines)
                            elif tinv.product_id.storage_type.name == sty and values == tinv.charge_unit_type.name and tinv.in_date != False and tinv.out_date != False and e >= tinv.in_date <= s and s <= tinv.out_date >= e and tinv.storage_product == True:
                                duration = (abs((fields.Datetime.to_datetime(e).date()
                                                 - fields.Datetime.to_datetime(s).date()).days) + 1)

                                if unit == 'month':
                                    tcbm += tinv.product_id.prod_volume * tinv.out_qty if tinv.out_qty > 0 else tinv.quantity
                                    tsq += tinv.product_id.prod_sqm * tinv.out_qty if tinv.out_qty > 0 else tinv.quantity
                                    tpallet += 1
                                    tweight += tinv.product_id.weight * tinv.out_qty if tinv.out_qty > 0 else tinv.quantity
                                    tquo += 1
                                else:
                                    tcbm += tinv.product_id.prod_volume * tinv.out_qty if tinv.out_qty > 0 else tinv.quantity * duration
                                    tsq += tinv.product_id.prod_sqm * tinv.out_qty if tinv.out_qty > 0 else tinv.quantity * duration
                                    tpallet += 1
                                    tweight += tinv.product_id.weight * tinv.out_qty if tinv.out_qty > 0 else tinv.quantity * duration
                                    tquo += 1 * duration
                                summ = ({
                                    'start_date': s,
                                    'end_date': e,
                                    'quantity': tinv.out_qty if tinv.out_qty > 0 else tinv.quantity,
                                    'other': 1,
                                    'charge_type': 'storage',
                                    'product_id': tinv.product_id.id,
                                    'charge_unit_type': tchrg_unit_type[0].id,

                                })
                                summ_lines = self.env['summary.sheet.lines'].create(summ)
                                if summ_lines.quantity > 0:
                                    tsummary_lines.append(summ_lines)
                            elif tinv.product_id.storage_type.name == sty and values == tinv.charge_unit_type.name and tinv.in_date != False and e >= tinv.in_date <= s and tinv.out_date == False and tinv.storage_product == True:
                                duration = (abs((fields.Datetime.to_datetime(e).date()
                                                 - fields.Datetime.to_datetime(s).date()).days) + 1)

                                if unit == 'month':
                                    tcbm += tinv.product_id.prod_volume * tinv.out_qty if tinv.out_qty > 0 else tinv.quantity
                                    tsq += tinv.product_id.prod_sqm * tinv.out_qty if tinv.out_qty > 0 else tinv.quantity
                                    tpallet += 1
                                    tweight += tinv.product_id.weight * tinv.out_qty if tinv.out_qty > 0 else tinv.quantity
                                    tquo += 1
                                else:
                                    tcbm += tinv.product_id.prod_volume * tinv.out_qty if tinv.out_qty > 0 else tinv.quantity * duration
                                    tsq += tinv.product_id.prod_sqm * tinv.out_qty if tinv.out_qty > 0 else tinv.quantity * duration
                                    tpallet += 1
                                    tweight += tinv.product_id.weight * tinv.out_qty if tinv.out_qty > 0 else tinv.quantity * duration
                                    tquo += 1 * duration
                                summ = ({
                                    'start_date': s,
                                    'end_date': e,
                                    'quantity': tinv.out_qty if tinv.out_qty > 0 else tinv.quantity,
                                    'other': 1,
                                    'charge_type': 'storage',
                                    'product_id': tinv.product_id.id,
                                    'charge_unit_type': tchrg_unit_type[0].id,

                                })

                                summ_lines = self.env['summary.sheet.lines'].create(summ)
                                if summ_lines.quantity > 0:
                                    tsummary_lines.append(summ_lines)
                            elif tinv.product_id.storage_type.name == sty and values == tinv.charge_unit_type.name and tinv.out_date != False and tinv.in_date != False and e >= tinv.in_date <= s and tinv.out_date == False and tinv.storage_product == True:

                                duration = (abs((fields.Datetime.to_datetime(e).date()
                                                 - fields.Datetime.to_datetime(s).date()).days) + 1)
                                if unit == 'month':
                                    tcbm += tinv.product_id.prod_volume * tinv.out_qty if tinv.out_qty > 0 else tinv.quantity
                                    tsq += tinv.product_id.prod_sqm * tinv.out_qty if tinv.out_qty > 0 else tinv.quantity
                                    tpallet += 1
                                    tweight += tinv.product_id.weight * tinv.out_qty if tinv.out_qty > 0 else tinv.quantity
                                    tquo += 1
                                else:
                                    tcbm += tinv.product_id.prod_volume * tinv.out_qty if tinv.out_qty > 0 else tinv.quantity * duration
                                    tsq += tinv.product_id.prod_sqm * tinv.out_qty if tinv.out_qty > 0 else tinv.quantity * duration
                                    tpallet += 1
                                    tweight += tinv.product_id.weight * tinv.out_qty if tinv.out_qty > 0 else tinv.quantity * duration
                                    tquo += 1 * duration
                                summ = ({
                                    'start_date': s,
                                    'end_date': e,
                                    'quantity': tinv.out_qty if tinv.out_qty > 0 else tinv.quantity,
                                    'other': 1,
                                    'charge_type': 'storage',
                                    'product_id': tinv.product_id.id,
                                    'charge_unit_type': tchrg_unit_type[0].id,

                                })
                                summ_lines = self.env['summary.sheet.lines'].create(summ)
                                if summ_lines.quantity > 0:
                                    summary_lines.append(summ_lines)
                        print(tquo, '------------------tquo------------')
                        for temp in tstorage_charges:
                            print(temp.charge_unit_type.name, values, temp.product_id, temp.storage_type.name, sty,
                                  temp.agreement_id, agreement_id)

                        for temp in tstorage_charges.filtered(
                                lambda inv: inv.charge_unit_type.name == values and inv.storage_type.name == sty and inv.agreement_id == agreement_id):
                            print(temp,
                                  '------------------------------------temp----------------------------------------')
                            if temp.charge_type == 'storage' and temp.charge_unit_type.name == values and temp.storage_type:
                                print('if')
                                temp_line_values = {
                                    'product_id': temp.product_id and temp.product_id.id or False,
                                    'name': temp.product_id.name or '',
                                    'price_unit': temp.list_price or 0.00,
                                    'quantity': tquo,
                                    'currency_id': temp.currency_id.id,
                                    'tax_ids': [(6, 0, [temp.tax_id.id])] if temp.tax_id else False,
                                    'account_id': temp.product_id.property_account_income_id.id if temp.product_id.property_account_income_id
                                    else temp.product_id.categ_id.property_account_income_categ_id.id,
                                    # 'start_date': move_ids_without_package.start_date,
                                    # 'end_date': move_ids_without_package.end_date,

                                }
                                if temp_line_values['quantity'] > 0:
                                    tinvoice_line_list.append((0, 0, temp_line_values))
                            break

                if tser == False:

                    picking_id_in = self.env['stock.picking'].search(
                        [('picking_type_id.code', '=', 'incoming'), ('partner_id', '=', partner.id),
                         ('scheduled_date', '>=', s), ('product_id.storage_type', '!=', False)])
                    in_vals = []
                    for picking in picking_id_in:
                        if s <= picking.scheduled_date <= e:
                            for pick in picking.service_id:
                                # if pick.product_id
                                vals = (0, 0, {
                                    'name': pick.product_id.name,
                                    'product_id': pick.product_id.id,
                                    'price_unit': pick.price,
                                    'account_id': pick.product_id.property_account_income_id.id if pick.product_id.property_account_income_id
                                    else pick.product_id.categ_id.property_account_income_categ_id.id,
                                    'tax_ids': [(6, 0, [pick.taxes_id.id])] if pick.taxes_id else False,
                                    'quantity': pick.qty,

                                    # 'quantity': move_ids_without_package.quantt if move_ids_without_package.inv_meth else 1,
                                    # 'x_cbm': picking.x_cbm,
                                    # 'start_date': picking.scheduled_date,
                                    # 'end_date': picking.date_done,

                                })
                                in_vals.append(vals)
                                # invoice_line_list.append(vals)
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
                    consolidated_in_data = {}
                    for item in in_vals:
                        _, _, item_data = item
                        product_id = item_data['product_id']
                        price_unit = item_data['price_unit']
                        quantity = item_data['quantity']

                        if product_id in consolidated_in_data:
                            consolidated_in_data[product_id]['price_unit'] += price_unit
                            consolidated_in_data[product_id]['quantity'] += quantity

                        else:
                            consolidated_in_data[product_id] = item_data

                    consolidated_in_list = [(0, 0, data) for data in consolidated_in_data.values()]
                    print(consolidated_in_list, 'consolidated_in_list')
                    for c in consolidated_in_list:
                        print(c, '------------------------------------------------c-------------------------')
                        tinvoice_line_list.append(c)

                    picking_id_out = self.env['stock.picking'].search(
                        [('picking_type_id.code', '=', 'outgoing'), ('partner_id', '=', partner.id),
                         ('scheduled_date', '>=', s), ('product_id.storage_type', '!=', False)])
                    out_vals = []
                    for picking in picking_id_out:
                        if s <= picking.scheduled_date <= e:
                            for pick in picking.service_id:
                                vals = (0, 0, {
                                    'name': pick.product_id.name,
                                    'product_id': pick.product_id.id,
                                    'price_unit': pick.qty,
                                    'account_id': pick.product_id.property_account_income_id.id if pick.product_id.property_account_income_id
                                    else pick.product_id.categ_id.property_account_income_categ_id.id,
                                    'tax_ids': [(6, 0, [pick.taxes_id.id])] if pick.taxes_id else False,
                                    'quantity': pick.price,

                                    # 'quantity': move_ids_without_package.quantt if move_ids_without_package.inv_meth else 1,
                                    # 'x_cbm': picking.x_cbm,
                                    # 'start_date': picking.scheduled_date,
                                    # 'end_date': picking.date_done,

                                })
                                # invoice_line_list.append(vals)
                                out_vals.append(vals)
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
                    consolidated_out_data = {}
                    for item in out_vals:
                        _, _, item_data = item
                        product_id = item_data['product_id']
                        price_unit = item_data['price_unit']
                        quantity = item_data['quantity']

                        if product_id in consolidated_out_data:
                            consolidated_out_data[product_id]['price_unit'] += price_unit
                            consolidated_out_data[product_id]['quantity'] += quantity

                        else:
                            consolidated_out_data[product_id] = item_data

                    consolidated_out_list = [(0, 0, data) for data in consolidated_out_data.values()]
                    print(consolidated_out_list, 'consolidated_out_list')
                    for c in consolidated_out_list:
                        print(c, '------------------------------------------------c-------------------------')
                        tinvoice_line_list.append(c)

                    tser = True

            current_user = self.env.uid

            if agreement_id and tinvoice_line_list:
                tinvoice = partner.env['account.move'].create({
                    'type': 'out_invoice',
                    'sto_type': 'warehouse',
                    'start_date_sto': s,
                    'end_date_sto': e,
                    'invoice_origin': partner.name,
                    'invoice_user_id': current_user,
                    'narration': partner.name,
                    'partner_id': partner.id,
                    'currency_id': partner.env.user.company_id.currency_id.id,
                    # 'journal_id': int(UOMer_journal_id),
                    'invoice_payment_ref': partner.name,
                    # 'picking_id': picking_id.id,
                    'invoice_line_ids': tinvoice_line_list,
                    # 'invoice_type': 'storage',
                    'name': '/',

                })
                invoices.append(tinvoice.id)
                tinvoice._summary_sheet()

                tsummary = ({
                    'name': str(s) + '-' + str(e) + '-' + 'Temperature Control',
                    'partner_id': partner.id,
                    'invoice_id': tinvoice.id
                })
                tsummary = self.env['summary.sheet'].create(tsummary)
                for lines in tsummary_lines:
                    lines['sheet_id'] = tsummary
                # if tinvoice:
                #     message = 'Cheers! Your Invoice is Successfully Crafted'
                #     return {
                #         'type': 'ir.actions.client',
                #         'tag': 'display_notification',
                #         'params': {
                #             'message': message,
                #             'type': 'success'  # Use 'warning' for a warning notification
                #         }
                #     }
                # if lines.product_id.storage_type:
                #     lines['sheet_id'] = tsummary
        return invoices

    def create_inv_invoice_core_seperateexist(self):
        invoices = []
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
            charge_unit_types = {}
            for c in storage_charges:
                chrg = c['charge_unit_type']['name']
                sto = c['storage_uom']
                charge_unit_types[chrg] = sto
            # charge_unit_types = []
            # for c in storage_charges:
            #     if c.charge_unit_type:
            #         charge_unit_types.append(c.charge_unit_type.name)
            # values_except_UOM = list(filter(lambda x: x != 'UOM', charge_unit_types))
            values_except_UOM = {chrg: sto for chrg, sto in charge_unit_types.items() if chrg != 'UOM' and
                                 chrg in ['CBM', 'Pallet', 'Square Units', 'Weight']}
            other_values = {chrg: sto for chrg, sto in charge_unit_types.items() if chrg not in
                            ['CBM', 'Pallet', 'Square Units', 'Weight', 'UOM']}
            print(values_except_UOM, other_values)
            uoms = {}
            for u in storage_charges:
                if u.uom_id:
                    uom = u['uom_id']['id']
                    unit = u['storage_uom']
                    uoms[uom] = unit
            inven = self.env['product.summary'].search(
                [('partner_id', '=', partner.id), ('storage_product', '=', False),('gen_seperate_inv','=',False)])

            invoice_line_list = []
            summary_lines = []
            tsummary_lines = []

            if uoms:
                for uom, unit in uoms.items():
                    quantity_dict[uom] = 0
                    for inv in inven:
                        UOM = self.env['charge.types'].search([('name', '=', 'UOM')])
                        if uom == inv.uom_id.id:
                            if inv.charge_unit_type.name == 'UOM' and inv.in_date != False and inv.out_date != False and e >= inv.in_date >= s and s <= inv.out_date <= e and inv.storage_product == False:
                                if unit == 'month':
                                    quantity_dict[uom] += inv.out_qty if inv.out_qty > 0 else inv.quantity
                                else:
                                    quantity_dict[
                                        uom] += inv.out_qty if inv.out_qty > 0 else inv.quantity * inv.duration

                                summ = ({
                                    'start_date': inv.in_date,
                                    'end_date': inv.out_date,
                                    'quantity': inv.out_qty if inv.out_qty > 0 else inv.quantity,
                                    'charge_type': 'storage',
                                    'product_id': inv.product_id.id,
                                    'charge_unit_type': UOM[0].id,
                                })
                                summ_lines = self.env['summary.sheet.lines'].create(summ)
                                if summ_lines.quantity > 0:
                                    summary_lines.append(summ_lines)
                            elif inv.charge_unit_type.name == 'UOM' and inv.in_date != False and e >= inv.in_date >= s and inv.out_date == False and inv.storage_product == False:
                                duration = (abs((fields.Datetime.to_datetime(e).date()
                                                 - fields.Datetime.to_datetime(inv.in_date).date()).days) + 1)
                                if unit == 'month':
                                    quantity_dict[uom] += inv.out_qty if inv.out_qty > 0 else inv.quantity
                                else:
                                    quantity_dict[uom] += inv.out_qty if inv.out_qty > 0 else inv.quantity * duration
                                summ = ({
                                    'start_date': inv.in_date,
                                    'end_date': e,
                                    'quantity': inv.out_qty if inv.out_qty > 0 else inv.quantity,
                                    'charge_type': 'storage',
                                    'product_id': inv.product_id.id,
                                    'charge_unit_type': UOM[0].id,

                                })
                                summ_lines = self.env['summary.sheet.lines'].create(summ)
                                if summ_lines.quantity > 0:
                                    summary_lines.append(summ_lines)
                            elif inv.charge_unit_type.name == 'UOM' and inv.in_date != False and inv.out_date != False and e >= inv.in_date <= s and s <= inv.out_date <= e and inv.storage_product == False:

                                duration = (abs((fields.Datetime.to_datetime(inv.out_date).date()
                                                 - fields.Datetime.to_datetime(s).date()).days) + 1)
                                if unit == 'month':
                                    quantity_dict[uom] += inv.out_qty if inv.out_qty > 0 else inv.quantity
                                else:
                                    quantity_dict[uom] += inv.out_qty if inv.out_qty > 0 else inv.quantity * duration

                                summ = ({
                                    'start_date': s,
                                    'end_date': inv.out_date,
                                    'quantity': inv.out_qty if inv.out_qty > 0 else inv.quantity,
                                    'charge_type': 'storage',
                                    'product_id': inv.product_id.id,
                                    'charge_unit_type': UOM[0].id,

                                })
                                summ_lines = self.env['summary.sheet.lines'].create(summ)
                                if summ_lines.quantity > 0:
                                    summary_lines.append(summ_lines)
                            elif inv.charge_unit_type.name == 'UOM' and inv.in_date != False and inv.out_date != False and e >= inv.in_date <= s and s <= inv.out_date >= e and inv.storage_product == False:

                                duration = (abs((fields.Datetime.to_datetime(e).date()
                                                 - fields.Datetime.to_datetime(s).date()).days) + 1)
                                # quantity_dict[uom] += inv.out_qty if inv.out_qty > 0 else inv.quantity * duration
                                if unit == 'month':
                                    quantity_dict[uom] += inv.out_qty if inv.out_qty > 0 else inv.quantity
                                else:
                                    quantity_dict[uom] += inv.out_qty if inv.out_qty > 0 else inv.quantity * duration
                                summ = ({
                                    'start_date': s,
                                    'end_date': e,
                                    'quantity': inv.out_qty if inv.out_qty > 0 else inv.quantity,
                                    'charge_type': 'storage',
                                    'product_id': inv.product_id.id,
                                    'charge_unit_type': UOM[0].id,

                                })
                                summ_lines = self.env['summary.sheet.lines'].create(summ)
                                if summ_lines.quantity > 0:
                                    summary_lines.append(summ_lines)
                            elif inv.charge_unit_type.name == 'UOM' and inv.in_date != False and inv.out_date != False and inv.out_date != False and e >= inv.in_date >= s and s <= inv.out_date <= e and inv.storage_product == False:

                                duration = (abs((fields.Datetime.to_datetime(e).date()
                                                 - fields.Datetime.to_datetime(inv.in_date).date()).days) + 1)
                                # quantity_dict[uom] += inv.out_qty if inv.out_qty > 0 else inv.quantity * duration
                                if unit == 'month':
                                    quantity_dict[uom] += inv.out_qty if inv.out_qty > 0 else inv.quantity
                                else:
                                    quantity_dict[uom] += inv.out_qty if inv.out_qty > 0 else inv.quantity * duration
                                summ = ({
                                    'start_date': inv.in_date,
                                    'end_date': e,
                                    'quantity': inv.out_qty if inv.out_qty > 0 else inv.quantity,
                                    'charge_type': 'storage',
                                    'product_id': inv.product_id.id,
                                    'charge_unit_type': UOM[0].id,

                                })
                                summ_lines = self.env['summary.sheet.lines'].create(summ)
                                if summ_lines.quantity > 0:
                                    summary_lines.append(summ_lines)
                            elif inv.charge_unit_type.name == 'UOM' and inv.in_date != False and e >= inv.in_date <= s and inv.out_date == False and inv.storage_product == False:

                                duration = (abs((fields.Datetime.to_datetime(e).date()
                                                 - fields.Datetime.to_datetime(s).date()).days) + 1)
                                # quantity_dict[uom] += inv.out_qty if inv.out_qty > 0 else inv.quantity * duration
                                if unit == 'month':
                                    quantity_dict[uom] += inv.out_qty if inv.out_qty > 0 else inv.quantity
                                else:
                                    quantity_dict[uom] += inv.out_qty if inv.out_qty > 0 else inv.quantity * duration
                                summ = ({
                                    'start_date': s,
                                    'end_date': e,
                                    'quantity': inv.out_qty if inv.out_qty > 0 else inv.quantity,
                                    'charge_type': 'storage',
                                    'product_id': inv.product_id.id,
                                    'charge_unit_type': UOM[0].id,

                                })
                                summ_lines = self.env['summary.sheet.lines'].create(summ)
                                if summ_lines.quantity > 0:
                                    summary_lines.append(summ_lines)
                            elif inv.charge_unit_type.name == 'UOM' and inv.out_date != False and inv.in_date != False and e >= inv.in_date >= s and s <= inv.out_date >= e and inv.storage_product == False:
                                duration = (abs((fields.Datetime.to_datetime(e).date()
                                                 - fields.Datetime.to_datetime(inv.in_date).date()).days) + 1)
                                if unit == 'month':
                                    quantity_dict[uom] += inv.out_qty if inv.out_qty > 0 else inv.quantity
                                else:
                                    quantity_dict[uom] += inv.out_qty if inv.out_qty > 0 else inv.quantity * duration
                                summ = ({
                                    'start_date': s,
                                    'end_date': e,
                                    'quantity': inv.out_qty if inv.out_qty > 0 else inv.quantity,
                                    'charge_type': 'storage',
                                    'product_id': inv.product_id.id,
                                    'charge_unit_type': UOM[0].id,

                                })
                                summ_lines = self.env['summary.sheet.lines'].create(summ)
                                if summ_lines.quantity > 0:
                                    summary_lines.append(summ_lines)
                    continue
                for temp in storage_charges:
                    if temp.charge_type == 'storage' and temp.charge_unit_type.name == 'UOM':
                        if uoms:
                            for q in uoms:
                                v = temp.uom_id.id
                                value = quantity_dict[v]
                                qty = value
                                temp_line_values = {
                                    'product_id': temp.product_id and temp.product_id.id or False,
                                    'name': temp.product_id.name or '',
                                    'price_unit': temp.list_price or 0.00,
                                    'quantity': qty,
                                    'currency_id': temp.currency_id.id,
                                    'tax_ids': [(6, 0, [temp.tax_id.id])] if temp.tax_id else False,
                                    'account_id': temp.product_id.property_account_income_id.id if temp.product_id.property_account_income_id
                                    else temp.product_id.categ_id.property_account_income_categ_id.id,
                                    # 'start_date': move_ids_without_package.start_date,
                                    # 'end_date': move_ids_without_package.end_date,
                                }
                                if temp_line_values['quantity'] > 0:
                                    invoice_line_list.append((0, 0, temp_line_values))
                                break
            if values_except_UOM:
                cbm = 0
                weight = 0
                sq = 0
                pallet = 0
                pallets = []
                types = []

                for values, unit in values_except_UOM.items():
                    chrg_unit_type = self.env['charge.types'].search([('name', '=', values)])
                    for inv in inven:
                        # print(s, 's', e, 'e', inv.in_date, 'in', inv.out_date, 'out', values, 'values',
                        #       inv.charge_unit_type.name, 'inv.charge_unit_type.name', inv.storage_product,
                        #       'inv.storage_product')
                        if values != 'Ppallet':
                            if values == inv.charge_unit_type.name and inv.in_date != False and inv.out_date != False and e >= inv.in_date >= s and s <= inv.out_date <= e and inv.storage_product == False:
                                print(inv.duration, 'dur 1', inv.product_id.prod_volume, inv.out_qty, inv.quantity)
                                if inv.charge_unit_type.name not in types:
                                    types.append(inv.charge_unit_type.name)
                                if unit == 'month':
                                    if values == 'CBM':
                                        cbm += inv.product_id.prod_volume * inv.out_qty if inv.out_qty > 0 else inv.product_id.prod_volume * inv.quantity
                                    if values == 'Square Units':
                                        sq += inv.product_id.prod_sqm * inv.out_qty if inv.out_qty > 0 else inv.product_id.prod_sqm * inv.quantity
                                    if values == 'Pallet':
                                        if inv.pallet_id:
                                            if inv.pallet_id.id not in pallets:
                                                pallets.append(inv.pallet_id.id)
                                        # pallet += 1
                                    if values == 'Weight':
                                        weight += inv.product_id.weight * inv.out_qty if inv.out_qty > 0 else inv.product_id.weight * inv.quantity
                                else:
                                    if values == 'CBM':
                                        cbm += inv.product_id.prod_volume * inv.out_qty * inv.duration if inv.out_qty > 0 else inv.product_id.prod_volume * inv.quantity * inv.duration
                                    if values == 'Square Units':
                                        sq += inv.product_id.prod_sqm * inv.out_qty * inv.duration if inv.out_qty > 0 else inv.product_id.prod_sqm * inv.quantity * inv.duration
                                    # if values == 'Pallet':
                                    #     pallet += 1 * inv.duration
                                    if values == 'Weight':
                                        weight += inv.product_id.weight * inv.out_qty * inv.duration if inv.out_qty > 0 else inv.product_id.weight * inv.quantity * inv.duration

                                summ = ({
                                    'start_date': inv.in_date,
                                    'end_date': inv.out_date,
                                    'quantity': inv.out_qty if inv.out_qty > 0 else inv.quantity,
                                    # 'cbm': cbm,
                                    'cbm': inv.product_id.prod_volume,
                                    'sqm': inv.product_id.prod_sqm,
                                    'pallet': 1,
                                    'weight': inv.product_id.weight,
                                    'charge_type': 'storage',
                                    'product_id': inv.product_id.id,
                                    'charge_unit_type': chrg_unit_type[0].id,

                                })
                                summ_lines = self.env['summary.sheet.lines'].create(summ)
                                # if summ_lines.quantity > 0 and values != 'Pallet' and unit != 'month':
                                #     summary_lines.append(summ_lines)
                                # if summ_lines.quantity > 0 and values == 'Pallet' and unit != 'month':
                                #     summary_lines.append(summ_lines)
                                if summ_lines.quantity > 0:
                                    summary_lines.append(summ_lines)
                            elif values == inv.charge_unit_type.name and inv.in_date != False and e >= inv.in_date >= s and inv.out_date == False and inv.storage_product == False:
                                if inv.charge_unit_type.name not in types:
                                    types.append(inv.charge_unit_type.name)
                                duration = (abs((fields.Datetime.to_datetime(e).date()
                                                 - fields.Datetime.to_datetime(inv.in_date).date()).days) + 1)
                                print(duration, 'dur 2', inv.product_id.prod_volume, inv.out_qty, inv.quantity)
                                if unit == 'month':
                                    if values == 'CBM':
                                        cbm += inv.product_id.prod_volume * inv.out_qty if inv.out_qty > 0 else inv.product_id.prod_volume * inv.quantity
                                    if values == 'Square Units':
                                        sq += inv.product_id.prod_sqm * inv.out_qty if inv.out_qty > 0 else inv.product_id.prod_sqm * inv.quantity
                                    if values == 'Pallet':
                                        if inv.pallet_id:
                                            if inv.pallet_id.id not in pallets:
                                                pallets.append(inv.pallet_id.id)
                                        # pallet += 1
                                    if values == 'Weight':
                                        weight += inv.product_id.weight * inv.out_qty if inv.out_qty > 0 else inv.product_id.weight * inv.quantity
                                else:
                                    if values == 'CBM':
                                        cbm += inv.product_id.prod_volume * inv.out_qty * duration if inv.out_qty > 0 else inv.product_id.prod_volume * inv.quantity * duration
                                    if values == 'Square Units':
                                        sq += inv.product_id.prod_sqm * inv.out_qty * duration if inv.out_qty > 0 else inv.product_id.prod_sqm * inv.quantity * duration
                                    # if values == 'Pallet':
                                    #     pallet += 1 * duration
                                    if values == 'Weight':
                                        weight += inv.product_id.weight * inv.out_qty * duration if inv.out_qty > 0 else inv.product_id.weight * inv.quantity * duration
                                summ = ({
                                    'start_date': inv.in_date,
                                    'end_date': e,
                                    'quantity': inv.out_qty if inv.out_qty > 0 else inv.quantity,
                                    'cbm': inv.product_id.prod_volume,
                                    'sqm': inv.product_id.prod_sqm,
                                    'pallet': 1,
                                    'weight': inv.product_id.weight,
                                    'charge_type': 'storage',
                                    'product_id': inv.product_id.id,
                                    'charge_unit_type': chrg_unit_type[0].id,

                                })
                                summ_lines = self.env['summary.sheet.lines'].create(summ)

                                if summ_lines.quantity > 0:
                                    summary_lines.append(summ_lines)
                            elif values == inv.charge_unit_type.name and inv.in_date != False and inv.out_date != False and e >= inv.in_date <= s and s <= inv.out_date <= e and inv.storage_product == False:
                                if inv.charge_unit_type.name not in types:
                                    types.append(inv.charge_unit_type.name)
                                duration = (abs((fields.Datetime.to_datetime(inv.out_date).date()
                                                 - fields.Datetime.to_datetime(s).date()).days) + 1)
                                print(inv.out_date, s, duration, 'dur 3', inv.product_id.prod_volume, inv.out_qty, inv.quantity)
                                if unit == 'month':
                                    if values == 'CBM':
                                        cbm += inv.product_id.prod_volume * inv.out_qty if inv.out_qty > 0 else inv.product_id.prod_volume * inv.quantity
                                    if values == 'Square Units':
                                        sq += inv.product_id.prod_sqm * inv.out_qty if inv.out_qty > 0 else inv.product_id.prod_sqm * inv.quantity
                                    if values == 'Pallet':
                                        if inv.pallet_id:
                                            if inv.pallet_id.id not in pallets:
                                                pallets.append(inv.pallet_id.id)
                                        # pallet += 1
                                    if values == 'Weight':
                                        weight += inv.product_id.weight * inv.out_qty if inv.out_qty > 0 else inv.product_id.weight * inv.quantity
                                else:
                                    if values == 'CBM':
                                        cbm += inv.product_id.prod_volume * inv.out_qty * duration if inv.out_qty > 0 else inv.product_id.prod_volume * inv.quantity * duration
                                    if values == 'Square Units':
                                        sq += inv.product_id.prod_sqm * inv.out_qty * duration if inv.out_qty > 0 else inv.product_id.prod_sqm * inv.quantity * duration
                                    # if values == 'Pallet':
                                    #     pallet += 1 * duration
                                    if values == 'Weight':
                                        weight += inv.product_id.weight * inv.out_qty * duration if inv.out_qty > 0 else inv.product_id.weight * inv.quantity * duration
                                summ = ({
                                    'start_date': s,
                                    'end_date': inv.out_date,
                                    'quantity': inv.out_qty if inv.out_qty > 0 else inv.quantity,
                                    'cbm': inv.product_id.prod_volume,
                                    'sqm': inv.product_id.prod_sqm,
                                    'pallet': 1,
                                    'weight': inv.product_id.weight,
                                    'charge_type': 'storage',
                                    'product_id': inv.product_id.id,
                                    'charge_unit_type': chrg_unit_type[0].id,

                                })
                                summ_lines = self.env['summary.sheet.lines'].create(summ)
                                # if summ_lines.quantity > 0 and values != 'Pallet' and unit != 'month':
                                #     summary_lines.append(summ_lines)
                                # if summ_lines.quantity > 0 and values == 'Pallet' and unit != 'month':
                                #     summary_lines.append(summ_lines)
                                if summ_lines.quantity > 0:
                                    summary_lines.append(summ_lines)
                            elif values == inv.charge_unit_type.name and inv.in_date != False and inv.out_date != False and e >= inv.in_date <= s and s <= inv.out_date >= e and inv.storage_product == False:
                                if inv.charge_unit_type.name not in types:
                                    types.append(inv.charge_unit_type.name)
                                duration = (abs((fields.Datetime.to_datetime(e).date()
                                                 - fields.Datetime.to_datetime(s).date()).days) + 1)
                                print(duration, 'dur 4', inv.product_id.prod_volume, inv.out_qty, inv.quantity)
                                if unit == 'month':
                                    if values == 'CBM':
                                        cbm += inv.product_id.prod_volume * inv.out_qty if inv.out_qty > 0 else inv.product_id.prod_volume * inv.quantity
                                    if values == 'Square Units':
                                        sq += inv.product_id.prod_sqm * inv.out_qty if inv.out_qty > 0 else inv.product_id.prod_sqm * inv.quantity
                                    if values == 'Pallet':
                                        if inv.pallet_id:
                                            if inv.pallet_id.id not in pallets:
                                                pallets.append(inv.pallet_id.id)
                                        # pallet += 1
                                    if values == 'Weight':
                                        weight += inv.product_id.weight * inv.out_qty if inv.out_qty > 0 else inv.product_id.weight * inv.quantity
                                else:
                                    if values == 'CBM':
                                        cbm += inv.product_id.prod_volume * inv.out_qty * duration if inv.out_qty > 0 else inv.product_id.prod_volume * inv.quantity * duration
                                    if values == 'Square Units':
                                        sq += inv.product_id.prod_sqm * inv.out_qty * duration if inv.out_qty > 0 else inv.product_id.prod_sqm * inv.quantity * duration
                                    # if values == 'Pallet':
                                    #     pallet += 1 * duration
                                    if values == 'Weight':
                                        weight += inv.product_id.weight * inv.out_qty * duration if inv.out_qty > 0 else inv.product_id.weight * inv.quantity * duration
                                summ = ({
                                    'start_date': s,
                                    'end_date': e,
                                    'quantity': inv.out_qty if inv.out_qty > 0 else inv.quantity,
                                    'cbm': inv.product_id.prod_volume,
                                    'sqm': inv.product_id.prod_sqm,
                                    'pallet': 1,
                                    'weight': inv.product_id.weight,
                                    'charge_type': 'storage',
                                    'product_id': inv.product_id.id,
                                    'charge_unit_type': chrg_unit_type[0].id,

                                })
                                summ_lines = self.env['summary.sheet.lines'].create(summ)
                                # if summ_lines.quantity > 0 and values != 'Pallet' and unit != 'month':
                                #     summary_lines.append(summ_lines)
                                # if summ_lines.quantity > 0 and values == 'Pallet' and unit != 'month':
                                #     summary_lines.append(summ_lines)
                                if summ_lines.quantity > 0:
                                    summary_lines.append(summ_lines)
                            elif values == inv.charge_unit_type.name and inv.in_date != False and inv.out_date != False and e >= inv.in_date >= s and s <= inv.out_date <= e and inv.storage_product == False:
                                if inv.charge_unit_type.name not in types:
                                    types.append(inv.charge_unit_type.name)
                                duration = (abs((fields.Datetime.to_datetime(e).date()
                                                 - fields.Datetime.to_datetime(inv.in_date).date()).days) + 1)
                                print(duration, 'dur 5', inv.product_id.prod_volume, inv.out_qty, inv.quantity)
                                if unit == 'month':
                                    if values == 'CBM':
                                        cbm += inv.product_id.prod_volume * inv.out_qty if inv.out_qty > 0 else inv.product_id.prod_volume * inv.quantity
                                    if values == 'Square Units':
                                        sq += inv.product_id.prod_sqm * inv.out_qty if inv.out_qty > 0 else inv.product_id.prod_sqm * inv.quantity
                                    if values == 'Pallet':
                                        if inv.pallet_id:
                                            if inv.pallet_id.id not in pallets:
                                                pallets.append(inv.pallet_id.id)
                                        # pallet += 1
                                    if values == 'Weight':
                                        weight += inv.product_id.weight * inv.out_qty if inv.out_qty > 0 else inv.product_id.weight * inv.quantity
                                else:
                                    if values == 'CBM':
                                        cbm += inv.product_id.prod_volume * inv.out_qty * duration if inv.out_qty > 0 else inv.product_id.prod_volume * inv.quantity * duration
                                    if values == 'Square Units':
                                        sq += inv.product_id.prod_sqm * inv.out_qty * duration if inv.out_qty > 0 else inv.product_id.prod_sqm * inv.quantity * duration
                                    # if values == 'Pallet':
                                    #     pallet += 1 * duration
                                    if values == 'Weight':
                                        weight += inv.product_id.weight * inv.out_qty * duration if inv.out_qty > 0 else inv.product_id.weight * inv.quantity * duration
                                summ = ({
                                    'start_date': inv.in_date,
                                    'end_date': e,
                                    'quantity': inv.out_qty if inv.out_qty > 0 else inv.quantity,
                                    'cbm': inv.product_id.prod_volume,
                                    'sqm': inv.product_id.prod_sqm,
                                    'pallet': 1,
                                    'weight': inv.product_id.weight,
                                    'charge_type': 'storage',
                                    'product_id': inv.product_id.id,
                                    'charge_unit_type': chrg_unit_type[0].id,

                                })
                                summ_lines = self.env['summary.sheet.lines'].create(summ)
                                # if summ_lines.quantity > 0 and values != 'Pallet' and unit != 'month':
                                #     summary_lines.append(summ_lines)
                                # if summ_lines.quantity > 0 and values == 'Pallet' and unit != 'month':
                                #     summary_lines.append(summ_lines)
                                if summ_lines.quantity > 0:
                                    summary_lines.append(summ_lines)
                            elif values == inv.charge_unit_type.name and inv.in_date != False and e >= inv.in_date <= s and inv.out_date == False and inv.storage_product == False:
                                if inv.charge_unit_type.name not in types:
                                    types.append(inv.charge_unit_type.name)
                                duration = (abs((fields.Datetime.to_datetime(e).date()
                                                 - fields.Datetime.to_datetime(s).date()).days) + 1)
                                print(duration, 'dur 6', inv.product_id.prod_volume, inv.out_qty, inv.quantity)
                                if unit == 'month':
                                    if values == 'CBM':
                                        cbm += inv.product_id.prod_volume * inv.out_qty if inv.out_qty > 0 else inv.product_id.prod_volume * inv.quantity
                                    if values == 'Square Units':
                                        sq += inv.product_id.prod_sqm * inv.out_qty if inv.out_qty > 0 else inv.product_id.prod_sqm * inv.quantity
                                    if values == 'Pallet':
                                        if inv.pallet_id:
                                            if inv.pallet_id.id not in pallets:
                                                pallets.append(inv.pallet_id.id)
                                        # pallet += 1
                                    if values == 'Weight':
                                        weight += inv.product_id.weight * inv.out_qty if inv.out_qty > 0 else inv.product_id.weight * inv.quantity
                                else:
                                    if values == 'CBM':
                                        cbm += inv.product_id.prod_volume * inv.out_qty * duration if inv.out_qty > 0 else inv.product_id.prod_volume * inv.quantity * duration
                                    if values == 'Square Units':
                                        sq += inv.product_id.prod_sqm * inv.out_qty * duration if inv.out_qty > 0 else inv.product_id.prod_sqm * inv.quantity * duration
                                    # if values == 'Pallet':
                                    #     pallet += 1 * duration
                                    if values == 'Weight':
                                        weight += inv.product_id.weight * inv.out_qty * duration if inv.out_qty > 0 else inv.product_id.weight * inv.quantity * duration
                                summ = ({
                                    'start_date': s,
                                    'end_date': e,
                                    'quantity': inv.out_qty if inv.out_qty > 0 else inv.quantity,
                                    'cbm': inv.product_id.prod_volume,
                                    'sqm': inv.product_id.prod_sqm,
                                    'pallet': 1,
                                    'weight': inv.product_id.weight,
                                    'charge_type': 'storage',
                                    'product_id': inv.product_id.id,
                                    'charge_unit_type': chrg_unit_type[0].id,

                                })
                                summ_lines = self.env['summary.sheet.lines'].create(summ)
                                # if summ_lines.quantity > 0 and values != 'Pallet' and unit != 'month':
                                #     summary_lines.append(summ_lines)
                                # if summ_lines.quantity > 0 and values == 'Pallet' and unit != 'month':
                                #     summary_lines.append(summ_lines)
                                if summ_lines.quantity > 0:
                                    summary_lines.append(summ_lines)
                            elif values == inv.charge_unit_type.name and inv.out_date != False and inv.in_date != False and e >= inv.in_date >= s and s <= inv.out_date >= e and inv.storage_product == False:
                                if inv.charge_unit_type.name not in types:
                                    types.append(inv.charge_unit_type.name)
                                duration = (abs((fields.Datetime.to_datetime(e).date()
                                                 - fields.Datetime.to_datetime(inv.in_date).date()).days) + 1)
                                print(duration, 'dur 7', inv.product_id.prod_volume, inv.out_qty, inv.quantity)
                                if unit == 'month':
                                    if values == 'CBM':
                                        cbm += inv.product_id.prod_volume * inv.out_qty if inv.out_qty > 0 else inv.product_id.prod_volume * inv.quantity
                                    if values == 'Square Units':
                                        sq += inv.product_id.prod_sqm * inv.out_qty if inv.out_qty > 0 else inv.product_id.prod_sqm * inv.quantity
                                    if values == 'Pallet':
                                        if inv.pallet_id:
                                            if inv.pallet_id.id not in pallets:
                                                pallets.append(inv.pallet_id.id)
                                        # pallet += 1
                                    if values == 'Weight':
                                        weight += inv.product_id.weight * inv.out_qty if inv.out_qty > 0 else inv.product_id.weight * inv.quantity
                                else:
                                    if values == 'CBM':
                                        cbm += inv.product_id.prod_volume * inv.out_qty * duration if inv.out_qty > 0 else inv.product_id.prod_volume * inv.quantity * duration
                                    if values == 'Square Units':
                                        sq += inv.product_id.prod_sqm * inv.out_qty * duration if inv.out_qty > 0 else inv.product_id.prod_sqm * inv.quantity * duration
                                    # if values == 'Pallet':
                                    #     pallet += 1 * duration
                                    if values == 'Weight':
                                        weight += inv.product_id.weight * inv.out_qty * duration if inv.out_qty > 0 else inv.product_id.weight * inv.quantity * duration
                                summ = ({
                                    'start_date': s,
                                    'end_date': e,
                                    'quantity': inv.out_qty if inv.out_qty > 0 else inv.quantity,
                                    'cbm': inv.product_id.prod_volume,
                                    'sqm': inv.product_id.prod_sqm,
                                    'pallet': 1,
                                    'weight': inv.product_id.weight,
                                    'charge_type': 'storage',
                                    'product_id': inv.product_id.id,
                                    'charge_unit_type': chrg_unit_type[0].id,

                                })
                                summ_lines = self.env['summary.sheet.lines'].create(summ)
                                # if summ_lines.quantity > 0 and values != 'Pallet' and unit != 'month':
                                #     summary_lines.append(summ_lines)
                                # if summ_lines.quantity > 0 and values == 'Pallet' and unit != 'month':
                                #     summary_lines.append(summ_lines)
                                if summ_lines.quantity > 0:
                                    summary_lines.append(summ_lines)

                            # break
                    print(inven, '-------------------inven------------')

                    pals = inven.filtered(lambda inv: inv.charge_unit_type.name == 'Pallet')
                    max = {}
                    for pinv in pals:
                        if values == pinv.charge_unit_type.name and pinv.in_date != False and pinv.out_date != False and e >= pinv.in_date >= s and s <= pinv.out_date <= e and pinv.storage_product == False:
                            print(pinv.duration, '-------dur 1')
                            duration = pinv.duration
                            pinv.duration_inv = duration
                            max[pinv] = {
                                'pallet_id':pinv.pallet_id.id,
                                'duration':duration}
                            # max[pinv] = {'summ': pinv,
                            #              'duration': duration,
                            #              }                                         }

                        elif values == pinv.charge_unit_type.name and pinv.in_date != False and e >= pinv.in_date >= s and pinv.out_date == False and pinv.storage_product == False:
                            if pinv.charge_unit_type.name not in types:
                                types.append(pinv.charge_unit_type.name)
                            duration = (abs((fields.Datetime.to_datetime(e).date()
                                             - fields.Datetime.to_datetime(pinv.in_date).date()).days) + 1)
                            pinv.duration_inv = duration
                            max[pinv] = {
                                'pallet_id': pinv.pallet_id.id,
                                'duration': duration}

                        elif values == pinv.charge_unit_type.name and pinv.in_date != False and pinv.out_date != False and e >= pinv.in_date <= s and s <= pinv.out_date <= e and pinv.storage_product == False:
                            if pinv.charge_unit_type.name not in types:
                                types.append(pinv.charge_unit_type.name)
                            duration = (abs((fields.Datetime.to_datetime(pinv.out_date).date()
                                             - fields.Datetime.to_datetime(s).date()).days) + 1)
                            pinv.duration_inv = duration
                            max[pinv] = {
                                'pallet_id': pinv.pallet_id.id,
                                'duration': duration}


                        elif values == pinv.charge_unit_type.name and pinv.in_date != False and pinv.out_date != False and e >= pinv.in_date <= s and s <= pinv.out_date >= e and pinv.storage_product == False:
                            if pinv.charge_unit_type.name not in types:
                                types.append(pinv.charge_unit_type.name)
                            duration = (abs((fields.Datetime.to_datetime(e).date()
                                             - fields.Datetime.to_datetime(s).date()).days) + 1)
                            pinv.duration_inv = duration
                            max[pinv] = {
                                'pallet_id': pinv.pallet_id.id,
                                'duration': duration}


                        elif values == pinv.charge_unit_type.name and pinv.in_date != False and pinv.out_date != False and e >= pinv.in_date >= s and s <= pinv.out_date <= e and pinv.storage_product == False:
                            if pinv.charge_unit_type.name not in types:
                                types.append(pinv.charge_unit_type.name)
                            duration = (abs((fields.Datetime.to_datetime(e).date()
                                             - fields.Datetime.to_datetime(pinv.in_date).date()).days) + 1)
                            pinv.duration_inv = duration
                            max[pinv] = {
                                'pallet_id': pinv.pallet_id.id,
                                'duration': duration}


                        elif pinv.out_date == False and values == pinv.charge_unit_type.name and pinv.in_date != False and e >= pinv.in_date <= s and pinv.storage_product == False:
                            if pinv.charge_unit_type.name not in types:
                                types.append(pinv.charge_unit_type.name)
                            duration = (abs((fields.Datetime.to_datetime(e).date()
                                             - fields.Datetime.to_datetime(s).date()).days) + 1)
                            pinv.duration_inv = duration
                            max[pinv] = {
                                'pallet_id': pinv.pallet_id.id,
                                'duration': duration}


                        elif pinv.out_date != False and values == pinv.charge_unit_type.name and pinv.in_date != False and pinv.out_date != False and e >= pinv.in_date >= s and s <= pinv.out_date >= e and pinv.storage_product == False:

                            if pinv.charge_unit_type.name not in types:
                                types.append(pinv.charge_unit_type.name)
                            duration = (abs((fields.Datetime.to_datetime(e).date()
                                             - fields.Datetime.to_datetime(pinv.in_date).date()).days) + 1)
                            pinv.duration_inv = duration
                            max[pinv] = {
                                'pallet_id': pinv.pallet_id.id,
                                'duration': duration}

                    print(max,'----------max')
                    MAX = max
                    data_list = [(key, value) for key, value in max.items()]

                    # Sort the list based on pallet_id
                    data_list.sort(key=lambda x: (x[1]['pallet_id'], -x[1]['duration']))

                    # Create a new dictionary to store the sorted and filtered data
                    sorted_data = {}

                    # Iterate through the sorted list and keep the summary records with the highest duration for each unique pallet_id
                    seen_pallets = set()
                    sorted_summ = []
                    for summary, info in data_list:
                        pallet_id = info['pallet_id']
                        duration = info['duration']

                        # If pallet_id is False, skip this entry
                        if pallet_id is False:
                            continue

                        # If pallet_id is not seen before or has a higher duration, add it to the new dictionary
                        if pallet_id not in seen_pallets or duration > sorted_data[pallet_id]['duration']:
                            sorted_data[pallet_id] = {'summary': summary, 'duration': duration}
                            seen_pallets.add(pallet_id)
                            sorted_summ.append(summary)

                    # Print the sorted and filtered data
                    for pallet_id, info in sorted_data.items():
                        print(f'Pallet ID: {pallet_id}, Summary: {info["summary"]}, Duration: {info["duration"]}')
                    print(sorted_summ, 'sorted_summ')
                    for inv in sorted_summ:
                        if values == inv.charge_unit_type.name and inv.in_date != False and inv.out_date != False and e >= inv.in_date >= s and s <= inv.out_date <= e and inv.storage_product == False:
                            print(inv.duration, 'dur 1')
                            duration = inv.duration
                            if inv.charge_unit_type.name not in types:
                                types.append(inv.charge_unit_type.name)
                            if unit == 'day':
                                pallet += duration
                            summ = ({
                                'start_date': inv.in_date,
                                'end_date': inv.out_date,
                                'quantity': inv.out_qty if inv.out_qty > 0 else inv.quantity,
                                'pallet': 1,
                                'charge_type': 'storage',
                                'product_id': inv.product_id.id,
                                'charge_unit_type': chrg_unit_type[0].id,

                            })
                            summ_lines = self.env['summary.sheet.lines'].create(summ)

                            if summ_lines.quantity > 0:
                                summary_lines.append(summ_lines)
                        elif values == inv.charge_unit_type.name and inv.in_date != False and e >= inv.in_date >= s and inv.out_date == False and inv.storage_product == False:
                            if inv.charge_unit_type.name not in types:
                                types.append(inv.charge_unit_type.name)
                            duration = (abs((fields.Datetime.to_datetime(e).date()
                                             - fields.Datetime.to_datetime(inv.in_date).date()).days) + 1)
                            print(duration, 'dur 2')
                            if unit == 'day':
                                pallet += duration
                            summ = ({
                                'start_date': inv.in_date,
                                'end_date': e,
                                'quantity': inv.out_qty if inv.out_qty > 0 else inv.quantity,
                                'pallet': 1,
                                'charge_type': 'storage',
                                'product_id': inv.product_id.id,
                                'charge_unit_type': chrg_unit_type[0].id,

                            })
                            summ_lines = self.env['summary.sheet.lines'].create(summ)

                            if summ_lines.quantity > 0:
                                summary_lines.append(summ_lines)
                        elif values == inv.charge_unit_type.name and inv.in_date != False and inv.out_date != False and e >= inv.in_date <= s and s <= inv.out_date <= e and inv.storage_product == False:
                            if inv.charge_unit_type.name not in types:
                                types.append(inv.charge_unit_type.name)
                            duration = (abs((fields.Datetime.to_datetime(inv.out_date).date()
                                             - fields.Datetime.to_datetime(s).date()).days) + 1)
                            print(inv.out_date, s, duration, 'dur 3')
                            if unit == 'day':
                                pallet += duration
                            summ = ({
                                'start_date': s,
                                'end_date': inv.out_date,
                                'quantity': inv.out_qty if inv.out_qty > 0 else inv.quantity,
                                'pallet': 1,
                                'charge_type': 'storage',
                                'product_id': inv.product_id.id,
                                'charge_unit_type': chrg_unit_type[0].id,

                            })
                            summ_lines = self.env['summary.sheet.lines'].create(summ)

                            if summ_lines.quantity > 0:
                                summary_lines.append(summ_lines)
                        elif values == inv.charge_unit_type.name and inv.in_date != False and inv.out_date != False and e >= inv.in_date <= s and s <= inv.out_date >= e and inv.storage_product == False:
                            if inv.charge_unit_type.name not in types:
                                types.append(inv.charge_unit_type.name)
                            duration = (abs((fields.Datetime.to_datetime(e).date()
                                             - fields.Datetime.to_datetime(s).date()).days) + 1)
                            print(duration, 'dur 4')
                            if unit == 'day':
                                pallet += duration

                            summ = ({
                                'start_date': s,
                                'end_date': e,
                                'quantity': inv.out_qty if inv.out_qty > 0 else inv.quantity,
                                'pallet': 1,
                                'charge_type': 'storage',
                                'product_id': inv.product_id.id,
                                'charge_unit_type': chrg_unit_type[0].id,

                            })
                            summ_lines = self.env['summary.sheet.lines'].create(summ)

                            if summ_lines.quantity > 0:
                                summary_lines.append(summ_lines)
                        elif values == inv.charge_unit_type.name and inv.in_date != False and inv.out_date != False and e >= inv.in_date >= s and s <= inv.out_date <= e and inv.storage_product == False:
                            if inv.charge_unit_type.name not in types:
                                types.append(inv.charge_unit_type.name)
                            duration = (abs((fields.Datetime.to_datetime(e).date()
                                             - fields.Datetime.to_datetime(inv.in_date).date()).days) + 1)
                            print(duration, 'dur 5')
                            if unit == 'day':
                                pallet += duration

                            summ = ({
                                'start_date': inv.in_date,
                                'end_date': e,
                                'quantity': inv.out_qty if inv.out_qty > 0 else inv.quantity,
                                'pallet': 1,
                                'charge_type': 'storage',
                                'product_id': inv.product_id.id,
                                'charge_unit_type': chrg_unit_type[0].id,

                            })
                            summ_lines = self.env['summary.sheet.lines'].create(summ)

                            if summ_lines.quantity > 0:
                                summary_lines.append(summ_lines)
                        elif values == inv.charge_unit_type.name and inv.in_date != False and e >= inv.in_date <= s and inv.out_date == False and inv.storage_product == False:
                            if inv.charge_unit_type.name not in types:
                                types.append(inv.charge_unit_type.name)
                            duration = (abs((fields.Datetime.to_datetime(e).date()
                                             - fields.Datetime.to_datetime(s).date()).days) + 1)
                            print(duration, 'dur 6')
                            if unit == 'day':
                                pallet += duration

                            summ = ({
                                'start_date': s,
                                'end_date': e,
                                'quantity': inv.out_qty if inv.out_qty > 0 else inv.quantity,
                                'pallet': 1,
                                'charge_type': 'storage',
                                'product_id': inv.product_id.id,
                                'charge_unit_type': chrg_unit_type[0].id,

                            })
                            summ_lines = self.env['summary.sheet.lines'].create(summ)

                            if summ_lines.quantity > 0:
                                summary_lines.append(summ_lines)
                        elif values == inv.charge_unit_type.name and inv.out_date != False and inv.in_date != False and e >= inv.in_date >= s and s <= inv.out_date >= e and inv.storage_product == False:
                            if inv.charge_unit_type.name not in types:
                                types.append(inv.charge_unit_type.name)
                            duration = (abs((fields.Datetime.to_datetime(e).date()
                                             - fields.Datetime.to_datetime(inv.in_date).date()).days) + 1)
                            print(duration, 'dur 7')
                            if unit == 'day':
                                pallet += duration

                            summ = ({
                                'start_date': s,
                                'end_date': e,
                                'quantity': inv.out_qty if inv.out_qty > 0 else inv.quantity,
                                'pallet': 1,
                                'charge_type': 'storage',
                                'product_id': inv.product_id.id,
                                'charge_unit_type': chrg_unit_type[0].id,

                            })
                            summ_lines = self.env['summary.sheet.lines'].create(summ)

                            if summ_lines.quantity > 0:
                                summary_lines.append(summ_lines)

                # print(pallet)
                if pallets:
                    pallet_count = len(pallets)
                    chrg_unit_type = self.env['charge.types'].search([('name', '=', 'Pallet')])
                    summ = ({

                        'pallet': pallet_count,
                        # 'weight': inv.product_id.weight,
                        'charge_type': 'storage',
                        # 'product_id': inv.product_id.id,
                        'charge_unit_type': chrg_unit_type[0].id,

                    })
                    summ_lines = self.env['summary.sheet.lines'].create(summ)
                    summary_lines.append(summ_lines)

                else:
                    pallet_count = 0
                print(pallet_count, '---pallet_count--------')
                print(types, '======sto==false====')
                if types:
                    for type in types:
                        print(type, '------------------------------------hb------------type1')
                        for temp in storage_charges:
                            if temp.charge_type == 'storage' and temp.charge_unit_type.name == 'CBM' and temp.charge_unit_type.name == type:
                                temp_line_values = {
                                    'product_id': temp.product_id and temp.product_id.id or False,
                                    'name': temp.product_id.name or '',
                                    'price_unit': temp.list_price or 0.00,
                                    'quantity': cbm,
                                    'currency_id': temp.currency_id.id,
                                    'tax_ids': [(6, 0, [temp.tax_id.id])] if temp.tax_id else False,
                                    'account_id': temp.product_id.property_account_income_id.id if temp.product_id.property_account_income_id
                                    else temp.product_id.categ_id.property_account_income_categ_id.id,
                                    # 'start_date': move_ids_without_package.start_date,
                                    # 'end_date': move_ids_without_package.end_date,

                                }
                                if temp_line_values['quantity'] > 0:
                                    invoice_line_list.append((0, 0, temp_line_values))

                            if temp.charge_type == 'storage' and temp.charge_unit_type.name == 'Weight' and temp.charge_unit_type.name == type:
                                temp_line_values = {
                                    'product_id': temp.product_id and temp.product_id.id or False,
                                    'name': temp.product_id.name or '',
                                    'price_unit': temp.list_price or 0.00,
                                    'quantity': weight,
                                    'currency_id': temp.currency_id.id,
                                    'tax_ids': [(6, 0, [temp.tax_id.id])] if temp.tax_id else False,
                                    'account_id': temp.product_id.property_account_income_id.id if temp.product_id.property_account_income_id
                                    else temp.product_id.categ_id.property_account_income_categ_id.id,
                                    # 'start_date': move_ids_without_package.start_date,
                                    # 'end_date': move_ids_without_package.end_date,

                                }
                                if temp_line_values['quantity'] > 0:
                                    invoice_line_list.append((0, 0, temp_line_values))

                            if temp.charge_type == 'storage' and temp.charge_unit_type.name == 'Square Units' and temp.charge_unit_type.name == type:
                                temp_line_values = {
                                    'product_id': temp.product_id and temp.product_id.id or False,
                                    'name': temp.product_id.name or '',
                                    'price_unit': temp.list_price or 0.00,
                                    'quantity': sq,
                                    'currency_id': temp.currency_id.id,
                                    'tax_ids': [(6, 0, [temp.tax_id.id])] if temp.tax_id else False,
                                    'account_id': temp.product_id.property_account_income_id.id if temp.product_id.property_account_income_id
                                    else temp.product_id.categ_id.property_account_income_categ_id.id,
                                    # 'start_date': move_ids_without_package.start_date,
                                    # 'end_date': move_ids_without_package.end_date,

                                }
                                if temp_line_values['quantity'] > 0:
                                    invoice_line_list.append((0, 0, temp_line_values))

                            if temp.charge_type == 'storage' and temp.charge_unit_type.name == 'Pallet' and temp.charge_unit_type.name == type:
                                temp_line_values = {
                                    'product_id': temp.product_id and temp.product_id.id or False,
                                    'name': temp.product_id.name or '',
                                    'price_unit': temp.list_price or 0.00,
                                    'quantity': pallet if pallet > 0 else pallet_count,
                                    'currency_id': temp.currency_id.id,
                                    'tax_ids': [(6, 0, [temp.tax_id.id])] if temp.tax_id else False,
                                    'account_id': temp.product_id.property_account_income_id.id if temp.product_id.property_account_income_id
                                    else temp.product_id.categ_id.property_account_income_categ_id.id,
                                    # 'start_date': move_ids_without_package.start_date,
                                    # 'end_date': move_ids_without_package.end_date,

                                }
                                if temp_line_values['quantity'] > 0:
                                    invoice_line_list.append((0, 0, temp_line_values))
            if other_values:

                for values, unit in other_values.items():
                    cbm = 0
                    weight = 0
                    sq = 0
                    pallet = 0
                    quo = 0

                    chrg_unit_type = self.env['charge.types'].search([('name', '=', values)])
                    for inv in inven:

                        if values == inv.charge_unit_type.name and inv.in_date != False and inv.out_date != False and e >= inv.in_date >= s and s <= inv.out_date <= e and inv.storage_product == False:
                            if unit == 'month':
                                cbm += inv.product_id.prod_volume * inv.out_qty if inv.out_qty > 0 else inv.quantity
                                sq += inv.product_id.prod_sqm * inv.out_qty if inv.out_qty > 0 else inv.quantity
                                pallet += 1
                                weight += inv.product_id.weight * inv.out_qty if inv.out_qty > 0 else inv.quantity
                                quo += 1
                            else:
                                cbm += inv.product_id.prod_volume * inv.out_qty if inv.out_qty > 0 else inv.quantity * inv.duration
                                sq += inv.product_id.prod_sqm * inv.out_qty if inv.out_qty > 0 else inv.quantity * inv.duration
                                pallet += 1
                                weight += inv.product_id.weight * inv.out_qty if inv.out_qty > 0 else inv.quantity * inv.duration
                                quo += 1 * inv.duration

                            summ = ({
                                'start_date': inv.in_date,
                                'end_date': inv.out_date,
                                'quantity': inv.out_qty if inv.out_qty > 0 else inv.quantity,

                                'other': 1,

                                'charge_type': 'storage',
                                'product_id': inv.product_id.id,
                                'charge_unit_type': chrg_unit_type[0].id,

                            })
                            summ_lines = self.env['summary.sheet.lines'].create(summ)
                            if summ_lines.quantity > 0:
                                summary_lines.append(summ_lines)

                        elif values == inv.charge_unit_type.name and inv.in_date != False and e >= inv.in_date >= s and inv.out_date == False and inv.storage_product == False:

                            duration = (abs((fields.Datetime.to_datetime(e).date()
                                             - fields.Datetime.to_datetime(inv.in_date).date()).days) + 1)
                            if unit == 'month':
                                cbm += inv.product_id.prod_volume * inv.out_qty if inv.out_qty > 0 else inv.quantity
                                sq += inv.product_id.prod_sqm * inv.out_qty if inv.out_qty > 0 else inv.quantity
                                pallet += 1
                                weight += inv.product_id.weight * inv.out_qty if inv.out_qty > 0 else inv.quantity
                                quo += 1
                            else:
                                cbm += inv.product_id.prod_volume * inv.out_qty if inv.out_qty > 0 else inv.quantity * duration
                                sq += inv.product_id.prod_sqm * inv.out_qty if inv.out_qty > 0 else inv.quantity * duration
                                pallet += 1
                                weight += inv.product_id.weight * inv.out_qty if inv.out_qty > 0 else inv.quantity * duration
                                quo += 1 * duration
                            summ = ({
                                'start_date': inv.in_date,
                                'end_date': e,
                                'quantity': inv.out_qty if inv.out_qty > 0 else inv.quantity,
                                'other': 1,
                                'charge_type': 'storage',
                                'product_id': inv.product_id.id,
                                'charge_unit_type': chrg_unit_type[0].id,

                            })
                            summ_lines = self.env['summary.sheet.lines'].create(summ)
                            if summ_lines.quantity > 0:
                                summary_lines.append(summ_lines)
                        elif values == inv.charge_unit_type.name and inv.in_date != False and inv.out_date != False and e >= inv.in_date <= s and s <= inv.out_date <= e and inv.storage_product == False:

                            duration = (abs((fields.Datetime.to_datetime(inv.out_date).date()
                                             - fields.Datetime.to_datetime(s).date()).days) + 1)
                            if unit == 'month':
                                cbm += inv.product_id.prod_volume * inv.out_qty if inv.out_qty > 0 else inv.quantity
                                sq += inv.product_id.prod_sqm * inv.out_qty if inv.out_qty > 0 else inv.quantity
                                pallet += 1
                                weight += inv.product_id.weight * inv.out_qty if inv.out_qty > 0 else inv.quantity
                                quo += 1
                            else:
                                cbm += inv.product_id.prod_volume * inv.out_qty if inv.out_qty > 0 else inv.quantity * duration
                                sq += inv.product_id.prod_sqm * inv.out_qty if inv.out_qty > 0 else inv.quantity * duration
                                pallet += 1
                                weight += inv.product_id.weight * inv.out_qty if inv.out_qty > 0 else inv.quantity * duration
                                quo += 1 * duration
                            summ = ({
                                'start_date': s,
                                'end_date': inv.out_date,
                                'quantity': inv.out_qty if inv.out_qty > 0 else inv.quantity,
                                'other': 1,
                                'charge_type': 'storage',
                                'product_id': inv.product_id.id,
                                'charge_unit_type': chrg_unit_type[0].id,

                            })
                            summ_lines = self.env['summary.sheet.lines'].create(summ)
                            if summ_lines.quantity > 0:
                                summary_lines.append(summ_lines)
                        elif values == inv.charge_unit_type.name and inv.in_date != False and inv.out_date != False and e >= inv.in_date <= s and s <= inv.out_date >= e and inv.storage_product == False:

                            duration = (abs((fields.Datetime.to_datetime(e).date()
                                             - fields.Datetime.to_datetime(s).date()).days) + 1)
                            if unit == 'month':
                                cbm += inv.product_id.prod_volume * inv.out_qty if inv.out_qty > 0 else inv.quantity
                                sq += inv.product_id.prod_sqm * inv.out_qty if inv.out_qty > 0 else inv.quantity
                                pallet += 1
                                weight += inv.product_id.weight * inv.out_qty if inv.out_qty > 0 else inv.quantity
                                quo += 1
                            else:
                                cbm += inv.product_id.prod_volume * inv.out_qty if inv.out_qty > 0 else inv.quantity * duration
                                sq += inv.product_id.prod_sqm * inv.out_qty if inv.out_qty > 0 else inv.quantity * duration
                                pallet += 1
                                weight += inv.product_id.weight * inv.out_qty if inv.out_qty > 0 else inv.quantity * duration
                                quo += 1 * duration
                            summ = ({
                                'start_date': s,
                                'end_date': e,
                                'quantity': inv.out_qty if inv.out_qty > 0 else inv.quantity,
                                'other': 1,
                                'charge_type': 'storage',
                                'product_id': inv.product_id.id,
                                'charge_unit_type': chrg_unit_type[0].id,

                            })
                            summ_lines = self.env['summary.sheet.lines'].create(summ)
                            if summ_lines.quantity > 0:
                                summary_lines.append(summ_lines)
                        elif values == inv.charge_unit_type.name and inv.in_date != False and inv.out_date != False and e >= inv.in_date >= s and s <= inv.out_date <= e and inv.storage_product == False:

                            duration = (abs((fields.Datetime.to_datetime(e).date()
                                             - fields.Datetime.to_datetime(inv.in_date).date()).days) + 1)
                            if unit == 'month':
                                cbm += inv.product_id.prod_volume
                                sq += inv.product_id.prod_sqm
                                pallet += 1
                                weight += inv.product_id.weight
                                quo += 1
                            else:
                                cbm += inv.product_id.prod_volume * inv.out_qty if inv.out_qty > 0 else inv.quantity * duration
                                sq += inv.product_id.prod_sqm * inv.out_qty if inv.out_qty > 0 else inv.quantity * duration
                                pallet += 1
                                weight += inv.product_id.weight * inv.out_qty if inv.out_qty > 0 else inv.quantity * duration
                                quo += 1 * duration
                            summ = ({
                                'start_date': inv.in_date,
                                'end_date': e,
                                'quantity': inv.out_qty if inv.out_qty > 0 else inv.quantity,
                                'other': 1,
                                'charge_type': 'storage',
                                'product_id': inv.product_id.id,
                                'charge_unit_type': chrg_unit_type[0].id,

                            })
                            summ_lines = self.env['summary.sheet.lines'].create(summ)
                            if summ_lines.quantity > 0:
                                summary_lines.append(summ_lines)
                        elif values == inv.charge_unit_type.name and inv.in_date != False and e >= inv.in_date <= s and inv.out_date == False and inv.storage_product == False:

                            duration = (abs((fields.Datetime.to_datetime(e).date()
                                             - fields.Datetime.to_datetime(s).date()).days) + 1)
                            if unit == 'month':
                                cbm += inv.product_id.prod_volume * inv.out_qty if inv.out_qty > 0 else inv.quantity
                                sq += inv.product_id.prod_sqm * inv.out_qty if inv.out_qty > 0 else inv.quantity
                                pallet += 1
                                weight += inv.product_id.weight * inv.out_qty if inv.out_qty > 0 else inv.quantity
                                quo += 1
                            else:
                                cbm += inv.product_id.prod_volume * inv.out_qty if inv.out_qty > 0 else inv.quantity * duration
                                sq += inv.product_id.prod_sqm * inv.out_qty if inv.out_qty > 0 else inv.quantity * duration
                                pallet += 1
                                weight += inv.product_id.weight * inv.out_qty if inv.out_qty > 0 else inv.quantity * duration
                                quo += 1 * duration
                            summ = ({
                                'start_date': s,
                                'end_date': e,
                                'quantity': inv.out_qty if inv.out_qty > 0 else inv.quantity,
                                'other': 1,
                                'charge_type': 'storage',
                                'product_id': inv.product_id.id,
                                'charge_unit_type': chrg_unit_type[0].id,

                            })
                            summ_lines = self.env['summary.sheet.lines'].create(summ)
                            if summ_lines.quantity > 0:
                                summary_lines.append(summ_lines)
                        elif values == inv.charge_unit_type.name and inv.out_date != False and inv.in_date != False and e >= inv.in_date <= s and inv.out_date == False and inv.storage_product == False:

                            duration = (abs((fields.Datetime.to_datetime(e).date()
                                             - fields.Datetime.to_datetime(s).date()).days) + 1)
                            if unit == 'month':
                                cbm += inv.product_id.prod_volume * inv.out_qty if inv.out_qty > 0 else inv.quantity
                                sq += inv.product_id.prod_sqm * inv.out_qty if inv.out_qty > 0 else inv.quantity
                                pallet += 1
                                weight += inv.product_id.weight * inv.out_qty if inv.out_qty > 0 else inv.quantity
                                quo += 1
                            else:
                                cbm += inv.product_id.prod_volume * inv.out_qty if inv.out_qty > 0 else inv.quantity * duration
                                sq += inv.product_id.prod_sqm * inv.out_qty if inv.out_qty > 0 else inv.quantity * duration
                                pallet += 1
                                weight += inv.product_id.weight * inv.out_qty if inv.out_qty > 0 else inv.quantity * duration
                                quo += 1 * duration
                            summ = ({
                                'start_date': s,
                                'end_date': e,
                                'quantity': inv.out_qty if inv.out_qty > 0 else inv.quantity,
                                'other': 1,
                                'charge_type': 'storage',
                                'product_id': inv.product_id.id,
                                'charge_unit_type': chrg_unit_type[0].id,

                            })
                            summ_lines = self.env['summary.sheet.lines'].create(summ)
                            if summ_lines.quantity > 0:
                                summary_lines.append(summ_lines)

                        # break
                    for temp in storage_charges.filtered(
                            lambda inv: inv.charge_unit_type.name == values and inv.agreement_id == agreement_id):
                        # print(temp,'--------------------temp---------------')
                        if temp.charge_type == 'storage' and temp.charge_unit_type.name == values and not temp.storage_type:
                            print(temp.agreement_id, agreement_id, quo)
                            temp_line_values = {
                                'product_id': temp.product_id and temp.product_id.id or False,
                                'name': temp.product_id.name or '',
                                'price_unit': temp.list_price or 0.00,
                                'quantity': quo,
                                'currency_id': temp.currency_id.id,
                                'tax_ids': [(6, 0, [temp.tax_id.id])] if temp.tax_id else False,
                                'account_id': temp.product_id.property_account_income_id.id if temp.product_id.property_account_income_id
                                else temp.product_id.categ_id.property_account_income_categ_id.id,
                                # 'start_date': move_ids_without_package.start_date,
                                # 'end_date': move_ids_without_package.end_date,

                            }
                            if temp_line_values['quantity'] > 0:
                                invoice_line_list.append((0, 0, temp_line_values))
                        break

            current_user = self.env.uid
            if agreement_id and invoice_line_list:
                invoice = partner.env['account.move'].create({
                    'type': 'out_invoice',
                    'sto_type': 'warehouse',
                    'start_date_sto': s,
                    'end_date_sto': e,
                    'invoice_origin': partner.name,
                    'invoice_user_id': current_user,
                    'narration': partner.name,
                    'partner_id': partner.id,
                    'currency_id': partner.env.user.company_id.currency_id.id,
                    # 'journal_id': int(UOMer_journal_id),
                    'invoice_payment_ref': partner.name,
                    # 'picking_id': picking_id.id,
                    'invoice_line_ids': invoice_line_list,
                    # 'invoice_type': 'storage',
                    'name': '/',

                })
                invoices.append(invoice.id)
                if invoice:
                    invoice._summary_sheet()

                # invoice.consolidate_invoice_lines(invoice)

                summary = ({
                    'name': str(s) + '-' + str(e),
                    'partner_id': partner.id,
                    'invoice_id': invoice.id
                })
                summary = self.env['summary.sheet'].create(summary)

                for lines in summary_lines:
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
            tstorage_charges = partner.env['agreement.charges'].search(
                ['&', ('charge_type', '=', 'storage'), ('agreement_id', '=', agreement_id.id),
                 ('storage_type', '!=', False)])
            tuoms = {}
            tquantity_dict = {}
            sto_type = []
            for styp in tstorage_charges:
                if styp.storage_type and styp.storage_type.name not in sto_type:
                    sto_type.append(styp.storage_type.name)
            tinvoice_line_list = []
            for sty in sto_type:

                for u in tstorage_charges:
                    if u.uom_id:
                        uom = u['uom_id']['id']
                        unit = u['storage_uom']
                        tuoms[uom] = unit
                tcharge_unit_types = {}
                for c in tstorage_charges:
                    chrg = c['charge_unit_type']['name']
                    sto = c['storage_uom']
                    tcharge_unit_types[chrg] = sto
                # tvalues_except_UOM = list(filter(lambda x: x != 'UOM', tcharge_unit_types))
                tvalues_except_UOM = {chrg: sto for chrg, sto in tcharge_unit_types.items() if chrg != 'UOM'
                                      and chrg in ['CBM', 'Pallet', 'Square Units', 'Weight', 'UOM']}

                tother_values = {chrg: sto for chrg, sto in tcharge_unit_types.items() if chrg not in
                                 ['CBM', 'Pallet', 'Square Units', 'Weight', 'UOM']}
                tinven = self.env['product.summary'].search(
                    [('partner_id', '=', partner.id), ('storage_product', '=', True),
                     ('product_id.storage_type.name', '=', sty), ('gen_seperate_inv','=',False)])
                # print(tvalues_except_UOM, tother_values)

                if tuoms:
                    for uom, unit in tuoms.items():
                        tquantity_dict[uom] = 0
                        for tinv in tinven:
                            UOM = self.env['charge.types'].search([('name', '=', 'UOM')])

                            if uom == tinv.uom_id.id:
                                # print(tinv.product_id.storage_type.name, sty,'----------------------')
                                if tinv.product_id.storage_type.name == sty and tinv.charge_unit_type.name == 'UOM' and tinv.in_date != False and tinv.out_date != False and e >= tinv.in_date >= s and s <= tinv.out_date <= e and tinv.storage_product == True:
                                    if unit == 'month':
                                        tquantity_dict[uom] += tinv.out_qty if tinv.out_qty > 0 else tinv.quantity
                                    else:
                                        tquantity_dict[
                                            uom] += tinv.out_qty if tinv.out_qty > 0 else tinv.quantity * tinv.duration
                                    # tquantity_dict[uom] += tinv.out_qty if tinv.out_qty > 0 else tinv.quantity * tinv.duration

                                    summ = ({
                                        'start_date': tinv.in_date,
                                        'end_date': tinv.out_date,
                                        'quantity': tinv.out_qty if tinv.out_qty > 0 else tinv.quantity,
                                        'cbm': tinv.product_id.prod_volume,
                                        'sqm': tinv.product_id.prod_sqm,
                                        'pallet': 0,
                                        'weight': tinv.product_id.weight,
                                        'charge_type': 'storage',
                                        'product_id': tinv.product_id.id,
                                        'charge_unit_type': UOM[0].id,
                                    })
                                    summ_lines = self.env['summary.sheet.lines'].create(summ)
                                    if summ_lines.quantity > 0:
                                        tsummary_lines.append(summ_lines)
                                elif tinv.product_id.storage_type.name == sty and tinv.charge_unit_type.name == 'UOM' and tinv.in_date != False and e >= tinv.in_date >= s and tinv.out_date == False and tinv.storage_product == True:
                                    duration = (abs((fields.Datetime.to_datetime(e).date()
                                                     - fields.Datetime.to_datetime(tinv.in_date).date()).days) + 1)
                                    if unit == 'month':
                                        tquantity_dict[uom] += tinv.out_qty if tinv.out_qty > 0 else tinv.quantity
                                    else:
                                        tquantity_dict[
                                            uom] += tinv.out_qty if tinv.out_qty > 0 else tinv.quantity * duration

                                    summ = ({
                                        'start_date': tinv.in_date,
                                        'end_date': e,
                                        'quantity': tinv.out_qty if tinv.out_qty > 0 else tinv.quantity,
                                        'cbm': tinv.product_id.prod_volume,
                                        'sqm': tinv.product_id.prod_sqm,
                                        'pallet': 0,
                                        'weight': tinv.product_id.weight,
                                        'charge_type': 'storage',
                                        'product_id': tinv.product_id.id,
                                        'charge_unit_type': UOM[0].id,

                                    })
                                    summ_lines = self.env['summary.sheet.lines'].create(summ)
                                    if summ_lines.quantity > 0:
                                        tsummary_lines.append(summ_lines)
                                # elif tinv.in_date != False and e >= tinv.in_date >= s and s <= tinv.out_date <= e and tinv.storage_product == True:
                                #     duration = abs((fields.Datetime.to_datetime(tinv.out_date).date()
                                #                     - fields.Datetime.to_datetime(s).date()).days)
                                #     # tcbm += tinv.product_id.x_vol * tinv.out_qty if tinv.out_qty > 0 else tinv.quantity * tinv.duration
                                #     # tsq += tinv.product_id.x_vol * tinv.out_qty if tinv.out_qty > 0 else tinv.quantity * tinv.duration
                                #     tcbm += tinv.product_id.prod_volume * tinv.out_qty if tinv.out_qty > 0 else tinv.quantity * duration
                                #     tsq += tinv.product_id.prod_sqm * tinv.out_qty if tinv.out_qty > 0 else tinv.quantity * duration
                                #     tpallet += 1
                                #     tweight += tinv.product_id.weight * tinv.out_qty if tinv.out_qty > 0 else tinv.quantity * duration
                                #     summ = ({
                                #         'start_date': s,
                                #         'end_date': tinv.out_date,
                                #         'quantity': tinv.out_qty if tinv.out_qty > 0 else tinv.quantity,
                                #         'cbm': cbm,
                                #         'sqm': sq,
                                #         'pallet': pallet,
                                #         'weight': weight,
                                #     })
                                #     summ_lines = self.env['summary.sheet.lines'].create(summ)
                                #     summary_lines.append(summ_lines)
                                elif tinv.product_id.storage_type.name == sty and tinv.charge_unit_type.name == 'UOM' and tinv.in_date != False and tinv.out_date != False and e >= tinv.in_date <= s and s <= tinv.out_date <= e and tinv.storage_product == True:
                                    duration = (abs((fields.Datetime.to_datetime(e).date()
                                                     - fields.Datetime.to_datetime(tinv.in_date).date()).days) + 1)
                                    if unit == 'month':
                                        tquantity_dict[uom] += tinv.out_qty if tinv.out_qty > 0 else tinv.quantity
                                    else:
                                        tquantity_dict[
                                            uom] += tinv.out_qty if tinv.out_qty > 0 else tinv.quantity * duration
                                    # tquantity_dict[uom] += tinv.out_qty if tinv.out_qty > 0 else tinv.quantity * duration

                                    summ = ({
                                        'start_date': tinv.in_date,
                                        'end_date': tinv.out_date,
                                        'quantity': tinv.out_qty if tinv.out_qty > 0 else tinv.quantity,
                                        'cbm': tinv.product_id.prod_volume,
                                        'sqm': tinv.product_id.prod_sqm,
                                        'pallet': 0,
                                        'weight': tinv.product_id.weight,
                                        'charge_type': 'storage',
                                        'product_id': tinv.product_id.id,
                                        'charge_unit_type': UOM[0].id,

                                    })
                                    summ_lines = self.env['summary.sheet.lines'].create(summ)
                                    if summ_lines.quantity > 0:
                                        tsummary_lines.append(summ_lines)
                                elif tinv.product_id.storage_type.name == sty and tinv.charge_unit_type.name == 'UOM' and tinv.in_date != False and tinv.out_date != False and e >= tinv.in_date <= s and s <= tinv.out_date >= e and tinv.storage_product == True:
                                    duration = (abs((fields.Datetime.to_datetime(e).date()
                                                     - fields.Datetime.to_datetime(s).date()).days) + 1)
                                    if unit == 'month':
                                        tquantity_dict[uom] += tinv.out_qty if tinv.out_qty > 0 else tinv.quantity
                                    else:
                                        tquantity_dict[
                                            uom] += tinv.out_qty if tinv.out_qty > 0 else tinv.quantity * duration

                                    # tquantity_dict[uom] += tinv.out_qty if tinv.out_qty > 0 else tinv.quantity * tinv.duration

                                    summ = ({
                                        'start_date': s,
                                        'end_date': e,
                                        'quantity': tinv.out_qty if tinv.out_qty > 0 else tinv.quantity,
                                        'cbm': tinv.product_id.prod_volume,
                                        'sqm': tinv.product_id.prod_sqm,
                                        'pallet': 0,
                                        'weight': tinv.product_id.weight,
                                        'charge_type': 'storage',
                                        'product_id': tinv.product_id.id,
                                        'charge_unit_type': UOM[0].id,

                                    })
                                    summ_lines = self.env['summary.sheet.lines'].create(summ)
                                    if summ_lines.quantity > 0:
                                        tsummary_lines.append(summ_lines)
                                elif tinv.product_id.storage_type.name == sty and tinv.charge_unit_type.name == 'UOM' and tinv.in_date != False and e >= tinv.in_date <= s and tinv.out_date == False and tinv.storage_product == True:
                                    duration = (abs((fields.Datetime.to_datetime(e).date()
                                                     - fields.Datetime.to_datetime(s).date()).days) + 1)
                                    if unit == 'month':
                                        tquantity_dict[uom] += tinv.out_qty if tinv.out_qty > 0 else tinv.quantity
                                    else:
                                        tquantity_dict[
                                            uom] += tinv.out_qty if tinv.out_qty > 0 else tinv.quantity * duration
                                    # tquantity_dict[uom] += tinv.out_qty if tinv.out_qty > 0 else tinv.quantity * tinv.duration

                                    summ = ({
                                        'start_date': s,
                                        'end_date': e,
                                        'quantity': tinv.out_qty if tinv.out_qty > 0 else tinv.quantity,
                                        'cbm': tinv.product_id.prod_volume,
                                        'sqm': tinv.product_id.prod_sqm,
                                        'pallet': 0,
                                        'weight': tinv.product_id.weight,
                                        'charge_type': 'storage',
                                        'product_id': tinv.product_id.id,
                                        'charge_unit_type': UOM[0].id,

                                    })

                                    summ_lines = self.env['summary.sheet.lines'].create(summ)
                                    if summ_lines.quantity > 0:
                                        tsummary_lines.append(summ_lines)
                                elif tinv.product_id.storage_type.name == sty and tinv.charge_unit_type.name == 'UOM' and tinv.out_date != False and tinv.in_date != False and e >= tinv.in_date >= s and s <= tinv.out_date >= e and tinv.storage_product == True:
                                    duration = (abs((fields.Datetime.to_datetime(e).date()
                                                     - fields.Datetime.to_datetime(tinv.in_date).date()).days) + 1)
                                    if unit == 'month':
                                        tquantity_dict[uom] += tinv.out_qty if tinv.out_qty > 0 else tinv.quantity
                                    else:
                                        tquantity_dict[
                                            uom] += tinv.out_qty if tinv.out_qty > 0 else tinv.quantity * duration
                                    summ = ({
                                        'start_date': s,
                                        'end_date': e,
                                        'quantity': tinv.out_qty if tinv.out_qty > 0 else tinv.quantity,
                                        'charge_type': 'storage',
                                        'product_id': tinv.product_id.id,
                                        'charge_unit_type': UOM[0].id,

                                    })
                                    summ_lines = self.env['summary.sheet.lines'].create(summ)
                                    if summ_lines.quantity > 0:
                                        summary_lines.append(summ_lines)

                    for temp in tstorage_charges.filtered(lambda inv: inv.charge_unit_type.name == 'UOM'):
                        # print(temp.storage_type.name, sty, '----------', temp.charge_unit_type.name , 'UOM', temp.charge_type, 'storage')
                        if temp.charge_type == 'storage' and temp.charge_unit_type.name == 'UOM' and temp.storage_type.name == sty:
                            # print('----------1')
                            if tuoms:
                                # print('----------2')

                                for q in tuoms:
                                    # print('----------3')
                                    v = temp.uom_id.id
                                    value = tquantity_dict[v]
                                    qty = value
                                    # print(qty, 'qty ', '----------3')
                                    temp_line_values = {
                                        'product_id': temp.product_id and temp.product_id.id or False,
                                        'name': temp.product_id.name or '',
                                        'price_unit': temp.list_price or 0.00,
                                        'quantity': qty,
                                        'currency_id': temp.currency_id.id,
                                        'tax_ids': [(6, 0, [temp.tax_id.id])] if temp.tax_id else False,
                                        'account_id': temp.product_id.property_account_income_id.id if temp.product_id.property_account_income_id
                                        else temp.product_id.categ_id.property_account_income_categ_id.id,
                                        # 'start_date': move_ids_without_package.start_date,
                                        # 'end_date': move_ids_without_package.end_date,
                                    }
                                    if temp_line_values['quantity'] > 0:
                                        print('ok')
                                        tinvoice_line_list.append((0, 0, temp_line_values))
                                        # print(tinvoice_line_list, 'tinvoice_line_list')
                if tvalues_except_UOM:
                    tcbm = 0
                    tweight = 0
                    tsq = 0
                    tpallet = 0
                    tpallets = []
                    types = []
                    for values, unit in tvalues_except_UOM.items():
                        tchrg_unit_type = self.env['charge.types'].search([('name', '=', values)])
                        for tinv in tinven:
                            # print(s, 's', e, 'e', tinv.in_date, 'in', tinv.out_date, 'out', values, 'values',
                            #       tinv.charge_unit_type.name, 'tinv.charge_unit_type.name', tinv.storage_product,
                            #       'tinv.storage_product')
                            if values != 'Ppallet':

                                if tinv.product_id.storage_type.name == sty and values == tinv.charge_unit_type.name and tinv.in_date != False and tinv.out_date != False and e >= tinv.in_date >= s and s <= tinv.out_date <= e and tinv.storage_product == True:
                                    print(tinv.duration, 'tdur1')
                                    if tinv.charge_unit_type.name not in types:
                                        types.append(tinv.charge_unit_type.name)
                                    if unit == 'month':
                                        if values == 'CBM':
                                            tcbm += tinv.product_id.prod_volume * tinv.out_qty if tinv.out_qty > 0 else tinv.product_id.prod_volume * tinv.quantity
                                        if values == 'Square Units':
                                            tsq += tinv.product_id.prod_sqm * tinv.out_qty if tinv.out_qty > 0 else tinv.product_id.prod_sqm * tinv.quantity
                                        if values == 'Pallet':
                                            if tinv.pallet_id:
                                                if tinv.pallet_id.id not in tpallets:
                                                    tpallets.append(tinv.pallet_id.id)
                                            # tpallet += 1
                                        if values == 'Weight':
                                            tweight += tinv.product_id.weight * tinv.out_qty if tinv.out_qty > 0 else tinv.product_id.weight * tinv.quantity
                                    else:
                                        if values == 'CBM':
                                            tcbm += tinv.product_id.prod_volume * tinv.out_qty * tinv.duration if tinv.out_qty > 0 else tinv.product_id.prod_volume * tinv.quantity * tinv.duration
                                        if values == 'Square Units':
                                            tsq += tinv.product_id.prod_sqm * tinv.out_qty * tinv.duration if tinv.out_qty > 0 else tinv.product_id.prod_sqm * tinv.quantity * tinv.duration
                                        # if values == 'Pallet':
                                        #     tpallet += 1 * tinv.duration
                                        if values == 'Weight':
                                            tweight += tinv.product_id.weight * tinv.out_qty * tinv.duration if tinv.out_qty > 0 else tinv.product_id.weight * tinv.quantity * tinv.duration
                                    print(tcbm, '-------tcbm1')
                                    summ = ({
                                        'start_date': tinv.in_date,
                                        'end_date': tinv.out_date,
                                        'quantity': tinv.out_qty if tinv.out_qty > 0 else tinv.quantity,
                                        'cbm': tinv.product_id.prod_volume,
                                        'sqm': tinv.product_id.prod_sqm,
                                        'pallet': 1,
                                        'weight': tinv.product_id.weight,
                                        'charge_type': 'storage',
                                        'product_id': tinv.product_id.id,
                                        'charge_unit_type': tchrg_unit_type[0].id,
                                    })
                                    summ_lines = self.env['summary.sheet.lines'].create(summ)
                                    # if summ_lines.quantity > 0 and values != 'Pallet' and unit != 'month':
                                    #     tsummary_lines.append(summ_lines)
                                    # if summ_lines.quantity > 0 and values == 'Pallet' and unit != 'month':
                                    #     tsummary_lines.append(summ_lines)
                                    if summ_lines.quantity > 0:
                                        tsummary_lines.append(summ_lines)
                                elif tinv.product_id.storage_type.name == sty and values == tinv.charge_unit_type.name and tinv.in_date != False and e >= tinv.in_date >= s and tinv.out_date == False and tinv.storage_product == True:
                                    if tinv.charge_unit_type.name not in types:
                                        types.append(tinv.charge_unit_type.name)
                                    duration = (abs((fields.Datetime.to_datetime(e).date()
                                                     - fields.Datetime.to_datetime(tinv.in_date).date()).days) + 1)
                                    print(duration, 'tdur2')
                                    if unit == 'month':
                                        if values == 'CBM':
                                            tcbm += tinv.product_id.prod_volume * tinv.out_qty if tinv.out_qty > 0 else tinv.product_id.prod_volume * tinv.quantity
                                        if values == 'Square Units':
                                            tsq += tinv.product_id.prod_sqm * tinv.out_qty if tinv.out_qty > 0 else tinv.product_id.prod_sqm * tinv.quantity
                                        if values == 'Pallet':
                                            if tinv.pallet_id:
                                                if tinv.pallet_id.id not in tpallets:
                                                    tpallets.append(tinv.pallet_id.id)
                                            # tpallet += 1
                                        if values == 'Weight':
                                            tweight += tinv.product_id.weight * tinv.out_qty if tinv.out_qty > 0 else tinv.product_id.weight * tinv.quantity
                                    else:
                                        if values == 'CBM':
                                            tcbm += tinv.product_id.prod_volume * tinv.out_qty * duration if tinv.out_qty > 0 else tinv.product_id.prod_volume * tinv.quantity * duration
                                        if values == 'Square Units':
                                            tsq += tinv.product_id.prod_sqm * tinv.out_qty * duration if tinv.out_qty > 0 else tinv.product_id.prod_sqm * tinv.quantity * duration
                                        # if values == 'Pallet':
                                        #     tpallet += 1 * duration
                                        if values == 'Weight':
                                            tweight += tinv.product_id.weight * tinv.out_qty * duration if tinv.out_qty > 0 else tinv.product_id.weight * tinv.quantity * duration
                                    print(tcbm, '-------tcbm2')
                                    summ = ({
                                        'start_date': tinv.in_date,
                                        'end_date': e,
                                        'quantity': tinv.out_qty if tinv.out_qty > 0 else tinv.quantity,
                                        'cbm': tinv.product_id.prod_volume,
                                        'sqm': tinv.product_id.prod_sqm,
                                        'pallet': 1,
                                        'weight': tinv.product_id.weight,
                                        'charge_type': 'storage',
                                        'product_id': tinv.product_id.id,
                                        'charge_unit_type': tchrg_unit_type[0].id,

                                    })
                                    summ_lines = self.env['summary.sheet.lines'].create(summ)
                                    # if summ_lines.quantity > 0 and values != 'Pallet' and unit != 'month':
                                    #     tsummary_lines.append(summ_lines)
                                    # if summ_lines.quantity > 0 and values == 'Pallet' and unit != 'month':
                                    #     tsummary_lines.append(summ_lines)
                                    if summ_lines.quantity > 0:
                                        tsummary_lines.append(summ_lines)
                                # elif tinv.in_date != False and e >= tinv.in_date >= s and s <= tinv.out_date <= e and tinv.storage_product == True:
                                #     duration = abs((fields.Datetime.to_datetime(tinv.out_date).date()
                                #                     - fields.Datetime.to_datetime(s).date()).days)
                                #     # tcbm += tinv.product_id.x_vol * tinv.out_qty if tinv.out_qty > 0 else tinv.quantity * tinv.duration
                                #     # tsq += tinv.product_id.x_vol * tinv.out_qty if tinv.out_qty > 0 else tinv.quantity * tinv.duration
                                #     tcbm += tinv.product_id.prod_volume * tinv.out_qty if tinv.out_qty > 0 else tinv.quantity * duration
                                #     tsq += tinv.product_id.prod_sqm * tinv.out_qty if tinv.out_qty > 0 else tinv.quantity * duration
                                #     tpallet += 1
                                #     tweight += tinv.product_id.weight * tinv.out_qty if tinv.out_qty > 0 else tinv.quantity * duration
                                #     summ = ({
                                #         'start_date': s,
                                #         'end_date': tinv.out_date,
                                #         'quantity': tinv.out_qty if tinv.out_qty > 0 else tinv.quantity,
                                #         'cbm': cbm,
                                #         'sqm': sq,
                                #         'pallet': pallet,
                                #         'weight': weight,
                                #     })
                                #     summ_lines = self.env['summary.sheet.lines'].create(summ)
                                #     summary_lines.append(summ_lines)
                                elif tinv.product_id.storage_type.name == sty and values == tinv.charge_unit_type.name and tinv.in_date != False and tinv.out_date != False and e >= tinv.in_date <= s and s <= tinv.out_date <= e and tinv.storage_product == True:
                                    if tinv.charge_unit_type.name not in types:
                                        types.append(tinv.charge_unit_type.name)
                                    duration = (abs((fields.Datetime.to_datetime(tinv.out_date).date()
                                                     - fields.Datetime.to_datetime(s).date()).days) + 1)
                                    # duration = (abs((fields.Datetime.to_datetime(e).date()
                                    #                  - fields.Datetime.to_datetime(tinv.in_date).date()).days) + 1)
                                    print(duration, tinv, 'tdur3')
                                    if unit == 'month':
                                        if values == 'CBM':
                                            tcbm += tinv.product_id.prod_volume * tinv.out_qty if tinv.out_qty > 0 else tinv.product_id.prod_volume * tinv.quantity
                                        if values == 'Square Units':
                                            tsq += tinv.product_id.prod_sqm * tinv.out_qty if tinv.out_qty > 0 else tinv.product_id.prod_sqm * tinv.quantity
                                        if values == 'Pallet':
                                            if tinv.pallet_id:
                                                if tinv.pallet_id.id not in tpallets:
                                                    tpallets.append(tinv.pallet_id.id)
                                            # tpallet += 1
                                        if values == 'Weight':
                                            tweight += tinv.product_id.weight * tinv.out_qty if tinv.out_qty > 0 else tinv.product_id.weight * tinv.quantity
                                    else:
                                        if values == 'CBM':
                                            tcbm += tinv.product_id.prod_volume * tinv.out_qty * duration if tinv.out_qty > 0 else tinv.product_id.prod_volume * tinv.quantity * duration
                                        if values == 'Square Units':
                                            tsq += tinv.product_id.prod_sqm * tinv.out_qty * duration if tinv.out_qty > 0 else tinv.product_id.prod_sqm * tinv.quantity * duration
                                        # if values == 'Pallet':
                                        #     tpallet += 1 * duration
                                        if values == 'Weight':
                                            tweight += tinv.product_id.weight * tinv.out_qty * duration if tinv.out_qty > 0 else tinv.product_id.weight * tinv.quantity * duration
                                    print(tcbm, '-------tcbm3')
                                    summ = ({
                                        'start_date': tinv.in_date,
                                        'end_date': tinv.out_date,
                                        'quantity': tinv.out_qty if tinv.out_qty > 0 else tinv.quantity,
                                        'cbm': tinv.product_id.prod_volume,
                                        'sqm': tinv.product_id.prod_sqm,
                                        'pallet': 1,
                                        'weight': tinv.product_id.weight,
                                        'charge_type': 'storage',
                                        'product_id': tinv.product_id.id,
                                        'charge_unit_type': tchrg_unit_type[0].id,

                                    })
                                    summ_lines = self.env['summary.sheet.lines'].create(summ)
                                    # if summ_lines.quantity > 0 and values != 'Pallet' and unit != 'month':
                                    #     tsummary_lines.append(summ_lines)
                                    # if summ_lines.quantity > 0 and values == 'Pallet' and unit != 'month':
                                    #     tsummary_lines.append(summ_lines)
                                    if summ_lines.quantity > 0:
                                        tsummary_lines.append(summ_lines)
                                elif tinv.product_id.storage_type.name == sty and values == tinv.charge_unit_type.name and tinv.in_date != False and tinv.out_date != False and e >= tinv.in_date <= s and s <= tinv.out_date >= e and tinv.storage_product == True:
                                    if tinv.charge_unit_type.name not in types:
                                        types.append(tinv.charge_unit_type.name)
                                    duration = (abs((fields.Datetime.to_datetime(e).date()
                                                     - fields.Datetime.to_datetime(s).date()).days) + 1)
                                    print(duration, 'tdur4')

                                    if unit == 'month':
                                        if values == 'CBM':
                                            tcbm += tinv.product_id.prod_volume * tinv.out_qty if tinv.out_qty > 0 else tinv.product_id.prod_volume * tinv.quantity
                                        if values == 'Square Units':
                                            tsq += tinv.product_id.prod_sqm * tinv.out_qty if tinv.out_qty > 0 else tinv.product_id.prod_sqm * tinv.quantity
                                        if values == 'Pallet':
                                            if tinv.pallet_id:
                                                if tinv.pallet_id.id not in tpallets:
                                                    tpallets.append(tinv.pallet_id.id)
                                            # tpallet += 1
                                        if values == 'Weight':
                                            tweight += tinv.product_id.weight * tinv.out_qty if tinv.out_qty > 0 else tinv.product_id.weight * tinv.quantity
                                    else:
                                        if values == 'CBM':
                                            tcbm += tinv.product_id.prod_volume * tinv.out_qty * duration if tinv.out_qty > 0 else tinv.product_id.prod_volume * tinv.quantity * duration
                                        if values == 'Square Units':
                                            tsq += tinv.product_id.prod_sqm * tinv.out_qty * duration if tinv.out_qty > 0 else tinv.product_id.prod_sqm * tinv.quantity * duration
                                        # if values == 'Pallet':
                                        #     tpallet += 1 * duration
                                        if values == 'Weight':
                                            tweight += tinv.product_id.weight * tinv.out_qty * duration if tinv.out_qty > 0 else tinv.product_id.weight * tinv.quantity * duration
                                    print(tcbm, '-------tcbm4')
                                    summ = ({
                                        'start_date': s,
                                        'end_date': e,
                                        'quantity': tinv.out_qty if tinv.out_qty > 0 else tinv.quantity,
                                        'cbm': tinv.product_id.prod_volume,
                                        'sqm': tinv.product_id.prod_sqm,
                                        'pallet': 1,
                                        'weight': tinv.product_id.weight,
                                        'charge_type': 'storage',
                                        'product_id': tinv.product_id.id,
                                        'charge_unit_type': tchrg_unit_type[0].id,

                                    })
                                    summ_lines = self.env['summary.sheet.lines'].create(summ)
                                    # if summ_lines.quantity > 0 and values != 'Pallet' and unit != 'month':
                                    #     tsummary_lines.append(summ_lines)
                                    # if summ_lines.quantity > 0 and values == 'Pallet' and unit != 'month':
                                    #     tsummary_lines.append(summ_lines)
                                    if summ_lines.quantity > 0:
                                        tsummary_lines.append(summ_lines)
                                elif tinv.product_id.storage_type.name == sty and values == tinv.charge_unit_type.name and tinv.in_date != False and e >= tinv.in_date <= s and tinv.out_date == False and tinv.storage_product == True:
                                    if tinv.charge_unit_type.name not in types:
                                        types.append(tinv.charge_unit_type.name)
                                    duration = (abs((fields.Datetime.to_datetime(e).date()
                                                     - fields.Datetime.to_datetime(s).date()).days) + 1)
                                    print(duration, tinv, 'tdur5', tinv.quantity, tinv.product_id.prod_volume, tinv.out_qty)
                                    if unit == 'month':
                                        if values == 'CBM':
                                            tcbm += tinv.product_id.prod_volume * tinv.out_qty if tinv.out_qty > 0 else tinv.product_id.prod_volume * tinv.quantity
                                        if values == 'Square Units':
                                            tsq += tinv.product_id.prod_sqm * tinv.out_qty if tinv.out_qty > 0 else tinv.product_id.prod_sqm * tinv.quantity
                                        if values == 'Pallet':
                                            if tinv.pallet_id:
                                                if tinv.pallet_id.id not in tpallets:
                                                    tpallets.append(tinv.pallet_id.id)
                                            # tpallet += 1
                                        if values == 'Weight':
                                            tweight += tinv.product_id.weight * tinv.out_qty if tinv.out_qty > 0 else tinv.product_id.weight * tinv.quantity
                                    else:
                                        if values == 'CBM':
                                            tcbm += tinv.product_id.prod_volume * tinv.out_qty * duration if tinv.out_qty > 0 else tinv.product_id.prod_volume * tinv.quantity * duration
                                        if values == 'Square Units':
                                            tsq += tinv.product_id.prod_sqm * tinv.out_qty * duration if tinv.out_qty > 0 else tinv.product_id.prod_sqm * tinv.quantity * duration
                                        # if values == 'Pallet':
                                        #     tpallet += 1 * duration
                                        if values == 'Weight':
                                            tweight += tinv.product_id.weight * tinv.out_qty * duration if tinv.out_qty > 0 else tinv.product_id.weight * tinv.quantity * duration
                                    print(tcbm, '-------tcbm5')
                                    summ = ({
                                        'start_date': s,
                                        'end_date': e,
                                        'quantity': tinv.out_qty if tinv.out_qty > 0 else tinv.quantity,
                                        'cbm': tinv.product_id.prod_volume,
                                        'sqm': tinv.product_id.prod_sqm,
                                        'pallet': 1,
                                        'weight': tinv.product_id.weight,
                                        'charge_type': 'storage',
                                        'product_id': tinv.product_id.id,
                                        'charge_unit_type': tchrg_unit_type[0].id,

                                    })

                                    summ_lines = self.env['summary.sheet.lines'].create(summ)
                                    # if summ_lines.quantity > 0 and values != 'Pallet' and unit != 'month':
                                    #     tsummary_lines.append(summ_lines)
                                    # if summ_lines.quantity > 0 and values == 'Pallet' and unit != 'month':
                                    #     tsummary_lines.append(summ_lines)
                                    if summ_lines.quantity > 0:
                                        tsummary_lines.append(summ_lines)
                                elif tinv.product_id.storage_type.name == sty and values == tinv.charge_unit_type.name and tinv.out_date != False and tinv.in_date != False and e >= tinv.in_date >= s and s <= tinv.out_date >= e and tinv.storage_product == True:
                                    if tinv.charge_unit_type.name not in types:
                                        types.append(tinv.charge_unit_type.name)
                                    duration = (abs((fields.Datetime.to_datetime(e).date()
                                                     - fields.Datetime.to_datetime(s).date()).days) + 1)
                                    print(duration, 'tdur5')
                                    if unit == 'month':
                                        if values == 'CBM':
                                            tcbm += tinv.product_id.prod_volume * tinv.out_qty if tinv.out_qty > 0 else tinv.product_id.prod_volume * tinv.quantity
                                        if values == 'Square Units':
                                            tsq += tinv.product_id.prod_sqm * tinv.out_qty if tinv.out_qty > 0 else tinv.product_id.prod_sqm * tinv.quantity
                                        if values == 'Pallet':
                                            if tinv.pallet_id:
                                                if tinv.pallet_id.id not in tpallets:
                                                    tpallets.append(tinv.pallet_id.id)
                                            # tpallet += 1
                                        if values == 'Weight':
                                            tweight += tinv.product_id.weight * tinv.out_qty if tinv.out_qty > 0 else tinv.product_id.weight * tinv.quantity
                                    else:
                                        if values == 'CBM':
                                            tcbm += tinv.product_id.prod_volume * tinv.out_qty * duration if tinv.out_qty > 0 else tinv.product_id.prod_volume * tinv.quantity * duration
                                        if values == 'Square Units':
                                            tsq += tinv.product_id.prod_sqm * tinv.out_qty * duration if tinv.out_qty > 0 else tinv.product_id.prod_sqm * tinv.quantity * duration
                                        # if values == 'Pallet':
                                        #     tpallet += 1 * duration
                                        if values == 'Weight':
                                            tweight += tinv.product_id.weight * tinv.out_qty * duration if tinv.out_qty > 0 else tinv.product_id.weight * tinv.quantity * duration
                                    print(tcbm, '-------tcbm6')
                                    summ = ({
                                        'start_date': s,
                                        'end_date': e,
                                        'quantity': tinv.out_qty if tinv.out_qty > 0 else tinv.quantity,
                                        'cbm': tinv.product_id.prod_volume,
                                        'sqm': tinv.product_id.prod_sqm,
                                        'pallet': 1,
                                        'weight': tinv.product_id.weight,
                                        'charge_type': 'storage',
                                        'product_id': tinv.product_id.id,
                                        'charge_unit_type': tchrg_unit_type[0].id,

                                    })

                                    summ_lines = self.env['summary.sheet.lines'].create(summ)
                                    # if summ_lines.quantity > 0 and values != 'Pallet' and unit != 'month':
                                    #     tsummary_lines.append(summ_lines)
                                    # if summ_lines.quantity > 0 and values == 'Pallet' and unit != 'month':
                                    #     tsummary_lines.append(summ_lines)
                                    if summ_lines.quantity > 0:
                                        tsummary_lines.append(summ_lines)
                        pals = tinven.filtered(lambda
                                                   inv: inv.charge_unit_type.name == 'Pallet' and inv.product_id.storage_type.name == sty)
                        print(pals, '-------------------pals---------------')
                        max = {}
                        for pinv in pals:
                            if values == pinv.charge_unit_type.name and pinv.in_date != False and pinv.out_date != False and e >= pinv.in_date >= s and s <= pinv.out_date <= e and pinv.storage_product == True:
                                print(pinv.duration, '-------dur 1')
                                duration = pinv.duration
                                pinv.duration_inv = duration
                                max[pinv] = {
                                    'pallet_id': pinv.pallet_id.id,
                                    'duration': duration}
                                # max[pinv] = {'summ': pinv,
                                #              'duration': duration,
                                #              }                                         }

                            elif values == pinv.charge_unit_type.name and pinv.in_date != False and e >= pinv.in_date >= s and pinv.out_date == False and pinv.storage_product == True:
                                if pinv.charge_unit_type.name not in types:
                                    types.append(pinv.charge_unit_type.name)
                                duration = (abs((fields.Datetime.to_datetime(e).date()
                                                 - fields.Datetime.to_datetime(pinv.in_date).date()).days) + 1)
                                pinv.duration_inv = duration
                                max[pinv] = {
                                    'pallet_id': pinv.pallet_id.id,
                                    'duration': duration}

                            elif values == pinv.charge_unit_type.name and pinv.in_date != False and pinv.out_date != False and e >= pinv.in_date <= s and s <= pinv.out_date <= e and pinv.storage_product == True:
                                if pinv.charge_unit_type.name not in types:
                                    types.append(pinv.charge_unit_type.name)
                                duration = (abs((fields.Datetime.to_datetime(pinv.out_date).date()
                                                 - fields.Datetime.to_datetime(s).date()).days) + 1)
                                pinv.duration_inv = duration
                                max[pinv] = {
                                    'pallet_id': pinv.pallet_id.id,
                                    'duration': duration}


                            elif values == pinv.charge_unit_type.name and pinv.in_date != False and pinv.out_date != False and e >= pinv.in_date <= s and s <= pinv.out_date >= e and pinv.storage_product == True:
                                if pinv.charge_unit_type.name not in types:
                                    types.append(pinv.charge_unit_type.name)
                                duration = (abs((fields.Datetime.to_datetime(e).date()
                                                 - fields.Datetime.to_datetime(s).date()).days) + 1)
                                pinv.duration_inv = duration
                                max[pinv] = {
                                    'pallet_id': pinv.pallet_id.id,
                                    'duration': duration}


                            elif values == pinv.charge_unit_type.name and pinv.in_date != False and pinv.out_date != False and e >= pinv.in_date >= s and s <= pinv.out_date <= e and pinv.storage_product == True:
                                if pinv.charge_unit_type.name not in types:
                                    types.append(pinv.charge_unit_type.name)
                                duration = (abs((fields.Datetime.to_datetime(e).date()
                                                 - fields.Datetime.to_datetime(pinv.in_date).date()).days) + 1)
                                pinv.duration_inv = duration
                                max[pinv] = {
                                    'pallet_id': pinv.pallet_id.id,
                                    'duration': duration}


                            elif pinv.out_date == False and values == pinv.charge_unit_type.name and pinv.in_date != False and e >= pinv.in_date <= s and pinv.storage_product == True:
                                if pinv.charge_unit_type.name not in types:
                                    types.append(pinv.charge_unit_type.name)
                                duration = (abs((fields.Datetime.to_datetime(e).date()
                                                 - fields.Datetime.to_datetime(s).date()).days) + 1)
                                pinv.duration_inv = duration
                                max[pinv] = {
                                    'pallet_id': pinv.pallet_id.id,
                                    'duration': duration}


                            elif pinv.out_date != False and values == pinv.charge_unit_type.name and pinv.in_date != False and pinv.out_date != False and e >= pinv.in_date >= s and s <= pinv.out_date >= e and pinv.storage_product == True:

                                if pinv.charge_unit_type.name not in types:
                                    types.append(pinv.charge_unit_type.name)
                                duration = (abs((fields.Datetime.to_datetime(e).date()
                                                 - fields.Datetime.to_datetime(pinv.in_date).date()).days) + 1)
                                pinv.duration_inv = duration
                                max[pinv] = {
                                    'pallet_id': pinv.pallet_id.id,
                                    'duration': duration}

                        print(max, '----------max')
                        MAX = max
                        data_list = [(key, value) for key, value in max.items()]

                        # Sort the list based on pallet_id
                        data_list.sort(key=lambda x: (x[1]['pallet_id'], -x[1]['duration']))

                        # Create a new dictionary to store the sorted and filtered data
                        sorted_data = {}

                        # Iterate through the sorted list and keep the summary records with the highest duration for each unique pallet_id
                        seen_pallets = set()
                        sorted_summ = []
                        for summary, info in data_list:
                            pallet_id = info['pallet_id']
                            duration = info['duration']

                            # If pallet_id is False, skip this entry
                            if pallet_id is False:
                                continue

                            # If pallet_id is not seen before or has a higher duration, add it to the new dictionary
                            if pallet_id not in seen_pallets or duration > sorted_data[pallet_id]['duration']:
                                sorted_data[pallet_id] = {'summary': summary, 'duration': duration}
                                seen_pallets.add(pallet_id)
                                sorted_summ.append(summary)

                        # Print the sorted and filtered data
                        for pallet_id, info in sorted_data.items():
                            print(f'Pallet ID: {pallet_id}, Summary: {info["summary"]}, Duration: {info["duration"]}')
                        print(sorted_summ, 'sorted_summ')
                        for inv in sorted_summ:
                            if values == inv.charge_unit_type.name and inv.in_date != False and inv.out_date != False and e >= inv.in_date >= s and s <= inv.out_date <= e and inv.storage_product == True:
                                print(inv.duration, 'dur 1')
                                duration = inv.duration
                                if inv.charge_unit_type.name not in types:
                                    types.append(inv.charge_unit_type.name)
                                if unit == 'day':
                                    tpallet += duration
                                summ = ({
                                    'start_date': inv.in_date,
                                    'end_date': inv.out_date,
                                    'quantity': inv.out_qty if inv.out_qty > 0 else inv.quantity,
                                    'pallet': 1,
                                    'charge_type': 'storage',
                                    'product_id': inv.product_id.id,
                                    'charge_unit_type': tchrg_unit_type[0].id,

                                })
                                summ_lines = self.env['summary.sheet.lines'].create(summ)

                                if summ_lines.quantity > 0:
                                    summary_lines.append(summ_lines)
                            elif values == inv.charge_unit_type.name and inv.in_date != False and e >= inv.in_date >= s and inv.out_date == False and inv.storage_product == True:
                                if inv.charge_unit_type.name not in types:
                                    types.append(inv.charge_unit_type.name)
                                duration = (abs((fields.Datetime.to_datetime(e).date()
                                                 - fields.Datetime.to_datetime(inv.in_date).date()).days) + 1)
                                print(duration, 'dur 2')
                                if unit == 'day':
                                    tpallet += duration
                                summ = ({
                                    'start_date': inv.in_date,
                                    'end_date': e,
                                    'quantity': inv.out_qty if inv.out_qty > 0 else inv.quantity,
                                    'pallet': 1,
                                    'charge_type': 'storage',
                                    'product_id': inv.product_id.id,
                                    'charge_unit_type': tchrg_unit_type[0].id,

                                })
                                summ_lines = self.env['summary.sheet.lines'].create(summ)

                                if summ_lines.quantity > 0:
                                    summary_lines.append(summ_lines)
                            elif values == inv.charge_unit_type.name and inv.in_date != False and inv.out_date != False and e >= inv.in_date <= s and s <= inv.out_date <= e and inv.storage_product == True:
                                if inv.charge_unit_type.name not in types:
                                    types.append(inv.charge_unit_type.name)
                                duration = (abs((fields.Datetime.to_datetime(inv.out_date).date()
                                                 - fields.Datetime.to_datetime(s).date()).days) + 1)
                                print(inv.out_date, s, duration, 'dur 3')
                                if unit == 'day':
                                    tpallet += duration
                                summ = ({
                                    'start_date': s,
                                    'end_date': inv.out_date,
                                    'quantity': inv.out_qty if inv.out_qty > 0 else inv.quantity,
                                    'pallet': 1,
                                    'charge_type': 'storage',
                                    'product_id': inv.product_id.id,
                                    'charge_unit_type': tchrg_unit_type[0].id,

                                })
                                summ_lines = self.env['summary.sheet.lines'].create(summ)

                                if summ_lines.quantity > 0:
                                    summary_lines.append(summ_lines)
                            elif values == inv.charge_unit_type.name and inv.in_date != False and inv.out_date != False and e >= inv.in_date <= s and s <= inv.out_date >= e and inv.storage_product == True:
                                if inv.charge_unit_type.name not in types:
                                    types.append(inv.charge_unit_type.name)
                                duration = (abs((fields.Datetime.to_datetime(e).date()
                                                 - fields.Datetime.to_datetime(s).date()).days) + 1)
                                print(duration, 'dur 4')
                                if unit == 'day':
                                    tpallet += duration

                                summ = ({
                                    'start_date': s,
                                    'end_date': e,
                                    'quantity': inv.out_qty if inv.out_qty > 0 else inv.quantity,
                                    'pallet': 1,
                                    'charge_type': 'storage',
                                    'product_id': inv.product_id.id,
                                    'charge_unit_type': tchrg_unit_type[0].id,

                                })
                                summ_lines = self.env['summary.sheet.lines'].create(summ)

                                if summ_lines.quantity > 0:
                                    summary_lines.append(summ_lines)
                            elif values == inv.charge_unit_type.name and inv.in_date != False and inv.out_date != False and e >= inv.in_date >= s and s <= inv.out_date <= e and inv.storage_product == True:
                                if inv.charge_unit_type.name not in types:
                                    types.append(inv.charge_unit_type.name)
                                duration = (abs((fields.Datetime.to_datetime(e).date()
                                                 - fields.Datetime.to_datetime(inv.in_date).date()).days) + 1)
                                print(duration, 'dur 5')
                                if unit == 'day':
                                    tpallet += duration

                                summ = ({
                                    'start_date': inv.in_date,
                                    'end_date': e,
                                    'quantity': inv.out_qty if inv.out_qty > 0 else inv.quantity,
                                    'pallet': 1,
                                    'charge_type': 'storage',
                                    'product_id': inv.product_id.id,
                                    'charge_unit_type': tchrg_unit_type[0].id,

                                })
                                summ_lines = self.env['summary.sheet.lines'].create(summ)

                                if summ_lines.quantity > 0:
                                    summary_lines.append(summ_lines)
                            elif values == inv.charge_unit_type.name and inv.in_date != False and e >= inv.in_date <= s and inv.out_date == False and inv.storage_product == True:
                                if inv.charge_unit_type.name not in types:
                                    types.append(inv.charge_unit_type.name)
                                duration = (abs((fields.Datetime.to_datetime(e).date()
                                                 - fields.Datetime.to_datetime(s).date()).days) + 1)
                                print(duration, 'dur 6')
                                if unit == 'day':
                                    tpallet += duration

                                summ = ({
                                    'start_date': s,
                                    'end_date': e,
                                    'quantity': inv.out_qty if inv.out_qty > 0 else inv.quantity,
                                    'pallet': 1,
                                    'charge_type': 'storage',
                                    'product_id': inv.product_id.id,
                                    'charge_unit_type': tchrg_unit_type[0].id,

                                })
                                summ_lines = self.env['summary.sheet.lines'].create(summ)

                                if summ_lines.quantity > 0:
                                    summary_lines.append(summ_lines)
                            elif values == inv.charge_unit_type.name and inv.out_date != False and inv.in_date != False and e >= inv.in_date >= s and s <= inv.out_date >= e and inv.storage_product == True:
                                if inv.charge_unit_type.name not in types:
                                    types.append(inv.charge_unit_type.name)
                                duration = (abs((fields.Datetime.to_datetime(e).date()
                                                 - fields.Datetime.to_datetime(inv.in_date).date()).days) + 1)
                                print(duration, 'dur 7')
                                if unit == 'day':
                                    tpallet += duration

                                summ = ({
                                    'start_date': s,
                                    'end_date': e,
                                    'quantity': inv.out_qty if inv.out_qty > 0 else inv.quantity,
                                    'pallet': 1,
                                    'charge_type': 'storage',
                                    'product_id': inv.product_id.id,
                                    'charge_unit_type': tchrg_unit_type[0].id,

                                })
                                summ_lines = self.env['summary.sheet.lines'].create(summ)

                                if summ_lines.quantity > 0:
                                    summary_lines.append(summ_lines)

                    if tpallets:
                        tpallet_count = len(tpallets)
                        tchrg_unit_type = self.env['charge.types'].search([('name', '=', 'Pallet')])
                        summ = ({
                            # 'start_date': inv.in_date,
                            # 'end_date': inv.out_date,
                            # 'quantity': inv.out_qty if inv.out_qty > 0 else inv.quantity,
                            # 'cbm': cbm,
                            # 'cbm': inv.product_id.prod_volume,
                            # 'sqm': inv.product_id.prod_sqm,
                            'pallet': tpallet_count,
                            # 'weight': inv.product_id.weight,
                            'charge_type': 'storage',
                            # 'product_id': inv.product_id.id,
                            'charge_unit_type': tchrg_unit_type[0].id,

                        })
                        summ_lines = self.env['summary.sheet.lines'].create(summ)
                        tsummary_lines.append(summ_lines)
                    else:
                        tpallet_count = 0
                        print(types, '======sto==true====')
                    if types:

                        for type in types:
                            print(type, sty, '------------------------hb-------typesto-----------------')
                            for temp in tstorage_charges.filtered(lambda inv: inv.storage_type.name == sty):
                                # print(temp, temp.charge_unit_type.name, type, '-------------------------temp----------------------')
                                if temp.charge_type == 'storage' and temp.charge_unit_type.name == 'CBM' and temp.charge_unit_type.name == type:
                                    temp_line_values = {
                                        'product_id': temp.product_id and temp.product_id.id or False,
                                        'name': temp.product_id.name or '',
                                        'price_unit': temp.list_price or 0.00,
                                        'quantity': tcbm,
                                        'currency_id': temp.currency_id.id,
                                        'tax_ids': [(6, 0, [temp.tax_id.id])] if temp.tax_id else False,
                                        'account_id': temp.product_id.property_account_income_id.id if temp.product_id.property_account_income_id
                                        else temp.product_id.categ_id.property_account_income_categ_id.id,
                                        # 'start_date': move_ids_without_package.start_date,
                                        # 'end_date': move_ids_without_package.end_date,

                                    }
                                    if temp_line_values['quantity'] > 0:
                                        print(temp_line_values, temp.storage_type.name)
                                        tinvoice_line_list.append((0, 0, temp_line_values))

                                if temp.charge_type == 'storage' and temp.charge_unit_type.name == 'Weight' and temp.charge_unit_type.name == type:
                                    temp_line_values = {
                                        'product_id': temp.product_id and temp.product_id.id or False,
                                        'name': temp.product_id.name or '',
                                        'price_unit': temp.list_price or 0.00,
                                        'quantity': tweight,
                                        'currency_id': temp.currency_id.id,
                                        'tax_ids': [(6, 0, [temp.tax_id.id])] if temp.tax_id else False,
                                        'account_id': temp.product_id.property_account_income_id.id if temp.product_id.property_account_income_id
                                        else temp.product_id.categ_id.property_account_income_categ_id.id,
                                        # 'start_date': move_ids_without_package.start_date,
                                        # 'end_date': move_ids_without_package.end_date,

                                    }
                                    if temp_line_values['quantity'] > 0:
                                        print(temp_line_values, temp.storage_type.name)
                                        tinvoice_line_list.append((0, 0, temp_line_values))

                                if temp.charge_type == 'storage' and temp.charge_unit_type.name == 'Square Units' and temp.charge_unit_type.name == type:
                                    temp_line_values = {
                                        'product_id': temp.product_id and temp.product_id.id or False,
                                        'name': temp.product_id.name or '',
                                        'price_unit': temp.list_price or 0.00,
                                        'quantity': tsq,
                                        'currency_id': temp.currency_id.id,
                                        'tax_ids': [(6, 0, [temp.tax_id.id])] if temp.tax_id else False,
                                        'account_id': temp.product_id.property_account_income_id.id if temp.product_id.property_account_income_id
                                        else temp.product_id.categ_id.property_account_income_categ_id.id,
                                        # 'start_date': move_ids_without_package.start_date,
                                        # 'end_date': move_ids_without_package.end_date,

                                    }
                                    if temp_line_values['quantity'] > 0:
                                        print(temp_line_values, temp.storage_type.name)
                                        tinvoice_line_list.append((0, 0, temp_line_values))

                                if temp.charge_type == 'storage' and temp.charge_unit_type.name == 'Pallet' and temp.charge_unit_type.name == type:
                                    temp_line_values = {
                                        'product_id': temp.product_id and temp.product_id.id or False,
                                        'name': temp.product_id.name or '',
                                        'price_unit': temp.list_price or 0.00,
                                        'quantity': tpallet if tpallet > 0 else tpallet_count,
                                        'currency_id': temp.currency_id.id,
                                        'tax_ids': [(6, 0, [temp.tax_id.id])] if temp.tax_id else False,
                                        'account_id': temp.product_id.property_account_income_id.id if temp.product_id.property_account_income_id
                                        else temp.product_id.categ_id.property_account_income_categ_id.id,
                                        # 'start_date': move_ids_without_package.start_date,
                                        # 'end_date': move_ids_without_package.end_date,

                                    }
                                    if temp_line_values['quantity'] > 0:
                                        print(temp_line_values, temp.storage_type.name)
                                        tinvoice_line_list.append((0, 0, temp_line_values))

                if tother_values:
                    print(tother_values, '---------------tother_values')
                    for values, unit in tother_values.items():
                        tcbm = 0
                        tweight = 0
                        tsq = 0
                        tpallet = 0
                        tquo = 0
                        tchrg_unit_type = self.env['charge.types'].search([('name', '=', values)])
                        # print(tinven.charge_unit_type, '----tinven----')
                        for tinv in tinven.filtered(
                                lambda inv: inv.charge_unit_type.name == values and inv.product_id.storage_type.name == sty):
                            if tinv.product_id.storage_type.name == sty and values == tinv.charge_unit_type.name and tinv.in_date != False and tinv.out_date != False and e >= tinv.in_date >= s and s <= tinv.out_date <= e and tinv.storage_product == True:
                                if unit == 'month':
                                    tcbm += tinv.product_id.prod_volume * tinv.out_qty if tinv.out_qty > 0 else tinv.quantity
                                    tsq += tinv.product_id.prod_sqm * tinv.out_qty if tinv.out_qty > 0 else tinv.quantity
                                    tpallet += 1
                                    tweight += tinv.product_id.weight * tinv.out_qty if tinv.out_qty > 0 else tinv.quantity
                                    tquo += 1
                                else:
                                    tcbm += tinv.product_id.prod_volume * tinv.out_qty if tinv.out_qty > 0 else tinv.quantity * tinv.duration
                                    tsq += tinv.product_id.prod_sqm * tinv.out_qty if tinv.out_qty > 0 else tinv.quantity * tinv.duration
                                    tpallet += 1
                                    tweight += tinv.product_id.weight * tinv.out_qty if tinv.out_qty > 0 else tinv.quantity * tinv.duration
                                    tquo += 1 * tinv.duration

                                summ = ({
                                    'start_date': tinv.in_date,
                                    'end_date': tinv.out_date,
                                    'quantity': tinv.out_qty if tinv.out_qty > 0 else tinv.quantity,
                                    'other': 1,
                                    'charge_type': 'storage',
                                    'product_id': tinv.product_id.id,
                                    'charge_unit_type': tchrg_unit_type[0].id,
                                })
                                summ_lines = self.env['summary.sheet.lines'].create(summ)
                                if summ_lines.quantity > 0:
                                    tsummary_lines.append(summ_lines)
                            elif tinv.product_id.storage_type.name == sty and values == tinv.charge_unit_type.name and tinv.in_date != False and e >= tinv.in_date >= s and tinv.out_date == False and tinv.storage_product == True:
                                duration = (abs((fields.Datetime.to_datetime(e).date()
                                                 - fields.Datetime.to_datetime(tinv.in_date).date()).days) + 1)

                                if unit == 'month':
                                    tcbm += tinv.product_id.prod_volume * tinv.out_qty if tinv.out_qty > 0 else tinv.quantity
                                    tsq += tinv.product_id.prod_sqm * tinv.out_qty if tinv.out_qty > 0 else tinv.quantity
                                    tpallet += 1
                                    tweight += tinv.product_id.weight * tinv.out_qty if tinv.out_qty > 0 else tinv.quantity
                                    tquo += 1
                                else:
                                    tcbm += tinv.product_id.prod_volume * tinv.out_qty if tinv.out_qty > 0 else tinv.quantity * duration
                                    tsq += tinv.product_id.prod_sqm * tinv.out_qty if tinv.out_qty > 0 else tinv.quantity * duration
                                    tpallet += 1
                                    tweight += tinv.product_id.weight * tinv.out_qty if tinv.out_qty > 0 else tinv.quantity * duration
                                    tquo += 1 * duration
                                summ = ({
                                    'start_date': tinv.in_date,
                                    'end_date': e,
                                    'quantity': tinv.out_qty if tinv.out_qty > 0 else tinv.quantity,
                                    'other': 1,
                                    'charge_type': 'storage',
                                    'product_id': tinv.product_id.id,
                                    'charge_unit_type': tchrg_unit_type[0].id,

                                })
                                summ_lines = self.env['summary.sheet.lines'].create(summ)
                                if summ_lines.quantity > 0:
                                    tsummary_lines.append(summ_lines)
                            # elif tinv.in_date != False and e >= tinv.in_date >= s and s <= tinv.out_date <= e and tinv.storage_product == True:
                            #     duration = abs((fields.Datetime.to_datetime(tinv.out_date).date()
                            #                     - fields.Datetime.to_datetime(s).date()).days)
                            #     # tcbm += tinv.product_id.x_vol * tinv.out_qty if tinv.out_qty > 0 else tinv.quantity * tinv.duration
                            #     # tsq += tinv.product_id.x_vol * tinv.out_qty if tinv.out_qty > 0 else tinv.quantity * tinv.duration
                            #     tcbm += tinv.product_id.prod_volume * tinv.out_qty if tinv.out_qty > 0 else tinv.quantity * duration
                            #     tsq += tinv.product_id.prod_sqm * tinv.out_qty if tinv.out_qty > 0 else tinv.quantity * duration
                            #     tpallet += 1
                            #     tweight += tinv.product_id.weight * tinv.out_qty if tinv.out_qty > 0 else tinv.quantity * duration
                            #     summ = ({
                            #         'start_date': s,
                            #         'end_date': tinv.out_date,
                            #         'quantity': tinv.out_qty if tinv.out_qty > 0 else tinv.quantity,
                            #         'cbm': cbm,
                            #         'sqm': sq,
                            #         'pallet': pallet,
                            #         'weight': weight,
                            #     })
                            #     summ_lines = self.env['summary.sheet.lines'].create(summ)
                            #     summary_lines.append(summ_lines)
                            elif tinv.product_id.storage_type.name == sty and values == tinv.charge_unit_type.name and tinv.in_date != False and tinv.out_date != False and e >= tinv.in_date <= s and s <= tinv.out_date <= e and tinv.storage_product == True:
                                duration = (abs((fields.Datetime.to_datetime(e).date()
                                                 - fields.Datetime.to_datetime(tinv.in_date).date()).days) + 1)

                                if unit == 'month':
                                    tcbm += tinv.product_id.prod_volume * tinv.out_qty if tinv.out_qty > 0 else tinv.quantity
                                    tsq += tinv.product_id.prod_sqm * tinv.out_qty if tinv.out_qty > 0 else tinv.quantity
                                    tpallet += 1
                                    tweight += tinv.product_id.weight * tinv.out_qty if tinv.out_qty > 0 else tinv.quantity
                                    tquo += 1
                                else:
                                    tcbm += tinv.product_id.prod_volume * tinv.out_qty if tinv.out_qty > 0 else tinv.quantity * duration
                                    tsq += tinv.product_id.prod_sqm * tinv.out_qty if tinv.out_qty > 0 else tinv.quantity * duration
                                    tpallet += 1
                                    tweight += tinv.product_id.weight * tinv.out_qty if tinv.out_qty > 0 else tinv.quantity * duration
                                    tquo += 1 * duration
                                summ = ({
                                    'start_date': tinv.in_date,
                                    'end_date': tinv.out_date,
                                    'quantity': tinv.out_qty if tinv.out_qty > 0 else tinv.quantity,
                                    'other': 1,
                                    'charge_type': 'storage',
                                    'product_id': tinv.product_id.id,
                                    'charge_unit_type': tchrg_unit_type[0].id,

                                })
                                summ_lines = self.env['summary.sheet.lines'].create(summ)
                                if summ_lines.quantity > 0:
                                    tsummary_lines.append(summ_lines)
                            elif tinv.product_id.storage_type.name == sty and values == tinv.charge_unit_type.name and tinv.in_date != False and tinv.out_date != False and e >= tinv.in_date <= s and s <= tinv.out_date >= e and tinv.storage_product == True:
                                duration = (abs((fields.Datetime.to_datetime(e).date()
                                                 - fields.Datetime.to_datetime(s).date()).days) + 1)

                                if unit == 'month':
                                    tcbm += tinv.product_id.prod_volume * tinv.out_qty if tinv.out_qty > 0 else tinv.quantity
                                    tsq += tinv.product_id.prod_sqm * tinv.out_qty if tinv.out_qty > 0 else tinv.quantity
                                    tpallet += 1
                                    tweight += tinv.product_id.weight * tinv.out_qty if tinv.out_qty > 0 else tinv.quantity
                                    tquo += 1
                                else:
                                    tcbm += tinv.product_id.prod_volume * tinv.out_qty if tinv.out_qty > 0 else tinv.quantity * duration
                                    tsq += tinv.product_id.prod_sqm * tinv.out_qty if tinv.out_qty > 0 else tinv.quantity * duration
                                    tpallet += 1
                                    tweight += tinv.product_id.weight * tinv.out_qty if tinv.out_qty > 0 else tinv.quantity * duration
                                    tquo += 1 * duration
                                summ = ({
                                    'start_date': s,
                                    'end_date': e,
                                    'quantity': tinv.out_qty if tinv.out_qty > 0 else tinv.quantity,
                                    'other': 1,
                                    'charge_type': 'storage',
                                    'product_id': tinv.product_id.id,
                                    'charge_unit_type': tchrg_unit_type[0].id,

                                })
                                summ_lines = self.env['summary.sheet.lines'].create(summ)
                                if summ_lines.quantity > 0:
                                    tsummary_lines.append(summ_lines)
                            elif tinv.product_id.storage_type.name == sty and values == tinv.charge_unit_type.name and tinv.in_date != False and e >= tinv.in_date <= s and tinv.out_date == False and tinv.storage_product == True:
                                duration = (abs((fields.Datetime.to_datetime(e).date()
                                                 - fields.Datetime.to_datetime(s).date()).days) + 1)

                                if unit == 'month':
                                    tcbm += tinv.product_id.prod_volume * tinv.out_qty if tinv.out_qty > 0 else tinv.quantity
                                    tsq += tinv.product_id.prod_sqm * tinv.out_qty if tinv.out_qty > 0 else tinv.quantity
                                    tpallet += 1
                                    tweight += tinv.product_id.weight * tinv.out_qty if tinv.out_qty > 0 else tinv.quantity
                                    tquo += 1
                                else:
                                    tcbm += tinv.product_id.prod_volume * tinv.out_qty if tinv.out_qty > 0 else tinv.quantity * duration
                                    tsq += tinv.product_id.prod_sqm * tinv.out_qty if tinv.out_qty > 0 else tinv.quantity * duration
                                    tpallet += 1
                                    tweight += tinv.product_id.weight * tinv.out_qty if tinv.out_qty > 0 else tinv.quantity * duration
                                    tquo += 1 * duration
                                summ = ({
                                    'start_date': s,
                                    'end_date': e,
                                    'quantity': tinv.out_qty if tinv.out_qty > 0 else tinv.quantity,
                                    'other': 1,
                                    'charge_type': 'storage',
                                    'product_id': tinv.product_id.id,
                                    'charge_unit_type': tchrg_unit_type[0].id,

                                })

                                summ_lines = self.env['summary.sheet.lines'].create(summ)
                                if summ_lines.quantity > 0:
                                    tsummary_lines.append(summ_lines)
                            elif tinv.product_id.storage_type.name == sty and values == tinv.charge_unit_type.name and tinv.out_date != False and tinv.in_date != False and e >= tinv.in_date <= s and tinv.out_date == False and tinv.storage_product == True:

                                duration = (abs((fields.Datetime.to_datetime(e).date()
                                                 - fields.Datetime.to_datetime(s).date()).days) + 1)
                                if unit == 'month':
                                    tcbm += tinv.product_id.prod_volume * tinv.out_qty if tinv.out_qty > 0 else tinv.quantity
                                    tsq += tinv.product_id.prod_sqm * tinv.out_qty if tinv.out_qty > 0 else tinv.quantity
                                    tpallet += 1
                                    tweight += tinv.product_id.weight * tinv.out_qty if tinv.out_qty > 0 else tinv.quantity
                                    tquo += 1
                                else:
                                    tcbm += tinv.product_id.prod_volume * tinv.out_qty if tinv.out_qty > 0 else tinv.quantity * duration
                                    tsq += tinv.product_id.prod_sqm * tinv.out_qty if tinv.out_qty > 0 else tinv.quantity * duration
                                    tpallet += 1
                                    tweight += tinv.product_id.weight * tinv.out_qty if tinv.out_qty > 0 else tinv.quantity * duration
                                    tquo += 1 * duration
                                summ = ({
                                    'start_date': s,
                                    'end_date': e,
                                    'quantity': tinv.out_qty if tinv.out_qty > 0 else tinv.quantity,
                                    'other': 1,
                                    'charge_type': 'storage',
                                    'product_id': tinv.product_id.id,
                                    'charge_unit_type': tchrg_unit_type[0].id,

                                })
                                summ_lines = self.env['summary.sheet.lines'].create(summ)
                                if summ_lines.quantity > 0:
                                    summary_lines.append(summ_lines)
                        # print(tquo, '------------------tquo------------')

                        for temp in tstorage_charges.filtered(
                                lambda inv: inv.charge_unit_type.name == values and inv.storage_type.name == sty and inv.agreement_id == agreement_id):
                            # print(temp, '------------------------------------temp----------------------------------------')
                            if temp.charge_type == 'storage' and temp.charge_unit_type.name == values and temp.storage_type:
                                # print('if')
                                temp_line_values = {
                                    'product_id': temp.product_id and temp.product_id.id or False,
                                    'name': temp.product_id.name or '',
                                    'price_unit': temp.list_price or 0.00,
                                    'quantity': tquo,
                                    'currency_id': temp.currency_id.id,
                                    'tax_ids': [(6, 0, [temp.tax_id.id])] if temp.tax_id else False,
                                    'account_id': temp.product_id.property_account_income_id.id if temp.product_id.property_account_income_id
                                    else temp.product_id.categ_id.property_account_income_categ_id.id,
                                    # 'start_date': move_ids_without_package.start_date,
                                    # 'end_date': move_ids_without_package.end_date,

                                }
                                if temp_line_values['quantity'] > 0:
                                    tinvoice_line_list.append((0, 0, temp_line_values))
                            break
                current_user = self.env.uid

            # print(lkj)
            if agreement_id and tinvoice_line_list:
                tinvoice = partner.env['account.move'].create({
                    'type': 'out_invoice',
                    'sto_type': 'warehouse',
                    'start_date_sto': s,
                    'end_date_sto': e,
                    'invoice_origin': partner.name,
                    'invoice_user_id': current_user,
                    'narration': partner.name,
                    'partner_id': partner.id,
                    'currency_id': partner.env.user.company_id.currency_id.id,
                    # 'journal_id': int(UOMer_journal_id),
                    'invoice_payment_ref': partner.name,
                    # 'picking_id': picking_id.id,
                    'invoice_line_ids': tinvoice_line_list,
                    # 'invoice_type': 'storage',
                    'name': '/',

                })
                invoices.append(tinvoice.id)
                tinvoice._summary_sheet()

                tsummary = ({
                    'name': str(s) + '-' + str(e) + '-' + 'Temperature Control',
                    'partner_id': partner.id,
                    'invoice_id': tinvoice.id
                })
                tsummary = self.env['summary.sheet'].create(tsummary)
                for lines in tsummary_lines:
                    lines['sheet_id'] = tsummary
                # if tinvoice:
                #     message = 'Cheers! Your Invoice is Successfully Crafted'
                #     return {
                #         'type': 'ir.actions.client',
                #         'tag': 'display_notification',
                #         'params': {
                #             'message': message,
                #             'type': 'success'  # Use 'warning' for a warning notification
                #         }
                #     }
                # if lines.product_id.storage_type:
                #     lines['sheet_id'] = tsummary
        return invoices
