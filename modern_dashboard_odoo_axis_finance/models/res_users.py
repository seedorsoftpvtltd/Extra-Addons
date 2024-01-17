# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class ResUsers(models.Model):
    _inherit = 'res.users'

    access_pos_dashboard = fields.Boolean("Sales Dashboard", default=True)
    access_today_sale_report = fields.Boolean("Today Sale Report", default=True)
    access_x_report = fields.Boolean("X-Report", default=True)
    access_sale_dashboard =fields.Boolean('Sale Dashboard',default=False)
    access_crm_dashboard =fields.Boolean('Crm Dashboard',default=True)
    access_inventory_dashboard =fields.Boolean('Inventory Dashboard')
    access_account_dashboard =fields.Boolean('Account Dashboard')



    





  