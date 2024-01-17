# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from datetime import datetime, timedelta ,date
from odoo import api, fields, models,tools, _
from odoo.exceptions import UserError, ValidationError
from odoo.tools import float_is_zero, float_compare, DEFAULT_SERVER_DATETIME_FORMAT
from odoo.osv import expression

	
class StockLocation(models.Model):
	_inherit = 'stock.location'

	responsible_user_ids = fields.Many2many('res.users',string="Responsible User")
	
	@api.model
	def _name_search(self, name, args=None, operator='ilike', limit=100, name_get_uid=None):
		""" search full name and barcode """
		args = args or []
		if operator == 'ilike' and not (name or '').strip():
			domain = []
		elif operator in expression.NEGATIVE_TERM_OPERATORS:
			domain = [('barcode', operator, name), ('complete_name', operator, name)]
		else:
			domain = ['|', ('barcode', operator, name), ('complete_name', operator, name)]
		
		limit = 30
		if self._context.get('loc'):
			location_ids = self.sudo()._search(expression.AND([domain, args]), limit=limit, access_rights_uid=name_get_uid)
		else:
			location_ids = self._search(expression.AND([domain, args]), limit=limit, access_rights_uid=name_get_uid)
		return models.lazy_name_get(self.sudo().browse(location_ids).with_user(name_get_uid))
