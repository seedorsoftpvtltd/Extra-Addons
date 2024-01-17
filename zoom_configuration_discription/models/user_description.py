from odoo import fields, models, api, _


class User(models.Model):
    _inherit = "res.users"

    zoom_description = fields.Text(string='Hint')
