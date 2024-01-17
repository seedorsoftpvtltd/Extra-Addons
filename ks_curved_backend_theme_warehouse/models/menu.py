from odoo import models, fields, _, api


class KsMenus(models.Model):
    _inherit = 'ir.ui.menu'

    warehouse = fields.Boolean('Is Warehouse')
    accounts = fields.Boolean('Is Accounts')
#    logistics = fields.Boolean('Is Logistics')
    freight = fields.Boolean('Is Freight')
    desk = fields.Boolean('Is Desk')
