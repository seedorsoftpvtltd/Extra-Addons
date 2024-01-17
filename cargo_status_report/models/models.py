from odoo import models, fields, api, _


class SubJob(models.Model):
    _inherit = 'sub.job'


    job_date=fields.Date('Job Date')