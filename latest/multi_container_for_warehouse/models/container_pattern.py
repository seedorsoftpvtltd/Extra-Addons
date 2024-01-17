from odoo import models, fields, api, _
import re
from odoo.exceptions import AccessError, UserError, ValidationError


class ContainerPattern(models.Model):
    _name = "container.pattern"

    company_id = fields.Many2one('res.company', string='Company', readonly=True)
    pattern = fields.Char(string="Container Pattern")
    country_id= fields.Many2one('res.country', required=True)
    example = fields.Char(string='Example')

    _sql_constraints = [('pattern', 'unique(country_id)', 'Only one pattern can be created for a country!')]