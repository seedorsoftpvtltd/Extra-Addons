import re
import pandas as pd
from datetime import datetime
from odoo import api, fields, models 

class CurrencyCustom(models.Model):
	_inherit = "res.currency"
	_description = "Currency"

	rate = fields.Float(compute='_compute_current_rate', inverse='_inverse_upper', store=True, string='Current Rate',
						help='The rate of the currency to the currency of rate 1.')

	def _inverse_upper(self):
		date = self._context.get('date') or fields.Date.today()
		company = self.env['res.company'].browse(self._context.get('company_id')) or self.env.user.company_id
		# the subquery selects the last rate before 'date' for the given currency/company

	def _get_rates(self, company, date):
		self.env['res.currency.rate'].flush(['rate', 'currency_id', 'company_id', 'name'])
		query = """SELECT c.id,
							COALESCE((SELECT r.rate FROM res_currency_rate r
								WHERE r.currency_id = c.id AND r.name <= %s
									AND (r.company_id IS NULL OR r.company_id = %s)
								ORDER BY r.company_id, r.name DESC
									LIMIT 1), 1.0) AS rate
					FROM res_currency c
					WHERE c.id IN %s"""
		self._cr.execute(query, (date, company.id, tuple(self.ids)))
		currency_rates = dict(self._cr.fetchall())
		return currency_rates

	@api.depends('rate_ids.rate')
	def _compute_current_rate(self):
		date = self._context.get('date') or fields.Date.today()
		company = self.env['res.company'].browse(self._context.get('company_id')) or self.env.user.company_id
		# the subquery selects the last rate before 'date' for the given currency/company
		currency_rates = self._get_rates(company, date)
		for currency in self:
			currency.rate = currency_rates.get(currency.id) or 1.0

