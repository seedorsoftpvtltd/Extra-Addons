from odoo import models, fields, _, api


class KsMenus(models.Model):
    _inherit = 'ir.ui.menu'

    compensation = fields.Boolean('Is compensation')
    workforce = fields.Boolean('Is workforce')
    people = fields.Boolean('Is People')
    desk = fields.Boolean('Is Desk')