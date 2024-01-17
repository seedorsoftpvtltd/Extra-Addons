from odoo import fields, models, api, _

class UtmMedium(models.Model):
    _inherit = 'utm.medium'

    is_job_category = fields.Boolean(string='Is Category',default=False)



