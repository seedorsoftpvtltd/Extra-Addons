from odoo import api, fields, models, tools, _

class Payment(models.Model):
    _inherit = 'account.payment'

    narration = fields.Text(string='Narration', store=True)
