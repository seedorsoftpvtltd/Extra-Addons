from odoo import api, fields, models


class ResPartner(models.Model):
    _inherit = "hr.employee"

    street = fields.Char(string='Street')
    zip = fields.Char(string='Zip')
    city = fields.Char(string='City')
    statee = fields.Char(string='State')
    country = fields.Char(string='Country')

    date_geo = fields.Char(string='Date')
    geo_latitude = fields.Char(string='Latitude')
    geo_longitude = fields.Char(string='Longitude')
    diameter = fields.Char(string='Diameter')
    emp_face = fields.Binary(' FaceImage', related='user_faces.image')

    @api.model
    def _geo_localize(self, street='', zip='', city='', statee='', country=''):
        geo_obj = self.env['base.geocoder']
        search = geo_obj.geo_query_address(street=street, zip=zip, city=city, state=statee, country=country)
        result = geo_obj.geo_find(search, force_country=country)
        if result is None:
            search = geo_obj.geo_query_address(city=city, state=statee, country=country)
            result = geo_obj.geo_find(search, force_country=country)
        return result

    def geo_localize(self):

        for partner in self.with_context(lang='en_US'):
            result = self._geo_localize(partner.street,
                                        partner.zip,
                                        partner.city,
                                        partner.statee,
                                        partner.country)

            if result:
                partner.write({
                    'geo_latitude': result[0],
                    'geo_longitude': result[1],
                    'date_geo': fields.Date.context_today(partner)
                })
        return True
