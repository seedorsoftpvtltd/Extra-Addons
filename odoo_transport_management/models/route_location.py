# -*- coding: utf-8 -*-

from odoo import fields, models

class RouteLocation(models.Model):
    _name = 'route.location'
    _description = "Route Location"
   
    name = fields.Char(
        string='Name',
        required = True,
    )

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
