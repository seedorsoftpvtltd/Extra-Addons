# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.
##############################################################################
from odoo.tools.float_utils import float_round as round
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT
from odoo.exceptions import UserError, ValidationError
from odoo import api, fields, models, _
from datetime import datetime
#from prettytable import PrettyTable
from tabulate import tabulate
from dateutil.relativedelta import relativedelta
from lxml import etree

class Res_Partner(models.Model):
	_inherit = 'res.partner'
	#rec1 = fields.Text(string='Amount Due In',readonly='True')

	
	@api.depends('balance_invoice_over_ids')
	def get_amounts_and_date_amount_over(self):

		u = []
		curr=[]
		list111=[]
		currency=[]
		value=[]
		mylist=[]
		list1=0
		c1=[]
		curr1=[]
		var=''
		var1=[]
		fn=[]
		fn2=[]
		user_id = self._uid
		company = self.env['res.users'].browse(user_id).company_id
		current_date = datetime.today().date()


		
		for partner in self:

			amount_due = amount_overdue = 0.0

			for rec in partner.balance_invoice_over_ids:
				for inv_cur in rec.currency_id:
					curr.append(inv_cur.name)
				# print(curr)
				mylist = list(dict.fromkeys(curr))
				l=len(mylist)
				# print(mylist)

			for list111 in mylist:
				for rec in partner.balance_invoice_over_ids:
					if rec.currency_id.name == list111:

						list1+=rec.result_over
				currency.append(list111)
				value.append(list1)
			print(currency)
			print(value)






			data = tabulate({"Currency": currency,"Amount": value}, headers = "keys")

			# define header names
			# col_names = ["Currency", "Amount"]

			# display table
			#partner['rec1']=data
			# col_names= tabulate({"Currency": currency,"Amount": value}, headers = "keys")





			# for list111 in mylist:
			#      for rec in partner.balance_invoice_over_ids:
			#
			# 		if rec.currency_id.name == list111:
			# 			print('---------------------------------------')
			# 			list1.append(rec.currency_id)
			# print(list1)




			for aml in partner.balance_invoice_over_ids:

				date_maturity = aml.invoice_date_due or aml.date
				amount_due += aml.result_over
				if (date_maturity <= current_date):
					amount_overdue += aml.result_over

			partner.update({
			'payment_amount_due_amt_over' : amount_due,
			'payment_amount_overdue_amt_over' :  amount_overdue
			})


		for rec in self:

			if rec.balance_invoice_over_ids:
				for ids in rec.balance_invoice_over_ids:


					if ids.result_over != 0.0:

						u.append(ids.id)


				rec.balance_invoice_over_ids = u
	# def line_remove(self):
	# 		for rec in self:
	# 			t=[]
	# 			print("hiii")
	# 			if rec.balance_invoice_over_ids:
	# 				for ids in rec.balance_invoice_over_ids:
	# 					print(ids.result_over)
	# 					if ids.result_over == 0.0:
	# 						print("hiiinvoice")
	# 					else:
	# 						t.append(ids)
	# 				rec.balance_invoice_over_ids = []

							# ids.unlink() # DELETE FROM res_partner WHERE id IN (14) res.partner la delete panna pakkura aana athu vera idathula dlt aaaganum


	def do_partner_mail(self):
		unknown_mails = 0

		for partner in self:
			partners_to_email = [child for child in partner.child_ids if child.type == 'invoice' and child.email]
			if not partners_to_email and partner.email:
				partners_to_email = [partner]
			if partners_to_email:
				for partner_to_email in partners_to_email:
					mail_template_id = self.env['ir.model.data'].xmlid_to_object('bi_payment_overdue.email_template_account_followup_default_id')
					mail_template_id.send_mail(partner_to_email.id)
				if partner not in partners_to_email:
						self.message_post([partner.id], body=_('Overdue email sent to %s' % ', '.join(['%s <%s>' % (partner.name, partner.email) for partner in partners_to_email])))
		return unknown_mails
	
	
	def do_button_print(self):
		return self.env.ref('bi_payment_overdue.report_customer_overdue_print').report_action(self)
	
	company_id = fields.Many2one('res.company', required=True, default=lambda self: self.env.company)

	balance_invoice_over_ids =fields.One2many('account.move', 'partner_id','Customer move lines',domain=[('type', '=', 'out_invoice'), ('state', 'in', ['posted']), ('amount_residual', '!=',0)])

	unreconciled_aml_ids = fields.One2many('account.move.line', 'partner_id','Move lines')

	payment_amount_due_amt_over=fields.Float( string="Balance Due",readonly=False,compute = 'get_amounts_and_date_amount_over')

	payment_amount_overdue_amt_over = fields.Float(compute='get_amounts_and_date_amount_over',string="Total Overdue Amount", readonly=False)

	today_date = fields.Date(default=fields.date.today())

	currency_id=fields.Many2one('res.currency',default=lambda self:self.env.user.currency_id)







