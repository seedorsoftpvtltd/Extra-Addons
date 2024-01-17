# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.
##############################################################################


from odoo import api, models, _
from datetime import datetime, timedelta
from odoo.exceptions import UserError
from odoo.tools import float_is_zero, float_compare, DEFAULT_SERVER_DATETIME_FORMAT
from odoo import SUPERUSER_ID



class SaleOrderLine(models.Model):
	_inherit = 'sale.order.line'
		
	def _action_launch_stock_rule(self, previous_product_uom_qty=False):
		precision = self.env['decimal.precision'].precision_get('Product Unit of Measure')
		procurements = []
		errors = []
		for line in self:
			if line.state != 'sale' or not line.product_id.type in ('consu', 'product'):
				continue
			qty = line._get_qty_procurement(previous_product_uom_qty)
			if float_compare(qty, line.product_uom_qty, precision_digits=precision) >= 0:
				continue

			group_id = line._get_procurement_group()

			if not group_id:
				group_id = self.env['procurement.group'].create(line._prepare_procurement_group_vals())
				line.order_id.procurement_group_id = group_id
			else:   
				if line.product_id.pack_ids:
					values = line._prepare_procurement_values(group_id=line.order_id.procurement_group_id)
					for val in values:
						try:
							pro_id = self.env['product.product'].browse(val.get('product_id'))
							stock_id = self.env['stock.location'].browse(val.get('partner_dest_id'))
							product_uom_obj = self.env['uom.uom'].browse(val.get('product_uom'))
							procurements.append(self.env['procurement.group'].Procurement(
								pro_id, 0, product_uom_obj,
								line.order_id.partner_shipping_id.property_stock_customer,
								val.get('name'), val.get('origin'), line.order_id.company_id, val
							))
						except UserError as error:
							errors.append(error.name)
				else:
					updated_vals = {}
					if group_id.partner_id != line.order_id.partner_shipping_id:
						updated_vals.update({'partner_id': line.order_id.partner_shipping_id.id})
					if group_id.move_type != line.order_id.picking_policy:
						updated_vals.update({'move_type': line.order_id.picking_policy})
					if updated_vals:
						group_id.write(updated_vals)


			if line.product_id.pack_ids:
				values = line._prepare_procurement_values(group_id=line.order_id.procurement_group_id)
				# product_qty = line.product_uom_qty - qty
				for val in values:
					try:
						pro_id = self.env['product.product'].browse(val.get('product_id'))
						stock_id = self.env['stock.location'].browse(val.get('partner_dest_id'))
						product_uom_obj = self.env['uom.uom'].browse(val.get('product_uom'))
						procurements.append(self.env['procurement.group'].Procurement(
							pro_id, val.get('product_qty'), product_uom_obj,
							line.order_id.partner_shipping_id.property_stock_customer,
							val.get('name'), val.get('origin'), line.order_id.company_id, val
						))
					except UserError as error:
						errors.append(error.name)
			else:
				values = line._prepare_procurement_values(group_id=group_id)
				product_qty = line.product_uom_qty - qty
				line_uom = line.product_uom
				quant_uom = line.product_id.uom_id
				product_qty, procurement_uom = line_uom._adjust_uom_quantities(product_qty, quant_uom)
				procurements.append(self.env['procurement.group'].Procurement(
					line.product_id, product_qty, procurement_uom,
					line.order_id.partner_shipping_id.property_stock_customer,
					line.name, line.order_id.name, line.order_id.company_id, values
				))

		if procurements:
			self.env['procurement.group'].run(procurements)
			
		orders = list(set(x.order_id for x in self))
		for order in orders:
		    reassign = order.picking_ids.filtered(lambda x: x.state=='confirmed' or (x.state in ['waiting', 'assigned'] and not x.printed))
		    if reassign:
		        reassign.action_assign()
			
		return True


		
	def _prepare_procurement_values(self, group_id):
		res = super(SaleOrderLine, self)._prepare_procurement_values(group_id=group_id)
		values = []
		# date_planned = datetime.strptime(str(self.order_id.confirmation_date), DEFAULT_SERVER_DATETIME_FORMAT)\
		#     + timedelta(days=self.customer_lead or 0.0) - timedelta(days=self.order_id.company_id.security_lead)
		if  self.product_id.pack_ids:
			for item in self.product_id.pack_ids:
				line_route_ids = self.env['stock.location.route'].browse(self.route_id.id)
				values.append({
					'name': item.product_id.name,
					'origin': self.order_id.name,
					# 'date_planned': date_planned.strftime(DEFAULT_SERVER_DATETIME_FORMAT),
					'product_id': item.product_id.id,
					'product_qty': item.qty_uom * abs(self.product_uom_qty),
					'product_uom': item.uom_id and item.uom_id.id,
					'company_id': self.order_id.company_id,
					'group_id': group_id,
					'sale_line_id': self.id,
					'warehouse_id' : self.order_id.warehouse_id and self.order_id.warehouse_id,
					'location_id': self.order_id.partner_shipping_id.property_stock_customer.id,
					'route_ids': self.route_id and line_route_ids or [],
					'partner_dest_id': self.order_id.partner_shipping_id,
					'partner_id': self.order_id.partner_id.id
				})
			return values
		else:
			res.update({
			'company_id': self.order_id.company_id,
			'group_id': group_id,
			'sale_line_id': self.id,
			# 'date_planned': date_planned.strftime(DEFAULT_SERVER_DATETIME_FORMAT),
			'route_ids': self.route_id,
			'warehouse_id': self.order_id.warehouse_id or False,
			'partner_dest_id': self.order_id.partner_shipping_id
		})    
		return res

	@api.depends('move_ids.state', 'move_ids.scrapped', 'move_ids.product_uom_qty', 'move_ids.product_uom')
	def _compute_qty_delivered(self):
		super(SaleOrderLine, self)._compute_qty_delivered()
		for line in self:  # TODO: maybe one day, this should be done in SQL for performance sake
			if line.qty_delivered_method == 'stock_move':
				qty = 0.0
				flag = False
				if line.product_id.is_pack == True:
					list_of_sub_product = []
					for product_item in line.product_id.pack_ids:
						list_of_sub_product.append(product_item.product_id)
					for move in line.move_ids.filtered(lambda r: r.state == 'done' and not r.scrapped and  r.product_id in list_of_sub_product  ):
						if move.state == 'done' and move.product_uom_qty == move.quantity_done:
							flag = True
						else:
							flag = False
							break
					if flag == True:
						line.qty_delivered = line.product_uom_qty
					
				else:
					for move in line.move_ids.filtered(lambda r: r.state == 'done' and not r.scrapped and line.product_id == r.product_id):
						if move.location_dest_id.usage == "customer":
							if not move.origin_returned_move_id or (move.origin_returned_move_id and move.to_refund):
								qty += move.product_uom._compute_quantity(move.product_uom_qty, line.product_uom)
						elif move.location_dest_id.usage != "customer" and move.to_refund:
							qty -= move.product_uom._compute_quantity(move.product_uom_qty, line.product_uom)
					line.qty_delivered = qty

 

