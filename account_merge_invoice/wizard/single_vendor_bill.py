# -*- coding: utf-8 -*-

from odoo import fields, models, api, _
from odoo.tools.float_utils import float_is_zero, float_compare
from odoo.exceptions import UserError
import datetime

class SingleModel(models.Model):

	_inherit = 'account.move'
	
	fiscal_position_id = fields.Many2one('account.fiscal.position', string='Fiscal Position',
										 domain="['|', ('company_id', '=', False), ('company_id', '=', company_id)]")


class SingleMove(models.Model):
	_inherit = 'stock.move'



	taxes_id = fields.Many2many('account.tax', string='Taxes',
								domain=['|', ('active', '=', False), ('active', '=', True)])

class SingleVendorBill(models.TransientModel):

	_name = 'single.vendor.bill'

	# Return created Invoices

	def create_return_vendor_bill(self):
		customer_invoice_id  = self.create_single_vendor_bill()
		tree_view_ref = self.env.ref('account.invoice_supplier_tree',False)
		form_view_ref = self.env.ref('account.invoice_supplier_form',False)
		return {
					'name':'Invoices',
					'res_model':'account.move',
					'view_type':'form',
					'view_mode':'tree,form',
					'target':'current',
					'domain':[('id','=',customer_invoice_id.id)],
					'type':'ir.actions.act_window',
					'views': [(tree_view_ref and tree_view_ref.id or False,'tree'),(form_view_ref and form_view_ref.id or False,'form')],
				}

	# Create single Invoice from multiple orders

	def create_single_vendor_bill(self):
		stock_orders = self.env['account.move'].browse(self._context.get('active_ids'))

		name_orders = [order.name for order in stock_orders]
		partners = [order.partner_id.id for order in stock_orders]
		print(partners)
		fiscal_positions = [order.fiscal_position_id.id for order in stock_orders]
		not_confirmed_order = []
		for order in stock_orders:
			if order.state != 'draft':
				not_confirmed_order.append(order.name)
			else:
				pass
		if (len(stock_orders)) < 2:
			raise UserError(_('Please select atleast two Invoices to create Single Invoice'))
		else:
			if(len(set(partners))!=1):
				raise UserError(_('Please select Invoices whose "Contacts" are same to create Single Invoice.'))
			else:
				if (len(set(fiscal_positions))!=1):
					raise UserError(_('Please select Invoices whose "Fiscal Poistions" are same to create Single Invoice.'))
				else:
					if any(order.state != 'draft' for order in stock_orders):
						raise UserError(_('Please select Invoices which are in "Draft" state to create Single Invoice.%s is not confirmed yet.') % ','.join(map(str, not_confirmed_order)))
					else:
						customer_invoice_id = self.prepare_vendor_bill()
						return customer_invoice_id


	def prepare_vendor_bill(self):
		print("HELOOO")
		invoice_line = self.env['account.move.line']
		stock_orders = self.env['account.move'].browse(self._context.get('active_ids'))
		name_orders = [order.name for order in stock_orders]
		journal_id = self.env['account.journal'].search([('type','=','sale')])[0]
		partner_ids = [order.partner_id for order in stock_orders if order.partner_id.id]
		invoice_lines = []
		for order in stock_orders:
			for line in order.invoice_line_ids:
				account_id = line.product_id.property_account_income_id or line.product_id.categ_id.property_account_income_categ_id
				invoice_lines.append(((0,0,{
							'name': line.name,
							'display_name': line.product_id.name,
							'account_id': account_id.id,
							'price_unit': line.price_unit,
							'quantity': line.quantity,
							'product_uom_id': line.product_uom_id.id,
					'analytic_account_id': line.analytic_account_id.id,
							'product_id': line.product_id.id or False,
							'tax_ids': [(6, 0, line.product_id.taxes_id.ids)],
						})))
		vendor_bill_vals = {
							'name': ','.join(map(str, name_orders)),
							'invoice_origin':','.join(map(str, name_orders)),
							'invoice_date':datetime.datetime.now().date(),
							'type': 'out_invoice',
							'state':'draft',
							'partner_id': order.partner_id.id,
							'invoice_line_ids': invoice_lines,
							'journal_id': journal_id.id,
			'team_id': order.team_id.id,
			'invoice_payment_ref': order.invoice_payment_ref,
			'invoice_partner_bank_id': order.invoice_partner_bank_id.id,
							'invoice_payment_term_id': order.invoice_payment_term_id.id,
							'fiscal_position_id': order.fiscal_position_id.id,
							'company_id': order.company_id.id,
							'user_id': order.activity_user_id and order.activity_user_id.id,
						}
		customer_invoice_id = self.env['account.move'].create(vendor_bill_vals)
		customer_invoice_id._onchange_invoice_line_ids()
		return customer_invoice_id