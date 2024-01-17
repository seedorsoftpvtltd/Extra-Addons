import ast
import re
from odoo import models, fields, api, _
from odoo.exceptions import AccessError, UserError, ValidationError
import logging

_logger = logging.getLogger(__name__)


class PatternTemplate(models.Model):
    _name = "pattern.template"
    _description = "Pattern Template"

    name = fields.Char(string="Bill of Entry Pattern",readonly=False)
    country_id = fields.Many2one('res.country', string="Country", required=True)
    display_name = fields.Char(string='Display Name', )
    example = fields.Char(string='Example', )

    _sql_constraints = [('name', 'unique(country_id)', 'Only one pattern can be created for a country!')]



    # @api.model
    # def create(self, vals):
    #     record = super(PatternTemplate, self).create(vals)
    #     company_country = self.env.company.country_id
    #
    #     if record.country_id == company_country:
    #         record.active_name = True
    #     else:
    #         record.active_name = False
    #
    #     return record
    # _sql_constraints = [('name', 'unique(country_id)', 'The Country have only one pattern.')]
    # @api.model
    # def create(self, vals):
    #     # Set active field value based on the company's country
    #     company_country = self.env.company.country_id
    #     record_country = self.env['res.country'].browse(vals.get('country_id'))
    #
    #     if record_country == company_country:
    #         vals['active_name'] = True
    #     else:
    #         vals['active_name'] = False
    #
    #     return super(PatternTemplate, self).create(vals)
    #
    # @api.depends('country_id')
    # def _compute_active_name(self):
    #     for company in self:
    #         if company.country_id == company.env.company.country_id:
    #             company.active_name = True
    #         else:
    #             company.active_name = False

    # @api.constrains('active_name')
    # def _check_active_balance(self):
    #     # Check if active balance is set to False in the company
    #     if self.active_name and self.env.company.active_name is False:
    #         raise UserError("Cannot edit the file. Active balance is already set as inactive.")

    # def write(self, vals):
    #     # Check if the 'country_id' field is being updated
    #     if 'country_id' in vals:
    #         company_country = self.env.company.country_id
    #         record_country = self.env['res.country'].browse(vals.get('country_id'))
    #
    #         if record_country == company_country:
    #             vals['active_name'] = True
    #         else:
    #             vals['active_name'] = False
    #
    #     return super(PatternTemplate, self).write(vals)
    #
    # @api.constrains('country_id', 'name')
    # def _check_country_pattern(self):
    #     for rec in self:
    #         country = rec.country_id
    #         pattern = rec.name
    #         if country and pattern:
    #             # Check for existing record with the same country and pattern
    #             existing_record = self.search(
    #                 [('id', '!=', rec.id), ('country_id', '=', country.id), ('name', '=', pattern)])
    #             if existing_record:
    #                 raise ValidationError("A record with the same country and pattern already exists.")
    #             # Check for existing record with the same country but different pattern
    #             existing_country_record = self.search(
    #                 [('id', '!=', rec.id), ('country_id', '=', country.id), ('name', '!=', False)])
    #             if existing_country_record:
    #                 raise ValidationError("A record with the same country already exists with a different pattern.")
                # Check for existing record with the same pattern but different country
                # existing_pattern_record = self.search(
                #     [('id', '!=', rec.id), ('country_id', '!=', country.id), ('name', '=', pattern)])
                # if existing_pattern_record:
                #     raise ValidationError("A record with the same pattern already exists with a different country.")


class WarehouseOrder(models.Model):
    _inherit = "warehouse.order"

    pattern_temp = fields.Many2one('pattern.template', string='Pattern Template', )

