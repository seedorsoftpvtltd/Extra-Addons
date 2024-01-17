from odoo import fields, models, api, _

class Accountmove(models.Model):
    _inherit="account.move"

    x_freight_type=fields.Many2one(related='operation_id.x_job_type',readonly=False)