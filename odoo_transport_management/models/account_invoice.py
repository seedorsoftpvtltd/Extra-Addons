# -*- coding: utf-8 -*-

from odoo import models, fields

class AccountInvoice(models.Model):
#    _inherit = 'account.invoice' odoo13
    _inherit = 'account.move'
    
    transporter_id = fields.Many2one(
        'res.partner',
        string="Transporter"
    )

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
