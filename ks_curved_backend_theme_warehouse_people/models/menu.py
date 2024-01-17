from odoo import models, fields, _, api


class KsMenus(models.Model):
    _inherit = 'ir.ui.menu'

    warehouse = fields.Boolean('Is Warehouse')
    accounts = fields.Boolean('Is Accounts')
    people = fields.Boolean('Is people')
    freight = fields.Boolean('Is Freight')
    desk = fields.Boolean('Is Desk')
