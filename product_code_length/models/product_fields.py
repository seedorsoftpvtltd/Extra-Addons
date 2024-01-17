from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class ProductTemplate(models.Model):
	_inherit = 'product.template'

	@api.onchange('name')
	def _check_code_length(self):
		for product in self:
			if product.name and len(product.name) > 100:
				raise ValidationError("Product Code cannot be longer than 100 characters.")


class ProductProduct(models.Model):
	_inherit = 'product.product'

	@api.onchange('name')
	def _check_code_length(self):
		for product in self:
			if product.name and len(product.name) > 100:
				raise ValidationError("Product Code cannot be longer than 100 characters.")










