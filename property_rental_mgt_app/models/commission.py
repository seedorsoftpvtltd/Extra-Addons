# -*- coding: utf-8 -*-

from odoo import models, fields, api, _

class UserCommission(models.Model):
	_name = 'user.commission'
	_description = 'User Commission'

	user_id = fields.Many2one('res.users')
	percentage = fields.Float()
	property_id = fields.Many2one('product.product', string="Property")

class CommissionLines(models.Model):
	_name = 'commission.line'
	_description = "Commission Lines"

	name = fields.Char()
	user_id = fields.Many2one('res.users')
	commission = fields.Float("Commission Amount")
	percentage = fields.Float("Percentage (%)")
	property_id = fields.Many2one('product.product', "Property")
	inv_pay_source = fields.Char(string="Invoice Reference")
	pay_reference = fields.Char(string="Payment Reference")
	payment_origin = fields.Char()
	invoice_id = fields.Many2one('account.move')
	is_created_worksheet = fields.Boolean("Worksheet Created")

class MergeWorksheet(models.Model):
	_name = 'merge.worksheet'
	_description = "Merge Worksheet"

	name = fields.Char()
	user_id = fields.Many2one('res.users', string="Commission User")
	commission = fields.Float("Commission Amount")
	percentage = fields.Float("Percentage(%)")
	property_origin = fields.Char(string="Property Reference")
	invoice_origin = fields.Char(string="Invoice Reference")
	payment_origin = fields.Char(string="Payment Reference")
	property_id = fields.Many2one('product.product')

class WorksheetLine(models.Model):
	_name = 'worksheet.line'
	_description = 'Commission Worksheet Lines'

	worksheet_id = fields.Many2one('commission.worksheet')
	percentage = fields.Float("Commission in Percentage(%)")
	commission = fields.Float("Commission Amount")
	property_origin =fields.Char(string="Property Reference")
	invoice_origin =fields.Char(string="Invoice Reference")
	payment_origin = fields.Char(string="Payment Reference")


class CommissionWorksheet(models.Model):
	_name = 'commission.worksheet'
	_description = "Commission Worksheet"

	name = fields.Char(string="Worksheet Number",help="Auto generated commission sequence number")
	user_id = fields.Many2one('res.users', string="Commission User")
	commission = fields.Float()
	comm_work_line_ids = fields.One2many('worksheet.line', 'worksheet_id', string="Commission Lines")
	state = fields.Selection([('draft',"Draft"),('bill',"Billing")], default="draft")
	invoice_bill_id = fields.Many2one('account.move',string="Bill Reference")

	def create_commission_bill(self):

		property_obj = self.env['ir.property']
		account_expense_id = property_obj.get('property_account_expense_categ_id', 'product.category')

		values = {
			'type': 'in_invoice',
			'invoice_origin':self.name,
			'partner_id': self.user_id.partner_id.id,
			'invoice_date_due':fields.Date.today(),
			'invoice_date':fields.Date.today(),
			'invoice_line_ids': [(0,0,{
				'name':self.name,
				'account_id': account_expense_id.id,
				'price_unit': self.commission})],
			}

		res = self.env["account.move"].create(values)
		if res:
			self.write({'state':'bill','invoice_bill_id':res.id})