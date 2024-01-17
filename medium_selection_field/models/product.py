from odoo import models, fields, api


class Product(models.Model):
    _inherit = "product.product"

    # x_medium = fields.Many2one('utm.medium', string="Job Type")

    x_segment = fields.Selection([('import','Import'),
                                  ('export','Export'),
                                  ('cross_trade','Cross Trade'),
                                  ('customs_brokerage','Custom Brokerage'),
                                  ('local_services','Local Services'),
                                  ('contract_logistics','Contract Logistics'),
                                  ('3pl','3 PL'),
                                  ('rental','Rental'),
                                  ('value_added','Value Added Services'),
                                  ('cross_docking','Cross Docking')],
                                 string="Segment",store=True)