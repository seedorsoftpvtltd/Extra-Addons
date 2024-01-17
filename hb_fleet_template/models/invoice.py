import time
from datetime import date, datetime, timedelta
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT, DEFAULT_SERVER_DATE_FORMAT, misc, ustr
from odoo.tools.float_utils import float_compare
from odoo import _, api, fields, models
from odoo.exceptions import ValidationError, Warning


class HbFleetVehicleLogServicess(models.Model):
    _inherit = 'fleet.vehicle.log.services'

    def action_donee(self):
        """Action Done Of Button."""
        context = dict(self.env.context)
        odometer_increment = 0.0
        increment_obj = self.env['next.increment.number']
        next_service_day_obj = self.env['next.service.days']
        mod_obj = self.env['ir.model.data']
        for work_order in self:
            service_inv = self.env['account.move'].search([
                ('type', '=', 'out_invoice'),
                ('vehicle_service_id', '=', work_order.id)])
            # if work_order.amount > 0 and not service_inv:
            #     raise ValidationError("Vehicle Service amount is greater"
            #                           " than Zero So, "
            #                           "Without Service Invoice you can not done the Service !!" "Please Generate Service Invoice first !!")

            for repair_line in work_order.repair_line_ids:
                if repair_line.complete is True:
                    continue
                elif repair_line.complete is False:
                    model_data_ids = mod_obj.search([
                        ('model', '=', 'ir.ui.view'),
                        ('name', '=', 'pending_repair_confirm_form_view')])
                    resource_id = model_data_ids.read(['res_id'])[0]['res_id']
                    context.update({'work_order_id': work_order.id})
                    # self.env.args = cr, uid, misc.frozendict(context)
                    return {
                        'name': _('WO Close Forcefully'),
                        'context': context,
                        'view_type': 'form',
                        'view_mode': 'form',
                        'res_model': 'pending.repair.confirm',
                        'views': [(resource_id, 'form')],
                        'type': 'ir.actions.act_window',
                        'target': 'new',
                    }

        increment_ids = increment_obj.search([
            ('vehicle_id', '=', work_order.vehicle_id.id)])
        if not increment_ids:
            return {
                'name': _('Next Service Day'),
                'res_model': 'update.next.service.config',
                'type': 'ir.actions.act_window',
                'view_id': False,
                'view_mode': 'form',
                'view_type': 'form',
                'target': 'new'
            }
        if increment_ids:
            odometer_increment = increment_ids[0].number

        next_service_day_ids = next_service_day_obj.search([
            ('vehicle_id', '=', work_order.vehicle_id.id)])
        if not next_service_day_ids:
            return {
                'name': _('Next Service Day'),
                'res_model': 'update.next.service.config',
                'type': 'ir.actions.act_window',
                'view_id': False,
                'view_mode': 'form',
                'view_type': 'form',
                'target': 'new'
            }
        work_order_vals = {}
        for work_order in self:
            # self.env.args = cr, uid, misc.frozendict(context)
            user = self.env.user
            if work_order.odometer == 0:
                raise Warning(_("Please set the current "
                                "Odometer of vehicle in work order!"))
            odometer_increment += work_order.odometer
            next_service_date = datetime.strptime(
                str(date.today()), DEFAULT_SERVER_DATE_FORMAT) + \
                                timedelta(days=next_service_day_ids[0].days)
            work_order_vals.update({
                'state': 'done',
                'next_service_odometer': odometer_increment,
                'already_closed': True,
                'closed_by': user,
                'date_close': fields.Date.today(),
                'next_service_date': next_service_date})
            work_order.write(work_order_vals)
            if work_order.vehicle_id:
                work_order.vehicle_id.write({
                    'state': 'complete',
                    'last_service_by_id': work_order.team_id and
                                          work_order.team_id.id or False,
                    'last_service_date': fields.Date.today(),
                    'next_service_date': next_service_date,
                    'due_odometer': odometer_increment,
                    'due_odometer_unit': work_order.odometer_unit,
                    'last_change_status_date': fields.Date.today(),
                    'work_order_close': True})
                if work_order.already_closed:
                    for repair_line in work_order.repair_line_ids:
                        for pending_repair_line in \
                                work_order.vehicle_id.pending_repair_type_ids:
                            if repair_line.repair_type_id.id == \
                                    pending_repair_line.repair_type_id.id and \
                                    work_order.name == \
                                    pending_repair_line.name:
                                if repair_line.complete is True:
                                    pending_repair_line.unlink()
        if work_order.parts_ids:
            parts = self.env['task.line'].search([
                ('fleet_service_id', '=', work_order.id),
                ('is_deliver', '=', False)])
            if parts:
                for part in parts:
                    part.write({'is_deliver': True})
                    source_location = self.env.ref(
                        'stock.picking_type_out').default_location_src_id
                    dest_location, loc = self.env[
                        'stock.warehouse']._get_partner_locations()
                    move = self.env['stock.move'].create({
                        'name': 'Used in Work Order',
                        'product_id': part.product_id.id or False,
                        'location_id': source_location.id or False,
                        'location_dest_id': dest_location.id or False,
                        'product_uom': part.product_uom.id or False,
                        'product_uom_qty': part.qty or 0.0
                    })
                    move._action_confirm()
                    move._action_assign()
                    move.move_line_ids.write({'qty_done': part.qty})
                    move._action_done()
        return True

    def action_create_invoicee(self):
        for service in self:
            # if service.amount <= 0.0:
            #     raise ValidationError("You can not create service invoice without amount!!"
            #                           "Please add Service amount first !!")

            deposit_inv_ids = self.env['account.move'].search([
                ('vehicle_service_id', '=', service.id), ('type', '=', 'out_invoice'),
                ('state', 'in', ['draft', 'open', 'in_payment'])
            ])
            if deposit_inv_ids:
                raise Warning(_("Deposit invoice is already Pending\n"
                                "Please proceed that deposit invoice first"))

            if not service.purchaser_id:
                raise Warning(
                    _("Please configure Driver from vehicle or in a service order!!"))

            inv_ser_line = [(0, 0, {
                'name': ustr(service.cost_subtype_id and
                             service.cost_subtype_id.name) + ' - Service Cost',
                'price_unit': service.amount,
                'account_id': service.vehicle_id and service.vehicle_id.income_acc_id and
                              service.vehicle_id.income_acc_id.id or False,
            })]
            for line in service.parts_ids:
                inv_line_values = {
                    'product_id': line.product_id and
                                  line.product_id.id or False,
                    'name': line.product_id and
                            line.product_id.name or '',
                    'price_unit': line.price_unit or 0.00,
                    'quantity': line.qty,
                    'account_id': service.vehicle_id and service.vehicle_id.income_acc_id and
                                  service.vehicle_id.income_acc_id.id or False
                }
                inv_ser_line.append((0, 0, inv_line_values))

            # for chk in service.checklist_ids:
            #     if chk.red or chk.yellow:
            #         chk_line_values = {
            #             'product_id': chk.service_prod and chk.service_prod.id or False,
            #             'name': chk.service_prod.name or '',
            #             'price_unit': chk.service_prod.list_price or 0.00,
            #             'quantity': chk.qty,
            #         }
            #         inv_ser_line.append((0, 0, chk_line_values))

            for chkk in service.checklist_ids:
                for chk in chkk.checklist:
                    if chk.red or chk.yellow:
                        chk_line_values = {
                            'product_id': chk.name and chk.name.id or False,
                            'name': chk.name.name or '',
                            'price_unit': chk.name.list_price or 0.00,
                            'quantity': chk.qty,
                        }
                        inv_ser_line.append((0, 0, chk_line_values))

            for temp in service.template_line_ids:
                if temp.result == 'failure':
                    temp_line_values = {
                        'product_id': temp.service_prod and temp.service_prod.id or False,
                        'name': temp.service_prod.name or '',
                        'price_unit': temp.service_prod.list_price or 0.00,
                        'quantity': temp.qty,
                    }
                    inv_ser_line.append((0, 0, temp_line_values))

            inv_values = {
                'partner_id': service.purchaser_id and
                              service.purchaser_id.id or False,
                'type': 'out_invoice',
                'invoice_date': service.date_open,
                'invoice_date_due': service.date_complete,
                'invoice_line_ids': inv_ser_line,
                'vehicle_service_id': service.id,
                'is_invoice_receive': True,
            }
            self.env['account.move'].create(inv_values)


