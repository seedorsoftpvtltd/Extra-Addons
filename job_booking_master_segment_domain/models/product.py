from odoo import models, fields, api

class ProductTemplate(models.Model):
    _inherit = "product.template"

    x_medium = fields.Many2one('utm.medium', string="Job Type", store=True)

class Product(models.Model):
    _inherit = "product.product"

#    x_medium = fields.Many2one('utm.medium', string="Job Type")
    
    x_segment = fields.Selection([('import','Import'),
                                  ('export','Export'),
                                  ('cross_trade','Cross Trade'),
                                  ('customs_brokerage','Custom Brokerage'),
                                  ('local_services','Local Services'),
                                  ('3pl','3 PL'),
                                  ('rental','Rental'),
                                  ('value_added','Value Added Services'),
                                  ('cross_docking','Cross Docking')],
                                 string="Segment",store=True)

    x_transport= fields.Selection([('land','Land'),
                                   ('ocean','Ocean'),
                                   ('air','Air'),
                                   ('local_services','Local Services'),
                                   ('not_required','Not Required')],
                                  string="Transport",store=True)
    x_land_shipping =fields.Selection([('ftl','FTL'),
                                       ('ltl','LTL'),
                                       ('fcl','FCL'),
                                       ('lcl','LCL'),
                                       ('dhl','DHL'),
                                       ('import','Import'),
                                       ('export','Export'),
                                       ('local_transport','Local Transport'),
                                       ('local_services', 'Local Services'),
                                       ('not_required', 'Not Required')],
                                      string="Service Type", store=True)

    x_ocean_shipping = fields.Selection([
                                        ('fcl', 'FCL'),
                                        ('lcl', 'LCL'),
                                        ('bulk', 'BULK'),
                                        ('import', 'Import'),
                                        ('export', 'Export'),
                                        ('not_required', 'Not Required')],
                                       string="Service Type", store=True)

    x_air_shipping = fields.Selection([
                                        ('import', 'Import'),
                                        ('export', 'Export'),
                                        ('lcl', 'LCL'),
                                        ('general', 'General'),
                                        ('perishable','Perishable'),
                                        ('temperature','Temperature Control')],
                                       string="Service Type", store=True)

    x_warehouse = fields.Selection([
                                        ('tc', 'TC'),
                                        ('chilled', 'Chilled'),
                                        ('dry', 'Dry'),
                                        ('frozen', 'Frozen'),
                                        ('open_yard', 'Open Yard'),
                                        ('wh_vas', 'WH VAS')],
                                        string="Service Type", store=True)

    seg_domain = fields.Boolean(string='segment domain',compute="compute_hide")


    @api.depends('name')
    def compute_hide(self):
        # print('asdasdasd')
        enable_val = self.env['res.config.settings'].get_values()['enable_domain']
        # print(enable_val)
        self.seg_domain = enable_val