class ProcurementRule(models.Model):
	_inherit = 'stock.rule'
	
	def _get_stock_move_values(self, product_id, product_qty, product_uom, location_id, name, origin, values, group_id):
		result = super(ProcurementRule, self)._get_stock_move_values(product_id, product_qty, product_uom, location_id, name, origin, values, group_id)
		
		if  product_id.pack_ids:
			for item in product_id.pack_ids:
				result.update({
					'product_id': item.product_id.id,
					'product_uom': item.uom_id and item.uom_id.id,
					'product_uom_qty': item.qty_uom,
					'origin': origin,
					})
		return result


class PurchaseOrderLine(models.Model):
	_inherit = 'purchase.order.line'

	def _prepare_stock_moves(self, picking):
		""" Prepare the stock moves data for one order line. This function returns a list of
		dictionary ready to be used in stock.move's create()
		"""
		res = super(PurchaseOrderLine, self)._prepare_stock_moves(picking=picking)
		self.ensure_one()
		res = []
		if self.product_id.type not in ['product', 'consu']:
			return res
		qty = 0.0
		price_unit = self._get_stock_move_price_unit()
		for move in self.move_ids.filtered(lambda x: x.state != 'cancel' and not x.location_dest_id.usage == "supplier"):
			qty += move.product_qty
		if  self.product_id.pack_ids:
			for item in self.product_id.pack_ids:
				template = {
					'name': item.product_id.name or '',
					'product_id': item.product_id.id,
					'product_uom': item.uom_id.id,
					'date': self.order_id.date_order,
					'date_expected': self.date_planned,
					'location_id': self.order_id.partner_id.property_stock_supplier.id,
					'location_dest_id': self.order_id._get_destination_location(),
					'picking_id': picking.id,
					'partner_id': self.order_id.dest_address_id.id,
					'move_dest_ids': [(4, x) for x in self.move_dest_ids.ids],
					'state': 'draft',
					'purchase_line_id': self.id,
					'company_id': self.order_id.company_id.id,
					'price_unit': price_unit,
					'picking_type_id': self.order_id.picking_type_id.id,
					'group_id': self.order_id.group_id.id,
					'origin': self.order_id.name,
					'route_ids': self.order_id.picking_type_id.warehouse_id and [(6, 0, [x.id for x in self.order_id.picking_type_id.warehouse_id.route_ids])] or [],
					'warehouse_id': self.order_id.picking_type_id.warehouse_id.id,
				}
				diff_quantity = item.qty_uom
				if float_compare(diff_quantity, 0.0,  precision_rounding=self.product_uom.rounding) > 0:
					template['product_uom_qty'] = diff_quantity * self.product_qty
					res.append(template)
			return res
		else:
			template = {
			'name': self.name or '',
			'product_id': self.product_id.id,
			'product_uom': self.product_uom.id,
			'date': self.order_id.date_order,
			'date_expected': self.date_planned,
			'location_id': self.order_id.partner_id.property_stock_supplier.id,
			'location_dest_id': self.order_id._get_destination_location(),
			'picking_id': picking.id,
			'partner_id': self.order_id.dest_address_id.id,
			'move_dest_ids': [(4, x) for x in self.move_dest_ids.ids],
			'state': 'draft',
			'purchase_line_id': self.id,
			'company_id': self.order_id.company_id.id,
			'price_unit': price_unit,
			'picking_type_id': self.order_id.picking_type_id.id,
			'group_id': self.order_id.group_id.id,
			'origin': self.order_id.name,
			'route_ids': self.order_id.picking_type_id.warehouse_id and [(6, 0, [x.id for x in self.order_id.picking_type_id.warehouse_id.route_ids])] or [],
			'warehouse_id': self.order_id.picking_type_id.warehouse_id.id,
		}
			diff_quantity = self.product_qty - qty
			if float_compare(diff_quantity, 0.0,  precision_rounding=self.product_uom.rounding) > 0:
				template['product_uom_qty'] = diff_quantity
				res.append(template)
		return res        

