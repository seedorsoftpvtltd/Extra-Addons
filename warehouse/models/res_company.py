# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models

class Company(models.Model):
    _inherit = 'res.company'

    po_lead = fields.Float(string='warehouse Lead Time', required=True,
        help="Margin of error for vendor lead times. When the system "
             "generates Warehouse Booking for procuring products, "
             "they will be scheduled that many days earlier "
             "to cope with unexpected vendor delays.", default=0.0)

    po_lock = fields.Selection([
        ('edit', 'Allow to edit Warehouse Booking'),
        ('lock', 'Confirmed Warehouse Booking are not editable')
        ], string="Warehouse Booking Modification", default="edit",
        help='Warehouse Booking Modification used when you want to Warehouse Booking editable after confirm')

    po_double_validation = fields.Selection([
        ('one_step', 'Confirm Warehouse Booking in one step'),
        ('tpo_step', 'Get 2 levels of approvals to confirm a Warehouse Booking'),
        ('two_step', '')
        ], string="Levels of Approvals", default='one_step',
        help="Provide a double validation mechanism for warehouses")

    po_double_validation_amount = fields.Monetary(string='Double validation amount', default=5000,
        help="Minimum amount for which a double validation is required")