class ResCurrencyCustom(models.Model):
	_name = "currency.scraping"
	_description = "Currency Rate Scraping"

	def get_currency_rate(self):
		date = datetime.now().date()
		dates = date.strftime('%Y-%m-%d')
		comapny = self.env.user.company_id
		df_all = pd.read_html('https://www.x-rates.com/table/?from=INR&amount=1', header=0, attrs={'class': "tablesorter"})
		df = pd.concat(df_all).reset_index(drop=True)

		df.columns = ['currency', 'rate', 'inv_rate']


		def calculate_cuurency_rate(ind):

			return(float(df['rate'][ind]))

		today_date=datetime.today().date()
		USD = calculate_cuurency_rate(51)
		usd_currency = self.env['res.currency'].search([('name','=',"USD")])
		usd_currency.update({'rate':USD})
		for rec in usd_currency.rate_ids.filtered(lambda record: record.name == today_date):
				rec.unlink()
		usd_currency.rate_ids.create({'name': dates, 'company_id': comapny.id, 'rate': USD, 'currency_id': usd_currency.id})
		EUR = calculate_cuurency_rate(14)
		usd_currency = self.env['res.currency'].search([('name', '=', "EUR")])
		usd_currency.update({'rate': EUR})
		for rec in usd_currency.rate_ids.filtered(lambda record: record.name == today_date):
				rec.unlink()
		usd_currency.rate_ids.create(
			{'name': dates, 'company_id': comapny.id, 'rate': EUR, 'currency_id': usd_currency.id})
		MUR = calculate_cuurency_rate(27)
		usd_currency = self.env['res.currency'].search([('name', '=', "MUR")])
		usd_currency.update({'rate': MUR})
		for rec in usd_currency.rate_ids.filtered(lambda record: record.name == today_date):
				rec.unlink()
		usd_currency.rate_ids.create(
			{'name': dates, 'company_id': comapny.id, 'rate': MUR, 'currency_id': usd_currency.id})
		AED = calculate_cuurency_rate(49)
		usd_currency = self.env['res.currency'].search([('name', '=', "AED")])
		usd_currency.update({'rate': AED})
		for rec in usd_currency.rate_ids.filtered(lambda record: record.name == today_date):
				rec.unlink()
		usd_currency.rate_ids.create(
			{'name': dates, 'company_id': comapny.id, 'rate': AED, 'currency_id': usd_currency.id})

		QAR = calculate_cuurency_rate(36)
		usd_currency = self.env['res.currency'].search([('name', '=', "QAR")])
		usd_currency.update({'rate': QAR})
		for rec in usd_currency.rate_ids.filtered(lambda record: record.name == today_date):
				rec.unlink()
		usd_currency.rate_ids.create(
			{'name': dates, 'company_id': comapny.id, 'rate': QAR, 'currency_id': usd_currency.id})
		BHD = calculate_cuurency_rate(3)
		usd_currency = self.env['res.currency'].search([('name', '=', "BHD")])
		usd_currency.update({'rate': BHD})
		for rec in usd_currency.rate_ids.filtered(lambda record: record.name == today_date):
				rec.unlink()
		usd_currency.rate_ids.create(
			{'name': dates, 'company_id': comapny.id, 'rate': BHD, 'currency_id': usd_currency.id})

		HKD = calculate_cuurency_rate(15)
		usd_currency = self.env['res.currency'].search([('name','=',"HKD")])
		usd_currency.update({'rate':HKD})
		for rec in usd_currency.rate_ids.filtered(lambda record: record.name == today_date):
				rec.unlink()
		usd_currency.rate_ids.create(
			{'name': dates, 'company_id': comapny.id, 'rate': HKD, 'currency_id': usd_currency.id})

		GBP = calculate_cuurency_rate(50)
		usd_currency = self.env['res.currency'].search([('name','=',"GBP")])
		usd_currency.update({'rate':GBP})
		for rec in usd_currency.rate_ids.filtered(lambda record: record.name == today_date):
				rec.unlink()
		usd_currency.rate_ids.create(
			{'name': dates, 'company_id': comapny.id, 'rate': GBP, 'currency_id': usd_currency.id})

		AUD = calculate_cuurency_rate(1)
		usd_currency = self.env['res.currency'].search([('name','=',"AUD")])
		usd_currency.update({'rate':AUD})

		for rec in usd_currency.rate_ids.filtered(lambda record: record.name == today_date):
				rec.unlink()
		usd_currency.rate_ids.create(
			{'name': dates, 'company_id': comapny.id, 'rate': AUD, 'currency_id': usd_currency.id})
		CAD = calculate_cuurency_rate(7)
		usd_currency = self.env['res.currency'].search([('name','=',"CAD")])
		usd_currency.update({'rate':CAD})
		for rec in usd_currency.rate_ids.filtered(lambda record: record.name == today_date):
				rec.unlink()
		usd_currency.rate_ids.create(
			{'name': dates, 'company_id': comapny.id, 'rate': CAD, 'currency_id': usd_currency.id})
		SGD = calculate_cuurency_rate(40)
		usd_currency = self.env['res.currency'].search([('name','=',"SGD")])
		usd_currency.update({'rate':SGD})
		for rec in usd_currency.rate_ids.filtered(lambda record: record.name == today_date):
				rec.unlink()
		usd_currency.rate_ids.create(
			{'name': dates, 'company_id': comapny.id, 'rate': SGD, 'currency_id': usd_currency.id})
		CHF = calculate_cuurency_rate(46)
		usd_currency = self.env['res.currency'].search([('name','=',"CHF")])
		usd_currency.update({'rate':CHF})
		for rec in usd_currency.rate_ids.filtered(lambda record: record.name == today_date):
				rec.unlink()
		usd_currency.rate_ids.create(
			{'name': dates, 'company_id': comapny.id, 'rate': CHF, 'currency_id': usd_currency.id})
		JPY = calculate_cuurency_rate(21)
		usd_currency = self.env['res.currency'].search([('name','=',"JPY")])
		usd_currency.update({'rate':JPY})

		for rec in usd_currency.rate_ids.filtered(lambda record: record.name == today_date):
				rec.unlink()
		usd_currency.rate_ids.create(
			{'name': dates, 'company_id': comapny.id, 'rate': JPY, 'currency_id': usd_currency.id})
		SAR = calculate_cuurency_rate(39)
		usd_currency = self.env['res.currency'].search([('name', '=', "SAR")])
		usd_currency.update({'rate': SAR})
		for rec in usd_currency.rate_ids.filtered(lambda record: record.name == today_date):
				rec.unlink()
		usd_currency.rate_ids.create(
			{'name': dates, 'company_id': comapny.id, 'rate': SAR, 'currency_id': usd_currency.id})
		ZAR = calculate_cuurency_rate(39)
		usd_currency = self.env['res.currency'].search([('name','=',"ZAR")])
		usd_currency.update({'rate':ZAR})
		for rec in usd_currency.rate_ids.filtered(lambda record: record.name == today_date):
				rec.unlink()
		usd_currency.rate_ids.create(
			{'name': dates, 'company_id': comapny.id, 'rate': ZAR, 'currency_id': usd_currency.id})
		SEK = calculate_cuurency_rate(43)
		usd_currency = self.env['res.currency'].search([('name','=',"SEK")])
		usd_currency.update({'rate':SEK})
		for rec in usd_currency.rate_ids.filtered(lambda record: record.name == today_date):
				rec.unlink()
		usd_currency.rate_ids.create(
			{'name': dates, 'company_id': comapny.id, 'rate': SEK, 'currency_id': usd_currency.id})
		NZD = calculate_cuurency_rate(30)
		usd_currency = self.env['res.currency'].search([('name','=',"NZD")])
		usd_currency.update({'rate':NZD})
		for rec in usd_currency.rate_ids.filtered(lambda record: record.name == today_date):
				rec.unlink()
		usd_currency.rate_ids.create(
			{'name': dates, 'company_id': comapny.id, 'rate': NZD, 'currency_id': usd_currency.id})
		THB = calculate_cuurency_rate(46)
		usd_currency = self.env['res.currency'].search([('name','=',"THB")])
		usd_currency.update({'rate':THB})
		for rec in usd_currency.rate_ids.filtered(lambda record: record.name == today_date):
				rec.unlink()
		usd_currency.rate_ids.create(
			{'name': dates, 'company_id': comapny.id, 'rate': THB, 'currency_id': usd_currency.id})
		PHP = calculate_cuurency_rate(34)
		usd_currency = self.env['res.currency'].search([('name','=',"PHP")])
		usd_currency.update({'rate':PHP})
		for rec in usd_currency.rate_ids.filtered(lambda record: record.name == today_date):
				rec.unlink()
		usd_currency.rate_ids.create(
			{'name': dates, 'company_id': comapny.id, 'rate': PHP, 'currency_id': usd_currency.id})
		IDR = calculate_cuurency_rate(20)
		usd_currency = self.env['res.currency'].search([('name','=',"IDR")])
		usd_currency.update({'rate':IDR})
		for rec in usd_currency.rate_ids.filtered(lambda record: record.name == today_date):
				rec.unlink()
		usd_currency.rate_ids.create(
			{'name': dates, 'company_id': comapny.id, 'rate': IDR, 'currency_id': usd_currency.id})

