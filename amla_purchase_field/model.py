from odoo import api, models, fields

class PurchaseVendorDetails(models.Model):
    _inherit = "purchase.order"      

    partner_id = fields.Many2one('res.partner', string='Customer')

    street = fields.Char(related='partner_id.street')
    street2 = fields.Char(related='partner_id.street2')
    city = fields.Char(related='partner_id.city')
    new_state = fields.Many2one(related='partner_id.state_id')
    zip_id = fields.Char(related='partner_id.zip')
    gst = fields.Char(related='partner_id.vat')
  
 