class AccountMove(models.Model):
	_inherit = 'account.move'

	def _stock_account_prepare_anglo_saxon_out_lines_vals(self):
		res = super(AccountMove, self)._stock_account_prepare_anglo_saxon_out_lines_vals()
		list_product_id = [product_id['product_id'] for product_id in res]
		if list_product_id:
			counter = 0
			list_product_id = list(set(list_product_id))
			product_product = self.env['product.product'].browse(list_product_id)
			list_product_id = product_product.filtered(lambda x: x.is_pack == True)

			move_id = [move_id['move_id'] for move_id in res]
			move_id = list(set(move_id))
			move_id = self.env['account.move'].browse(move_id)
			for line in move_id.invoice_line_ids[0]:
				for l_prod_id in list_product_id:
					for product_pack_id in l_prod_id.pack_ids:
						counter += 1
						# Filter out lines being not eligible for COGS.
						if product_pack_id.product_id.type != 'product' or product_pack_id.product_id.valuation != 'real_time':
							continue

						# Retrieve accounts needed to generate the COGS.
						accounts = (
							product_pack_id.product_id.product_tmpl_id
								.with_context(force_company=line.company_id.id)
								.get_product_accounts(fiscal_pos=move_id.fiscal_position_id)
						)
						debit_interim_account = accounts['stock_output']
						credit_expense_account = accounts['expense']
						if not credit_expense_account:
							if self.type == 'out_refund':
								credit_expense_account = self.journal_id.default_credit_account_id
							else:  # out_invoice/out_receipt
								credit_expense_account = self.journal_id.default_debit_account_id
						if not debit_interim_account or not credit_expense_account:
							continue

						# Compute accounting fields.
						sign = -1 if move_id.type == 'out_refund' else 1
						#if not self.product_id:
						#	return self.price_unit
						price_unit = product_pack_id.product_id._stock_account_get_anglo_saxon_price_unit(uom=line.product_uom_id)
						#price_unit = line._stock_account_get_anglo_saxon_price_unit()
						balance = sign * product_pack_id.qty_uom * price_unit

						# Add interim account line.
						if counter == 1:
							res = []
						res.append({
							'name': line.name[:64] + ' ' +(product_pack_id.product_id.name),
							'move_id': move_id.id,
							'product_id': product_pack_id.product_id.id,
							'product_uom_id': product_pack_id.product_id.uom_id.id,
							'quantity': product_pack_id.qty_uom,
							'price_unit': price_unit,
							'debit': balance < 0.0 and -balance or 0.0,
							'credit': balance > 0.0 and balance or 0.0,
							'account_id': debit_interim_account.id,
							'exclude_from_invoice_tab': True,
							'is_anglo_saxon_line': True,
						})

						# Add expense account line.
						res.append({
							'name': line.name[:64] + ' ' +(product_pack_id.product_id.name),
							'move_id': move_id.id,
							'product_id': product_pack_id.product_id.id,
							'product_uom_id': product_pack_id.product_id.uom_id.id,
							'quantity': product_pack_id.qty_uom,
							'price_unit': -price_unit,
							'debit': balance > 0.0 and balance or 0.0,
							'credit': balance < 0.0 and -balance or 0.0,
							'account_id': credit_expense_account.id,
							'analytic_account_id': line.analytic_account_id.id,
							'analytic_tag_ids': [(6, 0, line.analytic_tag_ids.ids)],
							'exclude_from_invoice_tab': True,
							'is_anglo_saxon_line': True,
						})
		return res