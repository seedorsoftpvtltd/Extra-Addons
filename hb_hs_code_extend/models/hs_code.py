from odoo import api, fields, models, tools, osv, http, _


class HsCodeExt(models.Model):
    _inherit = "hs.code"

    uom_id = fields.Many2one('uom.uom', string='UOM', store=True)
    tax_id = fields.Many2many('account.tax', string='Taxes', strore=True)

