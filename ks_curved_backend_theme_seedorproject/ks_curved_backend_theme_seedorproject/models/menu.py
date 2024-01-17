from odoo import models, fields, _, api


class KsMenus(models.Model):
    _inherit = 'ir.ui.menu'

  #  affinity = fields.Boolean('Is Affinity')
   # finance = fields.Boolean('Is Finance')
  #  people = fields.Boolean('Is People')
    project = fields.Boolean('Is project')
    desk = fields.Boolean('Is Desk')