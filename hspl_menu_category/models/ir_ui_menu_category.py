# -*- coding: utf-8 -*-
# Copyright 2018, 2020 Heliconia Solutions Pvt Ltd (https://heliconia.io)

from odoo import models, fields, api, _


class IrUiMenuCcategory(models.Model):
    _name = "ir.ui.menu.category"
    _order = "sequence asc"

    name = fields.Char(string='Name', required=True)
    sequence = fields.Integer(string='Sequence',
                              help="Gives the sequence category when displaying a list of menus at dashboard.")
    menu_id = fields.One2many('ir.ui.menu', 'category_id', string="Menu Items")



    @api.model
    def get_category(self):
        categories = self.env['ir.ui.menu.category'].search_read([('menu_id', '!=', False)])
        return categories
