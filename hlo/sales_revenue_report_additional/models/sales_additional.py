from odoo import api, fields, models, tools, _

class Account(models.Model):
    _inherit = 'account.move'

    x_rpd_mbl = fields.Char(string="MAWB MBL", related='operation_id.x_master_bl')