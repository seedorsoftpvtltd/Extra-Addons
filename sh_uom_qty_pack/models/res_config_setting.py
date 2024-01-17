# -*- coding: utf-8 -*-
# Copyright (C) Softhealer Technologies.

from odoo import fields, models

class ResCompany(models.Model):
    _inherit = 'res.company'

    sh_show_bag_size_order_line = fields.Boolean("Show Bag Size in Order Line")
    sh_show_bag_size_in_report = fields.Boolean("Show Bag Size in Report")

    sh_show_bag_size_purchase_order_line = fields.Boolean("Show Bag Size in Order Line")
    sh_show_bag_size_in_purchase_report = fields.Boolean("Show Bag Size in Report")
    
    sh_show_bag_size_stock_move_ids = fields.Boolean("Show Bag Size in Stock Picking")
    sh_show_bag_size_in_stock_report = fields.Boolean("Show Bag Size in Report")

    sh_show_bag_size_account_move_line = fields.Boolean("Show Bag Size in Invoice Line")
    sh_show_bag_size_in_account_invoice_report=fields.Boolean("Show Bag Size in Invoice Report")



class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    sh_show_bag_size_order_line = fields.Boolean(
        related="company_id.sh_show_bag_size_order_line", string="Show Bag Size in Order Line", readonly=False)
    sh_show_bag_size_in_report = fields.Boolean(
        related="company_id.sh_show_bag_size_in_report", string="Show Bag Size in Report", readonly=False)

    sh_show_bag_size_purchase_order_line = fields.Boolean(
        related="company_id.sh_show_bag_size_purchase_order_line", string="Show Bag Size in Order Line", readonly=False)
    sh_show_bag_size_in_purchase_report = fields.Boolean(
        related="company_id.sh_show_bag_size_in_purchase_report", string="Show Bag Size in Report", readonly=False)
    
    sh_show_bag_size_stock_move_ids = fields.Boolean(
        related="company_id.sh_show_bag_size_stock_move_ids", string="Show Bag Size in Stock Picking", readonly=False)
    sh_show_bag_size_in_stock_report = fields.Boolean(
        related="company_id.sh_show_bag_size_in_stock_report", string="Show Bag Size in Report", readonly=False)

    sh_show_bag_size_account_move_line = fields.Boolean(
        related="company_id.sh_show_bag_size_account_move_line", string="Show Bag Size in Invoice Line", readonly=False)
    sh_show_bag_size_in_account_invoice_report = fields.Boolean(
        related="company_id.sh_show_bag_size_in_account_invoice_report", string="Show Bag Size in Invoice Report", readonly=False)
